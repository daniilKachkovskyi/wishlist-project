from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Wish
from .forms import WishForm
from django.urls import reverse_lazy
from django.views import generic

def wish_list(request):
    wishes = Wish.objects.all() # перенесли всю базу даних
    return render(request, 'wish/wish_list.html', {'wishes': wishes}) # для хтмл


def wish_create(request):  # Назва може бути іншою, шукай свою функцію створення
    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            # 👇 МАГІЯ ТУТ 👇
            wish = form.save(commit=False)  # 1. Створи бажання, але поки не зберігай у базу
            wish.user = request.user  # 2. Приклей до нього поточного користувача request - дайє інфу про поточний сеанс
            wish.save()  # 3. Тепер зберігай остаточно

            return redirect('home')  # Або куди ти там перенаправляєш
    else:
        form = WishForm()

    return render(request, 'wish/wish_form.html', {'form': form})


def wish_fulfill(request, pk):
    wish = get_object_or_404(Wish, pk=pk) # pk=pk це ід яке відправив користувач збігається з вказаним
    wish.is_received = True
    wish.save()
    return redirect('wish_list')


def wish_delete(request, pk):
    wish = get_object_or_404(Wish, pk=pk)
    wish.delete()
    return redirect('wish_list')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# wish/views.py

def home(request):
    # Перевіряємо, чи увійшов користувач
    if request.user.is_authenticated:
        # Якщо увійшов - показуємо ТІЛЬКИ його бажання
        wishes = Wish.objects.filter(user=request.user)
    else:
        # Якщо не увійшов - список порожній (або показуємо приклад)
        wishes = []

    return render(request, 'wish/home.html', {'wishes': wishes})

def explore(request):
    # Беремо всі бажання і сортуємо: нові зверху ('-id')
    all_wishes = Wish.objects.all().order_by('-id')
    return render(request, 'wish/explore.html', {'wishes': all_wishes})

