# baxsh piyade sazi form haye marbut be CustomUser

# widgets برای سفارشی‌سازی ورودی‌های فرم
# می‌توانیم از widgets برای تغییر نحوه نمایش فیلدها استفاده کنیم:
# widgets = {
            # 'active_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد فعال‌سازی را وارد کنید'})
        # }

# for serializers we use extra_kwargs

# labels برای تغییر نام فیلدها
# نام نمایشی فیلدها را می‌توان تغییر داد:
# labels = {
#             'active_code': 'کد فعال‌سازی'
#         }

# help_texts برای راهنمایی کاربر
# اگر بخواهی زیر فیلد یک توضیح نمایش داده شود:
# help_texts = {
            # 'active_code': 'کد ۶ رقمی ارسال‌شده به شماره شما را وارد کنید.'
        # }

# __init__ برای شخصی‌سازی فرم در هنگام مقداردهی اولیه
# می‌توان مقدار پیش‌فرض فیلدها را تنظیم کرد:
# def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.fields['active_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'کد دریافتی را وارد کنید'})

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class UserCreationForm(ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="RePassword",widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['mobile_number','email','name','family','gender']
    
    # baraye emale shart ro field ha va check kardaneshun azin tabe estefade mikonim 
    # def clean(self) -> dict[str, Any]:
    #     return super().clean()
  
    # age faghat bexam field password2 ro check konam intor az clean estefade mikonam      
    # self, mohtavaye formi ast ke be dastemun reside.
    # baraye etebar sanji dar form ha.
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار ان با هم مغایرت دارد")
        return pass2
    
    # dobare nevisi tabe save modelform ha 
    # commit yani taiid nahaii shodan. va zamani etefagh miofte ke mixad zaxire beshe.
    # age in save ro dobare nevisi nakonam password ro bedune hash kardan ba baghiyeye dade ha save mikone.
    def save(self,commit=True):
        # commit false baes mishe user save nashe va user save nashode ro mirizim tu user
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

from django.contrib.auth.forms import ReadOnlyPasswordHashField

# mixam in passwordi ke in ja change mikonam baz hash beshe.
class UserChangeForm(ModelForm):
    # in baes mishe password dar safe changemun be surate read only bashe.
    # ezafe kardan be peighame marbute be password user marbute dar pannel admin.
    password  = ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کنید")
    class Meta:
        model = CustomUser
        fields = ['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
        

# hala bayad in form ha ro be panel admin ezaf konim.     

# ---------------------------------------------------------------------------------------------

# first step in creating form for usual user that don't normally access or use admin pannel though the model is the same.

class RegisterUserForm(ModelForm):
    # chon password field ro az jense form tarif kardi haminja tu forms besh lable ro midim.
    password1 = forms.CharField(label="رمز عبور",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    password2 = forms.CharField(label="تکرار رمز عبور",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}))
    class Meta:
        model = CustomUser
        # chon mobile field ro az jense model tarif kardi haminja tu model besh verbose_namesh ro midim.
        fields = ["mobile_number",]
        widgets = {
            "mobile_number" : forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'}),
        }
        
    def clean_password(self):
        pass1 = self.cleaned_data["passwprd1"]
        pass2 = self.cleaned_data["password2"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("پسورد و تکرار مجدد آن با هم مغایرت دارد")
        return pass2
        
        
# ----------------------------------------------------------------------------------------------------------------------
        
# در فیلد error_messages می‌توانید پیام‌های خطای مختلفی را برای انواع مختلف خطاهای اعتبارسنجی سفارشی کنید. به جز required
# invalid
# زمانی که مقدار ورودی معتبر نباشد، این پیام نمایش داده می‌شود.
# max_length
# زمانی که مقدار ورودی از مقدار max_length بیشتر باشد، این پیام نمایش داده می‌شود.
# min_length
# زمانی که مقدار ورودی از مقدار min_length کمتر باشد، این پیام نمایش داده می‌شود.
# max_value و min_value (برای فیلدهای عددی)
# برای مقدار بیش از حد مجاز یا کمتر از مقدار مجاز استفاده می‌شود.
# unique (در ModelForm)
# اگر مقدار وارد شده در دیتابیس از قبل وجود داشته باشد، این خطا نمایش داده می‌شود.

class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',error_messages={"required":"این فیلد نمی تواند خالی باشد"},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد دریافتی را وارد کنید'}))      
        
        
# ----------------------------------------------------------------------------------------------------------------------
        
# ijade formi baraye useri ke register ya sabte nam karde hala mixad login kone.
# az modele xasi tabaiyat nemikone.

# اگه تو لیبل اینجا چیزی بنویسیم سر تگ لیبل اچ تی ام ال اضاف میشه
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(max_length=11,label="موبایل",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل خود را وارد کنید'}))
        
    password = forms.CharField(label="رمز عبور",error_messages={"required":"این فیلد نمی تواند خالی باشد!"},widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' پسورد خود را وارد کنید'}))
    
# ------------------------------------------------------------------------------
            
# before Changing Password:
# we need a phone_number in this form and send user to an other page

class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label="موبایل",error_messages={'required':'شماره موبایل الزامی است'},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل خود را وارد کنید'}))

# ------------------------------------------------------------------------------



class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="رمز عبور",
                                error_messages={"required":"این فیلد نمی تواند خالی باشد!"},
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' پسورد خود را وارد کنید'}))
    
    password2 = forms.CharField(label="رمز عبور",
                                error_messages={"required":"این فیلد نمی تواند خالی باشد!"},
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' تکرار پسورد خود را وارد کنید'}))
    
    def clean_password(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password1']
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("پسورد و تکرار آن یکسان نمی باشد")
        return pass2
    
    
# ------------------------------------------------------------------------------

# readonly : به فیلدی میدیم که نمیخوایم تغییرش بده کاربر
class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل خود را وارد کنید','readonly':'readonly'}), error_messages={"required":"این فیلد نمی تواند خالی باشد!"})
    
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارد کنید'}), error_messages={"required":"این فیلد نمی تواند خالی باشد!"})
    
    family = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی خود را وارد کنید'}), error_messages={"required":"این فیلد نمی تواند خالی باشد!"})
    
    phone_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره تلفن ثابت خود را وارد کنید'}), error_messages={"required":"این فیلد نمی تواند خالی باشد!"})
    
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارد کنید'}),required=False)
    
    
    address = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'ادرس خود را وارد کنید'}), error_messages={"required":"این فیلد نمی تواند خالی باشد!"})
    
    
    image = forms.ImageField(label="",required=False)