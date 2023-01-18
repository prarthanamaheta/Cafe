from celery import shared_task
from core.models import Customer
from demo_django.models import Visitor, Food
from goals_demo import settings
from django_tenants.utils import tenant_context
from django.core.mail import EmailMessage
from django.template.loader import get_template


# celery -A workpoint worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
@shared_task
def send_mail_task(tenant_name, visitor):
    customer = Customer.objects.filter(name=tenant_name).first()
    with tenant_context(customer):
        visitor = Visitor.objects.filter(id=visitor).first()

        if visitor:
            email = visitor.email
            ordered_food = visitor.orders.foods_ordered
            food_details = []
            for foods in ordered_food:
                food = Food.objects.filter(id=foods).first()
                food_details.append(food)
            context = {
                'visitor': visitor,
                'food': food_details,
                'customer': customer
            }
            message = get_template("demo_django/invoice.html").render(context)
            subject = f'Invoice from {customer.name}'
            msg = EmailMessage(subject,
                               message,
                               settings.EMAIL_HOST_USER,
                               [email])
            msg.content_subtype = "html"
            msg.send()
            return "Mail has been sent........"
        return "No users found"
