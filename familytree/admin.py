from django import forms
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.db.models import Q

from .models import Person, Relationship, PersonMedia, PersonIwi, PersonHapu, PersonDocument, PersonVideo

class PersonForm(forms.ModelForm):


    DATE_INPUT_FORMATS = [
        "%d/%m/%Y", # '30/06/2000'
        "%Y-%m-%d", # '2000-06-30'
    ]

    birth_date = forms.DateField(input_formats=DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'type': 'date'}))
    death_date = forms.DateField(required=False, input_formats=DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Person
        fields = '__all__'

class PersonMediaInline(admin.TabularInline):
    model = PersonMedia

class PersonVideoInline(admin.TabularInline):
    def get_exclude(self, request, obj=None):
        if obj:  # Exclude 'video_id' field when editing an existing PersonVideo instance
            return ['video_id']
        return []  # Show 'video_id' field when creating a new PersonVideo instance
    model = PersonVideo

class PersonDocumentInline(admin.TabularInline):
    model = PersonDocument

class PersonIwiInline(admin.TabularInline):
    model = PersonIwi

class PersonHapuInline(admin.TabularInline):
    model = PersonHapu

class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
    
    inlines = [
        PersonIwiInline,
        PersonHapuInline,
        PersonMediaInline,
        PersonVideoInline,
        PersonDocumentInline,
    ]

    readonly_fields = ["children_list", "siblings_list", "half_siblings_list", "grandparents_list"]

    # description functions like a model field's verbose_name
    @admin.display(description="Children")
    def children_list(self, instance):
        return format_html_join(
            mark_safe("<br>"),
            "{} {}",
            ((person.first_name, person.last_name) for person in instance.get_children()),
        )
    
    @admin.display(description="Siblings")
    def siblings_list(self, instance):
        if(instance.mother is not None or instance.father is not None):
            return format_html_join(
                mark_safe("<br>"),
                "{} {}",
                ((person.first_name, person.last_name) for person in instance.get_siblings()),
            )
    
    @admin.display(description="Half-Siblings")
    def half_siblings_list(self, instance):
            return format_html_join(
                mark_safe("<br>"),
                "{} {}",
                ((person.first_name, person.last_name) for person in instance.get_half_siblings()),
            )

    @admin.display(description="Grandparents")
    def grandparents_list(self, instance):
            return format_html_join(
                mark_safe("<br>"),
                "{} {}",
                ((person.first_name, person.last_name) for person in instance.get_grandparents()),
            )


admin.site.register(Person, PersonAdmin)
admin.site.register(Relationship)