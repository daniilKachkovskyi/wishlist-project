from django.shortcuts import render, redirect, get_object_or_404
from .models import Wish
from .forms import WishForm
from django.contrib.auth.decorators import login_required # 👈 Для захисту функцій
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# 1. ГОЛОВНА СТОРІНКА (Просто вітання, без списку)
def home(request):
    return render(request, 'wish/home.html')

# 2. МОЇ БАЖАННЯ (Ось тут ми фільтруємо!)
@login_required # 👈 Цей декоратор не пустить сюди гостей (перекине на логін)
def wish_list(request):
    # Беремо ТІЛЬКИ бажання поточного користувача
    wishes = Wish.objects.filter(user=request.user)
    return render(request, 'wish/wish_list.html', {'wishes': wishes})

# 3. ВСІ БАЖАННЯ (Стрічка інших людей)
def explore(request):
    # Беремо ВСІ бажання, сортуємо нові зверху
    all_wishes = Wish.objects.all().order_by('-id')
    return render(request, 'wish/explore.html', {'wishes': all_wishes})

# 4. СТВОРЕННЯ
@login_required
def wish_create(request):
    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.user = request.user
            wish.save()
            # Після створення йдемо в "Мої бажання", а не на home
            return redirect('wish_list')
    else:
        form = WishForm()
    return render(request, 'wish/wish_form.html', {'form': form})

# 5. ОТРИМАВ (Виконати бажання)
@login_required
def wish_fulfill(request, pk):
    # Шукаємо бажання, але перевіряємо, чи воно належить саме ЦЬОМУ користувачу
    # (user=request.user), щоб чужі не можна було позначати
    wish = get_object_or_404(Wish, pk=pk, user=request.user)
    wish.is_received = True
    wish.save()
    return redirect('wish_list')

# 6. ВИДАЛИТИ
@login_required
def wish_delete(request, pk):
    # Так само: видаляти можна тільки свої
    wish = get_object_or_404(Wish, pk=pk, user=request.user)
    wish.delete()
    return redirect('wish_list')

# 7. РЕЄСТРАЦІЯ
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def wish_detail(request, pk):
    # Шукаємо бажання за його ID (pk)
    wish = get_object_or_404(Wish, pk=pk)
    return render(request, 'wish/wish_detail.html', {'wish': wish})