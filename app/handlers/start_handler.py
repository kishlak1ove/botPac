from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import app.keyboards.inline as kb_inline
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from app.states.group_states import RegUser, OrderPackage
from database.models import async_session, User, OrderDescription, PackagePrice
from sqlalchemy import select
import re

start_router = Router() 

@start_router.message(CommandStart())   
async def cmd_start(message: Message):
    await message.answer("<b>Здравствуйте!</b>", parse_mode="HTML")
    await message.answer_photo(
        photo = "https://vk.com/photo-174465574_457239705",
        caption = "<b>Чтобы вы хотели узнать?</b>",
        reply_markup = kb_inline.points_start,
        parse_mode = "HTML"
    )


@start_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "За помощью с ботом пишите @ZfrOmbrazuliaV",
        reply_markup= kb_inline.back_to_start_kb
    )

@start_router.callback_query(F.data == "back_to_start_menu")
async def back_to_start(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        photo = "https://vk.com/photo-174465574_457239705",
        caption = "<b>Чтобы вы хотели узнать?</b>",
        reply_markup = kb_inline.points_start,
        parse_mode = "HTML"
    )
    await callback_query.answer()

@start_router.message(Command("registration"))
async def reg_user_start(message: Message, state: FSMContext):
    await state.set_state(RegUser.name)
    await message.answer("Введите своё ФИО | Пример: Иванов Иван Иванович")

@start_router.message(RegUser.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(RegUser.phone)
    await message.answer("Введите ваш номер телефона в формате +79528125252:")

@start_router.message(RegUser.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not phone.startswith("+") or not phone[1:].isdigit():
        await message.answer("Неверный формат")
        return

    await state.update_data(phone=phone)
    await state.set_state(RegUser.username)
    await message.answer("Введите ваш Telegram username (без @). Пример: my_username")

def is_valid_username(username: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_]{4,31}$", username))

@start_router.message(RegUser.username)
async def get_username(message: Message, state: FSMContext):
    raw_username = message.text.strip()

    if not is_valid_username(raw_username):
        await message.answer("Неверный формат username")
        return

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    tg_id = message.from_user.id

    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)

        if user:
            user.name = name
            user.phone = phone
            user.username = raw_username
        else:
            user = User(
                tg_id=tg_id,
                name = name,
                phone = phone,
                username=raw_username
            )
            session.add(user)

        await session.commit()

    await state.clear()

    await message.answer(
        f"✅ Регистрация завершена!\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"🔗 Username: @{raw_username}",
        reply_markup=kb_inline.back_to_categories_kb,
        parse_mode="HTML"
    )


@start_router.callback_query(F.data == "my_resume")
async def my_profile(callback_query: CallbackQuery):
    await callback_query.answer()
    my_photo = "C:/botPac/my_photo.png"
    text_profile = "C:/botPac/profile.txt"
    with open(text_profile, "r", encoding="utf-8") as p_file:
        p_text = p_file.read()
    photo = FSInputFile(my_photo)
    await callback_query.message.answer_photo(
        photo=photo,
        caption=p_text,
        
        parse_mode="HTML",
        reply_markup = kb_inline.back_to_start_kb
    )
    

@start_router.callback_query(F.data == "service_package")
async def my_pack(callback_query: CallbackQuery, state: FSMContext):

    await callback_query.answer()

    tg_id = callback_query.from_user.id
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)

        if not user:
            await callback_query.message.answer(
                "❗Перед тем как продолжить оформление пакета, нужно зарегистрироваться.\n\n"
                "Пожалуйста, нажмите команду /registration"
            )
            return

    await callback_query.message.answer(
        "<b>Выберите категорию:</b>",
        reply_markup=kb_inline.package_categories,
        parse_mode="HTML"
    )

@start_router.callback_query(F.data == "back_to_categories")
async def back_to_start(callback_query: CallbackQuery):
    await callback_query.message.answer(
        "<b>Выберите категорию:</b>",
        reply_markup=kb_inline.package_categories,
        parse_mode="HTML"
    )
    await callback_query.answer()

@start_router.callback_query(F.data.in_(["wedding", "street", "individ", "paired", "school", "birthday", "matinee"]))
async def choose_category(callback_query: CallbackQuery, state: FSMContext):
    category = callback_query.data
    
    await state.update_data(selected_category=category)
    
    await callback_query.message.answer(
        "📍 Выберите город:",
        reply_markup=kb_inline.cities_kb
    )
    await callback_query.answer()

@start_router.callback_query(F.data.in_(["city_belgorod", "city_voronezh", "city_piter", "city_moscow"]))
async def choose_city(callback_query: CallbackQuery, state: FSMContext):
    city_key = callback_query.data.replace("city_", "")
    
    city_map = {
        "belgorod": "Белгород",
        "voronezh": "Воронеж",
        "piter": "Санкт-Петербург", 
        "moscow": "Москва"
    }
    
    city_name = city_map.get(city_key, city_key)
    
    await state.update_data(selected_city=city_key)

    
    data = await state.get_data()
    category = data.get('selected_category')

    
    await callback_query.message.answer(
        f"🏙 Вы выбрали город: <b>{city_name}</b>",
        parse_mode="HTML" 
    )

    file_path = f"C:/botPac/{category}_{city_key}.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        await callback_query.message.answer(
            text=text,
            parse_mode="HTML"
        )
    except FileNotFoundError:
        await callback_query.message.answer("❗ Файл с пакетами для этого города и категории не найден.")
        return

    category_keyboards = {
        "wedding": kb_inline.packages_wedding,
        "paired": kb_inline.packages_paired,
        "individ": kb_inline.packages_individ,
        "school": kb_inline.packages_school,
        "birthday": kb_inline.packages_birthday,
        "matinee": kb_inline.packages_matinee
    }

    keyboard = category_keyboards.get(category)
    await callback_query.message.answer(
        "<b>Выберите пакет, который вам больше понравился:</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    await callback_query.answer()

    
@start_router.callback_query(F.data.regexp(r"^(wedding|paired|individ|school|birthday|matinee)_.+"))
async def choose_package(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    full_data = callback_query.data 
    category_key, package_key = full_data.split("_", 1)

    category_names = {
        "wedding": "Свадебная съёмка",
        "individ": "Индивидуальная съёмка",
        "paired": "Парная съёмка",
        "school": "Школьная съёмка",
        "birthday": "День рождения",
        "matinee": "Утренник"
    }

    category_human = category_names.get(category_key, category_key)
    package_name = package_key.upper().replace("_", " ") 

    await state.update_data(
        category=category_human, 
        package=package_name,
        category_key=category_key,  
        package_key=package_key     
    )
    await state.set_state(OrderPackage.description)


    await callback_query.message.answer(
        f"📝 Вы выбрали пакет: <b>{package_name}</b>\n"
        f"📂 Категория: <b>{category_human}</b>\n\n"
        f"Пожалуйста, опишите ваши пожелания: <b>Дата, Время, Место и любые детали.</b>",
        parse_mode = "HTML"
    )

@start_router.message(OrderPackage.description)
async def get_description(message: Message, state: FSMContext):

    description = message.text.strip()
    data = await state.get_data() 

    tg_id = message.from_user.id
    category = data.get("category")
    package = data.get("package")
    city_key = data.get("selected_city")
    category_key = data.get("category_key")  
    package_key = data.get("package_key")    

    full_package_name = f"{category_key}_{package_key}"  

    city_map = {
        "belgorod": "Белгород",
        "voronezh": "Воронеж",
        "piter": "Санкт-Петербург",
        "moscow": "Москва"
    }
    city_name = city_map.get(city_key, city_key or "Не указан") 

    async with async_session() as session:
        
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)


        full_package_name = f"{category_key}_{package_key}".lower()

        if user:
           
            stmt_price = select(PackagePrice).where(
                PackagePrice.package_name == full_package_name,
                PackagePrice.city == city_key
            )
            package_price = await session.scalar(stmt_price)

            final_price = package_price.price if package_price else "❌ не найдена"

            
            order_description = OrderDescription(
                description=description,
                user=user.id,
                category=category,
                package=package,
                package_code=full_package_name,
                city=city_key
            )   
            session.add(order_description)
            await session.commit()

            
            await message.answer(
                f"✅ Заказ оформлен!\n\n"
                f"🏙 Город: {city_name}\n"
                f"📂 Категория: {category}\n"
                f"📦 Пакет: {package}\n"
                f"💰 Цена: {final_price} ₽\n"
                f"📝 Описание: {description}",
                reply_markup=kb_inline.back_to_start_kb
            )
        else:
            await message.answer("Ошибка: пользователь не найден в базе данных.")

    await state.clear()

