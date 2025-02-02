# myapp/context_processors.py

def cart_count(request):
    """Return the total quantity of items in the cart from the session."""
    cart = request.session.get('cart', {})
    count = 0
    for item in cart.values():
        if isinstance(item, dict) and 'quantity' in item:
            count += item['quantity']
    return {'cart_count': count}
