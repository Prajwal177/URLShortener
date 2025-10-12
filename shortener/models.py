import string
import random
from django.db import models
from django.contrib.auth.models import User

xor_encoding_key = "pkp2"

def xor_encoder(unique_id: int) -> str:
    id_str = str(unique_id)
    encoded_chars = []
    
    for i, char in enumerate(id_str):
        encoded_char = chr(int(char) ^ ord(xor_encoding_key[i % len(xor_encoding_key)]))
        encoded_chars.append(encoded_char)
    
    return ''.join(encoded_chars)

class ShortURL(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)

        if not self.short_code:
            self.short_code = xor_encoder(self.id)
            super().save(update_fields=['short_code'])
        else:
            super().save(*args, **kwargs)