from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.urls import path

from apps.task import task_send_email
from apps.utils import send_email
from apps.views import IndexView, BlogListView, BlogDetailView, CustomLoginView, RegisterFormView, ShopListView, \
    EmailView


def send_email_task(req):
    task_send_email.delay('math', 'fgf', ['behruzpdp01@gmail.com'])
    return JsonResponse({'success': True})


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog-list', BlogListView.as_view(), name='blog_list_page'),
    path('blog-detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail_page'),
    path('logout', LogoutView.as_view(next_page='login_page'), name='logout'),
    path('login', CustomLoginView.as_view(), name='login_page'),
    path('register', RegisterFormView.as_view(), name='register_page'),
    path('shop-list', ShopListView.as_view(), name="shop-list"),
    path('newletter/', EmailView.as_view(), name="newletter"),
    path('send/', send_email_task)
]
