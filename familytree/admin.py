from django import forms
from django.contrib import admin

from .models import Person, Relationship

class PersonForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=["%d/%m/%Y"])
    death_date = forms.DateField(required=False, input_formats=["%d/%m/%Y"])

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birth_date', 'death_date']

class PersonAdmin(admin.ModelAdmin):
    form = PersonForm

admin.site.register(Person, PersonAdmin)
admin.site.register(Relationship)