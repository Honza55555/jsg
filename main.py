import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

# ————— konfigurace —————
TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL = "https://<TVOJE-SLUG>.onrender.com"  # nahraď svým slugem
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"
PORT = int(os.environ.get("PORT", 10000))
# —————————————————————————

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()


# úvodní /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_cz = (
        "☕️ Vítejte v Coffee Perk!\n"
        "Těší nás, že jste tu. 🌟\n"
        "Prosím, vyberte si jazyk. 🗣️"
    )
    text_en = (
        "☕️ Welcome to Coffee Perk!\n"
        "We’re happy to see you here. 🌟\n"
        "Please choose your language. 🗣️"
    )
    keyboard = [
        [
            InlineKeyboardButton("🇨🇿 Čeština", callback_data="lang_cz"),
            InlineKeyboardButton("🌍 English", callback_data="lang_en"),
        ]
    ]
    await update.message.reply_text(
        f"{text_cz}\n\n{text_en}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# všechna callback data vyřešíme v jednom handleru
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data

    # po výběru jazyka ukážeme hlavní nabídku
    if data in ("lang_cz", "lang_en"):
        cz = data == "lang_cz"
        if cz:
            text = "Na co se mě můžeš zeptat:"
            buttons = [
                ("🧾 Menu a nabídka", "menu_cz"),
                ("🕐 Otevírací doba", "hours_cz"),
                ("📍 Kde nás najdete", "loc_cz"),
                ("📞 Kontakt / Rezervace", "contact_cz"),
                ("📦 Předobjednávka (již brzy)", "preorder_cz"),
                ("😎 Důvody, proč si zajít na kávu", "reasons_cz"),
            ]
        else:
            text = "What can you ask me:"
            buttons = [
                ("🧾 Menu & Offers", "menu_en"),
                ("🕐 Opening Hours", "hours_en"),
                ("📍 Location", "loc_en"),
                ("📞 Contact / Reservation", "contact_en"),
                ("📦 Pre-order (coming soon)", "preorder_en"),
                ("😎 Reasons for coffee", "reasons_en"),
            ]
        keyboard = [
            [InlineKeyboardButton(lbl, callback_data=cb)] for lbl, cb in buttons
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # jednotlivé sekce
    texts = {
        "menu_cz": (
            "🥐 COFFEE PERK MENU ☕️\n"
            "U nás nejde jen o kafe. Je to malý rituál. Je to nálada. Je to... láska v šálku. 💘\n\n"
            "☕ Výběrová káva\n"
            "🍳 Snídaně (lehké i pořádné)\n"
            "🍰 Domácí dorty\n"
            "🥗 Brunch a saláty\n\n"
            "📄 Kompletní menu:\n"
            "👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
            "Ať už si dáte espresso, matchu nebo zázvorovku – tady to chutná líp. 💛"
        ),
        "hours_cz": (
            "🕐 KDY MÁME OTEVŘENO?\n\n"
            "📅 Pondělí–Pátek: 7:30 – 17:00\n"
            "📅 Sobota & Neděle: ZAVŘENO\n\n"
            "Chcete nás navštívit? Jsme tu každý všední den od brzkého rána.\n"
            "Těšíme se na vás! ☕"
        ),
        "loc_cz": (
            "📍 KDE NÁS NAJDETE?\n\n"
            "🏠 Vyskočilova 1100/2, Praha 4\n"
            "🗺️ Mapa: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
            "Najdete nás snadno – stylová kavárna, příjemná atmosféra a lidi, co kávu berou vážně i s úsměvem.\n"
            "Zastavte se. Na chvilku nebo na celý den."
        ),
        "contact_cz": (
            "📞 KONTAKTUJTE NÁS\n\n"
            "📬 E-mail: info@coffeeperk.cz\n"
            "📞 Telefon: +420 725 422 518\n\n"
            "Rádi vám pomůžeme s rezervací, odpovíme na vaše dotazy nebo poradíme s výběrem.\n"
            "Neváhejte se nám ozvat – jsme tu pro vás."
        ),
        "preorder_cz": (
            "📦 PŘEDOBJEDNÁVKY\n\n"
            "Brzy spustíme možnost objednat si kávu a snídani předem přes Telegram.\n"
            "Zatím nás navštivte osobně – těšíme se! ☕️"
        ),
        "reasons_cz": (
            "😎 DŮVODY, PROČ SI ZAJÍT NA KÁVU\n\n"
            "☕ Protože svět se lépe řeší s kofeinem.\n"
            "📚 Protože práce počká – espresso ne.\n"
            "💬 Protože dobrá konverzace začíná u šálku.\n"
            "👀 Protože dnes jste už skoro byli produktivní.\n"
            "🧠 Protože mozek startuje až po druhé kávě.\n"
            "🌦️ Protože venku prší... nebo svítí slunce... nebo prostě cítíte, že je čas.\n\n"
            "A někdy netřeba důvod. Prostě jen přijďte. 💛"
        ),

        "menu_en": (
            "🥐 COFFEE PERK MENU ☕️\n"
            "It’s not just coffee here. It’s a little ritual, a mood, a... love in a cup. 💘\n\n"
            "☕ Specialty coffee\n"
            "🍳 Breakfast (light & hearty)\n"
            "🍰 Homemade cakes\n"
            "🥗 Brunch & salads\n\n"
            "📄 Full menu:\n"
            "👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
            "Whether you choose an espresso, matcha, or ginger tea – it tastes better here. 💛"
        ),
        "hours_en": (
            "🕐 OPENING HOURS\n\n"
            "📅 Mon–Fri: 7:30 AM – 5:00 PM\n"
            "📅 Sat & Sun: CLOSED\n\n"
            "Come visit us any weekday morning. We’re looking forward to serving you! ☕"
        ),
        "loc_en": (
            "📍 WHERE TO FIND US\n\n"
            "🏠 Vyskočilova 1100/2, Prague 4\n"
            "🗺️ Map: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
            "Our stylish café, cozy atmosphere, and smiling baristas await you.\n"
            "Stop by for a moment or stay all day."
        ),
        "contact_en": (
            "📞 CONTACT US\n\n"
            "📬 Email: info@coffeeperk.cz\n"
            "📞 Phone: +420 725 422 518\n\n"
            "We’re happy to help with reservations, answer questions, or advise on your order.\n"
            "Don’t hesitate to reach out – we’re here for you."
        ),
        "preorder_en": (
            "📦 PRE-ORDERS\n\n"
            "Soon you’ll be able to pre-order coffee and breakfast via Telegram.\n"
            "For now, please visit us in person – see you soon! ☕️"
        ),
        "reasons_en": (
            "😎 REASONS FOR COFFEE\n\n"
            "☕ Because the world is better solved with caffeine.\n"
            "📚 Because work can wait – espresso can’t.\n"
            "💬 Because good conversations start over a cup.\n"
            "👀 Because you’ve almost been productive today.\n"
            "🧠 Because your brain really fires up after that second cup.\n"
            "🌦️ Because it’s raining... or sunny... or you just feel it’s time.\n\n"
            "And sometimes no reason is needed. Just come. 💛"
        ),
    }

    if data in texts:
        await q.edit_message_text(texts[data])
        return


# zaregistrujeme handlery
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(on_callback))


# Flask webhook endpoint
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return "ok"


if __name__ == "__main__":
    asyncio.run(bot_app.bot.set_webhook(url=WEBHOOK_URL))
    app.run(host="0.0.0.0", port=PORT)
