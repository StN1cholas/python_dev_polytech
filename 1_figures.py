class Shape:
    """
    Родительский класс для фигур
    """
    name = 'геометрическая фигура'

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def __repr__(self):
        return f"{self.name} по координатам ({self.__x}, {self.__y})"


class Rectangle(Shape):
    """
    Класс прямоугольников 
    Использует базовый класс Shape для задания координат.
    """
    name = 'прямоугольник'

    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def area(self):
        """Вычисляет площадь прямоугольника."""
        return self.width * self.height

    def perimeter(self):
        """Вычисляет периметр прямоугольника."""
        return 2 * (self.width + self.height)

    def __repr__(self):
        return (f"{Shape.__repr__(self)}, со сторонами {self.width} и {self.height},"
                f" с площадью {self.area()} и периметром {self.perimeter()}")


class Square(Rectangle):
    """
    Класс квадратов 
    Использует Rectangle как базовый класс.
    Наследует зависимости от Shape через Rectangle
    """
    name = 'квадрат'

    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    def __repr__(self):
        return (f"{Shape.__repr__(self)}, со стороной {self.width},"
                f" с площадью {self.area()} и периметром {self.perimeter()}")
        
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, val):
        self._width = self._height = val
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, val):
        self._height = self._width = val


if __name__ == '__main__':
    figures = [Rectangle(2, 3), Square(2, 1, 1)]
    for figure in figures:
        print("До изменения: ", figure)
        figure.width = 3
        print("После изменения: ", figure)
