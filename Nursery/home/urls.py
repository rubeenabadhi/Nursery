from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('nursery_dashboard', views.nursery_dashboard, name='nursery_dashboard'),
    path('addplant_item/<int:admin_id>/',views.addplant_item,name='addplant_item'),
    path('<slug:cat_slug>/', views.home, name='categview'),
    path('<slug:cat_slug>/<slug:plant_slug>',views.plant_details,name='plant_details'),
    path('shop', views.shop, name='shop'),
    path('blog',views.blog,name='blog'),
    path('search',views.searching,name='search'),
    path('user_dashboard',views.user_dashboard,name='dashboard'),
    path('send_feedback_view',views.send_feedback_view,name='send_feedback'),
    path('feedback_done', views.feedback_done, name='feedback_done'),
    path('view_feedback/<int:admin_id>/', views.view_feedback, name='view_feedback'),
    path('admin_plants/<int:admin_id>/', views.admin_plants, name='admin_plants'),
    path('contact', views.contact, name='contact'),
    path('edit_plant/<int:plant_id>/', views.edit_plant, name='edit_plant')

            ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)