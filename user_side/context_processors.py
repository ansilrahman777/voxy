from .models import Category,Wishlist,CartItem,Cart,Product

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart =request.session.create()
    return cart

def custom_context(request,total=0, quantity=0, cart_items=None):
    user=request.user
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:  
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.discount_price * cart_item.quantity)
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    
    grand_total = total
    wishlist_products = []
    if user.is_authenticated:
        wishlist_products = [item.product for item in Wishlist.objects.filter(user=user)]
    context = {
        'cart_items': cart_items,
        'wishlist_products':wishlist_products,
        'grand_total':grand_total,
    }
    return context