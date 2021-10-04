
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/cat/', views.List_Search_Category.as_view()),
    # path('api/cat/<int:pk>', views.Single_Category.as_view()),
    path('api/post/', views.List_Search_Post.as_view()),
    path('api/post/cat/', views.List_Category_Wise_Post.as_view()),
    # path('api/post/<int:pk>', views.Single_Post.as_view()),
    url('api/post/fav/', views.getList.as_view()),
    path('api/login/', views.CutomAuthToken.as_view(), name='gettoken'),
    path('api/createuser/', csrf_exempt(views.CreateUserView.as_view()))


    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
