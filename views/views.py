from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *


def index(request):
    context = dict()
    context['votings'] = Voting.objects.all()
    return render(request, 'index.html', context)
