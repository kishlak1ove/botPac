from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


points_start = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="📄 Моё резюме", callback_data="my_resume")], 
        [InlineKeyboardButton(text="🎨 Мои работы", url = "https://disk.yandex.ru/d/dLWO2rXRFYD7_g")],
        [InlineKeyboardButton(text="💼 Пакет услуг", callback_data="service_package")]],     
)

package_categories = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Свадебная съёмка", callback_data = "wedding")], 
                       [InlineKeyboardButton(text = "Парная съёмка" , callback_data = "paired")],
                       [InlineKeyboardButton(text = "Индивидуальная съёмка" , callback_data = "individual")],
                       [InlineKeyboardButton(text = "Школьная съёмка" , callback_data = "school")],
                       [InlineKeyboardButton(text = "День рождения" , callback_data = "birthday")],
                       [InlineKeyboardButton(text = "Утренник в детском саду" , callback_data = "matinee")],
                       [InlineKeyboardButton(text="⏪ Назад в старт", callback_data="back_to_start_menu")]]
)

packages_wedding = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "LITE", callback_data = "wedding_lite")],
                       [InlineKeyboardButton(text = "LITE PLUS", callback_data = "wedding_lite_plus")],
                       [InlineKeyboardButton(text = "PREMIUM", callback_data = "wedding_premium")],
                       [InlineKeyboardButton(text = "PREMIUM +", callback_data = "wedding_premium_+")],
                       [InlineKeyboardButton(text = "LITE PHOTO + VIDEO", callback_data = "wedding_lite_photo_+_video")],
                       [InlineKeyboardButton(text = "PREMIUM PHOTO + VIDEO", callback_data = "wedding_premium_photo_+_video")],
                       [InlineKeyboardButton(text = "ULTRA", callback_data = "wedding_ultra")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_individual = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "PHOTO", callback_data = "individual_photo")],
                       [InlineKeyboardButton(text = "VIDEO", callback_data = "individual_video")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_paired = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "LOVE STORY PHOTO", callback_data = "paired_love_story_photo")],
                       [InlineKeyboardButton(text = "LOVE STORY VIDEO ", callback_data = "paired_love_story_video")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_school = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Школьный клип", callback_data = "school_clip")],
                       [InlineKeyboardButton(text = "Клип-сюрприз от родителей", callback_data = "school_clip_surprice")],
                       [InlineKeyboardButton(text = "Эксклюзив-клип от родителей", callback_data = "school_clip_surprice_exclusive")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])   

packages_birthday = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Фотосъёмка", callback_data = "birthday_photo")],
                       [InlineKeyboardButton(text = "Видеосъёмка", callback_data = "birthday_video")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_matinee = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Фотосъёмка", callback_data = "matinee_photo")],
                       [InlineKeyboardButton(text = "Видеосъёмка", callback_data = "matinee_video")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])   

back_to_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="⏪ Назад в старт", callback_data="back_to_start_menu")]]
)

back_to_categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]]
)

back_to_packages_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="⏪ Назад к пакетам", callback_data="back_to_packages")]]
)

cities_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Белгород", callback_data="city_belgorod")],
        [InlineKeyboardButton(text="Воронеж", callback_data="city_voronezh")],
        [InlineKeyboardButton(text="Санкт-Петербург", callback_data="city_piter")],
        [InlineKeyboardButton(text="Москва", callback_data="city_moscow")],
        [InlineKeyboardButton(text="Другой город...", callback_data="city_another")],
        [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]
    ]
)