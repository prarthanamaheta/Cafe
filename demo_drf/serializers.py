from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.password_validation import validate_password

from users.models import User
from demo_django.models import Food, Category, Type, Order
from demo_drf.models import Offer


class SignUpSerializer(serializers.ModelSerializer):
    """
    Register user serializer
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = User.objects.create(
            email=validated_data.get('email'),
        )
        if validated_data.get('first_name'):
            user.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            user.last_name = validated_data.get('first_name')
        user.set_password(validated_data.get('password'))
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    """
    Custom token pair serializer
    """

    def validate(self, attrs):
        request = self.context.get("request")

        user = User.objects.filter(email=attrs.get('email')).first()
        if user:
            data = super().validate(attrs)
            data.update({'user': self.user.email})
            data.update({'id': self.user.id})

            return data
        raise serializers.ValidationError(
            {"Credentials": "credentials didn't match. Please Login with correct credentials"})


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    change password serializer
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class FoodSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Food
        fields = ['name', 'items', 'price', 'category', 'categorys', 'type', 'types', 'image_url']


    def get_category(self, instance):
        if instance.categorys:
            return instance.categorys.name
        return None

    def get_type(self, instance):
        if instance.types:
            return instance.types.name
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['name', 'description', 'state', 'discount_percentage']


class OrderSerializer(serializers.ModelSerializer):
    offer = serializers.SerializerMethodField()
    foods_ordered = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['token', 'foods_ordered', 'status', 'total_payment', 'payment_received', 'offer', 'payment_mode']

    def get_offer(self, instance):
        if instance.offers:
            return instance.offers.values_list('name', flat=True)

    def get_foods_ordered(self, instance):
        if instance.foods_ordered:
            foods_ordered = []
            for foods in instance.foods_ordered:
                food = Food.objects.filter(id=foods).first()
                if food:
                    foods_ordered.append(food.name)
            return foods_ordered
