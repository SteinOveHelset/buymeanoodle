from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        try:
            creator = request.user.creator
        except Exception:
            return redirect('creator:edit')
        
    return render(request, 'core/index.html')