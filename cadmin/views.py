from django.shortcuts import render, redirect
from seller.models import Seller, Category, SubCategory, Product, Request
from django.http import HttpResponse
from . import views
# Create your views here.
def admindash(request):
    if not request.user.is_authenticated:
        return redirect('seller')
    else:

        products = Product.objects.all().order_by()[::-1] 
        context = {'products':products}
        print(products)
        return render(request, 'cadmin/admindash.html', context)

def productDetails(request, product_id):
    if not request.user.is_authenticated:
        return redirect('seller')
    else:

        product = Product.objects.get(id=product_id)
        return render(request, 'cadmin/productDetails.html',{'product':product})

def finalProduct(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')

        print('1')
        try:
            if request.POST['approve']:
                cname = request.POST.get('cname')
                sname = request.POST.get('sname')
                pname = request.POST.get('pname')
                print(cname)
                print(Category.objects.filter(name=cname).exists())
                print('approve')
                if Category.objects.filter(name=cname).exists():
                    print('2')
                    if SubCategory.objects.filter(name=sname).exists():
                        print('sab mil gaya')
                        product = Product.objects.get(id=pid)
                        product.status = 1
                        category =  Category.objects.get(name=cname)
                        subcategory =  SubCategory.objects.get(name=sname)
                        product.category = category
                        product.subcategory = subcategory
                        product.name = pname
                        product.save()
                        return redirect('dashboard')
                    else:
                        product = Product.objects.get(id=pid)
                        product.status = 1
                        category =  Category.objects.get(name=cname)
                        subcategory = SubCategory(category=category,name=sname)
                        subcategory.save()
                        product.category = category
                        product.subcategory = subcategory
                        product.name = pname
                        product.save()
                        return redirect('dashboard')
                else:
                    product = Product.objects.get(id=pid)
                    category = Category(name=cname)
                    category.save()
                    subcategory = SubCategory(category=category,name=sname)
                    subcategory.save()
                    product.status = 1
                    product.category = category
                    product.subcategory = subcategory
                    product.name = pname
                    product.save()
                    return redirect('dashboard')


                        



                # product = Product.objects.get(id=pid)
                # category = Category(name=cname)
                # category.save()
                # subcategory = SubCategory(category=category,name=sname)
                # subcategory.save()
                # product.status = 1
                # product.category = category
                # product.subcategory = subcategory
                # product.name = pname
                # product.save()

                # print(product.name)

                
        except:
            product = Product.objects.get(id=pid)
            product.status = -1
            product.save() 
            print('disapprove')
            return redirect('dashboard')

        
        
    else:
        return HttpResponse('not valid')


def adminHelp(request):
    if not request.user.is_authenticated:
        return redirect('seller')
    else:
        category = Category.objects.all()
        subcategory = SubCategory.objects.all()
        product = Product.objects.all()
        context = {
            'products':product,
            'subcategorys':subcategory,
            'categorys':category
        }
        return render(request,'cadmin/adminHelp.html',context)

def requestAdmin(request):
    if not request.user.is_authenticated:
        return redirect('seller')
    else:
        details = Request.objects.all().order_by()[::-1] 
        context = {
            'details':details
        }
        return render(request,'cadmin/requestadmin.html',context)
