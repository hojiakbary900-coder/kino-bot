from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_ID, CHANNEL_POST
from database import add_movie, get_movie

router = Router()

waiting = {}

START_TEXT = """
╔════════════════╗
      🎬 KINO BOT
╚════════════════╝

🔍 Kino kodini yuboring 🖊
"""


@router.message(F.text == "/start")
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("📢 VIP Drama", url="https://t.me/VIP_drama_uz01")],
            [InlineKeyboardButton("📢 Dramalar Olami", url="https://t.me/Dramalar_olami_uzz")],
            [InlineKeyboardButton("📢 Daxshat Kinolar", url="https://t.me/daxshat_kinolar_uzzz")]
        ]
    )

    await message.answer(START_TEXT, reply_markup=keyboard)


@router.message(F.text == "/admin")
async def admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("⚙️ ADMIN PANEL\n/add kino qo'shish")


@router.message(F.text.startswith("/add"))
async def add(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        text = message.text.replace("/add", "").strip()
        code, name, info = text.split(",", 2)

        waiting[message.from_user.id] = {
            "code": code.strip(),
            "name": name.strip(),
            "info": info.strip()
        }

        await message.answer("🎬 Endi kino videosini yuboring")

    except:
        await message.answer("Format: /add 5, Kino nomi, Ma'lumot")


@router.message(F.video)
async def save(message: Message, bot: Bot):
    if message.from_user.id != ADMIN_ID:
        return

    if message.from_user.id not in waiting:
        return

    data = waiting.pop(message.from_user.id)
    file_id = message.video.file_id

    add_movie(data["code"], data["name"], data["info"], file_id)

    await bot.send_video(
        chat_id=CHANNEL_POST,
        video=file_id,
        caption=f"🎬 {data['name']}\n{data['info']}\nKod: {data['code']}"
    )

    await message.answer("✅ Saqlandi va kanalga yuborildi")


@router.message(F.text)
async def get_movie(message: Message):
    code = message.text.strip()

    movie = get_movie(code)
    if not movie:
        return

    _, name, info, file_id = movie

    await message.answer_video(
        video=file_id,
        caption=f"🎬 {name}\n{info}"
  )
