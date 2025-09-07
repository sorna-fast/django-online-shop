from django.contrib import admin
from .models import Comment
# باید توی پنل ادمین هم کامنت ها رو ببینم - که مدیر در فعال یا غیرفعال کنترل کنه

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'commenting_user', 'comment_text', 'is_active']
    list_editable = ['is_active']
