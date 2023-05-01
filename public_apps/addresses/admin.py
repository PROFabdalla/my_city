from django.contrib import admin
from public_apps.addresses.models import Addresses


class AddressesAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "user", "country", "city", "address_line", "zip"]


admin.site.register(Addresses, AddressesAdmin)
