from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from .models import Payment
from apps.accounts.models import Customer
from apps.warehouses.models import Warehouse,WarehouseType
from django.conf import settings
import requests
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse



#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"  
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# ادرسی که به زرینپال میگه کار مشتری که تمام شد برگرده به صفحه ی من
CallbackURL = 'http://127.0.0.1:8080/payments/verify/'


# Create your views here.
# زرینپال رو مینویسیم چون ممکنه بعد ها از درگاه های دیگه هم استفاده کنیم
# قبل رفتن به درگاه باید اطمینان کنیم که کاربر لاگینه

# بعد از زدن دکمه ی ثبت سفارش در اپ اردر باید بیایم اینجا پس براش یو ار ال مینویسم



class ZarinpalPaymentView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        
        try:
            description = 'پرداخت از طریق درگاه زرین پال انجام شد'
            order = Order.objects.get(id=order_id)
            payment = Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=request.user),
                amount=order.get_order_total_price(),
                description=description,
                
                )
            
            payment.save()
            request.session['payment_session'] = {
                "order_id": order.id,
                "payment_id" : payment.id
                }
            
            user = request.user

            # اطلاعاتی که به درگاه زرین پال میخوام بفرستم
            req_data = {
                "MerchantID": settings.MERCHANT,
                "Amount": order.get_order_total_price(),
                "Description": description,
                "CallbackURL": CallbackURL,
                "metadata" : {"mobile":user.mobile_number,"email":user.email}
                }
            
            
            req_header = {'accept': 'application/json', 'content-type': 'application/json' }
            req = requests.post(url= ZP_API_REQUEST, data=json.dumps(req_data),headers=req_header)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
                
        except ObjectDoesNotExist:
            return redirect('orders:checkout_order' , order_id)
        
        
# مقدار MERCHANT اشتباهه، یا اطلاعات ناقص هستن و یا ارتباط با سرور زرین‌پال قطع شده

# import utils
# print(dir(utils))



# وقتی تراکنش کاربر انجام میشه این کار میکنه
# t_satus = request.GET.get('Status') , t_authority = request.GET.get('Authority') : از پاسخ کلاس بالا تولید میشن
class ZarinpalVerifyView(LoginRequiredMixin,View):
    def get(self,request):
        
        
        
        t_satus = request.GET.get('Status')
        t_authority = request.GET.get('Authority')
        if request.GET.get('Status') == 'OK':
            
            order_id = request.session["payment_session"]["order_id"]
            payment_id = request.session["payment_session"]["payment_id"]
        
            order = Order.objects.get(id=order_id)
            payment = Payment.objects.get(id=payment_id)
            
            req_header = {'accept': 'application/json', 'content-type': 'application/json'}
            
            req_data = {
                'MerchantID': settings.MERCHANT, 
                'Authority': t_authority, 
                'Amount': order.get_order_total_price(),
                }
            
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data),headers=req_header)
            if len(req.json()['errors']) == 0:
                t_satus = req.json()['data']['code']
                if t_satus == 100:
                    
                    order.is_finally = True
                    order.save()

                    
                    payment.is_finaly = True
                    payment.status_code = t_satus
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    
                    
                                        
                    # واسه سفارشی مه الان پولشو واریز کرده به ازای تعداد کالاهای سبد 3 بار این تابع صدا زده میشه
                    for item in order.orders_details1.all():
                        Warehouse.objects.create(
                            warehouse_type = WarehouseType.objects.get(id=2), # فروش
                            user_registered = request.user, # همینی که الان لاگینه
                            product = item.product,
                            qty = item.qty,
                            price = item.price,
                        )
                    
                    return redirect('payment:show_verify_message',f" پرداخت با موفقیت انجام شد کد رهگیری شما {str(req.json()['data']['ref_id'])}")
                    # return HttpResponse('Transaction success.\nRefID: ' + str(req.json()['data']['ref_id']))
                
                elif t_satus == 101:
                    
                    order.is_finally = True
                    order.save()
                    
                    payment.is_finaly = True
                    payment.status_code = t_satus
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    
                    for item in order.orders_details1.all():
                        Warehouse.objects.create(
                            warehouse_type = WarehouseType.objects.get(id=2), # فروش
                            user_registered = request.user, # همینی که الان لاگینه
                            product = item.product,
                            qty = item.qty,
                            price = item.price,
                        )
                    
                    
                    return redirect('payment:show_verify_message',f" پرداخت قبلا با موفقیت انجام شده کد رهگیری شما {str(req.json()['data']['ref_id'])}")
                    # return HttpResponse('Transaction submitted : ' + str(req.json()['data']['message']))
                
                else:
                    
                    payment.is_finaly = True
                    payment.status_code = t_satus
                    
                    payment.save()
                    
                    return redirect('payment:show_verify_message',f"خطا در فرایند پرداخت کد خطا : Error code: {t_satus}")
                    # return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                
                return redirect('payment:show_verify_message',f"خطا در فرایند پرداخت کد خطا : Error code: {e_code}, Error Message: {e_message}")
                # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return redirect('payment:show_verify_message',"خطا در فرایند پرداخت ")
            # return HttpResponse('Transaction failed or canceled by user')
                
                

def show_verify_message(request,message):
    return render(request,'payments_app/verify_message.html',{"message":message})