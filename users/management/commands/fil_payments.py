from django.core.management import BaseCommand

from materials.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_to_create = []
        for user in User.objects.all():
            payment_to_create.append(Payment(user=user,
                                             lesson=Lesson.objects.get(pk=1),
                                             paid_sum=10000,
                                             method='Cash'))
        for user in User.objects.all():
            payment_to_create.append(Payment(user=user,
                                             course=Course.objects.get(pk=1),
                                             paid_sum=100000,
                                             method='Transfer'))

        Payment.objects.bulk_create(payment_to_create)
