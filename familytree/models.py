from django.db import models
from django.db.models import Q
from django.urls import reverse
from .choices import IWI_CHOICES

class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    is_me = models.BooleanField(default=False)
    father = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='related_father', null=True, blank=True)
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='related_mother', null=True, blank=True)
    iwi = models.CharField(max_length=100, choices=IWI_CHOICES, null=True, blank=True)
    hapu = models.CharField(max_length=100, null=True, blank=True)

    def get_children(self):
        return Person.objects.filter(Q(mother = self) | Q(father = self))
    
    def get_siblings(self):
        return Person.objects.filter(Q(mother = self.mother) & Q(father = self.father)).exclude(Q(id=self.id) | Q(mother__isnull=True) | Q(father__isnull=True))
    
    def get_half_siblings(self):
        return Person.objects.filter(Q(mother = self.mother) ^ Q(father = self.father)).exclude(Q(id=self.id) | Q(mother__isnull=True) & Q(father__isnull=True))

    def get_grandparents(self):
        grandparents = Person.objects.none()

        if self.father:
            grandparents |= Person.objects.filter(
                Q(id=self.father.father_id) | Q(id=self.father.mother_id)
            )
        
        if self.mother:
            grandparents |= Person.objects.filter(
                Q(id=self.mother.father_id) | Q(id=self.mother.mother_id)
            )
        
        return grandparents

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_url(self):
        return reverse('home-by-user', kwargs={'id': self.id})

    class Meta:
        verbose_name_plural = "people"

class Relationship(models.Model):
    RELATIONSHIP_CHOICES = [
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('sibling', 'Sibling'),
        ('spouse', 'Spouse')
    ]

    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='from_person')
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='to_person')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)

    def __str__(self):
        return f"{self.from_person} {self.relationship_type} {self.to_person}"