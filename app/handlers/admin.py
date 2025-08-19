import os 
from aiogram import Router, F
from database.models import Broadcast, User, OrderDescription
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from database.models import Broadcast, User, async_session
from app.states.group_states import BroadcastState
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import pytz
from sqlalchemy import select

load_dotenv()

admin_router = Router()

ADMIN_IDS = tuple(int(x) for x in os.getenv("ADMIN_ID").split(","))

def admin_panel_buttons(): 
    keyboard = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = "Новые заказы", callback_data = "new_orders")],
        [InlineKeyboardButton(text = "Рассылки", callback_data = "broadcast")]
    ])

    return keyboard

def back_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = "⏪ Назад", callback_data = "back_admin")]
    ])

    return keyboard

def order_nav_buttons(index: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏩ Следующий", callback_data=f"order_next_{index}")],
        [InlineKeyboardButton(text="⏪ Назад", callback_data="back_admin")]
    ])


@admin_router.message(Command("admin"))
async def admin_panel(message:  Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет доступа к этой команде!")
        return
    await message.answer("Добро пожаловать в админ-панель", reply_markup = admin_panel_buttons())
    
@admin_router.callback_query(F.data == "back_admin")
async def back_menu_admin_buttons(callback: CallbackQuery):
    await callback.message.edit_text("Админ-панель: Выберите действие", reply_markup = admin_panel_buttons())
    await callback.answer()

@admin_router.callback_query(F.data == "new_orders")
async def check_orders(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(OrderDescription).order_by(OrderDescription.created_at.desc())
        )
        orders = result.scalars().all()

    if not orders:
        await callback.message.edit_text("Заказов пока нет.", reply_markup=back_menu())
        await callback.answer()
        return

    await state.update_data(orders_ids=[o.id for o in orders], current_index=0)
    await show_order(callback, orders[0], state)

async def show_order(callback: CallbackQuery, order_description: OrderDescription, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.id == order_description.user)
        )
        user = result.scalar_one_or_none()

    moscow_tz = pytz.timezone("Europe/Moscow")
    created_at = order_description.created_at.replace(tzinfo=pytz.UTC).astimezone(moscow_tz)
    created_at_str = created_at.strftime("%d.%m.%Y %H:%M")

    text = (
        f"📢 <b>Заказ ({created_at_str})</b>\n"
        f"👤 Пользователь: {user.name} (@{user.username}) | {user.phone}\n"
        f"📂 Категория: {order_description.category}\n"
        f"📦 Пакет: {order_description.package}\n"
        f"📝 Описание: {order_description.description}"
    )

    data = await state.get_data()
    index = data.get("current_index", 0)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=order_nav_buttons(index))
    await callback.answer()

@admin_router.callback_query(F.data.startswith("order_next_"))
async def next_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    orders_ids = data.get("orders_ids", [])
    current_index = data.get("current_index", 0) + 1

    if current_index >= len(orders_ids):
        await callback.message.edit_text("Новых заказов больше нет.", reply_markup=back_menu())
        await callback.answer()
        return

    async with async_session() as session:
        result = await session.execute(
            select(OrderDescription).where(OrderDescription.id == orders_ids[current_index])
        )
        order_description = result.scalar_one_or_none()

    await state.update_data(current_index=current_index)
    await show_order(callback, order_description, state)

@admin_router.callback_query(F.data == "broadcast")
async def process_broadcast(callblack: CallbackQuery, state: FSMContext):
    await callblack.message.edit_text("Введите текст для рассылки:", reply_markup = back_menu())
    await state.set_state(BroadcastState.waiting_for_broadcast_text)
    await callblack.answer()


@admin_router.message(BroadcastState.waiting_for_broadcast_text)
async def handle_broadcast_text(message: Message, state: FSMContext):
    broadcast_text = message.text
    count = 0

    async with async_session() as session:
        result = await session.execute(
            select(User)
        )
        users_list = result.scalars().all()

        for user in users_list:
            try:
                await message.bot.send_message(user.tg_id, broadcast_text)
                count += 1
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user.tg_id}: {e}")

        new_broadcast = Broadcast(message=broadcast_text)
        session.add(new_broadcast)
        await session.commit()

    await message.answer(f"Рассылка завершена! Сообщение отправлено {count} пользователям.")
    await state.clear()

