from .models import Product

# compare_product :میخوام اینو یکی از کی های رکوئست کنم که قرار ولیوش لیستی از ایدی کالا ها باشه

class CompareProduct:
    def __init__(self,request):
        self.session = request.session
        compare_product = self.session.get('compare_product')
        if not compare_product:
            compare_product = self.session['compare_product'] = []
        self.compare_product = compare_product
        self.count = len(self.compare_product)
    # ------------------------------------------------------------------------------------------------------
    def __iter__(self):
        compare_product = self.compare_product.copy()
        for item in compare_product:
            yield item
    # ------------------------------------------------------------------------------------------------------
    def add_to_compare_product(self, productId):
        productId = int(productId)
    
        current_product_group_id = Product.objects.filter(id=productId).values_list('product_group__id', flat=True).first()
        if current_product_group_id is None:
            return  # محصولی با این ID وجود نداره
    
        # گرفتن لیست گروه‌ محصولات برای آیتم‌های موجود در لیست مقایسه با یک کوئری
        group_parents_ids = list(
            Product.objects.filter(id__in=self.compare_product)
            .values_list('product_group__id', flat=True)
        )
    
        if productId not in self.compare_product:
            if current_product_group_id in group_parents_ids or not self.compare_product:
                self.compare_product.append(productId)
    
        self.count = len(self.compare_product)
        self.session.modified = True
    
    # ------------------------------------------------------------------------------------------------------
    def delete_from_compare_product(self,productId):
        self.compare_product.remove(int(productId))
        self.count = len(self.compare_product)
        self.session.modified = True
    # ------------------------------------------------------------------------------------------------------
    # هر وقت بخوام کل لیست پروداکت ایدی ها رو پاک کنم
    def clear_compare_product(self):
        del self.session['compare_product']
        self.session.modified = True
    # ------------------------------------------------------------------------------------------------------