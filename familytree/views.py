from django.shortcuts import render
from django.db.models import Q
from .models import Person


def home(request):
    person = Person.objects.get(is_me=True)

    # TODO: Needs refactoring
    siblings = Person.objects.filter(Q(mother = person.mother) & Q(father = person.father)).exclude(Q(id=person.id) | Q(mother__isnull=True) | Q(father__isnull=True))


    context = {
        'person': person,
        'siblings': siblings
    }
    return render(request, 'home.html', context)
