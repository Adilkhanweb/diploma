import json
from datetime import datetime
from django.db.models import Count, Sum, F
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from leaderboard.models import Leaderboard
from quiz_apps.multiplechoice.models import Attempt
from quiz_apps.quiz.models import Quiz
from users.forms import ProfileForm, UserUpdateForm, PasswordUpdateForm
from users.models import Profile


@login_required
def profile(request, user_id):
    quizzes = Quiz.objects.filter(attempts__user=request.user).order_by(
        '-end_time').distinct().prefetch_related('attempts')
    leaderboard = Leaderboard.objects.values(email=F('user__email'), first_name=F('user__first_name'),
                                             last_name=F('user__last_name'),
                                             picture=F('user__profile__picture')).order_by(
        'user').distinct().annotate(score=Sum('score')).order_by('-score')
    user_profile = get_object_or_404(Profile, user_id=user_id)
    profile_form = ProfileForm()
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordUpdateForm(user=request.user)
    if request.method == 'GET':
        if user_profile.user != request.user:
            return render(request, "base/404.html")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if request.method == 'POST':
        profile_form_req = ProfileForm(request.POST, request.FILES, instance=user_profile)
        user_form_req = UserUpdateForm(request.POST, instance=request.user)
        if profile_form_req.is_valid() and user_form_req.is_valid():
            request.user.first_name = user_form_req.cleaned_data['first_name']
            request.user.last_name = user_form_req.cleaned_data['last_name']
            request.user.save()
            profile_form_req.save()
            messages.add_message(request, *(messages.SUCCESS, "Өзгерістер Сақталды!"))
            return render(request, 'users/partials/profile_picture_form.html',
                          {'profile': user_profile, "profile_form": profile_form_req, "user_form": user_form_req,
                           "password_form": password_form, 'leaderboard': leaderboard, 'ip_address': ip})
        else:
            messages.add_message(request, *(messages.ERROR, "Өзгерістер Сақталмады!"))
            return render(request, 'users/partials/profile_picture_form.html',
                          {'profile': user_profile, "profile_form": profile_form_req, "user_form": user_form_req,
                           "password_form": password_form, 'leaderboard': leaderboard, 'ip_address': ip})
    return render(request, 'users/profile.html',
                  {'profile': user_profile, 'profile_form': profile_form, "user_form": user_form,
                   "password_form": password_form, "quizzes": quizzes, 'leaderboard': leaderboard, 'ip_address': ip})


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordUpdateForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.add_message(request, *(messages.SUCCESS, "Құпия сөз сақталды!"))
            return render(request, "users/partials/change_password_form.html",
                          {'password_form': password_form, 'success': True})
        else:
            return render(request, "users/partials/change_password_form.html",
                          {'password_form': password_form})
