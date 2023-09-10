from django import forms

from .models import Animal, Strayanimalrescue


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['breeds', 'color', 'sex','medical_condition','location', 'desc']
        # Add more fields if needed

    # Add additional fields needed for the adoption request form
    user_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)