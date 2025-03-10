from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login  
from .forms import UserRegisterForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .utils.movie_predict import Movie_predictor


mp = Movie_predictor('./accounts/utils/data/movies_cleaned.csv')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Зберігаємо користувача
            login(request, user)  # Автоматичний логін
            messages.success(request, f'Account created for {user.username}!')
            return redirect('success')  
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



def registration_success(request):
    return render(request, 'accounts/registration_success.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def home(request):
    return render(request, 'accounts/home.html')

def success(request):
    return render(request, 'accounts/registration_success.html')


def recommend_movies(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').lower() 
        count = request.POST.get('count', '') 
        try:
            results = mp.give_recomendations(title, int(count))

            # Якщо результат порожній, вивести повідомлення
            if results.empty:
                return render(request, 'accounts/recommend.html', {'recommendations': "No recommendations found."})

            # Якщо результат не порожній, передаємо його в шаблон
            return render(request, 'accounts/recommend.html', {'recommendations': results.to_dict(orient='records')})

        except ValueError as e:
            return render(request, 'accounts/recommend.html', {'error': str(e)})

    return render(request, 'accounts/recommend.html')




