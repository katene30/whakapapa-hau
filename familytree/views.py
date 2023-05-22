from django.shortcuts import render
from django.db.models import Q
from .models import Person


def home(request, id=1):
    root = Person.objects.get(pk = id)

    children = root.get_children()

    # TODO: Needs refactoring
    siblings = root.get_siblings()

    # TODO: Needs refactoring
    half_siblings = root.get_half_siblings()

    context = {
        'person': root,
        'children': children,
        'siblings': siblings,
        'half_siblings': half_siblings
    }
    return render(request, 'home.html', context)
