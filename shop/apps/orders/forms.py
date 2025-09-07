from django import forms
from .models import Order,PaymentType

# Chice_PaymentType=((1,"پرداخت از طریق درگاه بانکی"),(2,"پرداخت در محل"))
class OrderForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام'
        }),
        error_messages={
            'required': 'این فیلد نمیتواند خالی باشد'
        },

        
    )
    
    family = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی'
        }),
        error_messages={
            'required': 'این فیلد نمیتواند خالی باشد'
        },

    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }),
        required=False
    )
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره تلفن'
        }),
        required=False
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'آدرس',
            "rows": "2",

        }),
        error_messages={
            'required': 'این فیلد نمیتواند خالی باشد'
        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'توضیحات',
            "rows": "4"
        }),
        required=False
    )
    
    payment = forms.ModelChoiceField(
        queryset=PaymentType.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )
