from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
import sqlite3
import time

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

# token file
with open("tokenfile.txt","r") as tf:
    tokenfile = tf.read()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        text="sadece /hepsi ve /hangisi komutlarini kullanabilirsiniz")


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_caps)


async def hepsi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if q_result := c.execute(
            "SELECT query, datetime(TIME, 'unixepoch', 'localtime') TIME, min(price) price, link FROM prices WHERE TIME =  (SELECT max(TIME) FROM prices) GROUP BY query, TIME;"
    ).fetchall():
        timestamp = q_result[0][1]
        result_str = f"{timestamp} tarihindeki en uygun fiyatlar:\n\n"
        result_str += '\n'.join([
            f"{row[0]} ( {row[2]} TL ) <a href='{row[3]}'>{row[3].split('/')[0]}</a>"
            for row in q_result
        ])
        upmsg = update.message or update.edited_message
        if not c.execute(  # if user not in db
                f"select exists (select 1 from users where user_id  = {upmsg.chat.id});"
        ).fetchall()[0][0]:
            c.execute(
                f"INSERT INTO users VALUES ('{upmsg.chat.first_name}' , {upmsg.chat.id}, '{upmsg.chat.last_name}', {time.time()} );"
            )
        c.execute(
            f"INSERT INTO usage VALUES({upmsg.chat.id}, '{upmsg.text}',  {time.time()})"
        )
        conn.commit()
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=result_str,
                                       parse_mode='HTML',
                                       disable_web_page_preview=True)
    else:
        result_str = "No results found"
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=result_str)


async def hangisi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the possible options
    options = [
        "Radeon RX 7900 XTX", "Radeon RX 7900 XT", "Radeon RX 6950 XT",
        "Radeon RX 6900 XT", "Radeon RX 6800 XT", "Radeon RX 6800",
        "Radeon RX 6750 XT", "Radeon RX 6700 XT", "Radeon RX 6700",
        "Radeon RX 6650 XT", "Radeon RX 6600 XT", "Radeon RX 6600",
        "Radeon RX 6500 XT", "GeForce RTX 4090", "GeForce RTX 4080",
        "GeForce RTX 4070 Ti", "GeForce RTX 3090 Ti", "GeForce RTX 3090",
        "GeForce RTX 3080 Ti", "GeForce RTX 3080", "GeForce RTX 3070 Ti",
        "GeForce RTX 3070", "GeForce RTX 3060", "GeForce RTX 3050"
    ]

    # Create the button list
    button_list = [InlineKeyboardButton(x, callback_data=x) for x in options]

    # Create the keyboard markup
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

    # Send the message with the keyboard markup
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text='Ekran Karti Seç:',
                                   reply_markup=reply_markup)


async def hangisi_selection(update: Update, context: CallbackContext):
    query_name = update.callback_query.data
    if q_result := c.execute(
            "SELECT query, datetime(time, 'unixepoch', 'localtime') time, price, link FROM prices WHERE TIME = (SELECT max(TIME) FROM prices) and query = ?;",
        (query_name, ),
    ).fetchall():
        if not c.execute(  # add if user not in db 
                f"select exists (select 1 from users where user_id  = {update.effective_user.id});"
        ).fetchall()[0][0]:
            c.execute(
                f"INSERT INTO users VALUES ('{update.effective_user.first_name}' , {update.effective_user.id}, '{update.effective_user.last_name}', {time.time()} );"
            )
        c.execute(
            f"INSERT INTO usage VALUES({update.effective_user.id}, '/hangisi',  {time.time()})"
        )
        conn.commit()
        timestamp = q_result[0][1]
        # Construct the result string with the timestamp only at the beginning
        result_str = f"{timestamp} tarihindeki en uygun fiyatlar:\n\n"
        result_str += '\n'.join([
            f"{row[0]} ( {row[2]} TL ) <a href='{row[3]}'>{row[3].split('/')[0]}</a>"
            for row in q_result
        ])
        # Set the parse_mode parameter to 'HTML'
        await context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text=result_str,
            parse_mode='HTML',
            disable_web_page_preview=True)
    else:
        result_str = "No results found"
        await context.bot.send_message(
            chat_id=update.callback_query.message.chat_id, text=result_str)


# Helper function to build the button menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="boyle bir komut yok, sadece /hepsi ve /hangisi kullanilabilir")


if __name__ == '__main__':
    application = ApplicationBuilder().token(tokenfile).build()

    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    hepsi_handler = MessageHandler(filters.Regex(r'^/hepsi($|\s)'), hepsi)
    hangisi_handler = CommandHandler('hangisi', hangisi)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    

    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(hepsi_handler)
    application.add_handler(hangisi_handler)
    application.add_handler(CallbackQueryHandler(hangisi_selection))
    application.add_handler(unknown_handler)

    application.run_polling()
