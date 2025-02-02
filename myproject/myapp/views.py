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
    (No removal functionality is provided.)
    """
    cart_session = request.session.get('cart', {})
    cart_items = []
    for key, item in cart_session.items():
        if isinstance(item, dict):
            cart_items.append(item)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)
