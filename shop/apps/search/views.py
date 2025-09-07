from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from apps.products.models import Product

# Create your views here.


# ?q=پفک
# در کوئری درواقع داریم که کلمه کلیدی که کاربر وارد کرده رو میگیریم
# __icontains : واسه برسی شامل بودن - کافیه کلمه ی سرچ شده توی نام پروداکت ها وجود داشته باشه

# Q(product_name__icontains=query) |
# Q(product_description__icontains=query)
# بهش میگیم علاوه بر نام ها توی توضیحاتشونم نگاه کن

class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        
        products = Product.objects.filter(
            Q(produce_name__icontains=query) |
            Q(description__icontains=query) |
            Q(summery_description__icontains=query)
        )
        
        context = {
            "products": products,
        }
        
        return render(request, 'search_app/search.html', context)