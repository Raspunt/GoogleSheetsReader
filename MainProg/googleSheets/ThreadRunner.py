
import time
import asyncio

from . SheetsConnector import SheetsConnector

def UpdateLoop():
    print("Запуст бесконечного цикла для обновления базы данных")
    while True:


        sc = SheetsConnector()
        sc.connect()
        values = sc.GetAllDataFromGoogleSheets()
        asyncio.run(sc.getDolarsKyrse(values['values']))
        sc.saveToDbOrders()


        time.sleep(3600)



