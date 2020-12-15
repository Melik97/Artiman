from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from Artiman.settings import MEDIA_ROOT
from django.db.models import Count
from dateutil.parser import parser
from random import seed, randint
from .models import Album , Product
from .update_stock import extract_data
from telegram import Bot
import logging
import django
import os
# from django.core.mail import send_mail

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
ALBUM , PRODUCT, ADMIN, PRODUCT_IMAGE, VIDEO_INPUT, GIF_INPUT, ALBUM_NAME, PRODUCT_NAME, PRODUCT_CODE, PRODUCT_STOCK, CUSTOMER, SEND_PRODUCT, SEND_ALBUM, SHOW_ALBUM, ORDER, FILE_INPUT= range(16)
reply_keyboard = [['Album'], ['Product']]
admin_menu_keyboard = [['اپدیت موجودی'],['افزودن البوم','افزودن محصول'],['ارسال پست']]
admin_keyboard = [['Image','Video','Gif'],['Post']]
order_keyboard = [['برگشت','لغو'],['ثبت سفارش']]
customer_menu_keyboard = [['محصولات'],['البوم']]
albumValue_keyboard = [['ویدیو','گیف'],['لغو']]
cancel_keyboard = [['لغو']]
# for save video name
def create_product(code, name, stock, image):
    obj, create = Product.objects.update_or_create(id=code ,defaults={
        'name': name,
        'id': code,
        'image': image,
        'stock':stock })

def create_album(name, video, gif):
    obj, create = Album.objects.update_or_create(defaults={
        'name': name,
        'video': video,
        'gif': gif})


random_number = randint(100000000, 99999999999)
#click /start and runbot
def start(update: Update, context: CallbackContext) -> int:
    print('start bot...')
    user_info = update.message.chat
    user_id = user_info['id']
    user_name = user_info['username']
    name = user_info['first_name']
    if user_name == 'melika_akz':
        print('Admin start bot')
        update.message.reply_text('سلام ادمین ',
                                  reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))
        return ADMIN
    # show keyboard cve,vip,other
    print(f'{user_id} user {user_name} start bot')
    update.message.reply_text('سلام , مشتری گرامی لطفا برای دیدن البوم و سفارش محصولات یک گزینه را انتخاب کنید:',
                              reply_markup=ReplyKeyboardMarkup(customer_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return CUSTOMER


# admin menu
index_list = []
def admin(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    if update.message.text == 'افزودن البوم':
        update.message.reply_text('اسم البوم را وارد کنید',
                        reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ALBUM_NAME

    if update.message.text == 'افزودن محصول':
        update.message.reply_text('کد محصول را وارد کنید:',
                        reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return PRODUCT_CODE

    if update.message.text == 'ارسال پست':
        update.message.reply_text('حالا موارد خواسته شده را وارد کنید',
                        reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return SEND_POST

    if update.message.text == 'اپدیت موجودی':
        update.message.reply_text('فایل را بفرستید(فرمت xls :)',
                        reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return FILE_INPUT
    else:
        logger.info("No match ")
        update.message.reply_text('انتخاب کنید',
                        reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))
        return ADMIN


# album botton ================================================================
#get albumname and add list for create db
def album_name(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    name = update.message.text

    if name == 'لغو':
        update.message.reply_text('انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True,resize_keyboard=True))

        return ADMIN
    else:
        index_list.append(name)
        update.message.reply_text('ویدیو البوم را ارسال کنید توجه داشته باشید حجم کمتر از ۲۰ مگ باشد.',
                    reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return VIDEO_INPUT

# get video and add in list for create db
def video_input(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    text = update.message.text

    if text == 'لغو':
        update.message.reply_text('انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN
    else:
        update.message.reply_text('لطفا کمی صبرکنید تا فایل توسط بات دانلود شود')
        random_number = randint(100000000, 99999999999)
        video_ = update.message.video.get_file()
        video_.download(MEDIA_ROOT+'/video/'+str(random_number)+'.mp4')
        video_name = str(random_number)+'.mp4'
        index_list.append(video_name)
        update.message.reply_text('دریافت شد ادمین')
        update.message.reply_text('گیف البوم را ارسال کنید.',
                        reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))


        return GIF_INPUT

#get gif and add list and create db here with function create_album
def gif_input(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    text = update.message.text

    if text == 'لغو':
        update.message.reply_text(':انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN
    else:
        user = update.message.from_user
        update.message.reply_text('لطفا کمی صبرکنید تا فایل توسط بات دانلود شود.')
        random_number = randint(100000000, 99999999999)
        gif_ = update.message.animation.get_file()
        gif_.download(MEDIA_ROOT+'/gif/'+str(random_number)+'.mp4')
        index_list.append(str(random_number)+'.mp4')
        update.message.reply_text('دریافت شد.')
        create_album(index_list[0],index_list[1],index_list[2])
        index_list.clear()
        update.message.reply_text('ادمین لطفا یک گزینه را انتخاب کن:')

        return ADMIN

# end album botton ===========================================================
# add product bottom =========================================================

# add code to index_list for create product
def product_code(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    text = update.message.text
    if text == 'لغو':
        update.message.reply_text(':انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN
    else:
        index_list.append(int(text))
        update.message.reply_text('حالا اسم محصول را وارد کنید:',
                    reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        print(index_list)
        return PRODUCT_NAME

# add name to index_list for create product
def product_name(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    name = update.message.text
    if name == 'لغو':
        update.message.reply_text('انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN
    else:
        index_list.append(str(name))
        update.message.reply_text('خب حالا موجودی محصول را وارد کنید:',
                    reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        print(index_list)
        return PRODUCT_STOCK

# add stock to index_list for create product
def product_stock(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    text = update.message.text
    if text == 'لغو':
        update.message.reply_text('انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN
    else:
        index_list.append(int(text))
        update.message.reply_text('خب حالا عکس محصول را بفرستید:',
                    reply_markup=ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True, resize_keyboard=True))

        print(index_list)
        return PRODUCT_IMAGE

# add image to index_list and create product
def product_image(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    text = update.message.text
    if text == 'لغو':
        update.message.reply_text('انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN
    else:
        update.message.reply_text('لطفا کمی صبرکنید تا فایل توسط بات دانلود شود')
        random_number = randint(100000000, 99999999999)
        photo = update.message.photo[-1].get_file()
        photo.download(MEDIA_ROOT+'/image/'+str(random_number)+'.jpg')
        index_list.append(str(random_number)+'.jpg')
        update.message.reply_text('دریافت شد.')
        create_product(index_list[0],index_list[1],index_list[2],index_list[3])
        index_list.clear()
        update.message.reply_text('ادمین لطفا یک گزینه را انتخاب کن:'
                    ,reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN


# end create product ===========================================================
# add update product bottom ====================================================

#get file and update and create products
def file_input(update: Update, context: CallbackContext)-> int:
    user = update.message.from_user
    text = update.message.text

    if text == 'لغو':
        update.message.reply_text('انتخاب کنید',
                    reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN

    else:
        update.message.reply_text('لطفا کمی صبرکنید تا فایل توسط بات دانلود شود')
        file_ = update.message.document.get_file()
        file_.download(MEDIA_ROOT + '/update/' + 'update.xls')
        extract_data()
        update.message.reply_text('ادمین لطفا یک گزینه را انتخاب کن:',
                        reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return ADMIN

# end update product ===========================================================
#customer bottom ===============================================================
list_a = []
list_p = []
def customer(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    if update.message.text == 'البوم':
        print('injaiim')
        album_db = Album.objects.values('name')
        album_keyboard = [['لغو']]

        for a in album_db:
            la = []
            la.append(a['name'])
            album_keyboard.append(la)

        update.message.reply_text('مشتری گرامی لطفا یک گزینه را انتخاب کنید:',
                        reply_markup=ReplyKeyboardMarkup(album_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return SEND_ALBUM

    elif update.message.text == 'محصولات':
        product_db = Product.objects.values('id')
        product_keyboard = [['لغو']]

        for i in product_db:
            lp = []
            lp.append(i['id'])
            product_keyboard.append(lp)

        update.message.reply_text('مشتری گرامی لطفا یک گزینه را انتخاب کنید:',
                        reply_markup=ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return SEND_PRODUCT

    else:

        logger.info("No match ")
        update.message.reply_text('یافت نشد.دوباره انتخاب کنید:',
                            reply_markup=ReplyKeyboardMarkup(customer_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return CUSTOMER


def send_album(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text

    if text == 'لغو':
        update.message.reply_text('لغو شد. دوباره انتخاب کنید:',
                    reply_markup=ReplyKeyboardMarkup(customer_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return CUSTOMER

    else:
        album_val = Album.objects.all()
        for alb in album_val:
            if str(alb) == text:
                gif = alb.gif
                list_a.append(str(gif))
                video = alb.video
                list_a.append(str(video))

        update.message.reply_text('انتخاب کنید:',
                    reply_markup=ReplyKeyboardMarkup(albumValue_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return SHOW_ALBUM


def show_album(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text

    if text == 'لغو':
        update.message.reply_text('لغو شد. دوباره انتخاب کنید:',
                    reply_markup=ReplyKeyboardMarkup(customer_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))
        list_a.clear()
        return CUSTOMER

    if text == 'گیف':

        update.message.reply_text('لطفا کمی صبرکنید تا فایل توسط بات فرستاده شود...')
        gif = list_a[0]
        loc = MEDIA_ROOT+'/gif/'+gif
        context.bot.sendAnimation(chat_id=update.message.chat_id, video=open(loc, 'rb'), supports_streaming=True)

        return SEND_ALBUM

    if text == 'ویدیو':

        update.message.reply_text('لطفا کمی صبرکنید تا فایل توسط بات فرستاده شود...')
        video = list_a[1]
        loc = MEDIA_ROOT+'/video/'+video
        context.bot.send_video(chat_id=update.message.chat_id, video=open(loc, 'rb'), supports_streaming=True)

        return SEND_ALBUM


def send_product(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text
    logger.info("choose of %s: %s", user.first_name, update.message.text)

    if text == 'لغو':
        update.message.reply_text('لغو شد. دوباره انتخاب کنید:',
                    reply_markup=ReplyKeyboardMarkup(customer_menu_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return CUSTOMER

    else:
        product_val = Product.objects.all()
        for pro in product_val:
            if int(pro) == text:
                name = alb.name
                list_p.append(text)
                list_p.append(str(name))
                stock = alb.stock
                list_p.append(int(stock))
                image = alb.image
                list_p.append(str(image))


        # update.message.reply_text('انتخاب کنید:',
        #             reply_markup=ReplyKeyboardMarkup(order_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return SHOW_PRODUCT


# def show_product(update: Update, context: CallbackContext) -> in:
#     pass
    # user = update.message.from_user
    # text = update.message.text
    # code = list_p[0]
    # name = list_p[1]
    # stock = list_p[2]
    # image = list_p[3]
    #
    # loc = MEDIA_ROOT + '/image/'+ image
    # context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open(loc, 'rb'))
    # update.message.reply_text(f'کد محصول :{text} \n اسم محصول:{str(name)} \n موجودی:{int(stock)}')
    # return CURTOMER

def order(update: Update, context: CallbackContext) -> int:
    pass


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))

    return ConversationHandler.END
#
# def error(update: Update, context: CallbackContext) -> int:
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update)


def main() -> None:
    updater = Updater(token='1453806194:AAEwBJPb2JS_PL0IVBs7I_2d75tWaZr7Wlo', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ADMIN:[MessageHandler(Filters.text, admin)],
            ALBUM_NAME:[MessageHandler(Filters.text, album_name)],
            PRODUCT_NAME:[MessageHandler(Filters.text, product_name)],
            PRODUCT_CODE:[MessageHandler(Filters.text, product_code)],
            PRODUCT_STOCK:[MessageHandler(Filters.text, product_stock)],
            PRODUCT_IMAGE:[MessageHandler(Filters.photo, product_image)],
            VIDEO_INPUT:[MessageHandler(Filters.video,video_input)],
            GIF_INPUT:[MessageHandler(Filters.animation,gif_input)],
            FILE_INPUT:[MessageHandler(Filters.document,file_input)],
            CUSTOMER:[MessageHandler(Filters.text, customer)],
            SEND_PRODUCT:[MessageHandler(Filters.text, send_product)],
            # SHOW_PRODUCT:[MessageHandler(Filters.text, show_product)],
            ORDER:[MessageHandler(Filters.text, order)],
            SEND_ALBUM:[MessageHandler(Filters.text, send_album)],
            SHOW_ALBUM:[MessageHandler(Filters.text, show_album)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()
