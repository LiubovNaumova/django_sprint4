from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from blog.forms import UserProfileForm


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'blog/user.html', {'form': form})
