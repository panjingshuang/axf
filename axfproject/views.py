from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Nav,Mustbuy,Shop,MainShow,FoodTypes,Goods, User,wheel,Cart,Order
import os
from django.conf import settings
import time
import random
from django.contrib.auth import logout
# Create your views here.

def home(request):
    wheelsList = wheel.objects.all()
    navList = Nav.objects.all()
    mustbyList = Mustbuy.objects.all()
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2= shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    mainList = MainShow.objects.all()

    return render(request,'axfproject/home.html',{"title":"home","wheelsList":wheelsList,
                    'navList':navList,'mustbyList':mustbyList,'shop1':shop1,'shop2':shop2,'shop3':shop3,'shop4':shop4,'mainList':mainList})


def market(request,categoryid,cid,sortid):
    leftSlider = FoodTypes.objects.all()

    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid=cid)

    if sortid == '1':
        productList = productList.order_by('productnum')
    elif sortid=='2':
        productList = productList.order_by('price')
    elif sortid=='3':
        productList = productList.order_by('-price')

    group = leftSlider.get(typeid=categoryid)
    childNameList = []
    childnames  = group.childtypenames
    arrl = childnames.split('#')
    for str in arrl:
        arr2 = str.split(":")
        obj = {'childName':arr2[0],'childId':arr2[1]}
        childNameList.append(obj)

    cartlist = []
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)

    for p in productList:
        for c in cartlist:
            if c.productid == p.productid:
                p.num = c.productnum
                continue

    return render(request, 'axfproject/market.html',{"title":"market",'leftSlider':leftSlider,
    'productList':productList,'childNameList':childNameList,'categoryid':categoryid ,'cid':cid})



def cart(request):
    cartslist = []
    token = request.session.get("token")
    if token == None:
        return redirect('/login/')
    else:
        userdemo = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount = userdemo.userAccount)
        return render(request, 'axfproject/cart.html', {"title":"购物车","cartslist":cartslist,'user':userdemo})






#修改购物车
def changecart(request,flag):
    #判断是否登陆,利用token值
    token = request.session.get('token')
    if token is None:
        return JsonResponse({"data":-1})
    else:
        # # 先根据这个人的token将人的账号值获取得到，再根据商品id将商品的信息获取得到
        productid = request.POST.get('productid')
        user = User.objects.get(userToken= token)
        food = Goods.objects.get(productid=productid)
        my_cart = Cart.objects.filter(productid=productid)

        c = None
        price = 0
        if flag == '0':
            if food.storenums == 0:
                return JsonResponse({'data': -2})
            if my_cart.count() == 0:
                # 购物车中不存在该食品时,就直接添加
                c = Cart.createcart(user.userAccount,productid,1,food.price,True,food.productimg,food.productlongname,False)
                price = food.price
                c.save()
                number = 1;
            else:
                c = Cart.objects.get(productid=productid,userAccount=user.userAccount)
                c.productnum = c.productnum+1
                number = c.productnum
                c.productprice = "%.2f" % (float(food.price)*c.productnum)
                price = c.productprice
                c.save()
            food.storenums = food.storenums-1
            food.save()
            return JsonResponse({'data': 0,'price':price, 'status': 'success', 'number': number})
        elif flag == '1':
            # 购物车中是否存在该人买的该物
            #若存在就修改数量和价格 ，以及在库存中的数量，当对该商品的数据减到0的时候就删除
            if my_cart.count() == 0:
                # 购物车中不存在该食品时,就直接添加
                return JsonResponse({'data':-2})
            else:
                c = Cart.objects.get(productid=productid,userAccount=user.userAccount)
                c.productnum = c.productnum-1
                number = c.productnum
                c.productprice = "%.2f" % (float(food.price)*c.productnum)
                price = c.productprice
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
                food.storenums = food.storenums+1
                food.save()
                return JsonResponse({'data': 1,'price':price, 'status': 'success', 'number': number})

        elif flag == '2':
            c = Cart.objects.get(productid=productid, userAccount=user.userAccount)
            c.isChose = not c.isChose
            c.save()
            str = ""
            if c.isChose:
                str= '√'
            all_user_food = Cart.objects.filter(userAccount=user.userAccount)
            search_all = 1
            for item in all_user_food:
                if item.isChose != True:
                    search_all =0


            return JsonResponse({'data':2,'ischose':str,'search_all':search_all})



def saveorder(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({"data": -1})
    else:
        user = User.objects.get(userToken=token)
        c = Cart.objects.filter(userAccount=user.userAccount,isChose= True)

        if c.count() ==0:
            return JsonResponse({'data':0})
        else:
            money = 0
            oid = time.time() + random.randrange(1,100000)
            oid = "%2d" % oid
            order = Order.createorder(oid,user.userAccount,0)
            order.save()
            for item in c:
                item.isDelete = True
                item.orderid = oid
                item.save()
            return JsonResponse({'status':'success'})













def mine(request):
    username = request.session.get('username')
    return render(request, 'axfproject/mine.html',{"title":"mine",'username':username})

from .forms.models import LoginForm
def login(request):

    if request.method=='POST':
        f = LoginForm(request.POST)
        if f.is_valid():

            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            try:
                user = User.objects.get(userAccount=username)
                if password != user.userPasswd:
                     print("sss")
                     return redirect('/login/')
            except User.DoesNotExist as e :
                return redirect('/login/')

            user.userToken = time.time() + random.randrange(1, 100000)
            user.save()

            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axfproject/login.html', {"title": "login",'error':f.errors})
    else:
        f = LoginForm()
        return render(request, 'axfproject/login.html', {"title": "login",'form':f})


def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get('userAccount')
        userPasswd = request.POST.get('userPasswd')
        userName = request.POST.get('userName')
        userPhone= request.POST.get('userPhone')
        userAdderss = request.POST.get('userAdderss')

        userToken = time.time() + random.randrange(1, 100000)
        userToken = str(userToken)
        userRank = 0

        f = request.FILES["userImg"]
        userImg  = os.path.join(settings.MDEIA_ROOT,userAccount+".png")
        with open(userImg, 'wb') as fp:
            for item in f.chunks():
                fp.write(item)
        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()

        request.session['username'] = userName
        request.session['usertoken'] = userToken

        return redirect('/mine/')



    else:
        return render(request, 'axfproject/register.html', {"title": "register", })


def checkuserid(request):
    if request.method=='POST':
        userid = request.POST.get('userid')
        try:
            user = User.objects.get(userAccount=userid )
            return JsonResponse({'status':'error'})
        except User.DoesNotExist as e:
            return JsonResponse({'status':'success'})
    else:
        return render(request, 'axfproject/register.html', {"title": "register",})


def quit(request):
    logout(request)
    return redirect('/mine/')