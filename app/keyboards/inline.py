from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


points_start = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="📄 Моё резюме", callback_data="my_resume")], 
        [InlineKeyboardButton(text="🎨 Мои работы", url = "https://disk.yandex.ru/d/dLWO2rXRFYD7_g")],
        [InlineKeyboardButton(text="💼 Пакет услуг", callback_data="service_package")]],     
)

package_categories = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Свадебная съёмка", callback_data = "wedding")], 
                       [InlineKeyboardButton(text = "Уличная съёмка" , callback_data = "street")],
                       [InlineKeyboardButton(text = "Парная/Индивидуальная съёмка" , callback_data = "paired")],
                       [InlineKeyboardButton(text = "Школьная съёмка" , callback_data = "school")],
                       [InlineKeyboardButton(text = "День рождения" , callback_data = "birthday")],
                       [InlineKeyboardButton(text = "Утренник в детском саду" , callback_data = "matinee")],
                       [InlineKeyboardButton(text="⏪ Назад в старт", callback_data="back_to_start_menu")]]
)

packages_wedding = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "LITE", callback_data = "wedding_lite")],
                       [InlineKeyboardButton(text = "LITE PLUS", callback_data = "wedding_lite_plus")],
                       [InlineKeyboardButton(text = "PREMIUM", callback_data = "wedding_premium")],
                       [InlineKeyboardButton(text = "ULTRA", callback_data = "wedding_ultra")],
                       [InlineKeyboardButton(text = "LITE PHOTO", callback_data = "wedding_lite_photo")],
                       [InlineKeyboardButton(text = "PREMIUM PHOTO", callback_data = "wedding_premium_photo")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_street = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "PHOTO", callback_data = "street_photo")],
                       [InlineKeyboardButton(text = "PLUS", callback_data = "street_plus")],
                       [InlineKeyboardButton(text = "VIDEO", callback_data = "street_video")],
                       [InlineKeyboardButton(text = "PREMIUM", callback_data = "street_premium")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_paired = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Индивидуальная фотосъёмка", callback_data = "paired_individ_photo")],
                       [InlineKeyboardButton(text = "Парная фотосъёмка", callback_data = "paired_paired_photo")],
                       [InlineKeyboardButton(text = "LOVE STORY PHOTO", callback_data = "paired_love_story_photo")],
                       [InlineKeyboardButton(text = "LOVE STORY VIDEO ", callback_data = "paired_love_story_video")],
                       [InlineKeyboardButton(text="⏪ Назад к категориям", callback_data="back_to_categories")]])

packages_school = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Школьный фотоальбом", callback_data = "school_photo_album")],
                       [InlineKeyboardButton(text = "Школьный фотоальбом PREMIUM", callback_data = "school_photo_album_premium")],
                       [InlineKeyboardButton(text = "Клип-сюрприз от родителей", callback_data = "school_clip_surprice")],
                       [InlineKeyboardButton(text = "Школьный клип", callback_data = "school_clip")],
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