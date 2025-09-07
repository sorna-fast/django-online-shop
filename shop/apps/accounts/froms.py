from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="RePassword",widget=forms.PasswordInput)
    class Meta:
        model=CustomUser
        fields=['mobile_number','email',"name","family","gender"]

    def clean_password2(self):
        pass1= self.cleaned_data["password1"]
        pass2= self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار ان با عم مغایرت دارند")
        return pass2
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
#______________________________________________________________________________________________________        
class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کنید")
    class Meta:
        model=CustomUser
        fields=['mobile_number','email',"name","family","gender","is_active","is_admin"]
        
#______________________________________________________________________________________________________        

class RegisterUserForm(ModelForm):
    password1 = forms.CharField(label="رمز عبور",widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':'رمز عبور را وارد کنید'},))
    password2 = forms.CharField(label="تکرار رمز عبور",widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':'تکرار رمز عبور را وارد کنید'},))
    class Meta:
        model=CustomUser
        fields =['mobile_number']
        widgets={
            'mobile_number':forms.TextInput(attrs={'class':"form-control",'placeholder':'موبایل را وارد کنید'},),}

    def clean_password2(self):
        pass1= self.cleaned_data["password1"]
        pass2= self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار ان با عم مغایرت دارند")
        return pass2

#______________________________________________________________________________________________________        

# class VerifyregisterForm(forms.Form):
#     active_code=forms.CharField(label="کد فعال سازی",
#                                 error_messages={"required":"این فیلد نمیتواند خالی باشد"},
#                                 widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل خود را وارد کنید'}))

class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',error_messages={"required":"این فیلد نمی تواند خالی باشد"},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد دریافتی را وارد کنید'}))

#______________________________________________________________________________________________________        

class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label="شماره موبایل",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.TextInput(attrs={'class':"form-control","placeholder":"شماره موبایل را وارد کنید"}))
    password=forms.CharField(label="رمز ورود",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.PasswordInput(attrs={'class':"form-control","placeholder":" رمز را وارد کنید"}))

#______________________________________________________________________________________________________        

class ChangePasswordForm(forms.Form):
                                    
    password1=forms.CharField(label="رمز ورود",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.PasswordInput(attrs={'class':"form-control","placeholder":" رمز را وارد کنید"}))
                                 
    password2=forms.CharField(label="رمز ورود",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.PasswordInput(attrs={'class':"form-control","placeholder":"  تکرار رمز را وارد کنید"}))
    def clean_password2(self):
        pass1= self.cleaned_data["password1"]
        pass2= self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار ان با عم مغایرت دارند")
        return pass2

#______________________________________________________________________________________________________        


class RememberPasswordForm(forms.Form):
        mobile_number=forms.CharField(label="شماره موبایل",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.TextInput(attrs={'class':"form-control","placeholder":"شماره موبایل را وارد کنید"}))