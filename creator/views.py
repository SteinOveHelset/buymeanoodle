from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cryptomus import Client

from .forms import CreatorForm
from .models import Creator, Support

MERCHANT_UUID = '621379c1-acca-4252-b066-2e86bfccff04'
PAYMENT_KEY = '1P0521ebLUozs8zAW2EOfNreI6DKi8qKeFuQaDWGzug8r3Wz7k32NCEdlzj5QjgaiagUfXisxmOqPND2HebpIfW1nB1aSrbuQg02PHvIxaj5opvEan9S52t92DV7C9bG'


@login_required
def mypage(request):
    creator = request.user.creator
    supports = creator.supports.filter(is_paid=True)
    total = 0

    for support in supports:
        total += support.amount

    return render(request, 'creator/mypage.html', {
        'creator': creator,
        'supports': supports,
        'total': total
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('creator:login')
    else:
        form = UserCreationForm()

    return render(request, 'creator/signup.html', {
        'form': form
    })


def creators(request):
    creators = Creator.objects.all()

    return render(request, 'creator/creators.html', {
        'creators': creators
    })


def creator(request, pk):
    creator = Creator.objects.get(pk=pk)

    return render(request, 'creator/creator.html', {
        'creator': creator
    })


def support_success(request, creator_id, support_id):
    support = Support.objects.get(pk=support_id)
    payment = Client.payment(PAYMENT_KEY, MERCHANT_UUID)

    result = payment.info({
        "uuid": f"{support.cryptomus_uuid}",
        "order_id": f"{support.id}"
    })

    if result['payment_status'] == 'paid':
        support.is_paid = True
        support.save()

    return render(request, 'creator/success.html')


def edit(request):
    try:
        creator = request.user.creator

        if request.method == 'POST':
            form = CreatorForm(request.POST, request.FILES, instance=creator)

            if form.is_valid():
                form.save()

                return redirect('core:index')
        else:
            form = CreatorForm(instance=creator)
    except Exception:
        if request.method == 'POST':
            form = CreatorForm(request.POST, request.FILES)

            if form.is_valid():
                creator = form.save(commit=False)
                creator.user = request.user
                creator.save()

                return redirect('core:index')
        else:
            form = CreatorForm()

    return render(request, 'creator/edit.html', {
        'form': form
    })