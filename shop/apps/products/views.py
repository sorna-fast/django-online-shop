from django.shortcuts import render,redirect
from .models import Product,PoductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from django.shortcuts import get_object_or_404
from django.http  import JsonResponse
from django.core.paginator import Paginator
from .filters import ProductFilter
def get_root_group():
    return  PoductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
#-------------------------------------------------------------------------------------------------------------

# ارزان ترین محصولاات
def get_cheapest_products(request,*args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:8]
    products_groups =get_root_group()
    context={
        'products':products,
        'products_groups':products_groups,
    }
    return render(request,"product_app/partials/cheapest_products.html",context=context) 
#-------------------------------------------------------------------------------------------------------------

# جدید ترین محصولات
def get_last_products(request,*args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:8]
    products_groups = get_root_group()
    context={
        'products':products,
        'products_groups':products_groups,
    }
    return render(request,"product_app/partials/last_products.html",context=context)
#-------------------------------------------------------------------------------------------------------------

def get_popular_product_groups(request,*args, **kwargs):
    product_group=PoductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_group')).order_by('-count')[:6]
    context={
        'product_group':product_group,
    }
    return render(request,"product_app/partials/popular_product_group.html",context=context)
#-------------------------------------------------------------------------------------------------------------

# جزییات محصول
class ProductDetailView(View):
    def get(self,request,slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            return render(request,"product_app/product_detail.html",{"product":product})
#-------------------------------------------------------------------------------------------------------------

# محصولات مرتبط
def get_related_products(request,*args, **kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_product=[]
    for group in current_product.product_group.all():
        related_product.extend(
            Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id))
        )
    return render(request,"product_app/partials/related_products.html",{"related_product":related_product})
#-------------------------------------------------------------------------------------------------------------
# لیست کلیه گروه های محصولات
class ProductGroupsView(View):
    def get(self,request):
        product_groups=PoductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_group')).order_by('-count')
        return render(request,"product_app/partials/product_groups.html",{"product_groups":product_groups})
    
#-------------------------------------------------------------------------------------------------------------
# لیست گروه محصولات برای فیلتر
def get_product_groups(request):
    product_groups = PoductGroup.objects.annotate(count=Count('products_of_group')).filter(Q(is_active=True) & ~Q(count=0)).order_by('-count')
    return render(request,"product_app/partials/product_groups.html",{"product_groups":product_groups})


#-------------------------------------------------------------------------------------------------------------
# لیست برند ها برای فیلتر
def get_brands(request,*args, **kwargs):
    product_group = get_object_or_404(PoductGroup,slug=kwargs['slug'])
    brand_list_id=product_group.products_of_group.filter(is_active=True).values('brand_id')
    brands=Brand.objects.filter(pk__in=brand_list_id).annotate(count=Count('product_of_brands')).filter(~Q(count=0)).order_by('-count')
    return render(request,'product_app/partials/brands.html',{'brands':brands})
#-------------------------------------------------------------------------------------------------------------

# tow dropdown in adminpanel
def filter_value_for_feature(request):
    if request.method == "GET":
        feature_id = request.GET.get('feature_id')
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res,safe=False)
    

#-------------------------------------------------------------------------------------------------------------
def get_features_for_filtre(request,*args, **kwargs):
    product_group = get_object_or_404(PoductGroup,slug=kwargs['slug'])
    features_list=product_group.features_of_group.all()
    features_dict=dict()
    for features in features_list:
        features_dict[features]=features.feature_values.all();
    return render(request,'product_app/partials/features_filter.html',{'feature_dict':features_dict})
    
#-------------------------------------------------------------------------------------------------------------
# لیست محصولات هر گروه محصولات

class ProductsByGroupView(View):
    def get(self,request,*args, **kwargs):
        
        slug = kwargs['slug']
        
        current_group_detection = get_object_or_404(PoductGroup,slug=kwargs['slug'])

        products = Product.objects.filter(Q(product_group=current_group_detection) & Q(is_active=True))
        
        res_aggre = products.aggregate(min=Min('price'),max=Max('price')) # خروجی اگرگیت یک دیکشنریه
        # price filter
        filters =ProductFilter(request.GET,queryset=products)
        products = filters.qs
        
        # brand filter
        brand_filter = request.GET.getlist('brand')
        if brand_filter:
            products = products.filter(brand__id__in=brand_filter)
            
        features_filter = request.GET.getlist("feature")
        if features_filter:
            products = products.filter(product_features__filter_value__id__in=features_filter).distinct()
            
        # sort type
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = "0"
        if sort_type == "1":
            products = products.order_by('price')
        elif sort_type == "2":
            products = products.order_by('-price')
        
# Tip: Always perform all product filters before paging the site and then paging. You can see an example in this code.
        group_slug = slug
        product_per_page = int(request.GET.get('product_numbers',2))
        
        paginator = Paginator(products,product_per_page) 
        page_number = request.GET.get('page') # find number page
        page_obj =paginator.get_page(page_number) # List of products after pagination on the current page
        product_count = products.count() # The total number of products in this group

        # A list of numbers to create a drop-down menu to determine the number of items on each page by the user
        show_count_product = []
        i=product_per_page
        while i< product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)


        # همیشه مقدار انتخاب‌شده را در لیست نگه می‌داریم
        if product_per_page not in show_count_product:
            show_count_product.append(product_per_page)

        # مرتب‌سازی لیست تا مقدار انتخاب‌شده در جای درست قرار بگیرد
        show_count_product.sort()


        context = {
            'products' : products,
            'current_group' : current_group_detection,
            'res_aggre' :res_aggre,
            'group_slug' : group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'filter':filters,
            'show_count_product':show_count_product,
            'sort_type':sort_type,
            'product_current_number':product_per_page,
        }
        return render(request,'product_app/products.html',context)

#  ______________________________________________________________________________________________________
       
    
# ___________________________________________________________________________________________________________________________________
# صفجه ی اصلی مقایسه : نمایش کالا های اضافه شده به لیست مقایسه

class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        context = {
            'compare_list' : compare_list,
        }
        return render(request,'product_app/compare_list.html',context)

# -----------------------------------------------
# نمایش جدول کالاهای لیست مقایسه

from .compare import CompareProduct

def compare_table(request):
    compareList = CompareProduct(request)
    
    # فقط ایدی کالا بدرد نمیخوره و چون به نام و همه اطلاعات کالا نیاز دارم کالا ها رو بدست اوردم
    products = []
    for productId in compareList.compare_product:
        product = Product.objects.get(id=productId)
        products.append(product)
        
    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
                
    context = {
        'products' : products,
        'features' : features,
    }
    
    return render(request,'product_app/partials/compare_table.html',context)

# -----------------------------------------------
# محاسبه ی کالا های موجود در لیست مقایسه
# مورد | توضیح
# HttpResponse() | پاسخ خام و ساده به کلاینت می‌ده
# محتواش | می‌تونه متن، عدد، HTML، JSON (اگه با JsonResponse باشه) و... باشه
# توی این مثال | فقط تعداد کالاهای داخل لیست مقایسه رو برمی‌گردونه (مثلاً 3)

from django.http import HttpResponse

def status_of_compare_list(request):
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)

# -----------------------------------------------
# اضافه کردن کالا به لیست مقایسه

def add_to_compare_list(request):
    productId = request.GET.get("productId")
    # productGroupId = request.GET.get("productGroupId")
    compareList = CompareProduct(request)
    compareList.add_to_compare_product(productId)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')


# -----------------------------------------------
# حذف کردن کالا از لیست مقایسه

def delete_from_compare_list(request):
    productId = request.GET.get("productId")
    compareList = CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect('products:compare_table')


    
def handler404(request, exception=None):
    return render(request, 'main_app/404.html', status=404)