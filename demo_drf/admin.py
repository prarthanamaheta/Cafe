from django.contrib import admin

from demo_drf.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'discount_percentage']
    search_fields = ['name', 'discount_percentage']
    actions = ['set_state']

    @admin.action(description='set offer is open or closed')
    def set_state(self, request, queryset):
        queryset.update(state=True)
