from demo_drf.utils import total_discount
from users.models import User
from demo_django.models import Food, Order, Category, Type, Visitor
from demo_drf.models import Offer
from demo_drf.response_example import api_response
from demo_drf.serializers import LoginTokenObtainSerializer, SignUpSerializer, ChangePasswordSerializer, \
    OrderSerializer, \
    FoodSerializer, OfferSerializer, TypeSerializer, CategorySerializer

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters

from demo_drf.swagger_response import api_signup, api_login, api_change_password
from demo_drf.tasks import *


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        responses=api_signup,
        tags=["Authentication"],
        operation_summary="SignUp API"),
)
class SignUpApiView(CreateAPIView):
    """
    Register user
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        responses=api_login,
        tags=["Authentication"],
        operation_summary="Login API"),
)
class LogInApiView(TokenObtainPairView):
    """
    Custom token obtain pair view
    """
    serializer_class = LoginTokenObtainSerializer


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        responses=api_change_password,
        tags=["Authentication"],
        operation_summary="Change Password API"),
)
class ChangePasswordView(generics.UpdateAPIView):
    """
    Change Password view
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    http_method_names = ('patch',)

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Menu"],
        operation_summary="Menu List API"),
)
class MenuListView(ListAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'types__name']
    filterset_fields = ['name', 'categorys__name', 'types__name']


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Category"],
        operation_summary="Adding category API"),
)
class AddCategoryView(CreateAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CategorySerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Category"],
        operation_summary="list all category API"),
)
class ListCategoryView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CategorySerializer


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["Category"],
        operation_summary="update category API"),
)
class CategoryUpdateView(generics.UpdateAPIView):
    """
     updating category
     """

    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Category"],
        operation_summary="delete category API"),
)
class CategoryDeleteView(generics.DestroyAPIView):
    """
        deleting post if Mediuser is authenticated
    """

    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Type"],
        operation_summary="Adding all Type API"),
)
class AddTypeView(CreateAPIView):
    queryset = Type.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = TypeSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Type"],
        operation_summary="list of  Type API"),
)
class ListTypeView(ListAPIView):
    queryset = Type.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = TypeSerializer


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["Type"],
        operation_summary="update type API"),
)
class TypeUpdateView(generics.UpdateAPIView):
    """
     updating category
     """

    permission_classes = [IsAdminUser]
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Type"],
        operation_summary="delete type API"),
)
class TypeDeleteView(generics.DestroyAPIView):
    """
        deleting type
    """

    permission_classes = [IsAdminUser]
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = 'id'


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Food"],
        operation_summary="Adding Food API"),
)
class AddFoodView(CreateAPIView):
    queryset = Food.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = FoodSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Food"],
        operation_summary="list of  Food API"),
)
class ListFoodView(ListAPIView):
    queryset = Food.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = FoodSerializer


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["Food"],
        operation_summary="update Food API"),
)
class FoodUpdateView(generics.UpdateAPIView):
    """
     updating category
     """

    permission_classes = [IsAdminUser]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Food"],
        operation_summary="delete food API"),
)
class FoodDeleteView(generics.DestroyAPIView):
    """
        deleting type
    """

    permission_classes = [IsAdminUser]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'id'


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            required=['token', 'foods', 'status'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_INTEGER),
                "foods": openapi.Parameter(
                    'foods',
                    type=openapi.TYPE_ARRAY,
                    in_=openapi.IN_QUERY,
                    description=api_response["foods_description"],
                    items={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="id of the food ",
                        ),
                    }
                ),
                'status': openapi.Schema(type=openapi.TYPE_STRING),
                'offer': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        tags=["Order"],
        operation_summary="Place a order API",
        operation_description='Place a order API',
    ),
)
class PlaceOrderView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        token = self.request.data.get('token')
        foods = self.request.data.get('foods')
        status = self.request.data.get('status')
        offers = self.request.data.get('offer')
        order, created = Order.objects.get_or_create(token=token, status=status, foods_ordered=foods)
        order.offers.add(offers)
        if created:
            return Response({"data": f'Order {status} with {token} number will be served soon'})
        return Response({"data": f'Order  with {token} number already exists'})


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Order"],
        operation_summary="list of order API"),
)
class ListOrderView(ListAPIView):
    queryset = Order.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = OrderSerializer


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            required=['token', 'foods', 'status'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_INTEGER),
                'status': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=["Order"],
        operation_summary="Change order status API",
        operation_description='Change order status API',
    ),
)
class ChangeStatusView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        token = self.request.data.get('token')
        status = self.request.data.get('status')
        order = Order.objects.filter(token=token).first()

        if order:

            if order.status == 'received' and status == 'completed':
                order.status = status
                total = []
                for foods in order.foods_ordered:
                    foods_price = Food.objects.filter(id=foods).first()

                    if foods_price:
                        total.append(foods_price.price)

                if order.offers.all():
                    discount = order.offers.all()[0]
                    total_payment = total_discount(discount.discount_percentage, total)
                    order.total_payment = total_payment
                    order.save()
                    return Response({"data": f'Order Total :{total_payment} rs'})
                else:
                    total_payment = sum(total)
                    order.total_payment = total_payment
                    order.save()
                    return Response({"data": f'Order Total :{total_payment} rs'})

            if order.status == 'received' and status == 'progress':
                return Response({"data": f'Order In progress please updated the status when it get completed'})

            if order.status == 'completed' and order.total_payment == 0:
                if order.payment_received is None:
                    return Response(
                        {"data": f'Order  with {token} number process is completed Please make payment!!!!'})
                return Response({"data": f'Order  with {token} number process already completed'})

            elif order.status == 'completed' and order.total_payment > 0:
                return Response({"data": f'Order  with {token} number payment already completed and received payment'})

        return Response({"data": f'Order with {token} number does not exists'})


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            required=['token'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                "mobile": openapi.Schema(type=openapi.TYPE_INTEGER),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'payment_mode': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        tags=["Order"],
        operation_summary="Change order status API",
        operation_description='Change order status API',
    ),
)
class ReceivePaymentView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        token = self.request.data.get('token')
        name = self.request.data.get('name')
        mobile = self.request.data.get('mobile')
        email = self.request.data.get('email')
        payment_mode = self.request.data.get('payment_mode')
        order = Order.objects.filter(token=token).first()

        if order:
            if order.total_payment > 0 and order.status == 'completed':
                order.payment_received = True
                order.payment_mode = payment_mode
                order.save()
                visitor, created = Visitor.objects.get_or_create(name=name, mobile=mobile, email=email)
                visitor.orders = order
                visitor.save()
                send_mail_task.delay(tenant_name=self.request.tenant.name, visitor=visitor.id)
                # send_mail_task(tenant_name=self.request.tenant.name, visitor=visitor.id)
                return Response({
                    "data": f'Order  with {token} number Payment received, Thank you {visitor.name} Visit again!!!!!!!'})
            return Response({"data": f'Order  with {token} status should be updated'})
        return Response({"data": f'Order  with {token} does not exists'})


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Offer"],
        operation_summary="Adding offer API"),
)
class AddOfferView(CreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = OfferSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Offer"],
        operation_summary="List of  Food API"),
)
class ListOfferView(ListAPIView):
    queryset = Offer.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = OfferSerializer


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["Offer"],
        operation_summary="update offer API"),
)
class OfferUpdateView(generics.UpdateAPIView):
    """
     updating category
     """

    permission_classes = [IsAdminUser]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Offer"],
        operation_summary="delete offer API"),
)
class OfferDeleteView(generics.DestroyAPIView):
    """
        deleting type
    """

    permission_classes = [IsAdminUser]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'id'
