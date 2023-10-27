from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from user_side.models import Product,Category,User,Order,Payment,OrderProduct,Coupons,UserCoupons,ReviewRating,Wallet,ContactUs
from django.contrib import messages,auth
from user_side.forms import SignupForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.utils.text import slugify
from django.db import IntegrityError
from datetime import datetime,timedelta
from django.utils import timezone 
from decimal import Decimal,InvalidOperation  
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import JsonResponse
import json
from django.db.models import Sum,Count
from django.template.loader import get_template
from django.db.models.functions import TruncMonth
from django.db.models import F
from django.db.models import FloatField


def admin_index(request):
    if request.user.is_authenticated and request.user.is_admin and request.user.is_superadmin:
        total_revenue = OrderProduct.objects.filter(ordered=True).aggregate(total_revenue=Sum('product_price'))['total_revenue'] or 0.0
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        monthly_report = OrderProduct.objects.filter(ordered=True).annotate(month=TruncMonth('created_at')).values('month').annotate(total_revenue=Sum(F('product_price'),
        output_field=FloatField()),total_orders=Count('order')).order_by('-month')    
        current_date = datetime.now()

        six_months_ago = current_date - timedelta(days=180)
        monthly_report = monthly_report.filter(month__gte=six_months_ago)    
        last_orders = Order.objects.order_by('-created_at')[:5]

        first_day_current_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        first_day_last_month = first_day_current_month - timedelta(days=first_day_current_month.day)
        last_month_data = monthly_report.filter(month=first_day_last_month)


        context={
            'total_revenue':total_revenue,
            'total_orders':total_orders,
            'total_products':total_products,
            'monthly_report':monthly_report,
            'last_orders':last_orders,
            'last_month_data':last_month_data,
        }
        
        return render(request,'admin_temp/admin_index.html',context)
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

    paginator = Paginator(categories,6)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    categories_count = categories.count()

    context = {
        'categories' : categories,
        'categories':paged_categories,
        'categories_count':categories_count,
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
        offer_str = request.POST.get('offer')
        try:
            offer_decimal = Decimal(offer_str)
            if offer_decimal < 0 or offer_decimal > 100: 
                raise InvalidOperation
            if (offer_decimal * 100) % 1 != 0:
                raise InvalidOperation
        except (ValueError, InvalidOperation):
            messages.error(request, 'Invalid offer value. Please enter a valid percentage value ')
            return render(request, 'admin_temp/admin_add_category.html')


        
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
            offer=offer_decimal,
        )
        category.save()

        messages.success(request, 'Category added successfully.')
        return redirect('admin_category')
    else:
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
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        category_image = request.FILES.get('category_image')
        offer_str = request.POST.get('offer')
        try:
            offer_decimal = Decimal(offer_str)
            if offer_decimal < 0 or offer_decimal > 100: 
                raise InvalidOperation
            if (offer_decimal * 100) % 1 != 0:
                raise InvalidOperation
            category.offer = offer_decimal
        except (ValueError, InvalidOperation):
            messages.error(request, 'Invalid offer value. Please enter a valid percentage.')
            return render(request, 'admin_temp/admin_edit_category.html', {'category': category})

        base_slug = slugify(category.category_name)
        slug = base_slug
        count = 1

        while Category.objects.filter(slug=slug).exclude(id=category.id).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        Category.objects.filter(id=id).update(
            category_name=category_name,
            slug=slug,
            description=description,
            offer=offer_decimal,
        )
        if category_image:
            category.category_image = category_image

        category.slug = slug  
        category.save()

        messages.success(request, 'Category updated successfully.')
        return redirect('admin_category')

    return render(request, 'admin_temp/admin_edit_category.html', {'category': category})

@login_required(login_url='admin_login')
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

    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()
    
    context = {
        'products' : products,
        'products':paged_products,
        'products_count':products_count,
    }
    return render(request,'admin_temp/admin_products.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_add_product(request):
    if not request.user.is_authenticated and not request.user.is_admin:
        messages.success(request,"Please Login")
        return redirect('admin_login')
    categories = Category.objects.all()
    if request.method == 'POST':

        product_name = request.POST['product_name']
        category_id = request.POST['category']
        description = request.POST['description']
        price_str = request.POST['price']
        quantity_str = request.POST['quantity']
        
        if not price_str.isdigit():
            messages.error(request, 'Price should be a valid number.')
            return render(request, 'admin_temp/admin_add_product.html', {'categories': categories})
        
        if not quantity_str.isdigit():
            messages.error(request, 'Quantity should be a valid number.')
            return render(request, 'admin_temp/admin_add_product.html', {'categories': categories})

        

        price = Decimal(price_str)
        quantity = int(quantity_str)
        if price < 1 :
            messages.error(request, 'Price cannot be less than 0')
            return render(request, 'admin_temp/admin_add_product.html', {'categories': categories})

        product_images = request.FILES.get('product_images')
        product_image_1 = request.FILES.get('product_image_1')
        product_image_2 = request.FILES.get('product_image_2')
        product_image_3 = request.FILES.get('product_image_3')
        discount_percentage_str = request.POST.get('discount_percentage')
        try:
            discount_percentage = Decimal(discount_percentage_str)
            if discount_percentage < 0 or discount_percentage > 100: 
                raise InvalidOperation("Discount percentage is out of range.")
            if (discount_percentage * 100) % 1 != 0:
                raise InvalidOperation("Discount percentage must be a whole number.")
        except InvalidOperation as e:
            messages.error(request, f'Invalid discount percentage value: {e}. Please enter a valid percentage.')
            return render(request, 'admin_temp/admin_add_product.html', {'categories': categories})


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
                description=description,
                price=price,
                quantity=quantity,
                discount_percentage=discount_percentage,
                product_images=product_images,
                product_image_1=product_image_1,
                product_image_2=product_image_2,
                product_image_3=product_image_3,
            )

        try:
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_products')
        except IntegrityError as e:
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
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'product': product,
    }

    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_id = request.POST['category']
        description = request.POST['description']
        price_str = request.POST['price']
        quantity_str = request.POST['quantity']
        if not price_str.isdigit():
            messages.error(request, 'Price should be a valid number.')
            return render(request,'admin_temp/admin_edit_product.html',context)
        
        if not quantity_str.isdigit():
            messages.error(request, 'Quantity should be a valid number.')
            return render(request,'admin_temp/admin_edit_product.html',context)

        price = Decimal(price_str)
        quantity = int(quantity_str)
        if price < 1:
            messages.error(request, 'Price cannot be less than 0')
            return render(request,'admin_temp/admin_edit_product.html',context)

        product_images = request.FILES.get('product_images')
        product_image_1 = request.FILES.get('product_image_1')
        product_image_2 = request.FILES.get('product_image_2')
        product_image_3 = request.FILES.get('product_image_3')
        base_slug = slugify(product_name)
        discount_percentage_str = request.POST.get('discount_percentage')
        try:
            discount_percentage = Decimal(discount_percentage_str)
            if discount_percentage< 0 or discount_percentage > 100: 
                raise InvalidOperation
            if (discount_percentage* 100) % 1 != 0:
                raise InvalidOperation
            product.discount_percentage = discount_percentage
        except (ValueError, InvalidOperation):
            messages.error(request, 'Invalid discount percentage value. Please enter a valid percentage.')
            return render(request,'admin_temp/admin_edit_product.html',context)
        
        slug = base_slug
        count = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
            
        Product.objects.filter(id=product_id).update(
            product_name=product_name,
            slug=slug,
            category_id=category_id,
            description=description,
            price=price,
            quantity=quantity,
            discount_percentage=discount_percentage,
        )

        if product_images:
            product.product_images = product_images
        if product_image_1:
            product.product_image_1 = product_image_1
        if product_image_2:
            product.product_image_2 = product_image_2
        if product_image_3:
            product.product_image_3 = product_image_3
        
        product.discount_percentage = discount_percentage   
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

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'product': product,
    }
    return render(request,'admin_temp/admin_edit_product.html',context)


@login_required(login_url='admin_login')
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

    paginator = Paginator(users,6)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    users_count = users.count()
    
    context = {
        'users' : users,
        'users':paged_users,
        'users_count':users_count,
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


@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    paginator = Paginator(orders,10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    orders_count = orders.count()

    context={
        'orders':orders,
        'orders':paged_orders,
        'orders_count':orders_count,
    }
    return render(request,'admin_temp/admin_orders.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, pk=order_id)
    order_products = OrderProduct.objects.filter(order__id=order_id)
    
    if new_status == 'Cancelled':
        order.status = 'Cancelled'
        for order_product in order_products:
            product = order_product.product
            product.quantity += order_product.quantity
            product.save()
        if order.payment.payment_method == 'Razorpay':
            try:
                user_wallet = Wallet.objects.get(user=order.user)
                user_wallet.amount += float(order.order_total)
                user_wallet.save()
            except ObjectDoesNotExist:
                user_wallet = Wallet.objects.create(user=order.user, amount=float(order.order_total))
                user_wallet.save()
    elif new_status == 'Accepted':
        order.status = 'Shipped'
    elif new_status == 'Delivered':
        order.status = 'Delivered'
    elif new_status == 'Return':
        order.status = 'Returned'
            
    if new_status == 'Return':
        for order_product in order_products:
            product = order_product.product
            product.quantity += order_product.quantity
            product.save()
            try:
                user_wallet = Wallet.objects.get(user=order.user)
                user_wallet.amount += float(order.order_total)
                user_wallet.save()
            except ObjectDoesNotExist:
                user_wallet = Wallet.objects.create(user=order.user, amount=float(order.order_total))
                user_wallet.save()

            
    
    order.save()
    
    messages.success(request, f"Order #{order.order_number} has been updated to '{new_status}' status.")
    
    return redirect('admin_orders')
    
@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
def admin_coupons(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    coupons = Coupons.objects.all()

    paginator = Paginator(coupons,6)
    page = request.GET.get('page')
    paged_coupons = paginator.get_page(page)
    coupons_count = coupons.count()

    context={
        'coupons':coupons,
        'coupons':paged_coupons,
        'coupons_count':coupons_count,
    }
    return render(request, 'admin_temp/admin_coupons.html', context)
    
@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_delete_coupons(request, coupon_id):
    try:
        coupon = Coupons.objects.get(pk=coupon_id)
    except Coupons.DoesNotExist:
        return redirect('admin_coupons')

    
    coupon.delete()
    messages.success(request, "Coupon deleted successfully.")
    
    return redirect('admin_coupons')

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_review(request):
    reviews = ReviewRating.objects.all()
    paginator = Paginator(reviews,6)
    page = request.GET.get('page')
    paged_reviews = paginator.get_page(page)
    reviews_count = reviews.count()
    context={
        'reviews':reviews,
        'reviews':paged_reviews,
        'reviews_count':reviews_count,
    }

    return render(request, 'admin_temp/admin_review.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_review_replay(request, id):
    review = get_object_or_404(ReviewRating, id=id)

    if request.method == 'POST':
        review_reply = request.POST.get('review_reply')
        review.review_reply = review_reply
        review.save() 
        return redirect('admin_review')

    context = {
        'review': review, 
    }
    return render(request, 'admin_temp/admin_review_replay.html', context)


def get_weekly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(weekly_sales=Sum('quantity'))


def get_monthly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(monthly_sales=Sum('quantity'))


def get_yearly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=365)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(yearly_sales=Sum('quantity'))


def sales_report(request):
    weekly_sales_data = list(get_weekly_sales().values('product__product_name','weekly_sales'))  # Convert QuerySet to a list of dictionaries
    monthly_sales_data = list(get_monthly_sales().values('product__product_name','monthly_sales'))
    yearly_sales_data = list(get_yearly_sales().values('product__product_name','yearly_sales'))
    sales_data = {
        'weekly_sales': weekly_sales_data,
        'monthly_sales': monthly_sales_data,
        'yearly_sales': yearly_sales_data,
    }
    return JsonResponse(sales_data, safe=False)

@login_required(login_url='admin_login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_contact(request):
    contact_us = ContactUs.objects.all()
  
    context = {
        'contact_us': contact_us, 
    }
    return render(request, 'admin_temp/admin_contact.html', context)
    