from Artiman.settings import MEDIA_ROOT
from bot_service.models import Product
from xml.dom import minidom
from unidecode import unidecode
import xlrd
import os


list = []
ll = []
def create_product(code, name, stock, image):
    obj, create = Product.objects.update_or_create(id=code ,defaults={
        'name': name,
        'id': code,
        'image': image,
        'stock':stock })

def data_():
    image_loc = MEDIA_ROOT+'/image/whitehall'
    sp_list = list[1].split(' ')
    count = len(sp_list)
    code_fa = sp_list[-1]
    code = unidecode(code_fa)
    name = ' '.join(sp_list[:(count-1)])
    stock = int(list[2])
    for filename in os.listdir(image_loc):
        image_code = filename.split('r')[0]
        if image_code == code:
            image = filename
            create_product(code, name, stock, image)


def extract_data():
    media_loc=MEDIA_ROOT+'/doc'
    for doc in os.listdir(media_loc):
        file = MEDIA_ROOT+'/doc/'+doc
        wb = xlrd.open_workbook(file)
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
