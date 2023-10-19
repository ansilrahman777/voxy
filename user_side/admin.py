from django.contrib import admin
from .models import  Category ,User ,Product , Cart,CartItem,Variation,TempUser,Address,Order,OrderProduct,Payment,Wishlist,Coupons,UserCoupons,ReviewRating,Wallet
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links =('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('date_joined',)
    
    
    filter_horizontal =()
    list_filter=()
    fieldsets = ()
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display = ('category_name','slug')

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display = ('product_name','price','category','quantity','is_available','discount_price')

class VariationAdmin(admin.ModelAdmin):
    list_display =('product','variation_category','variation_value','is_active')

class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')

class AddressAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','address_line_1','city','state','is_default')

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields =('user','order','payment','product','product_price','ordered','quantity',)
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=('user','order_number','payment','address','order_total','is_ordered','status')
    inlines =[OrderProductInline]

class CouponsAdmin(admin.ModelAdmin):
    list_display=('coupon_code','description','minimum_amount','discount','is_expired','valid_from','valid_to')

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user','review',  'created_at','status')
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','amount','updated_at',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(User,AccountAdmin)
admin.site.register(TempUser)
admin.site.register(Address,AddressAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(Wishlist)
admin.site.register(Coupons,CouponsAdmin)
admin.site.register(UserCoupons)
admin.site.register(ReviewRating,ReviewRatingAdmin)
admin.site.register(Wallet,WalletAdmin)