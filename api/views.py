from django.http.response import JsonResponse
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Category, Post
from api.serializers import CategorySerialize, PostSeriliazer, UserSerializer
from rest_framework import generics
from rest_framework import filters
from api.pagination import PostListPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User


# Get List of Categories and Search List of Categories
class List_Search_Category(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Category.objects.all().order_by('id').reverse()
    serializer_class = CategorySerialize
    
# Get Single Category Record
class Single_Category(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialize

# Get List of Post and Search List of Posts
class List_Search_Post(generics.ListAPIView):
    search_fields = ['title','=category__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Post.objects.all().order_by('date').reverse()
    serializer_class = PostSeriliazer
    pagination_class = PostListPagination
# Get List of Post By Category Id
class List_Category_Wise_Post(generics.ListAPIView):
    search_fields = ['=category__id']
    filter_backends = (filters.SearchFilter,)
    queryset = Post.objects.all().order_by('date').reverse()
    serializer_class = PostSeriliazer

# Get Single Post Record
class Single_Post(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSeriliazer

# Get List of Filtered Posts according ids
# Taking query parameter of type : ids=1,2,3
class getList(APIView):
    def get(self,request):
        id_list = request.GET.get('ids')
        id_list = id_list.split(',')
        if id_list is not None:
            try:
                post = Post.objects.filter(pk__in=id_list)
            except:
                post = Post.objects.all()
                serialized_data = PostSeriliazer(post,many=True)
                return JsonResponse(serialized_data.data,safe=False)
        else:
            post = Post.objects.all()
        serialized_data = PostSeriliazer(post,many=True)
        return JsonResponse(serialized_data.data,safe=False)

#Create User , SignUp
@method_decorator(csrf_exempt,name='post')
class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

#Login User and Get Token
class CutomAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny ]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created =Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }) 
