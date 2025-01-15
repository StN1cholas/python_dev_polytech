from math import pi

class Shape:
    """Базовый класс для всех геометрических фигур"""
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def position(self):
        return f"расположена в точке ({self._x}, {self._y})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.position()}"


class Rectangle(Shape):
    """Прямоугольник"""
    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self._width = width
        self._height = height

    def area(self):
        return self._width * self._height

    def perimeter(self):
        return 2 * (self._width + self._height)

    def __str__(self):
        return (f"{super().__str__()}, ширина: {self._width}, высота: {self._height}, "
                f"площадь: {self.area()}, периметр: {self.perimeter()}")


class Square(Shape):
    """Квадрат"""
    def __init__(self, side, x=0, y=0):
        super().__init__(x, y)
        self._side = side

    def area(self):
        return self._side ** 2

    def perimeter(self):
        return 4 * self._side

    def __str__(self):
        return (f"{super().__str__()}, сторона: {self._side}, "
                f"площадь: {self.area()}, периметр: {self.perimeter()}")


class Circle(Shape):
    """Круг"""
    def __init__(self, radius, x=0, y=0):
        super().__init__(x, y)
        self._radius = radius

    def area(self):
        return pi * self._radius ** 2

    def perimeter(self):
        return 2 * pi * self._radius

    def __str__(self):
        return (f"{super().__str__()}, радиус: {self._radius}, "
                f"площадь: {self.area():.2f}, периметр: {self.perimeter():.2f}")


if __name__ == '__main__':
    shapes = [
        Rectangle(2, 3),
        Square(2, 1, 1),
        Circle(1, 0, 0)
    ]
    for shape in shapes:
        print(shape)
