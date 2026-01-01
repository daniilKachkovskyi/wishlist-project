from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Wish
from .forms import WishForm
from django.urls import reverse_lazy
from django.views import generic

def wish_list(request):
    wishes = Wish.objects.all() # перенесли всю базу даних
    return render(request, 'wish/wish_list.html', {'wishes': wishes}) # для хтмл


def wish_create(request): # Створює /wishes/create спочатку перевіряє чи відправив чи просто глянув сторінку а потім код
    if request.method  == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wish_list')
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

