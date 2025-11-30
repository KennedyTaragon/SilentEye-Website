from django.urls import path

from .views.home import homepage_view, contact_form_view
from .views.blog import blog_list_view, blog_detail_view
from .views.products import product_list_view, product_detail_view

app_name = 'website'

urlpatterns = [
    path('', homepage_view, name='home'),
    path('contact/', contact_form_view, name='contact_submit'),
    path('blog/', blog_list_view, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail_view, name='blog_detail'),
    path('products/', product_list_view, name='product_list'),
    path('products/<slug:slug>/', product_detail_view, name='product_detail'),
]