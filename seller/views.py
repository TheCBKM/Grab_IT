from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import Seller, Category, SubCategory, Product, Pcount


# Create your views here.
def home(request):
    pcount = Pcount.objects.get(id=1)
    c = pcount.count + 1
    pcount.count = c
    print(pcount.count)
    pcount.save()
    users = User.objects.all().count()
    print(users)
    context = {
         'users' : users,
         'count' : c

    }
    return render(request,'seller/home.html', context)

def seller(request):
    return render(request,'seller/slogin.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        branch = request.POST['branch']                                        
        contact = request.POST['contact']
        print(username,email,contact)     

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('/seller')
            else:
                user = User.objects.create_user(username=username, email=email, password = password1, first_name = password1)
                seller = Seller(user_id=user.id, branch=branch, contact=contact, lcount=1)
                user.save()
                seller.save()
                print('user created')
                user = auth.authenticate(username=username,password=password1)
                if user is not None:
                    auth.login(request,user)
                    return redirect('addProduct')
                else:
                    return redirect('seller')
        else:
            messages.info(request,'password matched incorrect')
            return redirect('seller')
    else:
        return redirect('/seller')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            cuser = User.objects.get(email=email)
            print(cuser)
            cseller = Seller.objects.get(user_id=cuser.id)
            user = auth.authenticate(username=cuser.username, password=password)
            seller = Seller.objects.get(user_id=user.id)
            print("=========")
            print(user,seller)
            print("========")
            if user is not None:
               
                if seller.isadmin == 1:
                    auth.login(request,user)
                    return redirect('dashboard')
                else:
                    auth.login(request,user)
                    c = seller.lcount + 1
                    seller.lcount = c
                    print(seller.lcount)
                    seller.save()
                    
                    return redirect('addProduct')
            else:
                return redirect('seller')
        except:
            print('except')
            return redirect('seller')

    else:
        return redirect('seller')

def logout(request):
    auth.logout(request)
    return redirect('seller')

def dashboard(request):
    return HttpResponse('dashboard')

def addProduct(request):
    
    if not request.user.is_authenticated:
        return redirect('seller')
    else:
        #print(request.session['seller'])    
        category = Category.objects.all()
        subCategory = SubCategory.objects.all()
        context = {'category':category, 'subCategory':subCategory}
        return render(request,'seller/product.html', context)


def getCategory(request,c_id):
        print(c_id)
        if c_id == '-1':
            res = "<option value='-1'>please select category</option>"
        else:
            res = ''
            subCategory = SubCategory.objects.filter(category_id=c_id)
            for s in subCategory:
                res+='<option value='+ str(s.id) +' >'+s.name+'</option>'
            res+='<option value="4">others</option>'
            print(subCategory)
        return HttpResponse(res)



def getSubCategory(request, s_id):
    if s_id == '-1':
        res = "<option value='-1'>please select subcategory</option>"
    else:
        products = Product.objects.filter(subcategory_id=s_id)
        res = ''
        for p in products:
            res+='<option value='+ str(p.id) +'>'+p.name+'</option>'
        res+='<option value="o">others</option>'
        
    return HttpResponse(res)
   
def checkmail(request, email_id):
    print(email_id)
    res=''
    if User.objects.filter(email=email_id).exists():
        res = 'email already registered'
        return HttpResponse(res)
    else:
        return HttpResponse('')

def storeProduct(seller, category, subcategory, name, contact, price, status, image):
    tempProduct = Product(seller=seller,contact=contact ,name=name ,price=price, category=category, subcategory=subcategory, status=status, image=image)
    tempProduct.save()



def sendProduct(request):

    price = request.POST['price']
    contact = request.POST['contact']
    image = request.FILES['image']
    # return HttpResponse(image)
    print(request.user.email)
    uid=request.user.id
    # user = User.objects.get(username=User.username)
    seller = Seller.objects.get(user_id=uid)
    
    if request.method == 'POST':
        try:
            if request.POST['addNewProduct']:
                if request.POST['category'] != '3':
                    print('category found')
                    if request.POST['subcategory'] != '4':
                        print('subcategory found')
                        if request.POST['product'] != 'o':
                            print('product found')
                        else:
                            category = request.POST['category']
                            subcategory = request.POST['subcategory']
                            product = request.POST['addNewProduct']
                            cat = Category.objects.get(id = category)
                            sub = SubCategory.objects.get(id = subcategory)
                            
                            storeProduct(seller, cat, sub, product, contact, price, 0, image)
                            print('product others')
                            return redirect('/seller/sellerhome')
                            return HttpResponse('product Others')
                    else:
                        category = request.POST['category']
                        product = request.POST['addNewProduct']
                        cat = Category.objects.get(id = category)
                        sub = SubCategory.objects.get(name = 'others')
                        # seller = Seller.objects.get(id=4)
                        storeProduct(seller, cat, sub, product, contact, price, 4, image)
                        print('subcategory others')
                        return redirect('/seller/sellerhome')
                        return HttpResponse('SubCategory Others')
                else:
                    category = request.POST['category']
                    product = request.POST['addNewProduct']
                    cat = Category.objects.get(name = 'others')
                    sub = SubCategory.objects.get(name = 'others')
                    # seller = Seller.objects.get(id=4)
                    storeProduct(seller, cat, sub, product, contact, price, 3, image)
                    
                    print('category others')
                    return redirect('/seller/sellerhome')
                    return HttpResponse('Category Others')
        except:
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            product = request.POST['product']
            if category == '-1':
                messages.info(request,'!!Please Select Relevant Options!!')
                return redirect('/addProduct/')
            elif subcategory == '-1':
                messages.info(request,'!!Please Select Relevant Options!!')
                return redirect('/addProduct/')
            elif product == '-1':
                messages.info(request,'!!Please Select Relevant options!!')
                return redirect('/addProduct/')
            print(product)
            prod = Product.objects.get(id = product)
            cat = Category.objects.get(id = category)
            sub = SubCategory.objects.get(id = subcategory)
            # seller = Seller.objects.get(id=4)
            storeProduct(seller, cat, sub, prod.name, contact, price, 0, image)
            return redirect('/seller/sellerhome')
            return HttpResponse('Product Found')

def sellerhome(request):
    if not request.user.is_authenticated:
        return redirect('seller')
    else:

        print(request.user.id)
        seller = Seller.objects.get(user=request.user)
        products = Product.objects.filter(seller=seller)
        context = {'products':products}
        return render(request,'seller/shome.html',context)

def sold(request, product_id):
    product = Product.objects.get(id = product_id)
    product.status = 2
    product.save()

    return redirect('/seller/sellerhome')

def buyer(request):
    categorys = Category.objects.all()
    subcategorys = SubCategory.objects.all()
    products = Product.objects.all()
    context = {'categorys' : categorys,
    'subcategorys' : subcategorys,
    'products' : products,
    }
    return render(request, 'seller/buyer.html' ,context)

def subcategory(request, cat_id):
    category = Category.objects.get(id=cat_id)
    subcategorys = SubCategory.objects.filter(category=category)
    products = []
    for subcategory in subcategorys:
        product = Product.objects.filter(subcategory=subcategory)
        for pro in product:
            products.append(pro)
    context={
        'subcategorys':subcategorys,
        'products':products,
    }

    
    print(products)
    
    return render(request,'seller/buyproduct.html', context)

# def error_404(request, exception):
#     return HttpResponse('Hello 404')

# def error_500(request):
#     return HttpResponse('Hello 500')





