from django.shortcuts import render
from .models import Person

def home(request):
    people = Person.objects.all()
    context = {
        'people': people,
    }
    return render(request, 'home.html', context)
