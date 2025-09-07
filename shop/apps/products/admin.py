from django.contrib import admin
from .models import Brand,PoductGroup,Product,ProductFeature,Feature,ProductGallery,FeatureValue
from django.db.models.aggregates import Count
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import  Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field

#-------------------------------------------------------------------------------------
# BrandAdmin

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title','slug')
    list_filter = ("brand_title",)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)
    
#-------------------------------------------------------------------------------------
# PoductGroupAdmin

def de_active_product_group(modeladmin,request,queryset,message):
    res=queryset.update(is_active=False)
    message = f'تعداد گروه  {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)

def active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message = f' تعداد گروه {res} کالا فعال شد'
    modeladmin.message_user(request,message)

def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='application/json')
    serializers.serialize('json',queryset,stream=response)
    return response

class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = PoductGroup
    # extra برای تعداد اینلاین ها
    extra = 1

class GroupFilter(SimpleListFilter):
    title = "گروه محصولات"
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        sub_groups=PoductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title) for item in groups]

    def queryset(self, request, queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset



@admin.register(PoductGroup)
class PoductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title','is_active','group_parent','slug','register_data','update_date','count_sub_group','count_produc_of_group')
    list_filter=(GroupFilter,'is_active')
    #list_filter = ('group_title',('group_parent',DropdownFilter),)
    search_fields = ("group_title",)
    ordering = ('group_parent','group_title',)
    inlines = [ProductGroupInstanceInlineAdmin]
    actions=[de_active_product_group,active_product_group,export_json]

    # list_editable تبدیل کردن حالت تیکی در بتایپ های بولین 
    list_editable = ['is_active']

    def get_queryset(self,*args, **kwargs):
        qs=super(PoductGroupAdmin,self).get_queryset(*args, **kwargs)
        qs=qs.annotate(sub_group=Count('groups'))
        qs = qs.annotate(produc_of_group=Count("products_of_group"))
        return qs

    @short_description("تعداد کالاهای گروه")
    @order_field('produc_of_group')
    def count_produc_of_group(self,obj):
        return obj.produc_of_group

    @short_description('تعداد زیر گروه ها')
    @order_field('sub_group')
    def count_sub_group(self,obj):
        return obj.sub_group

    # count_sub_group.short_description = 'تعداد زیر گروه ها'
    de_active_product_group.short_description = "غیرفعال کردن گروه های انتخاب شده"
    active_product_group.short_description = "فعال کردن گروه های انتخاب شده"
    export_json.short_description="خروجی json از گروه های انتخاب شده"

#-------------------------------------------------------------------------------------
# ProductAdmin

def de_active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message = f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)

def active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message = f' تعداد {res} کالا فعال شد'
    modeladmin.message_user(request,message)

class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 5
    class Media:
        css = {
            'all':('css/admin_style.css',)
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )

class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('produce_name','displaye_product_groups',"price",'brand','is_active','update_date','slug',)
    list_filter=(('brand__brand_title',DropdownFilter),('product_group__group_title',DropdownFilter))
    search_fields=("produce_name",)
    ordering=('update_date','produce_name')
    actions=[de_active_product,active_product,export_json]
    inlines = [ProductFeatureInlineAdmin,ProductGalleryInlineAdmin]

    de_active_product.short_description="غیر فعال کردن کالا های انتخابی"
    active_product.short_description="فعال کردن کالا های انتخابی"
    

    def displaye_product_groups(self,obj):
       return ', '.join([grrup.group_title for grrup in obj.product_group.all()])
    displaye_product_groups.short_description= "گروه های کالا"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "product_group":
            kwargs['queryset']=PoductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets=(
        ('اطلاعات محصول',{'fields':(
            'produce_name',
            'price',
            'image_name',
            ('product_group','brand','is_active'),
            'summery_description',
            'description',
            'slug',
            'published_date',
            )}),
        ('تاریخ و زمان',{'fields':(
            )}),
        )


#-------------------------------------------------------------------------------------
# FeatureAdmin
class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 3



@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name','display_groups','display_feature_values')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInline]
    
    def display_groups(self,obj):
        return ", ".join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_values(self,obj):
        return ", ".join([feature_values.value_title for feature_values in obj.feature_values.all()])
    display_groups.short_description ='گروه ها دارای این ویژگی'
    display_feature_values.short_description ='مقادیر ممکن برای این ویژگی'

#-------------------------------------------------------------------------------------
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res,safe=False)
