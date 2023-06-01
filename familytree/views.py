from django.shortcuts import render
from .models import Person


def home(request, id=2):
    root = Person.objects.get(pk = id)

    children = root.get_children()

    siblings = root.get_siblings()

    half_siblings = root.get_half_siblings()

    context = {
        'person': root,
        'children': children,
        'siblings': siblings,
        'half_siblings': half_siblings
    }
    return render(request, 'home.html', context)
