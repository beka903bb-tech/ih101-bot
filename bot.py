import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "8670727342:AAHmeh5Qgs_tbiDAviiOyUoYfJ2ysVaVwtE")

# 20 ta savol - IH101 Isitish tizimlari mavzusida
QUESTIONS = [
    {
        "q": "Isitish tizimlarini oquvchanligi (suyuqlik shakli)ga ko'ra necha turga bo'lish mumkin?",
        "options": ["Uch turga", "To'rt turga", "Ikki turga", "Besh turga"],
        "answer": 2,
        "explanation": "Isitish tizimlarini oquvchanligi (suyuqlik shakli)ga ko'ra ikki turga bo'lish mumkin: suv bilan isitish va havo orqali isitish."
    },
    {
        "q": "Havo bilan isitish qaysi tizim orqali bajariladi?",
        "options": ["Radiatorli tizim", "Kondisioner tizimi", "Yerdan isitish", "Fankoyl tizimi"],
        "answer": 1,
        "explanation": "Havo bilan isitish kondisioner tizimlari orqali bajariladi. Suv bilan isitish esa radiatorli, fankoyl, konvektorli va yerdan isitish shaklida amalga oshirilishi mumkin."
    },
    {
        "q": "Qozonxonalar nima vazifasini bajaradi?",
        "options": [
            "Faqat suvni saqlash",
            "Kimyoviy energiyani issiqlik energiyasiga aylantiradi va tashuvchi suyuqlikka o'tkazadi",
            "Havoni tozalash",
            "Bosimni kamaytirish"
        ],
        "answer": 1,
        "explanation": "Qozonxonalar yoqilg'ining kimyoviy energiyasini yonish orqali issiqlik energiyasiga aylantiradi va bu energiyani tashuvchi suyuqlikka o'tkazadigan mashinalardır."
    },
    {
        "q": "Juft qozonli tizimlarda balanslash idishida nima mavjud?",
        "options": ["Dumaloq teshik", "Teshikli devor (list)", "Spiral nay", "Elektr isitgich"],
        "answer": 1,
        "explanation": "Juft qozonli tizimlarda ishlatiladigan balanslash idishi ichida teshikli devor (list) mavjud. Bu devor orqali suvdagi zarrachali loy va iflos moddalar to'planadi."
    },
    {
        "q": "Kondensasiya qozonlarining drenaji qayerga ulanmasligi kerak?",
        "options": [
            "To'g'ridan-to'g'ri chiqindi suv quvuriga",
            "Kengayish bakiga",
            "Filtrga",
            "Sifoniga"
        ],
        "answer": 0,
        "explanation": "Kondensasiya qozonlarining drenaji to'g'ridan-to'g'ri chiqindi suv quvuriga ulanmasligi kerak, chunki kanalizatsiyadan chiqadigan metan gazi portlashga olib kelishi mumkin. Sifon 40 sm balandlikda o'rnatilishi kerak."
    },
    {
        "q": "Isitish tizimiga suvni to'ldirish uchun qayerga to'ldirish krani o'rnatilishi kerak?",
        "options": [
            "Radiatorga",
            "Sifoniga",
            "Sirkulyasiya nasosining so'rg'ich kollektoriga isitish suvini to'ldirish kraniga",
            "Kengayish bakiga"
        ],
        "answer": 2,
        "explanation": "Isitish tizimiga suvni to'ldirish uchun sirkulyasiya nasosining so'rg'ich kollektoriga isitish suvini to'ldirish krani o'rnatilishi kerak. To'ldirish krani qozonga o'rnatilmasligi kerak."
    },
    {
        "q": "To'ldirish liniyasining o'lchami qanday bo'lishi kerak?",
        "options": ["1/8\" yoki 1/4\"", "1/2\" yoki 3/4\"", "1\" yoki 1.5\"", "2\" yoki 3\""],
        "answer": 1,
        "explanation": "To'ldirish liniyasining o'lchami 1/2\" yoki 3/4\" bo'lishi kerak. Nasosning so'rg'ichlarida filtr bo'lmasa, to'ldirish liniyasiga 11/4\" o'lchamidagi filtr qo'yilishi kerak."
    },
    {
        "q": "Yagona qozon tizimida isitish qozonining kirish va chiqish joylarida nima o'rnatilmasligi kerak?",
        "options": ["Termometr", "Manometr", "Ventel (kran)", "Filtr"],
        "answer": 2,
        "explanation": "Yagona qozon tizimida isitish qozonining kirish va chiqish joylarida ventel (kran)lar o'rnatilmasligi kerak, chunki qozonga kran o'rnatilganda, kran qadog'idan oqishi mumkin bo'lgan suv qozon izolyasiyasini buzadi."
    },
    {
        "q": "Xavfsizlik klapanining chiqishi qayerga tushirilishi kerak?",
        "options": [
            "Kanalizatsiyaga to'g'ridan-to'g'ri",
            "Bir xil diametrli quvur bilan yerdan 10 sm yuqoriga (perimetr kanaliga)",
            "Kengayish bakiga",
            "Sifoniga"
        ],
        "answer": 1,
        "explanation": "Xavfsizlik klapanining chiqishi bir xil diametrli quvur bilan yerdan 10 sm yuqoriga (perimetr kanaliga) tushirilishi kerak. Shu yo'l bilan xavfsizlik klapani suvni to'kish paytida atrofdagi izolyatsiyaga ta'sir qilmaydi."
    },
    {
        "q": "Avtomatik havo chiqarib yuboruvchi moslamaning tiqinini qanday qo'yilishi lozim?",
        "options": ["Mahkam yopilgan", "Ozgina bo'sh", "Butunlay olib tashlanishi kerak", "Vintli qilib"],
        "answer": 1,
        "explanation": "Avtomatik havo chiqarib yuboruvchi moslamaning tiqinini ozgina bo'sh qo'yilishi lozim. Qattiq yopilgan bo'lsa havo chiqara olmasligi mumkin."
    },
    {
        "q": "Gidromert va manometrdan oldin nima o'rnatilishi kerak?",
        "options": ["Filtr", "Kengayish baki", "Ventel (manometr krani)", "Sirkulyasiya nasosi"],
        "answer": 2,
        "explanation": "Gidromert va manometrdan oldin ventel (manometr krani) o'rnatilishi kerak."
    },
    {
        "q": "Isitish moslamasida ishlatiladigan fitting materiallari qanday bo'lishi kerak?",
        "options": [
            "Faqat plastikdan bo'lishi kerak",
            "Tegishli milliy standartlarga muvofiq sifatli va mustahkam bo'lishi kerak",
            "Faqat mis materialdan bo'lishi kerak",
            "Har qanday material bo'lishi mumkin"
        ],
        "answer": 1,
        "explanation": "Isitish moslamasida ishlatiladigan fitting materiallari tegishli milliy standartlarga muvofiq sifatli va mustahkam bo'lishi kerak, yoki milliy standart bo'lmasa, xalqaro standartlarga amal qilinishi zarur."
    },
    {
        "q": "Barcha isitish moslamalari nimaning minimal nazoratiga ega bo'lishi kerak?",
        "options": ["Havo bosimi", "Suv sathi", "Harorat", "Elektr quvvati"],
        "answer": 1,
        "explanation": "Barcha isitish moslamalari suv sathining minimal nazoratiga ega bo'lishi kerak."
    },
    {
        "q": "Isitish qozonlarida xavfsizlik klapanini qozondan qancha masofada o'rnatish kerak?",
        "options": ["Maksimal 5 m", "Maksimal 2 m", "Maksimal 10 m", "Istalgan masofada"],
        "answer": 1,
        "explanation": "Isitish qozonlarida xavfsizlik klapanini qozonga yaqin joyda o'rnatish kerak (maksimal 2 m)."
    },
    {
        "q": "Ustun quvurlari cho'zilish yuqori bo'lgan joylarda qancha atrofida bo'lishi kerak?",
        "options": ["1–1.5 m", "2–2.5 m", "3–4 m", "5 m"],
        "answer": 1,
        "explanation": "Ustun quvurlari cho'zilish yuqori bo'lgan joylarda 2–2.5 m atrofida bo'lishi kerak."
    },
    {
        "q": "Radiatör ustun quvurlari ulanishlari qanday bo'lishi kerak?",
        "options": [
            "To'g'ri burchakli",
            "S ni hosil qilish uchun bo'g'inli",
            "Parallel",
            "Spiral shaklida"
        ],
        "answer": 1,
        "explanation": "Radiatör ustun quvurlari ulanishlari S ni hosil qilish uchun bo'g'inli bo'lishi kerak. Aks holda, ventel yoki biriktiruvchi nuqtada sinishlar sodir bo'lishi mumkin."
    },
    {
        "q": "Ustunlardagi qavat o'tishlarida nimadan foydalanish kerak?",
        "options": ["Kengayish baki", "Uya", "Filtr", "Manometr"],
        "answer": 1,
        "explanation": "Ustunlardagi qavat o'tishlarida uyadan foydalanish kerak. Devor isitish ustunining 1-2 sm masofada tugashi kerak va ular orasi suvoq bilan to'ldirish kerak."
    },
    {
        "q": "Xavfsizlik klapanlari ishga tushirishdan oldin qanday sozlanishi kerak?",
        "options": [
            "Qurilish maydonchalarida sozlanadi",
            "Ish bosimiga qarab maxsus sozlanib yetkazib berilishi kerak",
            "Sozlash shart emas",
            "Foydalanuvchi o'zi sozlaydi"
        ],
        "answer": 1,
        "explanation": "Xavfsizlik klaplanlari ish bosimiga qarab maxsus sozlanib yetkazib berilishi kerak. Aks holda, qurilish maydonchalarida xavfsizlik klaplanlari sozlanadi va bu istalmaganba xtsiz hodisalarga olib keladi."
    },
    {
        "q": "Bosimni pasaytirish montaj ishlarida balanslash idishi qanday o'rnatilishi kerak?",
        "options": [
            "Vertikal quvur o'qiga",
            "Gorizontal quvur o'qiga",
            "45 darajali burchakda",
            "Istalgan holatda"
        ],
        "answer": 1,
        "explanation": "Bosimni pasaytirish montaj ishlarida balanslash idishi gorizontal quvur o'qiga o'rnatilishi kerak."
    },
    {
        "q": "Sovuq hududlarda qish oylarida isitish moslamasining suv sinovini o'tkazgandan so'ng nima qilish kerak?",
        "options": [
            "Hech narsa qilmasa ham bo'ladi",
            "Suvni to'ldirish yetarli",
            "Radiatorlarning pastki qismlarida qolgan suvni to'liq bo'shatish kerak",
            "Faqat qozonni o'chirish kerak"
        ],
        "answer": 2,
        "explanation": "Sovuq hududlarda qish oylarida isitish moslamasining suv sinovini o'tkazgandan so'ng, qozondan (ayniqsa, derazalar o'rnatilmagan bo'lsa) qurilma suvini to'kish yetarli bo'lmaydi. Radiatorlarning pastki qismlarida qolgan suv radiatorlarni olib tashlash orqali to'liq bo'shatilishi kerak."
    },
]

# Foydalanuvchi holati
user_data = {}

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "current": 0,
            "score": 0,
            "wrong_answers": []
        }
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"current": 0, "score": 0, "wrong_answers": []}
    
    await update.message.reply_text(
        "🔥 *IH101 - Isitish Tizimlari Testi*\n\n"
        "Salom! Bu test IH101 - Isitish tizimlarida sifat nazoratiга oid.\n\n"
        "📋 *20 ta savol* sizni kutmoqda.\n"
        "✅ Har bir to'g'ri javob uchun 1 ball.\n"
        "❌ Noto'g'ri javoblar oxirida tushuntiriladi.\n\n"
        "Boshlash uchun /test buyrug'ini yuboring.",
        parse_mode="Markdown"
    )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"current": 0, "score": 0, "wrong_answers": []}
    await send_question(update.message, user_id)

async def send_question(message, user_id):
    ud = get_user(user_id)
    idx = ud["current"]
    
    if idx >= len(QUESTIONS):
        await show_results(message, user_id)
        return
    
    q = QUESTIONS[idx]
    keyboard = [
        [InlineKeyboardButton(f"{chr(65+i)}) {opt}", callback_data=f"ans_{i}")]
        for i, opt in enumerate(q["options"])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(
        f"📝 *Savol {idx+1}/20*\n\n{q['q']}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    ud = get_user(user_id)
    idx = ud["current"]
    
    if idx >= len(QUESTIONS):
        return
    
    q = QUESTIONS[idx]
    chosen = int(query.data.split("_")[1])
    correct = q["answer"]
    
    if chosen == correct:
        ud["score"] += 1
        result_text = f"✅ *To'g'ri!*\n\n_{q['options'][correct]}_"
    else:
        ud["wrong_answers"].append({
            "num": idx + 1,
            "question": q["q"],
            "your_answer": q["options"][chosen],
            "correct_answer": q["options"][correct],
            "explanation": q["explanation"]
        })
        result_text = (
            f"❌ *Noto'g'ri!*\n\n"
            f"Siz tanladingiz: _{q['options'][chosen]}_\n"
            f"To'g'ri javob: _{q['options'][correct]}_"
        )
    
    ud["current"] += 1
    
    # Eski savolni o'chirish va natijani ko'rsatish
    await query.edit_message_text(
        f"📝 *Savol {idx+1}/20*\n\n{q['q']}\n\n{result_text}",
        parse_mode="Markdown"
    )
    
    # Keyingi savol
    if ud["current"] < len(QUESTIONS):
        next_q = QUESTIONS[ud["current"]]
        keyboard = [
            [InlineKeyboardButton(f"{chr(65+i)}) {opt}", callback_data=f"ans_{i}")]
            for i, opt in enumerate(next_q["options"])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            f"📝 *Savol {ud['current']+1}/20*\n\n{next_q['q']}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await show_results_callback(query, user_id)

async def show_results_callback(query, user_id):
    ud = get_user(user_id)
    score = ud["score"]
    total = len(QUESTIONS)
    wrong = ud["wrong_answers"]
    
    # Baho
    percent = (score / total) * 100
    if percent >= 90:
        grade = "🏆 A'lo (5)"
    elif percent >= 70:
        grade = "👍 Yaxshi (4)"
    elif percent >= 50:
        grade = "📚 Qoniqarli (3)"
    else:
        grade = "❗ Qoniqarsiz (2)"
    
    result_msg = (
        f"🎯 *Test yakunlandi!*\n\n"
        f"✅ To'g'ri javoblar: *{score}/{total}*\n"
        f"📊 Foiz: *{percent:.0f}%*\n"
        f"🏅 Baho: *{grade}*\n"
    )
    
    await query.message.reply_text(result_msg, parse_mode="Markdown")
    
    # Noto'g'ri javoblar tahlili
    if wrong:
        await query.message.reply_text(
            "📖 *Noto'g'ri javoblaringiz tahlili:*\n"
            "─────────────────────",
            parse_mode="Markdown"
        )
        
        for w in wrong:
            detail = (
                f"❓ *Savol {w['num']}:* {w['question']}\n\n"
                f"❌ Sizning javobingiz: _{w['your_answer']}_\n"
                f"✅ To'g'ri javob: _{w['correct_answer']}_\n\n"
                f"💡 *Tushuntirish:* {w['explanation']}\n"
                f"─────────────────────"
            )
            await query.message.reply_text(detail, parse_mode="Markdown")
    else:
        await query.message.reply_text(
            "🎉 *Barcha savollarga to'g'ri javob berdingiz! Ajoyib!*",
            parse_mode="Markdown"
        )
    
    await query.message.reply_text(
        "🔄 Qayta test topshirish uchun /test buyrug'ini yuboring.",
        parse_mode="Markdown"
    )

async def show_results(message, user_id):
    ud = get_user(user_id)
    score = ud["score"]
    await message.reply_text(f"Test tugadi! Natija: {score}/20")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^ans_"))
    
    print("✅ IH101 Test boti ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()