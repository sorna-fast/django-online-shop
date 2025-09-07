from apps.products.models import Product

class ShopCart:
    def __init__(self,request):
        self.session = request.session
        temp = self.session.get('ShopCart')
        if not temp:
            temp = self.session['ShopCart'] = {}
        self.shop_cart = temp
        self.count = len(self.shop_cart.keys())
        
        
    def add_to_shop_cart(self,product,quantity=1):
        product_id = str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id] = {'quantity':0,'price':product.price,"final_price":product.get_price_by_discount()}


        self.shop_cart[product_id]['quantity'] += int(quantity)
        self.count = len(self.shop_cart.keys())
        self.save()
        
    def delete_from_shop_cart(self,product):
        product_id = str(product.id)
        if product_id in self.shop_cart:
            del self.shop_cart[product_id]
            self.save()
            


    
    def update_shop_cart(self,product_id_list,qty_list):
        i=0
        for product_id in product_id_list:
            self.shop_cart[product_id]["quantity"] = int(qty_list[i])
            i+=1
        self.save()
            
    def save(self):
        self.session.modified=True
        self.session.save()
                  
    def __iter__(self):
        list_id = self.shop_cart.keys()
        products=Product.objects.filter(id__in=list_id)
        temp=self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]['product'] = product
            
        for item in temp.values():
            item["total_price"] = int(item['final_price']) * int(item['quantity'])
            yield item
            
    def calc_total_price(self):
        sum_=0
        for item in self.shop_cart.values():
            sum_+= int(item['quantity']) * int(item['final_price'])
        return sum_
    




