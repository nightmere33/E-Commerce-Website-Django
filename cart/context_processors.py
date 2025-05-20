from .cart import Cart

#create a context processor so our cart is available in all templates

def cart(request):
    #rerturn the default data from our cart 
    return {'cart': Cart(request)}
