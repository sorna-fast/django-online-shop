from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .forms import CommentForm
from apps.products.models import Product
from apps.comment_scoring_favorites.models import Comment,Favorite
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

class CommentView(View):
    def get(self, request, *args, **kwargs):
        productId = request.GET.get("productId")
        commentId = request.GET.get("commentId")
        slug = kwargs['slug']
        
        # مقدار دهی اولیه فرم - کلید ها باید هم نام با فیلد های فرم باشن میریزشون تو اینپوت مخفیا
        initial_dict = {
            "product_id": productId,
            "comment_id": commentId,
        }
        
        form = CommentForm(initial=initial_dict)
        
        context = {
            "form": form,
            "slug": slug,
        }
        
        return render(request, "csf_app/partials/create_comment.html", context)
    
    
    def post(self, request, *args, **kwargs):
        
        slug = kwargs.get("slug")
        product = get_object_or_404(Product, slug=slug)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            # check if it is comment to post or replay to a comment
            parent = None
            if(cd['comment_id']):
                parentId = cd['comment_id']  
                parent = Comment.objects.get(id=parentId)
                
            Comment.objects.create(
                product = product,
                commenting_user = request.user,
                comment_text = cd['comment_text'],
                comment_parent = parent
            )
            
            messages.success(request, "نظر شما با موفقیت ثبت شد", "success")
            return redirect("products:product_details", product.slug)
        messages.error(request, "خطا در ثبت نظر", "danger")
        return redirect("products:product_details", product.slug)
    
    
# -----------------------------------------------------------------------------------------------------------------

from .models import Scoring
from django.http import JsonResponse

def add_score(request):
    productId = request.GET.get('productId')
    score = request.GET.get('score')
    
    product = Product.objects.get(id=productId)
    Scoring.objects.create(
        product = product,
        scoring_user = request.user,
        score = score,
    )
    
    avg_score = product.get_average_score()
    
    return JsonResponse({
        'message': 'امتیاز شما با موفقیت ثبت شد',
        'avg_score': round(avg_score, 1)
    })
# -----------------------------------------------------------------------------------------------------------------


def add_to_favorites(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'لطفا وارد شوید'}, status=403)
    
    if request.method == 'GET':
        product_id = request.GET.get('productId')
        product = get_object_or_404(Product, id=product_id)
        
        favorite, created = Favorite.objects.get_or_create(
            favorite_user=request.user,
            product=product
        )
        
        if not created:
            favorite.delete()
            status = 'removed'
            icon_class = 'fa-heart-broken'
            message = 'از علاقه‌مندی‌ها حذف شد'
        else:
            status = 'added'
            icon_class = 'fa-heart'
            message = 'به علاقه‌مندی‌ها اضافه شد'
        
        return JsonResponse({
            'status': status,
            'icon_class': icon_class,
            'message': message
        })
    

#----------------------------------------------------------------------------------------------------------------------------

class UserFavoriteView(View):
    def get(self,request,*args, **kwargs):
        user_favorite_product=Favorite.objects.filter(Q(favorite_user=request.user.id))
        return render(request, "csf_app/user_favorites.html",{"user_favorite_product":user_favorite_product})
    
@login_required
def status_of_favorite(request):
    count = Favorite.objects.filter(favorite_user=request.user).count()
    return JsonResponse({'count': count})