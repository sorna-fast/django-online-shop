def create_random_code(count):
    import random
    count-=1
    return random.randint(10**count,10**(count+1)-1)
#-----------------------------------------------------------------------------------------
# سورس کد تستی استفاده از سامانه پیامکی کاوه نگار
import kavenegar
def send_SMS(mobile_number,message):
    ...
    # try:
    #     api= kavenegar.KavenegarAPI("6E5566497267596E4F643764556C725A4D716D5A777744575351616A6B64516538685848676461476777303D")
    #     params={'sander':'','receptor':mobile_number,'message':message}
    #     response = api.sms_send(params)
    #     return response
    # except kavenegar.APIException as error:
    #     print(f"APIException : {error}")
    # except kavenegar.HTTPException as error:
    #     print(f'HTTPException : {error}')
#-----------------------------------------------------------------------------------------
import os
from uuid import uuid4 
   
class FileUpload:
    def __init__(self,dir,prefix):
        self.dir=dir
        self.prefix=prefix
    def upload_to(self,instance,filename):
        filename,ext=os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'
#-----------------------------------------------------------------------------------------
def price_by_delivery_tax(price,discount=0):
    delivery=25
    if price>500000:
        delivery=0
    tax=(price+delivery)*0.09
    sum_=price+delivery+tax
    sum_=sum_-(sum_+discount/100)
    return int(sum_),delivery,int(tax)
