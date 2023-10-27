from django.urls import path
from admin_side import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),

    path('admin_index',views.admin_index,name='admin_index'),
    path('admin_category',views.admin_category,name='admin_category'),
    path('admin_products',views.admin_products,name='admin_products'),
    
    path('admin_users',views.admin_users,name='admin_users'),
    path('admin_user_block_unblock/<int:id>',views.admin_user_block_unblock,name='admin_user_block_unblock'),

    path('admin_enable_disable_category/<int:id>',views.admin_enable_disable_category,name='admin_enable_disable_category'),
    path('admin_unlist_list_product/<int:product_id>',views.admin_unlist_list_product,name='admin_unlist_list_product'),

    path('admin_add_category',views.admin_add_category,name='admin_add_category'),
    path('admin_add_product',views.admin_add_product,name='admin_add_product'),

    path('admin_edit_category/<int:id>/',views.admin_edit_category,name='admin_edit_category'),
    path('admin_edit_product/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),

    path('admin_orders',views.admin_orders,name='admin_orders'),
    path('admin_update_order_status/<int:order_id>/<str:new_status>/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin_order_details/<int:order_id>/',views.admin_order_details,name='admin_order_details'),
    path('admin_review',views.admin_review,name='admin_review'),
    path('admin_review_replay/<int:id>/',views.admin_review_replay,name='admin_review_replay'),


    path('admin_coupons',views.admin_coupons,name='admin_coupons'),
    path('admin_add_coupons',views.admin_add_coupons,name='admin_add_coupons'),
    path('admin_edit_coupons/<int:coupon_id>/',views.admin_edit_coupons,name='admin_edit_coupons'),
    path('admin_delete_coupons/<int:coupon_id>/',views.admin_delete_coupons,name='admin_delete_coupons'),

    path('sales-report',views.sales_report,name='sales-report'),

    path('admin_contact',views.admin_contact,name='admin_contact'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)