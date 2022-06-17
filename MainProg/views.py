import threading

from django.shortcuts import render

from .googleSheets.ThreadRunner import UpdateLoop
from . models import Orders


# Запускаем бесконечный цикл, Обновляюший базу данных каждый час
th = threading.Thread(target=UpdateLoop)
th.start()




def StartPage(request):

    orders_ = Orders.objects.all() 

    return render(request,'MainProg/index.html',
    {
        'orders':orders_
    })




