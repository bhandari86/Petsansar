from django.contrib import admin, messages

from petsansar.models import (AdoptionRequest, Animal, Contact, Donation,
                              Strayanimalrescue, Surrender, Notification,ListAdoptionRequest)

# Register your models here.
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('animal', 'user', 'status')

    def save_model(self, request, obj, form, change):
        original_obj = self.model.objects.get(pk=obj.pk) if change else None
        super().save_model(request, obj, form, change)

        if change and obj.status != original_obj.status:
            new_status_display = obj.get_status_display()
            message = f"Adoption request status for {obj.animal.breeds} has been changed to {new_status_display}."
            Notification.objects.create(user=obj.user, message=message, adoption_request=obj)

            messages.success(request,
                             f"Adoption request status has been changed to {new_status_display}. Notification sent.")

    save_model.short_description = "Save and Send Notification"


admin.site.register(Contact)
admin.site.register(Animal)
admin.site.register(Surrender)
admin.site.register(Donation)
admin.site.register(Strayanimalrescue)
admin.site.register(AdoptionRequest, AdoptionRequestAdmin)
admin.site.register(Notification)
admin.site.register(ListAdoptionRequest)



