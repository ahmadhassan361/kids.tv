from api.models import Category,Post
from django.contrib import admin

# Register your models here.
@admin.register(Category)
class catAdmin(admin.ModelAdmin):
    list_display = ['id','name','image']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','category','thumbnail','yt_link','video','date']
