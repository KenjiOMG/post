import os
import logging
import bot.constants as con
from typing import Dict

from telegram import (
    Update,
    ParseMode,
    BotCommand,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def facts_to_str(user_data: Dict[str, str]):
    nombre = user_data['nombre']
    categoria = user_data['categoria']
    plataforma = user_data['plataforma']
    peso = user_data['peso']
    vercion = user_data['vercion']
    partes = user_data['partes']
    argumento = user_data['argumento']
    return (
        f'βοΈ<b>{nombre}βοΈ</b>\n\nποΈ <b>CategorΓ­a:</b> {categoria}\nβοΈ <b>Plataforma:</b> {plataforma}\n'
        f'π¦ <b>Peso:</b> {peso}\nπ§Ύ <b>VersiΓ³n:</b> {vercion}\nποΈ <b>Partes:</b> {partes}\n\n'
        f'π <b>Argumento:</b> {argumento}\n\nπ€'
        '<b>Subido por:</b> <a href="tg://user?id={user}">{name}</a>\n'
        'βββββββββββββββββββββββ\nβ°οΈ <a href="https://t.me/minecraftxoficial"><b>X Minecraft</b></a> β°οΈ'
    )


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if user_id in con.administradores:
        update.message.reply_text(
            text=f'Hola <a href="tg://user?id={user_id}">{first_name}</a>\nPulsa /comenzar para generar una plantilla.',
            parse_mode=ParseMode.HTML
            )
        context.bot.set_my_commands([
            BotCommand(command='comenzar', description='Generar una plantilla.'),
            BotCommand(command='cancelar', description='Detener el proceso actual.')
            ]
        )
    else:
        update.message.reply_text(
            text=f'<a href="tg://user?id={user_id}">{first_name}</a> no tienes acceso para usar este bot.',
            parse_mode=ParseMode.HTML
            )


def comenzar(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        update.message.reply_text(
            "Enviame la imagen de la plantilla.",
            )
        return con.PHOTO


def photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('bot/photo/{}.jpg'.format(update.message.chat_id))
    update.message.reply_text(
        'Enviame el nombre del archivo.'
    )
    return con.NOMBRE


def nombre(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['nombre'] = text
    update.message.reply_text(
        f'Enviame la categorΓ­a #Mods #Shader #Mapa #PackTextura #Server #ModsPack.'
    )
    return con.CATEGORIA


def categoria(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['categoria'] = text
    update.message.reply_text(
        f'Enviame la plataforma #PC #Android.'
    )
    return con.PLATAFORMA


def plataforma(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['plataforma'] = text
    update.message.reply_text(
        f'Enviame el peso del archivo.'
    )
    return con.PESO


def peso(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['peso'] = text
    update.message.reply_text(
        f'Enviame la verciΓ³n del Minecraft el cual es compatible.'
    )
    return con.VERCION


def vercion(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['vercion'] = text
    update.message.reply_text(
        f'Enviame la cantidad de Archivos.'
    )
    return con.PARTES


def partes(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['partes'] = text
    update.message.reply_text(
        f'Enviame la descripciΓ³n.'
    )
    return con.ARGUMENTO


def argumento(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['argumento'] = text

    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    update.message.reply_text(
        text=f"β Plantilla creada correctamente\n<b>Resultado:</b>\n\n{facts_to_str(context.user_data)}".format(user=user_id, name=first_name) +
            "\n\nPulsa el botΓ³n de debajo para enviar la plantilla. π’",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup([['Enviar plantilla β']],
            one_time_keyboard=True,
            resize_keyboard=True
            )
        )
    return con.SEND


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name


    context.bot.send_photo(
        chat_id=con.CHANNEL,
        photo=open(f'bot/photo/{update.message.chat_id}.jpg', 'rb'),
        caption=f'{facts_to_str(user_data)}'.format(user=user_id, name=first_name),
        parse_mode=ParseMode.HTML,
    )
    user_data.clear()
    return ConversationHandler.END


def stop(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        update.message.reply_text(
            text='OperaciΓ³n cancelada.',
            reply_markup=ReplyKeyboardRemove(selective=True)
        )
        return ConversationHandler.END

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('comenzar', comenzar)],
        states={
            con.PHOTO: [
                MessageHandler(Filters.photo, photo),
            ],
            con.NOMBRE: [
                MessageHandler(Filters.text, nombre)
            ],
            con.CATEGORIA: [
                MessageHandler(Filters.text, categoria)
            ],
            con.PLATAFORMA: [
                MessageHandler(Filters.text, plataforma)
            ],
            con.PESO: [
                MessageHandler(Filters.text, peso)
            ],
            con.VERCION: [
                MessageHandler(Filters.text, vercion)
            ],
            con.PARTES: [
                MessageHandler(Filters.text, partes),
            ],
            con.ARGUMENTO: [
                MessageHandler(Filters.text, argumento),
            ],
            con.SEND: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Enviar plantilla β$')), done),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('^Enviar plantilla β$'), done),
            CommandHandler('cancelar', stop),
            ],
        allow_reentry=True
    )
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
