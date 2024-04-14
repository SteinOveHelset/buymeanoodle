import json

from django.http import JsonResponse

from cryptomus import Client

from .models import Creator, Support

MERCHANT_UUID = '621379c1-acca-4252-b066-2e86bfccff04'
PAYMENT_KEY = '1P0521ebLUozs8zAW2EOfNreI6DKi8qKeFuQaDWGzug8r3Wz7k32NCEdlzj5QjgaiagUfXisxmOqPND2HebpIfW1nB1aSrbuQg02PHvIxaj5opvEan9S52t92DV7C9bG'


def create_support(request):
    print('request', request.POST)

    if request.method == 'POST':
        creator = request.POST
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        creator_id = request.POST.get('creator_id', '')

        # Create support

        support = Support.objects.create(
            creator_id=creator_id,
            amount=amount,
            email=email
        )

        # Talk to cryptomus

        data = {
            'amount': '1.1',
            'currency': 'USD',
            'network': 'Tron',
            'order_id': str(support.id),
            'url_return': f'https://buymeanoodle.onrender.com/creators/{creator_id}/',
            'url_success': f'https://buymeanoodle.onrender.com/creators/{creator_id}/success/{str(support.id)}/',
            'to_currency': 'USDT',
        }

        payment = Client.payment(PAYMENT_KEY, MERCHANT_UUID)

        result = payment.create(data)

        uuid = result['uuid']
        url = result['url']

        support.cryptomus_uuid = uuid
        support.save()

        return JsonResponse({'uuid': uuid, 'url': url})
    else:
        return JsonResponse({'success': False})