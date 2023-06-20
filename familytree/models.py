from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from .choices import IWI_CHOICES
import re


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

class PersonVideo(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='video')
    video_url = models.URLField(help_text=
            "Supports links from YouTube or Vimeo like "
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ "
            "or https://vimeo.com/13020606")
    video_id = models.CharField(max_length=20, blank=True, null=True)
    video_service = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)

    VIDEO_SERVICE_ID_REGEX = re.compile(
    r"(http:\/\/|https:\/\/|)(player.|www.)?"
    r"(vimeo\.com|youtu(be\.com|\.be|be\.googleapis\.com))"
    r"\/(video\/|embed\/|channels\/staffpicks\/|watch\?v=|v\/)?"
    r"([A-Za-z0-9._%-]*)?"
    )

    VIDEO_SERVICE_YOUTUBE = "youtube"
    VIDEO_SERVICE_VIMEO = "vimeo"

    error = (
        "Please enter a Youtube or Vimeo URL only, "
        "e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ or "
        "https://vimeo.com/13020606"
    )

    regex_error = (
        "The video URL appears to be invalid, please check that you copied "
        "it in its entirety."
    )

    @classmethod
    def parse_video_service(cls, video_url):
        """
        Determines which video service (YouTube or Vimeo) the URL is for.
        :param video_url:
        :return:
        """
        if "vimeo.com" in video_url:
            return PersonVideo.VIDEO_SERVICE_VIMEO
        elif (
            "youtube.com" in video_url
            or "youtu.be" in video_url
            or "youtube.googleapis.com" in video_url
        ):
            return PersonVideo.VIDEO_SERVICE_YOUTUBE

    @classmethod
    def parse_video_id(cls, video_url):
        """
        Retrieves the ID from a YouTube or Vimeo URL.

        To tweak or edit the regex you can do so at
        https://regex101.com/r/gdJ0pt/5

        Supported URL structures:
        http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
        http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
        https://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
        http://www.youtube.com/embed/0zM3nApSvMg?rel=0
        http://www.youtube.com/watch?v=0zM3nApSvMg
        http://youtu.be/0zM3nApSvMg
        https://youtube.googleapis.com/v/My2FRPA3Gf8
        https://vimeo.com/67736784
        https://vimeo.com/channels/staffpicks/242573626
        http://player.vimeo.com/video/25451551
        //player.vimeo.com/video/25451551

        :param video_url:
        :return:
        """
        m = PersonVideo.VIDEO_SERVICE_ID_REGEX.search(video_url)
        if m and m.group(6):
            return m.group(6)

    def __str__(self):
        return self.title
    
    def clean(self):
        video_url = self.video_url

        video_service = self.parse_video_service(video_url)
        if not video_service:
            raise ValidationError({"video_url": [self.error]})

        video_id = self.parse_video_id(video_url)
        if not video_id:
            raise ValidationError({"video_url": [self.regex_error]})

        self.video_id = video_id
        self.video_service = video_service
        super().clean()

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

class PersonDocument(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='documentation')
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
        verbose_name_plural = "Iwi"

class PersonHapu(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='hapu')
    hapu = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.hapu
    
    class Meta:
        verbose_name_plural = "Hapu"

class Whanau(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(Person, related_name='whanau')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Whanau"
        