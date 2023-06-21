from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from .choices import IWI_CHOICES
from .mixins import VideoMixin


class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    maiden_name = models.CharField(max_length=50,null=True, blank=True, help_text="Enter the previous surname or any other name used before marriage. Leave this field blank if not applicable.")
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    is_me = models.BooleanField(default=False)
    father = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='related_father', null=True, blank=True)
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='related_mother', null=True, blank=True)

    def get_children(self):
        if self.pk is None:
            # Person instance has not been saved yet, return an empty queryset
            return Person.objects.none()
        return Person.objects.filter(Q(mother = self) | Q(father = self))
    
    def get_siblings(self):
        return Person.objects.filter(Q(mother = self.mother) & Q(father = self.father)).exclude(Q(id=self.id) | Q(mother__isnull=True) | Q(father__isnull=True))

    def get_half_siblings(self):
        if self.pk is None:
            # Person instance has not been saved yet, return an empty queryset
            return Person.objects.none()
        
        if self.mother or self.father:
            half_siblings = Person.objects.filter(Q(mother = self.mother) ^ Q(father = self.father)).exclude(Q(id = self.id) | Q(mother__isnull = True) & Q(father__isnull = True))

            # Remove instances where the two people share a Null parent
            for half_sibling in half_siblings:
                if half_sibling.father is None and self.father is None or half_sibling.mother is None and self.mother is None:
                    half_siblings = half_siblings.exclude(Q(id=half_sibling.id))
                    
            return half_siblings
        
        return Person.objects.none()

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

    def get_descendants(self,depth):
        hierarchy = {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "children": []
        }

        if depth < 1:
            return hierarchy
        
        children = self.get_children()
        for child in children:
            hierarchy["children"].append(child.get_descendants(depth-1))

        return hierarchy
    
    def get_ancestors(self, depth):
        hierarchy = {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "parents": []
        }

        father = self.father
        mother = self.mother

        if depth < 1:
            return hierarchy
        if father:
            hierarchy["parents"].append(father.get_ancestors(depth - 1))
        
        if mother:
            hierarchy["parents"].append(mother.get_ancestors(depth - 1))

        return hierarchy
    
    def clean(self):
        if self.is_me:
            # Check if there is any other Person instance with is_me=True
            if Person.objects.filter(is_me=True).exclude(pk=self.pk).exists():
                raise ValidationError("Only one person can be marked as 'me'.")
        
        super().clean()

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

class PersonMedia(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField()
    alt_text = models.CharField(max_length=50, help_text='Provide alternative text for the image. Alt text is used by screen readers to describe the image for visually impaired users.')
    title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"

class PersonVideo(VideoMixin, models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='videos')
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        verbose_name = "Video"
        verbose_name_plural = "Videos"

class PersonDocument(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField()
    title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"

class PersonIwi(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='iwi')
    iwi = models.CharField(max_length=100, choices=IWI_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.iwi
    
    class Meta:
        verbose_name = "Iwi"
        verbose_name_plural = "Iwi"

class PersonHapu(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='hapu')
    hapu = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.hapu
    
    class Meta:
        verbose_name = "Hapu"
        verbose_name_plural = "Hapu"

class Whanau(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(Person, related_name='whanau')

    def get_url(self):
        return reverse('whanau-by-id', kwargs={'id': self.id})
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Whanau"

class WhanauIwi(models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='iwi')
    iwi = models.CharField(max_length=100, choices=IWI_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.iwi
    
    class Meta:
        verbose_name = "Iwi"
        verbose_name_plural = "Iwi"

class WhanauHapu(models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='hapu')
    hapu = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.hapu
    
    class Meta:
        verbose_name = "Hapu"
        verbose_name_plural = "Hapu"

class WhanauImage(models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.CharField(max_length=200, null=True, blank=True)
    alt_text = models.CharField(max_length=50, help_text='Provide alternative text for the image. Alt text is used by screen readers to describe the image for visually impaired users.')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WhanauVideo(VideoMixin, models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='videos')
    description = models.CharField(max_length=200, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        verbose_name = "Video"
        verbose_name_plural = "Videos"

class WhanauDocument(models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField()
    title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"

class WhanauWaiata(VideoMixin, models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='waiata')
    name = models.CharField(max_length=100)
    songwriter = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    lyrics = models.TextField(max_length=2000, null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    class Meta:
        abstract = False
        verbose_name_plural = "Waiata"
    
class WhanauHaka(VideoMixin, models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='haka')
    name = models.CharField(max_length=100)
    composer = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    lyrics = models.TextField(max_length=2000, null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    class Meta:
        abstract = False
        verbose_name_plural = "Haka"

# Under review if it's important enough to keep. Whether we want it now or later
# Needs evaluating the value of this feature 
class WhanauStory(models.Model):
    whanau = models.ForeignKey(Whanau, on_delete=models.CASCADE, related_name='whanau_stories')
    title = models.CharField(max_length=100)
    narrative = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Whanau Stories"

class WhanauStoryImage(models.Model):
    whanau_story = models.ForeignKey(WhanauStory, on_delete=models.CASCADE, related_name='whanau_story_images')
    title = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.CharField(max_length=200, null=True, blank=True)
    alt_text = models.CharField(max_length=50, help_text='Provide alternative text for the image. Alt text is used by screen readers to describe the image for visually impaired users.')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
