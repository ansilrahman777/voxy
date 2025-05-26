from django.urls import path
from user_side import views

urlpatterns = [
    path('',views.user_index,name='user_index'),
    path('user_about',views.user_about,name='user_about'),
    path('user_contact',views.user_contact,name='user_contact'),

    path('user_login',views.user_login,name='user_login'),
    path('user_sign_up',views.user_sign_up,name='user_sign_up'),
    path('user_forgot_password',views.user_forgot_password,name='user_forgot_password'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('user_reset_password_validate/<uidb64>/<token>/',views.user_reset_password_validate,name='user_reset_password_validate'),
    path('user_reset_password',views.user_reset_password,name='user_reset_password'),

    path('user_shop',views.user_shop,name='user_shop'),
    path('user_shop/category/<str:category_slug>/',views.user_shop,name='products_by_category'),
    path('user_shop/category/<str:category_slug>/<str:product_slug>/', views.user_product_detail, name='user_product_detail'),
    path('user_shop/search/',views.search,name='search'),

    path('user_product_detail/<int:product_id>/',views.user_product_detail,name='user_product_detail'),
    path('user_coming_soon/<int:id>/',views.user_coming_soon,name='user_coming_soon'),


    path('user_cart',views.user_cart,name='user_cart'),
    path('user_add_cart/<int:product_id>/',views.user_add_cart,name='user_add_cart'),
    path('user_remove_cart/<int:product_id>/<int:cart_item_id>/', views.user_remove_cart, name='user_remove_cart'),
    path('user_remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.user_remove_cart_item, name='user_remove_cart_item'),

    path('user_profile',views.user_profile,name='user_profile'),
    path('user_profile_edit',views.user_profile_edit,name='user_profile_edit'),
    path('user_change_password',views.user_change_password,name='user_change_password'),
    
    path('user_address',views.user_address,name='user_address'),
    path('user_add_address',views.user_add_address,name='user_add_address'),
    path('user_edit_address/<int:id>',views.user_edit_address,name='user_edit_address'),
    path('user_remove_address/<int:id>',views.user_remove_address,name='user_remove_address'),
    path('user_wallet',views.user_wallet,name='user_wallet'),

    path('user_shipping',views.user_shipping,name='user_shipping'),
    path('user_checkout',views.user_checkout,name='user_checkout'),
    path('user_place_order',views.user_place_order,name='user_place_order'),
    path('user_payment/<str:order_number>/', views.user_payment, name='user_payment'),
    path('user_cash_on_delivery/<str:order_number>/', views.user_cash_on_delivery, name='user_cash_on_delivery'),

    path('user_order',views.user_order,name='user_order'),
    path('user_update_order_status/<int:order_id>/<str:new_status>/', views.user_update_order_status, name='user_update_order_status'),
    path('user_order_detailed_view/<int:order_id>/',views.user_order_detailed_view,name='user_order_detailed_view'),
    path('user_sumbit_review/<int:product_id>/',views.user_sumbit_review,name='user_sumbit_review'),
    path('user_order_invoice/<int:order_id>/',views.user_order_invoice,name='user_order_invoice'),


    path('user_wishlist', views.user_wishlist, name='user_wishlist'),
    path('user_add_wishlist/<int:product_id>/', views.user_add_wishlist, name='user_add_wishlist'),
    path('user_remove_wishlist/<int:product_id>/', views.user_remove_wishlist, name='user_remove_wishlist'),
    path('user_apply_coupon', views.user_apply_coupon, name='user_apply_coupon'),


    path('contact/', views.contact_us, name='contact_us'),
 
]