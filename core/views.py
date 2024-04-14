from django.shortcuts import render, redirect

from creator.models import Creator


def index(request):
    creators = Creator.objects.all()

    if request.user.is_authenticated:
        try:
            creator = request.user.creator
        except Exception:
            return redirect('creator:edit')
        
    return render(request, 'core/index.html', {
        'creators': creators
    })