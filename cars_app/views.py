from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product, Cart, Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Empty Fields"
        elif upass != ucpass:
            context['errmsg']="Both Passwords not match"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="Created Successfully, You can Login now"
            except Exception:
                context['errmsg']="Account with same username already there!!!!"
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Empty Fields"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                context['errmsg']="Please write valid username and password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):  
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1&q2)
    print(p)    
    context={}
    context['products']=p    
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=Product.objects.order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)   
        p=Product.objects.filter(id=pid)   
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(c)  
        n=len(c)   
        context={}
        if n == 1: 
            context['msg']="Parts are already present in Store!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Part is added to Store!!"
        context['products']=p
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id) 
    np=len(c)    
    s=0
    for x in c:
        s=s + x.pid.price * x.qty
    print(s)
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)

def remove(request,cid):   
    c=Cart.objects.filter(id=cid)   
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
    else:
       if c[0].qty>1:
            t=c[0].qty - 1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id 
    c=Cart.objects.filter(uid=userid) 
    oid=random.randrange(1000,9999)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()  
    context={}
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders) 
    context['data']=orders
    context['n']=np
    s=0
    for x in orders:
        s= s + x.pid.price * x.qty
    context['total']=s 
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s= s + x.pid.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_10OBDkwWTbBzdQ", "NxP46jxjJOPC09CmcNggVsga"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    uemail=request.user.email
    print(uemail)
    context['uemail']=uemail
    return render(request,'pay.html',context)

def sendusermail(request,uemail):
    msg="Store details are:---"
    send_mail(
        "Parts are placed successfully",
        msg,
        "nikhilsurtekar88@gmail.com",  
        [uemail], 
        fail_silently=False,
    )
    return HttpResponse("Mail sent successfully")


    
