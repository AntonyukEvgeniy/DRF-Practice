from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Создать группу модераторов и добавить туда пару пользователей'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+', type=str,
                            help='Email-адреса для добавления в группу')

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                moderators_group, created = Group.objects.get_or_create(name='moderators')
                if created:
                    self.stdout.write(self.style.SUCCESS('Группа модераторов создана'))

                emails = options['emails']
                for email in emails:
                    try:
                        user = User.objects.get(email=email)
                        user.groups.add(moderators_group)
                        self.stdout.write(
                            self.style.SUCCESS(f'Added user {email} to moderators group')
                        )
                    except User.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'User with email {email} not found')
                        )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating moderators: {str(e)}')
            )