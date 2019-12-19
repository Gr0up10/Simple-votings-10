from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *


def index(request):
    context = {}

    context['votings'] = Voting.objects.all()
    context['votes'] = Vote.objects.all()

    if request.method == 'POST':
        option_id = request.POST.get('vote_button')
        num = int(Vote.objects.filter(option_id=option_id)[0].number)
        num +=1
        Vote.objects.filter(option_id=option_id).update(number=num)

    return render(request, 'index.html', context)

