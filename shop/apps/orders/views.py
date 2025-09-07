from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from .models import Order,OrderDetails,PaymentType
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from apps.discounts.froms import CouponForm
from apps.discounts.models import Coupon
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
import utils
#___________________________________________________________________________________________________________________
class ShopCartView(View):
    def get(self,request,*args, **kwargs):
        shop_cart=ShopCart(request)
        return render(request,'orders_app/shop_cart.html',{'shop_cart':shop_cart})

def show_shop_cart_View(request):
    shop_cart = ShopCart(request)
    total_price=shop_cart.calc_total_price()
    order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
    context={
        'shop_cart':shop_cart,
        "shop_cart_count":shop_cart.count,
        "total_price":total_price,
        "delivery":delivery,
        "tax":tax,
        "order_final_price":order_final_price}
    return render(request,'orders_app/partials/show_shop_cart.html',context)

def add_to_shop_cart_view(request):
    product_id=request.GET.get('product_id')
    quantity = request.GET.get("quantity")
    shop_cart=ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,quantity)
    return HttpResponse(shop_cart.count)


def delete_from_shop_cart_View(request):
    product_id=request.GET.get("product_id")
    product=get_object_or_404(Product,id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart")


def update_shop_cart(request):
    product_id_list = request.GET.getlist("product_id_list[]")
    qty_list = request.GET.getlist("qty_list[]")
    
    shop_cart = ShopCart(request)
    shop_cart.update_shop_cart(product_id_list,qty_list)
    
    return redirect('orders:show_shop_cart')

def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)
#______________________________________________________________
class CreateOrderView(LoginRequiredMixin,View):
    def get(self,request):

        try:
            customer = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = Customer.objects.create(user=request.user)
        order = Order.objects.create(Customer=customer,payment=get_object_or_404(PaymentType,id=1))
        shop_cart=ShopCart(request)

        for item in shop_cart:
            product = item['product']
            OrderDetails.objects.create(
                Order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'])

        return redirect("orders:checkout_order",order.id)

#_____________________________________________________________________
class CheckoutOrderViwe(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        shop_cart = ShopCart(request)
        order = get_object_or_404(Order, id=order_id)
        total_price = shop_cart.calc_total_price()
        order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price,order.discount)
        data = {
            'name': user.name,  
            'family': user.family,
            'email': user.email,
            'phone_number': customer.phone,
            'address': customer.address,
            "description": order.description,
            "payment": order.payment
        }
        
        form_order = OrderForm(data) 
        form_coupon=CouponForm() 
        context = {
            'shop_cart': shop_cart,
            'total_price': total_price,
            'delivery': delivery,
            'tax': tax,
            "order":order,
            'order_final_price': order_final_price,
            'form_order': form_order,
            "form_coupon":form_coupon
        }

        return render(request, "orders_app/checkout.html", context)
    
    def post(self, request, order_id):
        form=OrderForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            try:
                order = Order.objects.get(id=order_id)
                order.description = cd["description"]
                order.payment = PaymentType.objects.get(id=cd["payment"])
                order.save()
                user=request.user
                user.name=cd["name"]
                user.family=cd["family"]
                user.email=cd["email"]
                user.save()
                customer = Customer.objects.gets(user=user)
                customer.phone=cd["phone_number"]
                customer.address=cd["address"]
                customer.save()
                order.customer = customer
                order.save()
                messages.success(request,"سفارش شما با موفقیت ثبت شد","success")
                return redirect("payments:zarinpal_payment",order_id)
            except ObjectDoesNotExist:
                messages.error(request,"فاکتوری با این مشخصات پیدا نشد","danger")
                return redirect("orders:checkout_order",order_id)
        else:
            return redirect("orders:checkout_order",order_id)

#_____________________________________________________________________
class ApplayCoupon(View):
    def post(self,request,*args, **kwargs):
        order_id = kwargs["order_id"]
        coupon_form=CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon_code = coupon_form.cleaned_data["coupon_code"]

            coupon=Coupon.objects.filter(Q(coupon_code=coupon_code) &
                                        Q(is_active=True) &
                                        Q(start_date__lte=timezone.now()) &
                                        Q(end_data__gte=timezone.now()))
            discount=0
            try:
                order=Order.objects.get(id=order_id)
                if coupon:
                    discount=coupon[0].discount
                    order.discount=discount
                    order.save()
                    messages.success(request,"اعمال کوپن با موفقیت انجام شد")
                    return redirect("orders:checkout_order", order_id)
                else:
                    order.discount=discount
                    order.save()
                    messages.error(request,"کد کوپن معتبر نیست","danger")
 

            except ObjectDoesNotExist:
                messages.error(request,"سفارش موجود نیست","danger")

        else:
            return redirect("orders:checkout_order", order_id)
#_____________________________________________________________________