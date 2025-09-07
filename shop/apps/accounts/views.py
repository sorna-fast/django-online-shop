from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .froms import RegisterUserForm,VerifyRegisterForm,LoginUserForm,ChangePasswordForm,RememberPasswordForm
import utils
from .models import CustomUser,Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
#----------------------------------------------------------------------------------------------------------
class RegisterUserView(View):
    template_name="accounts_app/register.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,*args,**kwargs):
        form = RegisterUserForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            active_code=utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1']
            )
            utils.send_SMS(mobile_number=data["mobile_number"],message=f"کد فعال سازی حساب کاربری شما {active_code}")
            request.session['user_session']={
               "active_code":str(active_code),
               'mobile_number':data['mobile_number'],
               'remember_password':False
               }
            
            messages.success(request," اطلاعات شما ثبت شد و کد فعال سازی را وارد کنید","success")
            return redirect("accounts:Verify")
        messages.error(request,"خطا در انجام ثبت نام","error")
        return render(request, self.template_name, {"form": form})
#----------------------------------------------------------------------------------------------------------
class VerifyRegisterCodeView(View):
    template_name="accounts_app/Verify_Register_Code.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,*args, **kwargs):        
        form = VerifyRegisterForm()
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args, **kwargs):
        form=VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            if data['active_code'] == user_session['active_code']:
                user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                if user_session['remember_password'] == False:
                    user.is_active=True
                    user.active_code=utils.create_random_code(5)
                    user.save()
                    messages.success(request,"ثبت نام با موفقیت انحام شد","success")
                    return redirect("main:index")
                else:
                    return redirect("accounts:change_password")
            else:
                messages.error(request,"کد فعال سازی وارد شده اشتباه میباشد","danger")
                return render(request,self.template_name,{"form":form})
        messages.error(request,"اظلاعات وارد شده معتبر نمیباشد","danger")
        return render(request,self.template_name,{"form":form})

#----------------------------------------------------------------------------------------------------------

class LoginUserView(View):
    template_name="accounts_app/Login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    
    def get(self,request,*args, **kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request,*args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data['mobile_number'],password=data['password'])
            if user is not None:
                db_user=CustomUser.objects.get(mobile_number=data['mobile_number'])

                if db_user.is_admin==False:
                    messages.success(request,"ورود با موفقیت انجام شد",'success')
                    login(request,user)
                    next_url=request.GET.get('next')
                    if next_url is not None:
                        return redirect((next_url))
                    else:
                        return redirect("main:index")
                else:
                    messages.error(request,"کاربر ادمین نمیتواند از اینجا وارد شود",'warning')
                    return render(request,self.template_name,{'form':form})
            else:
                messages.error(request,"اطلاعات کاربری وارد شده نادرست است","danger")
                return render(request,self.template_name,{'form':form})
        else:
            messages.error(request,"اطلاعات وارد شده نامعتبر است","danger")
            return render(request,self.template_name,{'form':form})



#----------------------------------------------------------------------------------------------------------
class LogoutUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        session_data=request.session.get('ShopCart')
        logout(request)
        request.session['ShopCart']=session_data
        return redirect("main:index")

#----------------------------------------------------------------------------------------------------------

class UserPanelView(LoginRequiredMixin,View):
    template_name = "accounts_app/userpanel.html"
    def get(self,request):
        user = request.user
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                "name" : user.name ,
                "family" : user.family ,
                "email" : user.email ,
                "phone_number" : customer.phone,
                "address" : customer.address ,
                "image" : customer.image ,
            }
            
        except ObjectDoesNotExist:
            user_info = {
                "name" : user.name ,
                "family" : user.family ,
                "email" : user.email ,
            }
            
        return render(request,self.template_name,{"user_info":user_info})

#----------------------------------------------------------------------------------------------------------
class ChangePasswordView(View):
    tempalte_name="accounts_app/Change_Password.html"
    def get(self,request,*args, **kwargs):
        form=ChangePasswordForm()
        return render(request,self.tempalte_name,{"form":form})
    def post(self,request,*args, **kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            if user.password == data['password1']:
                messages.error(request,"رمز عبور جدید نمیتواند با رمز عبور فعلی یکسان باشد","danger")
                return render(request,self.tempalte_name,{"form":form})
            user.set_password(data['password1'])
            user.active_code=utils.create_random_code(5)
            user.save()
            messages.success(request,"رمز عبور با موفقیت تغییر یافت","success")
            return redirect("accounts:Login")
        else:
            messages.error(request,"اطلاعات وارد شده معتبر نمیباشد","danger")
            return render(request,self.tempalte_name,{"form":form})

#----------------------------------------------------------------------------------------------------------

class RemeberPasswordView(View):
    template_name="accounts_app/remeber_password.html"
    def get(self,request,*args, **kwargs):
        form=RememberPasswordForm()
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args, **kwargs):
        form=RememberPasswordForm(request.POST)
        
        if form.is_valid():
            try:
                data=form.cleaned_data
                active_code=utils.create_random_code(5)
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                user.active_code=active_code
                user.save()
                utils.send_SMS(mobile_number=data["mobile_number"],message=f"کد تایید شماره موبایل شما{active_code}")
                request.session['user_session']={
                    'active_code':str(active_code),
                    'mobile_number':data['mobile_number'],
                    'remember_password':True
                }
                messages.success(request,"جهت تغییر رمز عبور کد فعال سازی را وارد کنید","success")
                return redirect("accounts:Verify")
            except:
                messages.error(request,"کاربری با این شماره موبایل وجود ندارد","danger")
                return render(request,self.template_name,{"form":form})
            
#----------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# نمایش آخرین سفارشات کاربر وارد شده در پنل کاربری
from apps.orders.models import Order

def show_last_orders(request):
    order = Order.objects.filter(Customer=request.user.id).order_by('-register_date')[:4]
    return render(request,'accounts_app/partials/show_last_orders.html',{'orders':order})


# ----------------------------------------------------------------------------------------------------
# نوشتن پیج مربوط به فرم اپدیت کردن یا ویرایش اطلاعات کاربر توسط خودش

from .forms import UpdateProfileForm
from django.core.exceptions import ObjectDoesNotExist

class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        # یوزری که لاگین کرده
        user = request.user
        try:
            customer = Customer.objects.get(user_id=user.id)
            
            # فیلد های این دیکشنری باید همنام فیلد های فرم باشن
            initial_dict = {
                'mobile_number':user.mobile_number,
                'name' : user.name,
                'family' : user.family,
                'email' : user.email,
                'phone_number' : customer.phone,
                'address' : customer.address
            }
        except ObjectDoesNotExist:
            # اگه یوزر کاستومر نبود فقط صرفا یوزر بود
            initial_dict = {
                'mobile_number':user.mobile_number,
                'name' : user.name,
                'family' : user.family,
                'email' : user.email,
            }
        form = UpdateProfileForm(initial=initial_dict)   
        
        context = {
            'form':form,
            'image_url':customer.image,
        }
        
        return render(request,'accounts_app/update_profile.html',context)
    
    def post(self,request):
        # request.FILES : اطلاعات فایلی مثل عکس رو میاره درصورتی که به فرمم enctype = multipart/form-data اضافه شود
        form = UpdateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            
            user.mobile_number = cd['mobile_number']
            user.name = cd['name']
            user.family = cd['family']
            user.email = cd['email']
            user.save()
            
            try:
                customer = Customer.objects.get(user_id=user.id)
                customer.phone_number = cd['phone_number']
                customer.address = cd['address']
                customer.image_name = cd['image']
                customer.save()

            except ObjectDoesNotExist:
                Customer.objects.create(
                    user = request.user,
                    phone_number = cd['phone_number'],
                    address = cd['address'],
                    image_name = cd['image']
                )
            
            messages.success(request,'اطلاعات شما با موفقیت ویرایش شد','success')
            return redirect('accounts_app:update_profile')
        # اگر فرم معتبر نبود
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
            return render(request,'accounts_app/update_profile.html',{'form':form})
        
        
# ----------------------------------------------------------------------------------------------

from apps.payments.models import Payment
from django.contrib.auth.decorators import login_required

@login_required
def show_user_payments(request):
    payments = Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
        
    return render(request,'accounts_app/show_user_payments.html',{'payments':payments})

# وقتی پرداخت کامل نشده، کاربر با کلیک روی دکمه "تکمیل خرید" بره به سبد خرید مرتبط با همون سفارش خاص، 
@login_required
def return_to_shop_cart(request, order_code):
    order = get_object_or_404(Order, order_code=order_code, customer__user=request.user)
    
    # باقی کدهای مربوط به نمایش سبد خرید
    return render(request, 'orders_app/shop_cart.html', {'order': order})
