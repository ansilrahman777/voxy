from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.urls import reverse
from django import forms
from django.db.models.signals import post_delete
from django.utils import timezone 
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
import logging
from django.core.files.storage import default_storage
from django.core.files import File


# Create your models here.
class User_manager(BaseUserManager):
    def create_user(self, email, username,first_name,last_name,mobile, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username,first_name,last_name, mobile, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            first_name=first_name,
            last_name=last_name,
            mobile = mobile
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

    


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=50, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','mobile','first_name','last_name']

    objects = User_manager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

class TempUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=50, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','mobile','first_name','last_name']

    objects = User_manager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=100,blank= True)
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    category_image = models.ImageField(upload_to='photos/categories',blank=True)
    offer = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,default=0)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
        else:
            # Check if the category_image field has changed
            if self.category_image and self.category_image != self._original_category_image:
                # If it has changed, delete the old image file
                if self._original_category_image:
                    default_storage.delete(self._original_category_image.path)
                
                # Save the new image and update the offer field
                super().save(update_fields=['category_image', 'offer'])
            else:
                super().save(update_fields=['offer'])

        # Rest of your code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_category_image = self.category_image


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    product_images = models.ImageField(upload_to='photos/products')
    product_image_1 = models.ImageField(upload_to='photos/products', blank=True)
    product_image_2 = models.ImageField(upload_to='photos/products', blank=True)
    product_image_3 = models.ImageField(upload_to='photos/products', blank=True)
    discount_percentage = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,default=0)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,)

    def save(self, *args, **kwargs):
        self.discount_price = self.price

        if type(self.discount_percentage) is Decimal:
            discount_factor = 1 - (self.discount_percentage / Decimal('100.00'))
            self.discount_price = Decimal(self.price) * discount_factor

        if self.category and self.category.offer is not None:
            category_discount_factor = 1 - (Decimal(self.category.offer) / Decimal('100.00'))
            self.discount_price = self.discount_price * category_discount_factor

        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('user_product_detail', args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name


class VariationManger(models.Manager):
    def colors(self):
        return super(VariationManger,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManger,self).filter(variation_category='size',is_active=True)

Variation_category_choice=(
    ('color','color'),
    ('size','size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category =models.CharField(max_length=100, choices = Variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManger()

    def __str__(self):
        return self.variation_value
    
    

class Cart(models.Model):
    cart_id = models.CharField(max_length=50,blank=True)
    date_added = models.DateField(auto_now_add= True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete =models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity =models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.discount_price*self.quantity

    def __unicode__(self):
        return self.product         

class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,blank=False, default='')
    last_name = models.CharField(max_length=50,blank=False, default='')
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=500,blank=False)
    address_line_2 = models.CharField(max_length=500,blank=False, default='')
    city = models.CharField(max_length=50,blank=False, default='')
    STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Delhi', 'Delhi'),
    ('Puducherry', 'Puducherry'),
    )
    state = models.CharField(max_length=100, choices=STATE_CHOICES, blank=False, default='')
    country = models.CharField(max_length=20)
    pin = models.IntegerField()
    is_default=models.BooleanField(default=False)
    

    def _str_(self):
        return str(self.pk)

    def delete(self, *args, **kwargs):
        super(Address, self).delete(*args, **kwargs)

        remaining_addresses = Address.objects.filter(user_id=self.user_id).exclude(pk=self.pk)
        remaining_addresses_count = remaining_addresses.count()

        if self.is_default and remaining_addresses_count == 0:
            return

        if remaining_addresses_count > 0:
            last_address = remaining_addresses.order_by('-pk').first()
            last_address.is_default = True
            last_address.save()

    def save(self, *args, **kwargs):
        super(Address, self).save(*args, **kwargs)

        other_default_addresses = Address.objects.filter(user_id=self.user_id).exclude(pk=self.pk, is_default=True)

        if self.is_default:
            other_default_addresses.update(is_default=False)


    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS =(
        ('Order Placed','Order Placed'),
        ('Accepted','Accepted'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return Pending','Return Pending'),
        ('Returned','Returned'),
        ('Payment Failed','Payment Failed'),
        ('Order Failed','Order Failed'),
    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=50)
    order_total = models.CharField(max_length=50)
    tax = models.FloatField()
    order_note = models.TextField(default='', blank=True)
    status = models.CharField(max_length=20,choices=STATUS,default='Order Placed')
    ip = models.CharField(blank=True,max_length=50)
    is_ordered = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    return_reason = models.TextField(max_length=100,blank=True)

    def __str__(self):
        return self.user.first_name
   
    def save(self, *args, **kwargs):
        if not self.is_ordered:
            self.status = 'Order Failed'
        super().save(*args, **kwargs)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)

class Coupons(models.Model):
    coupon_code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    minimum_amount = models.IntegerField(default=10000)
    discount = models.IntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.coupon_code

    def is_valid(self):
        now = timezone.now()
        if self.valid_to < now:
            self.is_expired = True
        return not self.is_expired


    def is_used_by_user(self, user):
        redeemed_details = UserCoupons.objects.filter(coupon=self, user=user, is_used=True)
        return redeemed_details.exists()

class UserCoupons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon.coupon_code

class ReviewRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    subject = models.CharField(max_length=50,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField(blank=True, null=True)
    review_reply = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Wallet for User : {self.user.first_name}"

