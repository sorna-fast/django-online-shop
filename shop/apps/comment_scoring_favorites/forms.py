from django import forms

# parent_id : یا می گیم روی چه کالایه
# comment_id : یا می گیم روی چه کامنتیه
# widget=forms.HiddenInput() : این فیلد مخفیه

class CommentForm(forms.Form):
    
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    comment_text = forms.CharField(label="", error_messages={'required':'این فیلد نمیتواند خالی باشد'} ,widget=forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'متن نظر' , 'rows': '4'}))