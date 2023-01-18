from django.urls import path

from demo_drf.views import LogInApiView, SignUpApiView, AddFoodView, MenuListView, PlaceOrderView, ChangeStatusView, \
    ReceivePaymentView, ChangePasswordView, AddCategoryView, AddTypeView, ListTypeView, ListCategoryView, \
    CategoryUpdateView, CategoryDeleteView, TypeUpdateView, TypeDeleteView, FoodUpdateView, FoodDeleteView, \
    ListFoodView, AddOfferView, ListOfferView, OfferUpdateView, OfferDeleteView, ListOrderView

urlpatterns = [
    path('login/', LogInApiView.as_view(), name='login'),
    path('signup/', SignUpApiView.as_view(), name='signup'),

    path('add-food/', AddFoodView.as_view(), name='add_food'),
    path('list-food/', ListFoodView.as_view(), name='food_list'),
    path('update/food/<int:id>/', FoodUpdateView.as_view(), name='type_food'),
    path('delete/food/<int:id>/', FoodDeleteView.as_view(), name='type_food'),

    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('list-category/', ListCategoryView.as_view(), name='type_category'),
    path('update/category/<int:id>/', CategoryUpdateView.as_view(), name='update_category'),
    path('delete/category/<int:id>/', CategoryDeleteView.as_view(), name='delete_category'),

    path('add-type/', AddTypeView.as_view(), name='add_type'),
    path('list-type/', ListTypeView.as_view(), name='type_list'),
    path('update/type/<int:id>/', TypeUpdateView.as_view(), name='update_type'),
    path('delete/type/<int:id>/', TypeDeleteView.as_view(), name='delete_type'),

    path('add-offer/', AddOfferView.as_view(), name='add_offer'),
    path('list-offer/', ListOfferView.as_view(), name='offer_list'),
    path('update/offer/<int:id>/', OfferUpdateView.as_view(), name='update_food'),
    path('delete/offer/<int:id>/', OfferDeleteView.as_view(), name='delete_food'),

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('menu-list/', MenuListView.as_view(), name='menu_list'),
    path('place-order/', PlaceOrderView.as_view(), name='place_order'),
    path('list-order/', ListOrderView.as_view(), name='list_order'),
    path('change-status/', ChangeStatusView.as_view(), name='change_status'),
    path('received-payment/', ReceivePaymentView.as_view(), name='received_payment')
]
