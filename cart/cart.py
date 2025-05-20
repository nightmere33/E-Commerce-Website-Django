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

    def add(self,product):

        product_id = str(product.id)

        #logic
        if product_id not in self.cart:
            pass
        else:
            self.cart[product_id] = {'price' : str(product.price),}     
        
        self.session.modified = True    

    def __len__(self):
        return len(self.cart)    
