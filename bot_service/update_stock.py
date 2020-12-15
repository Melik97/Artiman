from Artiman.settings import MEDIA_ROOT
from bot_service.models import Product
from xml.dom import minidom
from unidecode import unidecode
import xlrd
import os

def data_():
   sp_list = list[1].split(' ')
   count = len( sp_list)
   code_fa = sp_list[-1]
   code = unidecode(code_fa)
   name_sp = ' '.join(sp_list[:(count-1)])
   stock = int(list[2])
   obj = Product.objects.filter(id=code).update(stock=stock)

list = []
def extract_data():
    loc1=MEDIA_ROOT+'/update/update.xls'
    wb = xlrd.open_workbook(loc1)
    sheet = wb.sheet_by_index(0)
    n_rows = sheet.nrows
    n_cols = sheet.ncols
    for j in range(n_rows):
        for i in range(n_cols):
            sh = sheet.cell_value(j, i)
            if j == 0:
                pass
            else:
                list.append(sh)
                if i == n_cols - 1 :
                    data_()
                    list.clear()
