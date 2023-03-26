from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.forms import ProfileForm, UserUpdateForm
from account.models import Profile


@login_required
def profile(request, user_profile_id):
    user_profile = Profile.objects.get(id=user_profile_id)
    profile_form = ProfileForm()
    user_form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return render(request, 'account/partials/profile_picture_form.html',
                          {'profile': user_profile, "profile_form": profile_form, "user_form": user_form})
        else:
            print(profile_form.errors)
            return HttpResponse(status=400)
    if request.method == 'GET':
        if user_profile.user != request.user:
            return HttpResponse(status=404)
    return render(request, 'account/profile.html', {'profile': user_profile, 'profile_form': profile_form, "user_form": user_form})
