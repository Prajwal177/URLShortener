from django.contrib import admin
from .models import ShortURL

# Register your models here.
@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('id','short_code', 'original_url', 'owner', 'click_count', 'created_at')
    search_fields = ('short_code', 'original_url', 'owner_username')
    list_filter = ('created_at',)