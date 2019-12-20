from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class CreateVoting(forms.Form):
    #def __init__(self, num):
     #   super().__init__()
      #  self.num = num
    #options = list()
    main_text = forms.CharField(max_length=200, min_length=1, required=True, label='Основной текст')
    first = forms.CharField(max_length=50, min_length=1, required=True, label='Вариант ' + str(1))
    second = forms.CharField(max_length=50, min_length=1, required=True, label='Вариант ' + str(2))


class NumOfOptions(forms.Form):
    number = forms.IntegerField(max_value=10, min_value=1, required=True, label='Количество вариантов для голосования')
