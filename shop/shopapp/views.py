from django.shortcuts import render,HttpResponse,redirect
from shopapp.models import Product,Cart,Orders
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay
from django.core.mail import send_mail

def home(request):
    p=Product.objects.all()
    print(p)
    context={}
    context['user']="Itvedant"
    context['x']=30
    context['y']=40
    context['l']=[10,20,30,40]
    context['d']={"id":1,"name":"soap","price":100}
    context['data']=[
        {'id':1,'name':'soap','price':100},
        {"id":2,"name":"fridge","price":200},
        {"id":3,"name":"fruit","price":200},
    ]
    context['products']=p
    return render(request,"home.html",context)
    
def edit(request,rid):
    if request.method=="GET":
        p=Product.objects.filter(id=rid)
        context={}
        context['data']=p
        return render(request,'editproduct.html',context)
            
    else:
        uname=request.POST['pname']
        uprice=request.POST['price']
        #print("Name:",uname)
        #print("price:",uprice)
        p=Product.objects.filter(id=rid)
        p.update(name=uname,price=uprice)
        return redirect("/home")

def delete(request,rid):
    p=Product.objects.filter(id=rid)
    p.delete()
    return redirect('/home')



def greet(request):
    return render(request,"base.html")

def addproduct(request):
    print(request.method)
    if request.method=="GET":
        print("in if part")
        return render(request,"addproduct.html")
    else:
        print("in else part")
        product_name=request.POST["pname"]
        price=request.POST["price"]
        print("name:",product_name)
        print("price:",price)
        p=Product.objects.create(name=product_name,price=price)
        print("Product Object:",p)
        p.save()
       # return HttpResponse("Data is inserted")
        return redirect('/home')

def index(request):
    uid=request.user.id
    print(request.user.is_authenticated)
    print(request.user.username)
    p=Product.objects.filter(is_active=True)
    context={}
    context['product']=p
    return render(request,'index.html',context)

    
def details(request,id):
    p=Product.objects.filter(id=id)
    context={}
    context['products']=p
    return render(request,'details.html',context)

def contact(request):
    return render(request,'contact.html')


def payment(request):
    return render(request,'payment.html')

def register(request):
    context={}
    if request.method=="GET":
        return render(request,'register.html')
    
    else:
        user=request.POST['username']
        p=request.POST['psw']
        cp=request.POST['cpsw']
        #validation
    if user=='' or p=='' or cp=='':
        context['errmsg']='Fields cannot be empty'
        return render(request,'register.html',context)

    elif p!=cp:
        context['errrmsg']='password does not match'
        return render(request,'register.html',context)
    else:
        try:
            u=User.objects.create(username=user,password=p)
            u.set_password(p)
            u.save()
            context['success']='create user successfully'
            return render(request,'register.html',context)
        except Exception:
            context['errrmsg']='user already exists'
            return render(request,'register.html',context)



def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=1)
    #p=Product.objects.filter(cat=cv)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def pricerange(request):

    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=1)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def sort(request,sv):

    if sv== '1':
        para='-price'
    else:
        para='price'
    p=Product.objects.order_by(para).filter(is_active=1)
    context={}
    context['products']=p
    return render(request,'index.html',context)



def userlogin(request):
    context={}
    if request.method=='GET':
        return render(request,'userlogin.html')

    else:
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(lname)
        #print(lpass)
        u=authenticate(username=uname,password=upass)
        if u is not None:
            return redirect('/index')
        else:
            context['errmsg']='Invalid username and password'
            return render(request,'userlogin.html',context)

def userlogout(request):
        logout(request)
        return redirect('/userlogin')

def addcart(request,rid):
    context={}
    if request.user.id:
        p=Product.objects.filter(id=rid)
        u=User.objects.filter(id=request.user.id)
        q1=Q(pid=p[0])
        q2=Q(uid=u[0])
        res=Cart.objects.filter(q1 & q2)
        
        if res:
            context['dup']='product already exists in cart'
            context['products']=p
            return render(request,'details.html',context)
        else:
            u=User.objects.filter(id=request.user.id)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['products']=p
            context['success']='product added successfully in cart'
            return render(request,'details.html',context)
    else:
            return redirect('/userlogin')
        

def cart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(uid=request.user.id)
        i=len(c)
        s=0
        for x in c:
            s=s+(x.qty*x.pid.price)
        print('summation or total:',s)
        context['total']=s
        context['cdata']=c
        context['items']=i
        return render(request,'cart.html',context)
    else:
        return redirect('/userlogin')

def removecart(request,rid):
    c=Cart.objects.filter(id=rid)
    c.delete()
    return redirect('/cart')

def cartqty(request,sig,pid):
    q1=Q(uid=request.user.id)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    #print(c)
    qty=c[0].qty
    if sig== '0':
        if qty>1:
            qty=qty-1
            c.update(qty=qty)
    else:
        qty=qty+1
    c.update(qty=qty)
    print("Existing:",qty)
    return redirect("/cart")

def place_order(request):
    if request.user.is_authenticated:
        context={}
        c=Cart.objects.filter(uid=request.user.id)
        oid=random.randrange(1000,9999)
        print("Order Id:",oid)
        s=0
    
    for x in c:
        o=Orders.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
        o.save()
        x.delete

    o=Orders.objects.filter(uid=request.user.id)
    i=len(o)
    for  y in o:
        s=s+(y.qty*y.pid.price)
        
        
    context['cdata']=o
    context['total']=s
    context['items']=i
    return render(request,'order.html',context)

def payment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_f1UzTDh1Eifepl","sPlPnZzAL6NjvOwrhNxXUopC"))
    #print(client)
    o=Orders.objects.filter(uid=request.user.id)
    oid=str(o[0].order_id)
    s=0
    for y in o:
        s=s+(y.qty*y.pid.price)
    #print("Order Id:",oid)
    #print("Total:",s)
    s=s*100
    data = { "amount":s, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context['payment']=payment
    return render(request,'payment.html',context)

def sendmail(request):
    pid=request.GET['p1']
    oid=request.GET['p2']
    sign=request.GET['p3']
    rec_email=request.user.email 
    print(rec_email)

    #print('payment Id:',pid)
    #print("Order Id:",oid)
    #print("Signature:",sign)
    msg="Your order has been placed Successfully.Your Order Tracking ID:"+oid
    send_mail(
    "Ekart Order status",
    msg,
    "tejaskdm2001@gmail.com",
    [rec_email],
    fail_silently=False,
  )
    
    return HttpResponse("Email send")

    #uxtz fudd zmjv wdod APPCODE


            
            
            





    


