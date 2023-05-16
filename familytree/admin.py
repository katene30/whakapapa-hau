from django import forms
from django.contrib import admin

from .models import Person, Relationship

class PersonForm(forms.ModelForm):
    DATE_INPUT_FORMATS = [
        "%d/%m/%Y", # '30/06/2000'
        "%Y-%m-%d", # '2000-06-30'
    ]

    birth_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    death_date = forms.DateField(required=False, input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birth_date', 'death_date', 'is_me', 'mother', 'father', 'siblings']

class PersonAdmin(admin.ModelAdmin):
    form = PersonForm

admin.site.register(Person, PersonAdmin)
admin.site.register(Relationship)