

from django.contrib.auth.models import User


class UserAction:

    @staticmethod
    def user_exits(username):
        return User.objects.filter(username=username).exists()

    @staticmethod
    def user_create(username, email, password, extra_fields=None):
        user = User.objects.create_user(
            username, email, password, **extra_fields)
        user.save()
