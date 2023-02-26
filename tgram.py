import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler, CallbackContext, CallbackQueryHandler
import sqlite3

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="/hepsi ve /hangisi komutlarini kullanabilirsiniz")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_caps)


async def hepsi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q_result = c.execute(
        "SELECT query, datetime(TIME, 'unixepoch', 'localtime') TIME, min(price) price, link FROM prices WHERE TIME =  (SELECT max(TIME) FROM prices) GROUP BY query, TIME;"
    )
    result_str = '\n'.join(
        [f"{row[0]} - {row[2]} - {row[3]}" for row in q_result])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=result_str)


async def hangisi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the possible options
    options = [
        "Radeon RX 7900 XTX", "Radeon RX 7900 XT", "Radeon RX 6950 XT",
        "Radeon RX 6900 XT", "Radeon RX 6800 XT", "Radeon RX 6800",
        "Radeon RX 6750 XT", "Radeon RX 6700 XT", "Radeon RX 6700",
        "Radeon RX 6650 XT", "Radeon RX 6600 XT", "Radeon RX 6600",
        "Radeon RX 6500 XT", "GeForce RTX 3090 Ti", "GeForce RTX 3090",
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
        (query_name,),
    ).fetchall():
        timestamp = q_result[0][1]
        # Construct the result string with the timestamp only at the beginning
        result_str = f"{timestamp} tarihindeki fiyatlar:\n\n"
        result_str += '\n'.join(
            [f"{row[0]} - {row[2]} - {row[3]}" for row in q_result])
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


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper()),
        )
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(
        '6032820125:AAFg7K4LSMxPnFx0eSlahfGQynD62hXXZzE').build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    hepsi_handler = CommandHandler('hepsi', hepsi)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    hangisi_handler = CommandHandler('hangisi',
                                             hangisi)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(hepsi_handler)
    application.add_handler(hangisi_handler)  
    application.add_handler(
        CallbackQueryHandler(hangisi_selection))
    application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
