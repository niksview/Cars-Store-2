from django.urls import path
from cars_app import views
from django.conf.urls.static import static
from cars import settings

urlpatterns = [
    path('about',views.about),
    path('contact',views.contact),
    path('',views.home),
    path('pdetails/<pid>',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
