from rest_framework.permissions import BasePermission,SAFE_METHODS

# anvaye method haye ma 'GET','POST','PUT','DELETE',
# SAFE_METHOD be permission niyaz nadare

class CustomPermissionForProductFeature(BasePermission):
    message = "شما امکان حدف ویژگی را ندارید"
    def has_permission(self,request,obj):
        return request.user and request.user.is_authenticated
    
    # def has_object_permission(self,request,view,obj): #badaz inke ehraze hoviyat anjam shod.
    #     # request : darxaste amade az samte karbar ast, va mitunim check konim noye darxast chi boode, va ki un darxast ro dade.
    #     # object : sample of the model we wanna change. hamun nemooneh ii ke User mixad taghiresh bede. 
    #     if request.method in SAFE_METHODS:              
    #         return True             
    #     return obj.user_register == request.user
                                                               
                                                               
                                                               
# ویژگی                                          توضیح
# ------------------------------------------------------------------------
# request.user                  | آبجکت کاربر (ممکنه لاگین کرده باشه یا نه)
# request.user.is_authenticated | فقط می‌گه این کاربر لاگین کرده یا نه (True / False)