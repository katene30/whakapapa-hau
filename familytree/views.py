from django.shortcuts import render
from django.http import JsonResponse

from .models import Person


def home(request, id=2):
    root = Person.objects.get(pk = id)

    children = root.get_children()

    siblings = root.get_siblings()

    half_siblings = root.get_half_siblings()

    grandparents = root.get_grandparents()





    context = {
        'person': root,
        'children': children,
        'siblings': siblings,
        'half_siblings': half_siblings,
        'grandparents': grandparents,
    }
    return render(request, 'home.html', context)

def descendants(request, id=2):
    root = Person.objects.get(pk = id)
    hierarchy = root.get_descendants(3)
    return JsonResponse(hierarchy)

def ancestors(request, id=2):
    root = Person.objects.get(pk = id)
    hierarchy = root.get_ancestors(3)
    return JsonResponse(hierarchy)