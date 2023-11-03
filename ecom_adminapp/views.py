from django.shortcuts import render,redirect
from.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from decimal import Decimal

# Create your views here.


def admin_dash(request):
    
    return render(request,'index.html')

def orders(request):
    
    return render(request,'orders.html')

def admin(request):
    
    return render(request,'adminlogin.html')



def admin_login(request):
    if request.method == "POST":
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        
        user = authenticate(request, Username=Username, Password=Password)
        if user is not None:
            login(request, user)
            request.session['uid'] = Username
            return redirect('admin_dash')
        else:
            messages.error(request, "There is an error in logging in, please try again")
            return redirect('admin_dash')

    return render(request,'adminlogin.html')






def addcategory(request):
    if request.method=='POST':
        category_name=request.POST['category_name']
        category_image = request.FILES.get('category_image')
        if 'category_image':
            ctg=Addcategory(category_name=category_name,category_image=category_image)
            ctg.save()
            return redirect('category')
    return render(request,'addcategory.html')



def category(request):
    c=Addcategory.objects.all()
    return render(request,'category.html',{'ct':c})



def editcategory(request,pk):
    
    ct=Addcategory.objects.get(id=pk)
    
    if request.method=='POST':
        ct.category_name=request.POST['category_name']
        category_image = request.FILES.get('category_image')
        if category_image:
            ct.category_image = category_image
            ct.save()
        
        return redirect('category')
    return render(request,'editcategory.html',{'category':ct})



def deletecategory(request,pk):
    ct=Addcategory.objects.get(id=pk)
    ct.delete()
   
    return redirect('category')




def addsubcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_name')
        sub_category_name = request.POST['sub_category']

        # Get the category instance based on the selected category_id
        category = Addcategory.objects.get(id=category_id)

        # Create a SubCategory object and associate it with the category
        sub_category = SubCategory(category_name=category, sub_category=sub_category_name)
        sub_category.save()

        return redirect('subcategory')

    category = Addcategory.objects.all()
    return render(request, 'addsubcategory.html', {'category': category})

def subcategory(request):
    
    subcategory = SubCategory.objects.all()
    return render(request,'subcategory.html',{'subcategory':subcategory})


def editsubcategory(request,pk):
    subcategory=SubCategory.objects.get(id=pk)
    if request.method=='POST':
        category_id=request.POST.get('category_name')
        subcategory.category=Addcategory.objects.get(id=category_id)
        subcategory.sub_category=request.POST['sub_category']
        
        subcategory.save()
        
        return redirect('subcategory')
    
    categ=Addcategory.objects.all()
    return render(request,'editsubcategory.html',{'subcategory':subcategory,'categ':categ})

def deletesubcategory(request,pk):
    ct=SubCategory.objects.get(id=pk)
    ct.delete()
   
    return redirect('subcategory')


def addproduct(request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        title = request.POST['title']
        description = request.POST['description']
        price = Decimal(request.POST['price'])
        offer_price = Decimal(request.POST['offer_price'])
        stock_str = request.POST.get('stock', '')  # Get the 'stock' value as a string
        if stock_str.isdigit():  # Check if it's a valid integer
            stock = int(stock_str)
        else:
            # Handle the case where 'stock' is not a valid integer, e.g., show an error message or set a default value
            stock = 0
        is_available = request.POST.get('is_available') == 'on'

        size_ids = request.POST.getlist('size')
        selected_color_ids = request.POST.getlist('color')
        product_colors = Color.objects.filter(id__in=selected_color_ids)
        category = Addcategory.objects.get(id=category_id)
        subcategory = SubCategory.objects.get(id=subcategory_id)

        product = Product(
            category_name=category,
            sub_category=subcategory,
            title=title,
            description=description,
            price=price,
            offer_price=offer_price,
            stock=stock,
            is_available=is_available,
        )
        product.save()

        for size_id in size_ids:
            size = Size.objects.get(id=size_id)
            productsize = ProductSize(product=product, size=size)
            productsize.save()

        for color in product_colors:
            productcolor = ProductColor(product=product, color=color)
            productcolor.save()

        # Handle image upload
        for uploaded_file in request.FILES.getlist('images'):
            image = Image(product=product, image=uploaded_file)
            image.save()

        # Redirect to the product page or another appropriate URL
        return redirect('product')

    categories = Addcategory.objects.all()
    subcategories = SubCategory.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    return render(request, 'addproduct.html', {'categories': categories, 'subcategories': subcategories, 'sizes': sizes, 'colors': colors})

def product(request):
    produ = Product.objects.all()
    return render(request, 'product.html', {'produ': produ})

  
  
def editproduct(request, pk):
    ct = Product.objects.get(id=pk)

    if request.method == 'POST':
        ct.title = request.POST.get('title', ct.title)
        ct.description = request.POST.get('description', ct.description)
        ct.price = Decimal(request.POST.get('price', ct.price))
        ct.colour = request.POST.get('colour', ct.colour)
        size_ids = request.POST.getlist('size')  # Assuming the 'size' input is a multiple select
        selected_color_ids = request.POST.getlist('color')  # Assuming the 'color' input is a multiple select
        product_colors = Color.objects.filter(id__in=selected_color_ids)

        # Update product size and color associations
        ct.sizes.set(Size.objects.filter(id__in=size_ids))
        ct.colors.set(product_colors)

        # Handle stock and is_available fields
        stock_str = request.POST.get('stock', '0')
        if stock_str.isdigit():
            ct.stock = int(stock_str)
        else:
            ct.stock = 0
        ct.is_available = request.POST.get('is_available') == 'on'

        # Handle category and subcategory
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

        # Ensure category and subcategory exist before updating
        if category_id and subcategory_id:
            ct.category_id = category_id
            ct.subcategory_id = subcategory_id

        # Handle image update
        if 'image' in request.FILES:
            # Handle the uploaded image, assuming 'image' is the name of the file input
            image = request.FILES['image']
            product_image = Image(product=ct, image=image)
            product_image.save()

        ct.save()

        return redirect('product')

    cat = Addcategory.objects.all()
    subcategory = SubCategory.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    image=Image.objects.all()

    return render(request, 'editproduct.html', {'ct': ct, 'cat': cat, 'subcategory': subcategory, 'sizes': sizes, 'colors': colors})

def deleteproduct(request,pk):
    ct=Product.objects.get(id=pk)
    ct.delete()
   
    return redirect('product')





def addsize(request):
    if request.method=='POST':
        size=request.POST['name']
        ctg=Size(name=size)
        ctg.save()
        return redirect('size')
    return render(request,'addsize.html')




def size(request):
    c=Size.objects.all()
    return render(request,'size.html',{'ct':c})



def editsize(request,pk):
    
    ct=Size.objects.get(id=pk)
    
    if request.method=='POST':
        ct.name=request.POST['name']
   
        ct.save()
        
        return redirect('size')
    return render(request,'editsize.html',{'size':ct})


def deletesize(request,pk):
    ct=Size.objects.get(id=pk)
    ct.delete()
   
    return redirect('size')




def addcolor(request):
    if request.method=='POST':
        color=request.POST['name']
        ctg=Color(name=color)
        ctg.save()
        return redirect('color')
    return render(request,'addcolor.html')



def color(request):
    c=Color.objects.all()
    return render(request,'color.html',{'ct':c})




def editcolor(request,pk):
    
    ct=Color.objects.get(id=pk)
    
    if request.method=='POST':
        ct.name=request.POST['name']
   
        ct.save()
        
        return redirect('color')
    return render(request,'editcolor.html',{'color':ct})



def deletecolor(request,pk):
    ct=Color.objects.get(id=pk)
    ct.delete()
   
    return redirect('color')

