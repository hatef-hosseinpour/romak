from teska_main.models import Device
from django.contrib.auth.models import User
from users.models import Profile
from django.db.models import Q
from django.conf import settings
from base64 import b32encode, b32decode, b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import json


class DataEncryptionAgent:
    __AES_SECRET_KEY = settings.API_V2_SECRETS['AES_SECRET_KEY']
    __AES_IV = settings.API_V2_SECRETS['AES_IV']

    def create_aes_cipher(self):
        secret = b64decode(self.__AES_SECRET_KEY)
        iv = b64decode(self.__AES_IV)
        return AES.new(secret, AES.MODE_CBC, iv)

    def encrypt(self, plaintext):
        plain_json = json.dumps(plaintext, default=str)
        padded_plaintext = pad(plain_json.encode(), 16)
        ciphertext = self.create_aes_cipher().encrypt(padded_plaintext)
        ciphertext_b64 = b64encode(ciphertext).decode()
        return ciphertext_b64

    def decrypt(self, encrypted):
        enc = b64decode(encrypted)
        decrypted_data = unpad(self.create_aes_cipher().decrypt(enc), 16)
        decrypted_data = json.loads(decrypted_data)
        return decrypted_data


def get_object_by_user(user, queryset):

    if user.is_superuser and user.is_staff:
        queryset = queryset.all().order_by('-id')
    elif user.is_staff and not user.is_superuser:
        
        users = Profile.objects.filter(owner=user)
        user_ids = [profile['id'] for profile in users.values('id')]
        queryset = queryset.filter(Q(created_by=user.id) | Q(created_by__in=user_ids)).order_by('-id')
    else:
        queryset = queryset.filter(created_by=user.id).order_by('-id')

    return queryset

def get_device_status(status):
    acceptable_status = ''
    if status == True:
        acceptable_status = 'true'
    elif status == False:
        acceptable_status = 'false'
    else:
        acceptable_status = ''

    return acceptable_status
