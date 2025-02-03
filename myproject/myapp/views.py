import os
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404

# -------------------------------------------
# Utility Functions
# -------------------------------------------

def get_medicines_data():
    """Load medicines from JSON file."""
    json_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'medicines.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('medicines', [])

def get_medicine_by_id(med_id):
    """Look up a medicine by its id in the JSON data."""
    medicines = get_medicines_data()
    for med in medicines:
        if med.get('id') == med_id:
            return med
    return None

# -------------------------------------------
# Basic Views
# -------------------------------------------

def home(request):
    """Render the home page."""
    return render(request, 'home.html')

# -------------------------------------------
# Medicines View (with Reconciliation Logic)
# -------------------------------------------
def medicines(request):
    """
    Render the medicines page.
    Always recalculate available inventory from the fresh JSON data and the current cart.
    
    For each medicine:
      available = (quantity from JSON) - (quantity already in cart)
    Then update each medicine's quantity and availability accordingly.
    """
    medicines_list = get_medicines_data()
    cart = request.session.get('cart', {})

    # Recalculate inventory for each medicine using fresh JSON data.
    # This ignores any previously stored 'inventory' in the session.
    inventory = {}
    for med in medicines_list:
        json_quantity = med.get('quantity', 0)
        # Check if this medicine is already in the cart.
        key = str(med['id'])
        cart_qty = cart.get(key, {}).get('quantity', 0)
        # Compute available inventory.
        available = json_quantity - cart_qty
        inventory[key] = available
        # Update the medicine data for display.
        med['quantity'] = available
        if available <= 0:
            med['availability'] = "Out of Stock"
        else:
            med['availability'] = "In Stock"

    # Save the recalculated inventory into the session.
    request.session['inventory'] = inventory

    context = {
        'medicines_list': medicines_list
    }
    return render(request, 'medicines.html', context)

# -------------------------------------------
# Cart and Inventory Operations
# -------------------------------------------

def add_to_cart(request, med_id):
    """
    Add the chosen medicine to the session‐based cart.
    Decrease the available quantity (from session inventory) by 1 when added.
    """
    if request.method == "POST":
        med = get_medicine_by_id(med_id)
        if not med:
            raise Http404("Medicine not found")

        # Get the current inventory from the session.
        inventory = request.session.get('inventory', {})
        key = str(med_id)
        available = inventory.get(key, 0)

        # If no stock is available, simply redirect.
        if available <= 0:
            return redirect('medicines')

        # Decrease the available quantity by 1.
        inventory[key] = available - 1
        request.session['inventory'] = inventory

        # Now, add the medicine to the cart.
        cart = request.session.get('cart', {})
        if key in cart:
            if cart[key]['quantity'] < 20:
                cart[key]['quantity'] += 1
        else:
            cart[key] = {
                'id': med['id'],
                'name': med['name'],
                'quantity': 1,
                'price': med.get('price', 0),
                'image_url': med.get('image', '')
            }
        request.session['cart'] = cart
        return redirect('medicines')
    return redirect('medicines')

def cart(request):
    """
    Retrieve the session cart and calculate subtotals and total price.
    """
    cart_session = request.session.get('cart', {})

    # Remove any legacy keys that are not numeric.
    keys_to_remove = [key for key in cart_session if not key.isdigit()]
    for key in keys_to_remove:
        del cart_session[key]
    request.session['cart'] = cart_session

    cart_items = []
    total_price = 0
    for key, item in cart_session.items():
        if isinstance(item, dict):
            item['cart_key'] = key
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 1))
            subtotal = price * quantity
            item['subtotal'] = subtotal
            total_price += subtotal
            cart_items.append(item)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

def increase_quantity(request, med_id):
    """
    Increase the quantity of the medicine in the cart (if inventory allows).
    This action will decrease the overall inventory by 1.
    """
    if request.method == "POST":
        cart = request.session.get('cart', {})
        inventory = request.session.get('inventory', {})
        key = str(med_id)
        if key in cart and inventory.get(key, 0) > 0:
            if cart[key]['quantity'] < 20:
                cart[key]['quantity'] += 1
                # Decrease inventory by 1.
                inventory[key] = inventory.get(key, 0) - 1
                request.session['cart'] = cart
                request.session['inventory'] = inventory
    return redirect('cart')

def decrease_quantity(request, med_id):
    """
    Decrease the quantity of the medicine in the cart.
    This action will return 1 unit back to the overall inventory.
    If the quantity becomes zero, remove the item from the cart.
    """
    if request.method == "POST":
        cart = request.session.get('cart', {})
        inventory = request.session.get('inventory', {})
        key = str(med_id)
        if key in cart:
            if cart[key]['quantity'] > 1:
                cart[key]['quantity'] -= 1
                # Return 1 unit to inventory.
                inventory[key] = inventory.get(key, 0) + 1
            else:
                # If quantity is 1, remove the item and return 1 unit.
                inventory[key] = inventory.get(key, 0) + 1
                del cart[key]
            request.session['cart'] = cart
            request.session['inventory'] = inventory
    return redirect('cart')

def remove_from_cart(request, med_id):
    """
    Remove the chosen medicine entirely from the cart.
    Return its full quantity back to the overall inventory.
    """
    if request.method == "POST":
        cart = request.session.get('cart', {})
        inventory = request.session.get('inventory', {})
        key = str(med_id)
        if key in cart:
            # Return all of the item's quantity to inventory.
            qty = cart[key]['quantity']
            inventory[key] = inventory.get(key, 0) + qty
            del cart[key]
            request.session['cart'] = cart
            request.session['inventory'] = inventory
    return redirect('cart')
