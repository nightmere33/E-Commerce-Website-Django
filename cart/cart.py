from item.models import Item

class Cart():
    def __init__(self,request):
        self.session = request.session

        #get the cart from the session
        cart = self.session.get('session_key')

        # if user in new , no session key ! create one !
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
      
        # make sure car is available in all pages
        self.cart = cart

    """def add(self,product):

        product_id = str(product.id)

        #logic
        if product_id not in self.cart:
            pass
        else:
            self.cart[product_id] = {'price' : str(product.price),}     
        
        self.session.modified = True    """
    
    def add(self, product):
        product_id = str(product.id)

        # Add if not in cart
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
        else:
            # Increment quantity if already in cart
            self.cart[product_id]['quantity'] += 1

        self.session.modified = True


    def __len__(self):
        return len(self.cart)    

    def get_prods(self):
        #get id from cart
        product_ids = self.cart.keys()
        #user ids to liikup products in databse model
        products = Item.objects.filter(id__in=product_ids)
         # Attach quantity to each product
        for product in products:
            product.quantity = self.cart[str(product.id)]['quantity']
        #return the products
        return products
