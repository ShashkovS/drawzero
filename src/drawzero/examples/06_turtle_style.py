from drawzero import *

colors = [C.darkslategrey, C.dimgrey, C.slateblue, C.darkblue, C.yellowgreen, C.maroon,
          C.violetred, C.darkslategray, C.honeydew, C.mediumpurple, C.lightsalmon]

# Drawing regular polygons for n from 3 to 10
# Рисуем правильные треугольник (n=3), четырёхугольник и т.д. до десятиугольник
for n in range(3, 11):
    cur = Pt(600, 200)
    # Drawing n lines for regular polygon
    # Каждую сторону рисуем отдельно
    for i in range(n):
        prev = cur.copy()
        # How to get next point? We clone the old one, rotate left and move forward a bit
        # Чтобы получить новую вершину, мы клонируем старую, поворачиваемся и двигаемся вперёд
        cur.left(360 / n)
        cur.forward(200)
        line(colors[n], prev, cur)
