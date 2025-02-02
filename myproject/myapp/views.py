import os
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404

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

def get_medicine_by_name(med_name):
    """Look up a medicine by its name in the JSON data."""
    medicines = get_medicines_data()
    for med in medicines:
        if med.get('name') == med_name:
            return med
    return None

def home(request):
    return render(request, 'home.html')

def medicines(request):
    """Render the medicines page using the JSON data."""
    medicines_list = get_medicines_data()
    context = {
        'medicines_list': medicines_list
    }
    return render(request, 'medicines.html', context)

def add_to_cart(request, med_id):
    """
    Add the chosen medicine (by id) to the session‐based cart.
    Each POST increases the quantity by 1.
    """
    if request.method == "POST":
        med = get_medicine_by_id(med_id)
        if not med:
            raise Http404("Medicine not found")
        cart = request.session.get('cart', {})
        key = str(med_id)  # use the id (as string) as the key

        if key in cart:
            cart[key]['quantity'] += 1
        else:
            cart[key] = {
                'id': med['id'],
                'name': med['name'],
                'quantity': 1,
                'image_url': med.get('image', '')
            }
        request.session['cart'] = cart
        return redirect('medicines')
    else:
        return redirect('medicines')

def cart(request):
    """
    Retrieve the session cart and pass a list of items to the template.
    Attach a 'cart_key' to each item that is guaranteed to be a numeric string.
    """
    cart_session = request.session.get('cart', {})
    cart_items = []
    for key, item in cart_session.items():
        if isinstance(item, dict):
            # If the key is already numeric, use it.
            if key.isdigit():
                item['cart_key'] = key
            else:
                # Otherwise, try to look up the medicine by name and use its id.
                med = get_medicine_by_name(item.get('name', ''))
                if med and isinstance(med.get('id'), int):
                    item['cart_key'] = str(med['id'])
                else:
                    # Fallback: skip this item (or you could force deletion)
                    continue
            cart_items.append(item)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, med_id):
    """
    Remove the chosen medicine (by id) from the session-based cart.
    """
    if request.method == "POST":
        cart = request.session.get('cart', {})
        key = str(med_id)
        if key in cart:
            del cart[key]
            request.session['cart'] = cart
    return redirect('cart')
