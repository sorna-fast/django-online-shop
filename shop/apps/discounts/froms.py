from django import forms

class CouponForm(forms.Form):
    coupon_code = forms.CharField(label="",
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"کد تخفیف"}),
                                  required=False
                                  

)