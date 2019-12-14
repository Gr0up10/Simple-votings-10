from django.shortcuts import render
from .models import *


def index(request):
    context = {}

    context['votings'] = Voting.objects.all()

    return render(request, 'index.html', context)

