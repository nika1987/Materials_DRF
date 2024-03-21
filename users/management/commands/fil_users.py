from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        users_list = [
            {'email': 'user1@hell.ok', 'phone': '666453672', 'city': 'Satania'},
            {'email': 'user2@hell.ok', 'phone': '666139990', 'city': 'Babylon'}
        ]
        user_to_create = []
        for user_item in users_list:
            user_to_create.append(User(**user_item))

            User.objects.bulk_create(user_to_create)
