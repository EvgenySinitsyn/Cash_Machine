from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ReceiptSerializer
from .models import Item
from datetime import datetime
from receipt_proj.settings import MEDIA_ROOT, MEDIA_URL
import pdfkit
import qrcode


@api_view(['GET', 'POST'])
def api_receipt(request):

    # Представление для формирования POST запроса через браузер по адресу '{{root}}/cash_machine/'
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ReceiptSerializer(items, many=True)
        return Response(serializer.data)

    # Представление формирования ответа на POST запрос
    elif request.method == 'POST':

        # Формирование QuerySet на основе данных в POST запросе
        items = Item.objects.filter(pk__in=request.data['item'])

        # Подсчет количества товаров и общей стоимости
        total = 0
        for item in items:
            item.amount = request.data['item'].count(item.id)
            item.cost = item.price * item.amount
            total += item.cost

        time = datetime.now()                                               # Определение текущего времени и даты

        # Создание контекста для шаблона чека
        context = {
            'items': items,
            'datetime': time,
            'total': total,
        }
        template = render_to_string('receipt_app/receipt.html', context)     # Формирование шаблона с учетом контекста
        pdf_name = f'{time.strftime("%d_%m_%Y__%H_%M_%S")}.pdf'             # Задание имени pdf файла из даты и времени
        pdf_path = MEDIA_ROOT / pdf_name                                    # определение расположения для pdf файла
        pdf_url = "http://" + request.get_host() + MEDIA_URL + pdf_name            # Создание url для pdf файла
        pdfkit.from_string(template, pdf_path)                              # Формирование pdf файла

        img = qrcode.make(pdf_url)                                          # Создание QR кода с URL адресом чека
        img.save("media/qr_code_pdf_url.png")                               # Сохранение файла

        return render(request, 'receipt_app/qr_code.html')                   # Ответ


"""
{
"item": [1, 2, 3, 2, 3, 1, 2, 3, 4, 5]
}
"""
