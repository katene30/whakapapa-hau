from django.shortcuts import render
from .models import Person

def home(request):
    person = Person.objects.get(is_me=True)


    context = {
        'person': person,
    }
    return render(request, 'home.html', context)
