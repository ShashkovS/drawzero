def jsonize(parms, sep=','):
    if type(parms) == int or type(parms) == float:
        return str(parms)
    elif type(parms) == str:
        return '"' + parms.replace('"', '\\"') + '"'
    elif type(parms) == list or type(parms) == tuple:
        return '[' + sep.join(map(jsonize, parms)) + ']'
    else:
        raise ValueError('Тип не поддерживается')


def draw_resize(*parms):
    print('resize', format(jsonize(parms, sep=', ')))


def draw_line(*parms):
    print('line', format(jsonize(parms, sep=', ')))


def draw_circle(*parms):
    print('circle', format(jsonize(parms, sep=', ')))


def draw_filled_circle(*parms):
    print('filled_circle', format(jsonize(parms, sep=', ')))


def draw_rect(*parms):
    print('rect', format(jsonize(parms, sep=', ')))


def draw_filled_rect(*parms):
    print('filled_rect', format(jsonize(parms, sep=', ')))


def draw_polygon(*parms):
    print('polygon', format(jsonize(parms, sep=', ')))


def draw_filled_polygon(*parms):
    print('filled_polygon', format(jsonize(parms, sep=', ')))


def draw_text(*parms):
    print('text', format(jsonize(parms, sep=', ')))


def draw_fill(*parms):
    print('fill', format(jsonize(parms, sep=', ')))


def draw_clear(*parms):
    print('clear', format(jsonize(parms, sep=', ')))


def draw_image(*parms):
    print('image', format(jsonize(parms, sep=', ')))


def draw_tick(r=1):
    print('tick({})'.format(r))


def draw_sleep(t=1):
    print('sleep({})'.format(t))


def draw_set_line_width(w):
    print('set_line_width({})'.format(w))
    pass


surface_size = 1000
key_flags = None
