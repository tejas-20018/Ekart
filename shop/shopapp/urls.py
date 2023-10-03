
from django.contrib import admin
from django.urls import path
from shopapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    
    path("edit",views.edit),
    path("delete",views.delete),
    path("edit/<rid>",views.edit),
    path("greet",views.greet),
    path("index",views.index),
    path("details/<id>",views.details),
    path("payment",views.payment),
    path("contact",views.contact),
    path('register',views.register),
    path('userlogin',views.userlogin),
    path("catfilter/<cv>",views.catfilter),
    path('pricerange',views.pricerange),
    path('sort/<sv>',views.sort),
    path('userlogout',views.logout),
    path('addcart/<rid>',views.addcart),
    path('cart',views.cart),
    path('remove/<rid>',views.removecart),
    path('qty/<sig>/<pid>',views.cartqty),
    path('order',views.place_order),
    path('payment',views.payment),
    path("sendmail",views.sendmail),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


