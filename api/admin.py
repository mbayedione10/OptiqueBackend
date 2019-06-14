from django.contrib import admin

# Register your models here.
# Import our models module.
from . import models
# Register our "Message" model with the Django Admin/
admin.site.register(models.Client)
admin.site.register(models.Commande)
admin.site.register(models.Lunette)
admin.site.register(models.CustomUser)
fields = ( 'image_tag', )
readonly_fields = ('image_tag',)
