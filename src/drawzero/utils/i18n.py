import os
import locale
import ctypes

__all__ = ['I18N', 'set_lang']

_known_languages = {'en', 'ru'}


def _get_best_lang():
    if os.getenv('LANG', 'None').startswith('ru'):
        return 'ru'
    elif locale.getdefaultlocale() and locale.getdefaultlocale()[0].startswith('ru'):
        return 'ru'
    elif hasattr(ctypes, 'windll'):
        try:
            windll = ctypes.windll.kernel32
            lang_code = windll.GetUserDefaultUILanguage()
            if locale.windows_locale[lang_code].startswith('ru'):
                return 'ru'
        except:
            pass
    return 'en'


class I18N:
    lang = 'en'
    dummy = {
        'ru': 'dummy_ru',
        'en': 'dummy_en',
    }
    bad_color = {
        'ru': 'Некорректный цвет: {!r}',
        'en': 'Invalid color: {!r}',
    }
    use_color_hex = {
        'ru': 'В качестве цвета укажите строку вида "#xxyyzz"',
        'en': 'Use hex color such as "#xxyyzz"',
    }
    use_color_hexdigits = {
        'ru': 'В коде цвета в выражении вида "#xxyyzz" используйте только цифры 0-9 и буквы a-f',
        'en': 'Use hex digits 0-9a-f in hex color "#xxyyzz"',
    }
    use_color_consts = {
        'ru': 'В качестве цвета укажите одну из констант вида (C.red, C.green) или название цвета ("red", "green" и т.п.)',
        'en': 'As a color, specify one of the constants like (C.red, C.green) or a color name ("red", "green", etc.)',
    }
    use_color_tuple = {
        'ru': 'В качестве цвета укажите тройку чисел: количество красного, зелёного и синего (0 до 255) (например, (0, 128, 255))',
        'en': 'As a color, specify a triplet of numbers: the amount of red, green, and blue (0 to 255) (for example, (0, 128, 255))',
    }
    use_color_ints = {
        'ru': 'В качестве цвета укажите тройку именно целых чисел от 0 до 255 каждое (например, (0, 128, 255)',
        'en': 'As a color, specify a triplet of precisely integers ranging from 0 to 255 each (for example, (0, 128, 255))',
    }
    use_color_correct = {
        'ru': 'В качестве цвета укажите тройку чисел вида (0, 128, 255): количество красного, зелёного и синего (0 до 255), одну из констант вида (C.red, C.green) или название цвета ("red", "green" и т.п.)',
        'en': 'As a color, specify a triplet of numbers like (0, 128, 255): the amount of red, green, and blue (0 to 255), one of the constants like (C.red, C.green) or a color name ("red", "green", etc.)',
    }
    bad_coords = {
        'ru': 'Некорректные координаты: {!r}',
        'en': 'Invalid coordinates: {!r}',
    }
    use_coords_pair = {
        'ru': 'Координаты указывайте в виде (x, y) или [x, y], например, (100, 200.5)',
        'en': 'Specify coordinates as (x, y) or [x, y], for example, (100, 200.5)',
    }
    use_coords_iterable = {
        'ru': '(то есть нужно передать либо кортеж, либо список из двух чисел, либо точку класса Pt)',
        'en': '(That is, you need to pass either a tuple or a list of two numbers, or a point of the Pt class)',
    }
    use_coords_ints = {
        'ru': '(то есть координаты должны быть либо целыми, либо действительными числами)',
        'en': '(That is, the coordinates must be either integers or real numbers)',
    }
    bad_num = {
        'ru': 'Некорректное число: {!r}',
        'en': 'Incorrect number: {!r}',
    }
    bad_width = {
        'ru': 'Некорректная толщина линии: {!r}',
        'en': 'Incorrect line thickness: {!r}',
    }
    use_width_int = {
        'ru': 'Должно быть число, например, 4',
        'en': 'Should be a number, for example, 4',
    }
    bad_alpha = {
        'ru': 'Некорректная прозрачность: {!r}',
        'en': 'Incorrect transparency: {!r}',
    }
    use_alpha_int = {
        'ru': 'Прозрачность должна быть числом от 0 до 255 включительно',
        'en': 'Transparency should be a number from 0 to 255 inclusive',
    }
    bad_rect = {
        'ru': 'Некорректные координаты прямоугольника: {!r}',
        'en': 'Incorrect rectangle coordinates: {!r}',
    }
    use_rect_ints = {
        'ru': 'Координаты прямоугольника должны быть целыми или действительными (вида 100 или 100.25)',
        'en': 'Rectangle coordinates should be integers or real (like 100 or 100.25)',
    }
    use_rect_correct = {
        'ru': 'Укажите координаты прямоугольника в формате (x, y), w, h,\nгде (x, y) — координаты угла, и w, h — ширина и высота прямоугольника',
        'en': 'Specify the coordinates of the rectangle in the format (x, y), w, h,\nwhere (x, y) are the coordinates of the corner, and w, h are the width and height of the rectangle',
    }
    bad_polygon = {
        'ru': 'Некорректные координаты многоугольника: {!r}',
        'en': 'Incorrect polygon coordinates: {!r}',
    }
    use_polygon_list = {
        'ru': 'Укажите координаты вершин многоугольника в формате ((x1,y1), (x2, y2), ...)',
        'en': 'Specify the vertices of the polygon in the format ((x1,y1), (x2, y2), ...)',
    }
    use_polygon_ints = {
        'ru': 'Координаты многоугольника должны быть целыми или действительными (вида 100 или 100.25)',
        'en': 'Polygon coordinates should be integers or real (like 100 or 100.25)',
    }
    use_polygon_even = {
        'ru': 'Число координат вершин многоугольника должно быть чётным',
        'en': 'The number of polygon vertex coordinates must be even',
    }
    bad_text_align = {
        'ru': 'Некорректный параметр для выравнивания текста: {!r}',
        'en': 'Incorrect parameter for text alignment: {!r}',
    }
    use_text_align = {
        'ru': "параметр align должен быть одной из следующих констант: '<^', '.^', '>^', '<.', '..', '>.', '<v', '.v', '>v',\n"
              "(<=по левому краю, .=по центру, >=по правому краю), (^=по верхнему краю, .=по центра, v=по нижнему краю)",
        'en': "align parm must be one of '<^', '.^', '>^', '<.', '..', '>.', '<v', '.v', '>v',\n"
              "(<=left, .=center, >=right), (^=top, .=middle, v=bottom)",
    }
    example = {
        'ru': '== Пример корректного вызова ==',
        'en': '== Correct call example ==',
    }
    wrong_domain_types = {
        'ru': 'Для обозначения границ градиента должны использоваться только числа, {!r} не подходит.',
        'en': 'Only numbers should be used to denote gradient boundaries, {!r} is not suitable.',
    }
    wrong_domain = {
        'ru': 'Некорректное количество точек для входных данных: должно быть либо 2, либо ровно столько, сколько цветов, то есть {}',
        'en': 'Incorrect number of points for the input data: there should be either 2, or exactly as many as there are colors, that is, {}.',
    }

    @classmethod
    def set_lang(cls, lang):
        if lang not in _known_languages:
            raise ValueError(f'Unknown language {lang}')
        cls.lang = lang
        for attr in list(cls.__dict__.keys()):
            if attr in {'lang', 'set_lang'}: continue
            if attr.startswith('__'): continue
            if attr.endswith('__saved'): continue
            saved_attr = attr + '__saved'
            if saved_attr not in cls.__dict__:
                setattr(cls, saved_attr, cls.__dict__[attr])
            setattr(cls, attr, cls.__dict__[saved_attr].get(lang, None))
            if not cls.__dict__[attr]:
                setattr(cls, attr, cls.__dict__[saved_attr].get('en', 'None'))


I18N.set_lang(_get_best_lang())

set_lang = I18N.set_lang
