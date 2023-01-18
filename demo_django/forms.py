from django import forms

from demo_django.models import Food
from django.contrib.auth.forms import UserCreationForm

from users.models import User
from django.contrib.auth.password_validation import validate_password


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    username=forms.CharField(max_length=100)
    password = forms.CharField( required=True, validators=[validate_password])
    password2 = forms.CharField(required=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['email','username', 'password', 'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['password'].label = False
        self.fields['password2'].label = False
        self.fields['username'].label = False
        self.fields['first_name'].label = False
        self.fields['last_name'].label = False


    def save(self, commit=True):
        user = super().save(commit=False)
        print("-----", user)
        breakpoint()
        user.set_password(self.data.get('password'))
        user.save()
        self.save_m2m()
        return user

class FoodForm(forms.ModelForm):
    """
    Clip form
    """

    # name = forms.CharField(max_length=255, widget=forms.TextInput(
    #     attrs={"placeholder": "Enter Title For Clip"}
    # ), label='Food name:',required=True)

    class Meta:
        model = Food
        fields = ['name', 'categorys', 'types', 'price', 'items', 'image', 'image_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = False
        self.fields['categorys'].label = False
        self.fields['types'].label = False
        self.fields['price'].label = False
        self.fields['items'].label = False
        self.fields['image'].label = False
        self.fields['image_url'].label = False

    def save(self, commit=True):
        food_instance = super().save(commit=False)
        print("-----", food_instance)
        food_instance.save()
        self.save_m2m()
        return food_instance
