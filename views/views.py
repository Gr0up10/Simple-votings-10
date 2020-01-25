from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import *
from .forms import *
import json
from django.utils.safestring import SafeString
from django.contrib.auth import update_session_auth_hash


def login_page(request):
    context = dict()
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        post = User.objects.filter(username=username)
        # print(post)
        if post:
            # request.session['username'] = username
            from django.contrib import auth
            user1 = auth.authenticate(username=username, password=password)
            if user1 is not None and user1.is_active:
                # Правильный пароль и пользователь "активен"
                auth.login(request, user1)
                return redirect("home")
            else:
                return render(request, 'registration/login.html', context)
        else:
            return render(request, 'registration/login.html', context)
    return render(request, 'registration/login.html', context)


def theme_change(request):
    if request.method == "POST":
        if request.POST.get('theme_flag') == 'dark':
            print('flag is dark')
            flag = True
            item = ThemeBD(Theme=flag)
            item.save()
        elif request.POST.get('theme_flag') == 'light':
            print('flag is light')
            flag = False
            item = ThemeBD(Theme=flag)
            item.save()
    return render(request, 'theme.html')


def index(request):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['votings'] = Voting.objects.all()
    indexes = []

    for voting in context['votings']:
        indexes.append(int(voting.id))

    context['indexes'] = indexes

    context['len'] = len(context['votings'])
    ids = dict()
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)

    context['theme_flag'] = (data_t[lent].Theme)
    # context['optNum'] = len(context['options'])
    la = list()
    da = list()
    for i in range(context['len']):
        context['options'] = context['votings'][i].options()
        # print(context['options'])

        labels = []
        data = []

        for option in context['options']:
            labels.append(option.text)
            data.append(option.vote_count())

        la.append(SafeString(json.dumps(labels)))
        da.append(SafeString(json.dumps(data)))

    context['la'] = la
    context['da'] = da

    if request.method == 'POST':
        single_vote(request)

    #     f = ThemeForm(request.POST)
    #     if f.is_valid():
    #         flag = bool(request.POST.get('flag'))
    #         # Сохранение данных
    #         item = ThemeBD(Theme= flag)
    #         item.save()
    #         # Формирование ответа
    #         context['flag'] = flag
    #         context['form'] = f
    #     else:
    #         context['form'] = f
    else:
        context['nothing_entered'] = True
    if request.method == 'GET':
        context['ids'] = ids
    return render(request, 'index.html', context)


def single_vote(request):
    if request.method == 'POST':
        option_id = request.POST.getlist('answer')  # getlist - функция , которая возвращяет list всех answer
        voting_id = request.POST.get('voting_id')
        if request.user.is_authenticated:
            print('проверка повторного голосования')
            if not (Vote.objects.filter(user=request.user,
                                        voting=Voting.objects.get(
                                        id=voting_id)).exists()):  # Проверка голосовал ли пользователь в этом голосовании или нет
                for i in range(len(option_id)):  # добавление всех ответов
                    vote1 = Vote(option=Option.objects.get(id=option_id[i]),
                                 user=request.user,
                                 voting=Voting.objects.get(id=voting_id))
                    vote1.save()
                    print('Голос засчитан')
            else:
                print('Уже голосовал')
                context = dict()
                context['auth'] = request.user.is_authenticated  # нужно для отображения меню
                return redirect("alr")
        else:
            context = dict()
            context['auth'] = request.user.is_authenticated  # нужно для отображения меню
            return render(request, 'Log_in.html', context)


def already(request):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)
    return render(request, 'already.html', context)


def vote(request, option_id):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['voting'] = Voting.objects.get(id=option_id)  # добавление вопроса по его id
    context['options'] = Option.objects.filter(voting_id=option_id)  # добавление всех его вариантов ответа
    context['option_id'] = option_id  # номер вопроса
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)

    labels = []
    data = []

    for option in context['options']:
        labels.append(option.text)
        data.append(option.vote_count())

    context['labels'] = SafeString(json.dumps(labels))
    context['data'] = SafeString(json.dumps(data))

    single_vote(request)
    return render(request, 'vote.html', context)


def edit(request, option_id):
    context = dict()
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)
    context['auth'] = request.user.is_authenticated
    if request.method == "POST":
        if request.POST.get("delete"):
            context['need_buttons'] = False
            context['deleted'] = True
            voting = Voting.objects.get(id=option_id)
            voting.delete()
        if request.POST.get("delete_option"):
            context['need_buttons'] = True
            context['deleted'] = False
            context['mode'] = 2
            context['voting'] = Voting.objects.get(id=option_id)
            context['options'] = Option.objects.filter(voting_id=option_id)
            context['option_id'] = option_id
        if request.POST.get("delete_selected"):
            for i in request.POST:
                if not ((i == 'csrfmiddlewaretoken') or (i == 'delete_selected')):
                    id = int(i[7:])
                    option = Option.objects.get(id=id)
                    voting = Voting.objects.get(id=option.voting_id)
                    option.delete()
                    context['deleted'] = False
                    context['deleted_option'] = True
                    if Option.objects.filter(voting_id=voting.id).count() == 0:
                        voting.delete()
                        context['deleted'] = True
                        context['deleted_option'] = False
                    context['need_buttons'] = False
        if request.POST.get('add_option'):
            context['need_buttons'] = True
            context['deleted'] = False
            context['mode'] = 3
            context['voting'] = Voting.objects.get(id=option_id)
            context['options'] = Option.objects.filter(voting_id=option_id)
            context['opt_len'] = len(context['options'])
            context['count_options'] = context['options'].count()
            context['option_id'] = option_id
        if request.POST.get("done"):
            voting = Voting.objects.get(id=option_id)
            context['deleted'] = False
            context['need_buttons'] = False
            context['add_option'] = True
            for i in request.POST:
                if not ((i == 'csrfmiddlewaretoken') or (i == 'done') or (request.POST[i] == '')):
                    text = request.POST[i]
                    option = Option(voting=voting, text=text)
                    option.save()
    elif Voting.objects.filter(id=option_id).count() == 0:
        context['need_buttons'] = False
        context['deleted'] = True
    else:
        context['need_buttons'] = True
        context['deleted'] = False
        context['voting'] = Voting.objects.get(id=option_id)
        context['options'] = Option.objects.filter(voting_id=option_id)
        context['option_id'] = option_id
        context['mode'] = 1
        single_vote(request)
    return render(request, 'edit.html', context)


def user(request):
    if request.user.is_authenticated:
        context = dict()
        context['auth'] = request.user.is_authenticated  # нужно для отображения меню
        votings = Voting.objects.filter(author=request.user)
        context['votings'] = votings

        data_t = ThemeBD.objects.in_bulk()
        lent = len(data_t)
        context['theme_flag'] = data_t[lent].Theme

        votes = Vote.objects.filter(user=request.user)
        options = list()
        for vote1 in votes:
            options.append(vote1.option)
        votings = set()
        for option in options:
            votings.add(option.voting)
        context['votings_voted'] = votings

        indexes = []
        for voting in context['votings']:
            indexes.append(int(voting.id))
        for voting in context['votings_voted']:
            indexes.append(int(voting.id)+100)
        context['indexes'] = indexes

        la = list()
        da = list()
        for i in range(len(context['votings'])):
            context['options'] = context['votings'][i].options()

            labels = []
            data = []

            for option in context['options']:
                labels.append(option.text)
                data.append(option.vote_count())

            la.append(SafeString(json.dumps(labels)))
            da.append(SafeString(json.dumps(data)))

        votings_voted_list = list()
        for voting in context['votings_voted']:
            votings_voted_list.append(voting)

        for i in range(len(context['votings_voted'])):
            context['options'] = votings_voted_list[i].options()

            labels = []
            data = []

            for option in context['options']:
                labels.append(option.text)
                data.append(option.vote_count())

            la.append(SafeString(json.dumps(labels)))
            da.append(SafeString(json.dumps(data)))

        context['la'] = la
        context['da'] = da
    else:
        return render(request, 'Log_in.html')

    return render(request, 'user.html', context)


def create(request):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['mode'] = 1
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)
    if request.method == 'GET':
        context['form'] = CreateVoting()

    if request.method == 'POST':

        if request.user.is_authenticated:
            main_text = request.POST.get('main_text')
            isCheckbox = bool(request.POST.get('isCheckbox'))
            voting = Voting(question=main_text, author=request.user, isCheckbox=isCheckbox)
            voting.save()
            count = request.POST.get('count')
            if count:
                for i in range(1, int(count) + 1):
                    text = request.POST.get('option' + str(i))
                    option = Option(voting=voting, text=text)
                    option.save()

            tmp = Voting.objects.filter(author=request.user)  # отфильтровка вопросов данного пользователя
            voting_id = tmp[len(tmp) - 1].id  # определение id последнего вопроса
            return redirect(vote, voting_id)  # редирект на voting/voting_id
        else:
            return render(request, 'Log_in.html')
    else:
        context['nothing_entered'] = True

    return render(request, 'creation.html', context)


def register(request):
    context = dict()
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)
    if request.method == 'POST':
        form = RegisterFormView(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            _user = authenticate(username=username, password=my_password)
            if _user.is_active:
                login(request, _user)
                return render(request, 'index.html', context)
        return render(request, 'registration/register.html', context)
    else:
        form = RegisterFormView()
        context['form'] = form
        return render(request, 'registration/register.html', context)

@login_required()
def password_change(request):
    context = dict()
    data_t = ThemeBD.objects.in_bulk()
    lent = len(data_t)
    context['theme_flag'] = (data_t[lent].Theme)
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['form'] = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/login')
        else:
            return render(request, 'password.html', context)
    else:
        return render(request, 'password.html', context)