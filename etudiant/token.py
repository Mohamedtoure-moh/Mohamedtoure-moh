from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
# La class pour la generation du token(jeton)
class Generationdujeton(PasswordResetTokenGenerator):
    #la fonction permettant de hacher le token
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp)
        )
# L'instence
generateur  = Generationdujeton()