from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from user_side.models import Product,Category,User,Order,Payment,OrderProduct,Coupons,UserCoupons,ReviewRating,ReviewReply
from django.contrib import messages,auth
from user_side.forms import SignupForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.utils.text import slugify
from django.db import IntegrityError
from datetime import datetime
from django.utils import timezone

# Create your views here.

def admin_index(request):
    if request.user.is_authenticated and request.user.is_admin and request.user.is_superadmin:
        return render(request,'admin_temp/admin_index.html')
    return render(request,'admin_temp/admin_login.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None and user.is_superadmin: 
            auth.login(request, user)
            messages.success(request, "Login successful")
            return redirect('/admin_index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('admin_login')

    return render(request, 'admin_temp/admin_login.html')


@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_logout(request):
    auth.logout(request)
    messages.success(request,'Logout successfull')
    return redirect('admin_login')
                

#-------------------------------------category---------------------------------
@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_category(request):
    if not request.user.is_authenticated:
        messages.success(request,"Please Login")
        return redirect('admin_login')

    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request,'admin_temp/admin_category.html',context)
    
@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_add_category(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add a category.")
        return redirect('admin_login')

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        category_image = request.FILES.get('category_image')
        base_slug = slugify(category_name)
        slug = base_slug
        count = 1

        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        
        existing_category = Category.objects.filter(category_name=category_name).first()
        
        if existing_category:
            messages.error(request, f"A category with the name '{category_name}' already exists.")
            return redirect('admin_add_category')

        category = Category(
            category_name=category_name,
            slug=slug,
            description=description,
            category_image=category_image,
        )
        category.save()

        messages.success(request, 'Category added successfully.')
        return redirect('admin_category')
    else:
        return render(request, 'admin_temp/admin_add_category.html')

    return render(request, 'admin_temp/admin_add_category.html')

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_edit_category(request, id):
    if not request.user.is_authenticated:
        messages.success(request, "Please Login")
        return redirect('admin_login')

    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    if request.method == 'POST':
        category.category_name = request.POST.get('category_name')
        category.description = request.POST.get('description')
        category.stock = request.POST.get('stock')
        category.category_image = request.FILES.get('category_image')
        base_slug = slugify(category.category_name)
        slug = base_slug
        count = 1

        while Category.objects.filter(slug=slug).exclude(id=category.id).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        
        category.slug = slug  
        category.save()

        messages.success(request, 'Category updated successfully.')
        return redirect('admin_category')

    return render(request, 'admin_temp/admin_edit_category.html', {'category': category})

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_enable_disable_category(request,id):
    if not request.user.is_authenticated:
        messages.success(request,"Please Login")
        return redirect('admin_login')
    
    category = Category.objects.get(id=id)
    try:
        if category.soft_deleted:
            category.soft_deleted = False
            category.save()
            Product.objects.filter(category=category).update(soft_deleted=False)
            messages.success(request,'Category Enabled')
            return redirect('admin_category')
        else:
            category.soft_deleted = True
            category.save()
            Product.objects.filter(category=category).update(soft_deleted=True)
            messages.success(request,'Category Disabled')
            return redirect('admin_category')
    except :
            messages.warning(request,'Oops ! Error occurred')
    
    return redirect('admin_category')

#-------------------------------------product---------------------------------
@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_products(request):
    if not request.user.is_authenticated:
        messages.success(request,"Please Login")
        return redirect('admin_login')

    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request,'admin_temp/admin_products.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_add_product(request):
    if not request.user.is_authenticated and not request.user.is_admin:
        messages.success(request,"Please Login")
        return redirect('admin_login')

    if request.method == 'POST':

        product_name = request.POST['product_name']
        category_id = request.POST['category']
        # brand = request.POST['brand']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        product_images = request.FILES.get('product_images')
        product_image_1 = request.FILES.get('product_image_1')
        product_image_2 = request.FILES.get('product_image_2')
        product_image_3 = request.FILES.get('product_image_3')
        base_slug = slugify(product_name)
        slug = base_slug
        count = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        print('product_name',product_name)

        product = Product(
                product_name=product_name,
                slug=slug,
                category_id=category_id,
                # brand=brand,
                description=description,
                price=price,
                quantity=quantity,
                product_images=product_images,
                product_image_1=product_image_1,
                product_image_2=product_image_2,
                product_image_3=product_image_3,
            )

        try:
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_products')
        except IntegrityError as e:  # Handle IntegrityError
            messages.warning(request, 'Oops! Error occurred while adding the product.')
            return redirect('admin_add_product')
    
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    
    return render(request,'admin_temp/admin_add_product.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_edit_product(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add a category.")
        return redirect('admin_login')
    
    try:
        product = get_object_or_404(Product, id=product_id)
    except Http404:
        raise Http404("Product does not exist")

    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_id = request.POST['category']
        # brand = request.POST['brand']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        product_images = request.FILES.get('product_images')
        product_image_1 = request.FILES.get('product_image_1')
        product_image_2 = request.FILES.get('product_image_2')
        product_image_3 = request.FILES.get('product_image_3')
        base_slug = slugify(product_name)
        slug = base_slug
        count = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
            
        Product.objects.filter(id=product_id).update(
            product_name=product_name,
            slug=slug,
            category_id=category_id,
            # brand=brand,
            description=description,
            price=price,
            quantity=quantity,
        )

        if product_images:
            product.product_images = product_images
        if product_image_1:
            product.product_image_1 = product_image_1
        if product_image_2:
            product.product_image_2 = product_image_2
        if product_image_3:
            product.product_image_3 = product_image_3
   
        product.product_name = product_name
        product.slug = slug
        product.category_id = category_id
        product.description = description
        product.price = price
        product.quantity = quantity
        product.save()

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('admin_products')
        # except IntegrityError:
        #     messages.warning(request, 'Oops! Error occurred while updating the product.')
        #     return redirect('admin_edit_product', product_id=product.id)

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'product': product,
    }
    return render(request,'admin_temp/admin_edit_product.html',context)


@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_unlist_list_product(request,product_id):
    if not request.user.is_authenticated :
        messages.success(request,"Please Login")
        return redirect('admin_login')
    product = Product.objects.get(id=product_id)
    try:
        if product.soft_deleted:
            product.soft_deleted = False
            product.save()
            messages.success(request,'Product Listed')
            return redirect('admin_products')
        else:
            product.soft_deleted = True
            product.save()
            messages.success(request,'Product Unlisted')
            return redirect('admin_products')
    except:
        messages.warning(request,'Error Occurred while updating')
    if product.category.soft_deleted:
        messages.warning(request, 'Category is blocked. Cannot enable the product.')

    return redirect('admin_products')

#-------------------------------------user---------------------------------

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_users(request):
    if not request.user.is_authenticated:
        messages.success(request,"Please Login")
        return redirect('admin_login')

    users = User.objects.all().exclude(is_admin=True)
    context = {
        'users' : users
    }
    return render(request,'admin_temp/admin_users.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_user_block_unblock(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    user = User.objects.get(id=id)  
    try:
        if user.is_blocked:
            user.is_blocked=False
            user.save()
            messages.success(request,'User is Unblocked')
        else:
            user.is_blocked = True
            user.save()
            messages.success(request,'User is Blocked')
    except User.DoesNotExist:
        messages.warning(request, 'User does not exist')

    return redirect('admin_users')

def admin_banners(request):
    return render(request,'admin_temp/admin_banners.html')

@login_required
def admin_orders(request):
    orders = Order.objects.all()

    context={
        'orders':orders
    }
    return render(request,'admin_temp/admin_orders.html',context)

@login_required
def admin_order_details(request, order_id):
    
    order_products = OrderProduct.objects.filter(order__id=order_id)
    orders = Order.objects.filter(is_ordered=True, id=order_id)
    
    payments = Payment.objects.filter(order__id=order_id)

    for order_product in order_products:
        order_product.total = order_product.quantity * order_product.product_price
        order_product.single_product_total = order_product.quantity * order_product.product.price
    context = {
        'order_products': order_products,
        'orders': orders,
        'payments': payments,
    }

    return render(request, 'admin_temp/admin_order_details.html', context)

@login_required
def admin_update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, pk=order_id)
    
    if new_status == 'Cancelled':
        order.status = 'Cancelled'
    elif new_status == 'Accepted':
        order.status = 'Accepted'
    elif new_status == 'Delivered':
        order.status = 'Delivered'
    elif new_status == 'Return':
        order.status = 'Returned'
    
    order.save()
    
    messages.success(request, f"Order #{order.order_number} has been updated to '{new_status}' status.")
    
    return redirect('admin_orders')
    
@login_required    
def admin_coupons(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    coupons = Coupons.objects.all()
    context = {'coupons': coupons}
    return render(request, 'admin_temp/admin_coupons.html', context)
    
@login_required
def admin_add_coupons(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        description = request.POST.get('description')
        minimum_amount = request.POST.get('minimum_amount')
        discount = request.POST.get('discount')
        valid_from_str = request.POST.get('valid_from')
        valid_to_str = request.POST.get('valid_to')

        try:
            minimum_amount = int(minimum_amount)
            discount = int(discount)
        except ValueError:
            messages.error(request, "Minimum Amount and Discount must be integers.")
            return redirect('admin_add_coupons')

        try:
            valid_from = datetime.strptime(valid_from_str, '%Y-%m-%dT%H:%M')
            valid_to = datetime.strptime(valid_to_str, '%Y-%m-%dT%H:%M')

            valid_from = timezone.make_aware(valid_from, timezone=timezone.utc)
            valid_to = timezone.make_aware(valid_to, timezone=timezone.utc)
        except ValueError:
            messages.error(request, "Date and Time must be in a proper format.")
            return redirect('admin_add_coupons')

        coupon = Coupons(
            coupon_code=coupon_code,
            description=description,
            minimum_amount=minimum_amount,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to
        )
        coupon.save()
        messages.success(request, "Coupon added successfully.")
        return redirect('admin_coupons')

    return render(request,'admin_temp/admin_add_coupons.html')

@login_required
def admin_edit_coupons(request, coupon_id):
    try:
        coupon = Coupons.objects.get(pk=coupon_id)
    except Coupons.DoesNotExist:
        return redirect('admin_coupons')

    if request.method == 'POST':
        coupon.coupon_code = request.POST.get('coupon_code')
        coupon.description = request.POST.get('description')
        coupon.minimum_amount = int(request.POST.get('minimum_amount'))
        coupon.discount = int(request.POST.get('discount'))
        valid_from_str = request.POST.get('valid_from')
        valid_to_str = request.POST.get('valid_to')

        try:
            minimum_amount = int(request.POST.get('minimum_amount'))
            discount = int(request.POST.get('discount'))
        except ValueError:
            messages.error(request, "Minimum Amount and Discount must be integers.")
            return redirect('admin_edit_coupons', coupon_id=coupon_id)

        try:
            valid_from = datetime.strptime(valid_from_str, '%Y-%m-%dT%H:%M')
            valid_to = datetime.strptime(valid_to_str, '%Y-%m-%dT%H:%M')

            valid_from = timezone.make_aware(valid_from, timezone=timezone.utc)
            valid_to = timezone.make_aware(valid_to, timezone=timezone.utc)
        except ValueError:
            messages.error(request, "Date and Time must be in a proper format.")
            return redirect('admin_edit_coupons', coupon_id=coupon_id)

        coupon.valid_from = valid_from
        coupon.valid_to = valid_to
        
        coupon.save()
        
        return redirect('admin_coupons')

    context = {'coupon': coupon}
    return render(request, 'admin_temp/admin_edit_coupons.html', context)

@login_required
def admin_delete_coupons(request, coupon_id):
    try:
        coupon = Coupons.objects.get(pk=coupon_id)
    except Coupons.DoesNotExist:
        return redirect('admin_coupons')

    
    coupon.delete()
    messages.success(request, "Coupon deleted successfully.")
    
    return redirect('admin_coupons')

@login_required
def admin_review(request):
    reviews = ReviewRating.objects.all()
    context = {'reviews': reviews}

    return render(request, 'admin_temp/admin_review.html',context)

@login_required
def admin_review_replay(request,review_id):
    if request.method == "POST":
        pass
        


