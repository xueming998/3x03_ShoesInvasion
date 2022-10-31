from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
#from ShoesInvasionApp.models import UserTable

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        #print('user verified status:', user.verifiedStatus)
        #print("hash value:",six.text_type(user.verificationCode) + six.text_type(timestamp) + six.text_type(user.verifiedStatus))
        return (
            six.text_type(user.verificationCode) + six.text_type(timestamp) + six.text_type(user.verifiedStatus)
        )

account_activation_token = AccountActivationTokenGenerator()