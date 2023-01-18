from django.contrib import admin

from demo_django.models import Food, Category, Type, Order


class OfferInline(admin.TabularInline):
    model = Order.offers.through


class CategoryInline(admin.TabularInline):
    model = Category


class FoodInline(admin.TabularInline):
    model = Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'categorys', 'types', 'items', 'price', 'type_name']
    search_fields = ['name', 'categorys__name', 'types__name']
    list_display_links = ['name']
    list_editable = ["items", "categorys", "types"]
    raw_id_fields = ('categorys',)


    @admin.display()
    def type_name(self, obj):
        return obj.types.name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [FoodInline]


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [FoodInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['token', 'status', 'total_payment']
    search_fields = ['token']
    actions = ['received_payment']
    inlines = [OfferInline]

    @admin.action(description='mark when received payment')
    def received_payment(self, request, queryset):
        queryset.update(payment_received=True)