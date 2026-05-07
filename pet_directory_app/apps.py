from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group

    Group.objects.get_or_create(name="User")
    Group.objects.get_or_create(name="Shelter Admin")

class PetDirectoryAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pet_directory_app'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)

        from .models import Species
        default_species = ["Dog", "Cat", "Bearded Dragon", "Bird"]

        try:
            for name in default_species:
                Species.objects.get_or_create(name=name)
        except:
            pass
