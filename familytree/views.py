from django.shortcuts import render
from django.db.models import Q
from .models import Person


def home(request, id=1):
    root = Person.objects.get(pk = id)

    children = root.get_children()

    # TODO: Needs refactoring
    siblings = Person.objects.filter(Q(mother = root.mother) & Q(father = root.father)).exclude(Q(id=root.id) | Q(mother__isnull=True) | Q(father__isnull=True))

    # TODO: Needs refactoring
    half_siblings = Person.objects.filter(Q(mother = root.mother) ^ Q(father = root.father)).exclude(Q(id=root.id) | Q(mother=root) | Q(father=root))

    context = {
        'person': root,
        'children': children,
        'siblings': siblings,
        'half_siblings': half_siblings
    }
    return render(request, 'home.html', context)
