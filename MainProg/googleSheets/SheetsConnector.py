
import aiohttp
import asyncio

import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
from bs4 import BeautifulSoup

from  ..models import Orders
from excel_reader.settings import BASE_DIR

class SheetsConnector:


    CREDENTIALS_FILE = f'{BASE_DIR}/MainProg/googleSheets/creds.json'
    spreadsheet_id = '1nup-1HKojIeu9oFarljMW5AIRQlgl52E7FDg15jsBp8'
    service = None

    order_list = []

    SheetsColumSize = 150


    def connect(self):

        # Присоединяемся к google Sheets
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CREDENTIALS_FILE,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ])

        httpAuth = credentials.authorize(httplib2.Http()) 
        self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)  


    def GetAllDataFromGoogleSheets(self):

        # Берем информацию из таблицы  google Sheets 

        values =  self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f'A1:E{self.SheetsColumSize}',
            majorDimension='ROWS'

        ).execute()

        return values


    def SetSheetsColumSize(self,range_):
        self.SheetsColumSize = range_

    
    async def MakeAsyncRequest(self,row):

        product_id = row[1]
        dolars = row[2]
        date = row[3].replace(".","/")
        SiteUrl =f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date}&date_req2={date}&VAL_NM_RQ=R01235"

        async with aiohttp.ClientSession() as session:
            async with session.get(SiteUrl,timeout=5) as response:
                
                xml = await response.text()
                soup = BeautifulSoup(xml,'xml')

                for value in soup.find_all('Value'):
                    rubles = float(value.text.replace(",",".")) * float(dolars)
                    self.order_list.append((product_id,dolars,rubles,row[3]))


    def saveToDbOrders(self):
        
        if len(self.order_list) != 0:
            for order in self.order_list:
                if not Orders.objects.filter(product_number=order[0]):

                    Orders.objects.create(
                        product_number = order[0],
                        price_dollars  = order[1],
                        price_rubles   = order[2],
                        date = order[3]
                    )

        

    async def getDolarsKyrse(self,rows):

        # Делаем асинхронные запросы по всем ссылкам

        tasks = []        
        for row in rows:
            task = asyncio.create_task(self.MakeAsyncRequest(row))
            tasks.append(task)
        
        await asyncio.gather(*tasks)




        

    
    