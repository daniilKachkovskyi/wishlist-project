from django.shortcuts import render, redirect, get_object_or_404
from .models import Wish
from .forms import WishForm
from django.contrib.auth.decorators import login_required # 👈 Для захисту функцій
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# 1. ГОЛОВНА СТОРІНКА
def home(request):
    return render(request, 'wish/home.html')

@login_required
def wish_list(request):
    wishes = Wish.objects.filter(user=request.user)
    return render(request, 'wish/wish_list.html', {'wishes': wishes})

# ВСІ БАЖАННЯ
def explore(request):
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

# 5. ОТРИМАВ
@login_required
def wish_fulfill(request, pk):
    wish = get_object_or_404(Wish, pk=pk, user=request.user)
    wish.is_received = True
    wish.save()
    return redirect('wish_list')

# 6. ВИДАЛИТИ
@login_required
def wish_delete(request, pk):
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
    wish = get_object_or_404(Wish, pk=pk)
    return render(request, 'wish/wish_detail.html', {'wish': wish})