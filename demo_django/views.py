from django.urls.base import reverse_lazy, reverse
from django.views.generic import ListView

from demo_django.filters import MenuFilter
from demo_django.forms import FoodForm, SignUpForm
from demo_django.mixins import ModeratorRequiredMixin
from demo_django.models import Food
from django.views.generic import CreateView
from django.urls.base import reverse, reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render
from allauth.account.views import SignupView


# Create your views here.

class DashboardMenulistView(ListView):
    """
    Menu  View
    """
    login_url = reverse_lazy('login')
    template_name = "demo_django/menu_list.html"
    context_object_name = 'menus'
    filterset_class = MenuFilter

    def get_queryset(self):
        queryset = Food.objects.all().prefetch_related('categorys')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs.distinct()
        self.categorys = []
        for query in queryset:
            if query.categorys.name not in self.categorys:
                self.categorys.append(query.categorys.name)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['filterset'] = self.filterset
        context_data['request'] = self.request
        context_data['categorys'] = self.categorys
        return context_data


# class CreateFoodView(ModeratorRequiredMixin, TemplateView):
#     """
#     Creates multiple topics for a episode
#     """
#     login_url = reverse_lazy('login')
#     model = Food
#     form_class = FoodForm
#     template_name = "demo_django/create_food.html"
#
#     def get_queryset(self):
#         return self.model.objects.all().prefetch_related('categorys', 'types')
#
#     def get_success_url(self):
#         return reverse('menu')
#
#     def get_formset_kwargs(self):
#         """
#         Returns the keyword arguments for instantiating the formset.
#         """
#         super().get_formset_kwargs()
#         kwargs = self.formset_kwargs.copy()
#         kwargs['queryset'] = self.get_queryset()
#         kwargs.update({"initial": self.get_initial(), "prefix": self.get_prefix()})
#         if self.request.method in ("POST", "PUT"):
#             data = self.request.POST.copy()
#             kwargs.update(
#                 {"data": data, "files": self.request.FILES}
#             )
#             print(data)
#         return kwargs

class CreateFoodView(ModeratorRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'demo_django/create_food.html'
    form_class = FoodForm
    model = Food

    def get_success_url(self):
        return reverse('menu')


class SignUpView(CreateView):
    """
    Custom Signup View
    """
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'demo_django/signup.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     email = self.request.GET.get('email')
    #     context['email'] = email
    #     return context
