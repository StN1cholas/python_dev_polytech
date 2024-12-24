import math
import unittest
from math import sqrt, radians, sin, cos


class Quaternion:
    """Инициализация"""
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    """Сложение кватернионов"""
    def __add__(self, other):
        return Quaternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    """Вычитание кватернионов"""
    def __sub__(self, other):
        return Quaternion(self.w - other.w,
                          self.x - other.x,
                          self.y - other.y,
                          self.z - other.z)

    """Умножение кватернионов"""
    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    """Деление кватернионов"""
    def __truediv__(self, other):
        return self * other.reverse()

    """Сопряженный кватернион"""
    def sopr(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    """Норма кватерниона"""
    def normal(self):
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    """Нормализация кватерниона"""
    def normalize(self):
        n = self.normal()
        if n == 0:
            raise ZeroDivisionError("Невозможно нормализовать нулевой кватернион.")
        return Quaternion(self.w / n, self.x / n, self.y / n, self.z / n)

    """Обратный кватернион"""
    def reverse(self):
        var = self.normal() ** 2
        if var == 0:
            raise ZeroDivisionError("Невозможно найти обратный квантерион для нулевого кватерниона.")
        sopr1 = self.sopr()
        return Quaternion(sopr1.w / var,
                          sopr1.x / var,
                          sopr1.y / var,
                          sopr1.z / var)

    """Поворот вектора"""
    def rotate_vector(self, vector):
        q_vector = Quaternion(0, vector[0], vector[1], vector[2])
        q_rotated = self * q_vector * self.reverse()
        return [q_rotated.x, q_rotated.y, q_rotated.z]

    def __repr__(self):
        """Строковое представление кватерниона"""
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        """Метод сравнения кватернионов =="""
        return (math.isclose(self.w, other.w, abs_tol=1e-3) and
                math.isclose(self.x, other.x, abs_tol=1e-3) and
                math.isclose(self.y, other.y, abs_tol=1e-3) and
                math.isclose(self.z, other.z, abs_tol=1e-3))

class Test(unittest.TestCase):
    def test_add(self):
        q1 = Quaternion(1, 3, 5, 7)
        q2 = Quaternion(1, 1, 1, 1)
        result = q1.__add__(q2)
        expected = Quaternion(2, 4, 6, 8)
        self.assertEqual(result, expected)

    def test_sub(self):
        q1 = Quaternion(1, 3, 5, 7)
        q2 = Quaternion(1, 1, 1, 1)
        result = q1.__sub__(q2)
        expected = Quaternion(0, 2, 4, 6)
        self.assertEqual(result, expected)

    def test_mul(self):
        q1 = Quaternion(1, 3, 5, 7)
        q2 = Quaternion(1, 1, 1, 1)
        result = q1.__mul__(q2)
        expected = Quaternion(-14, 2, 10, 6)
        self.assertEqual(result, expected)

    def test_truediv(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        result = q1.__truediv__(q2)

        expected_w = (-60) / (5 ** 2 + 6 ** 2 + 7 ** 2 + 8 ** 2)
        expected_x = (12) / (5 ** 2 + 6 ** 2 + 7 ** 2 + 8 ** 2)
        expected_y = (30) / (5 ** 2 + 6 ** 2 + 7 ** 2 + 8 ** 2)
        expected_z = (24) / (5 ** 2 + 6 ** 2 + 7 ** 2 + 8 ** 2)

        expected = Quaternion(expected_w, expected_x, expected_y, expected_z)

    def test_sopr(self):
        q = Quaternion(1, 3, 5, 7)
        result = q.sopr()
        expected = Quaternion(1, -3, -5, -7)
        self.assertEqual(result, expected)

    def test_normal(self):
        q = Quaternion(1, 3, 5, 7)
        result = q.normal()
        expected = math.sqrt(84)  # sqrt(1^2 + 3^2 + 5^2 + 7^2)
        self.assertAlmostEqual(result, expected)

    def test_normalize(self):
        q = Quaternion(3, 4, 0, 0)
        result = q.normalize()
        expected_norm = math.sqrt(25)  # sqrt(3^2 + 4^2)
        expected = Quaternion(3 / expected_norm, 4 / expected_norm, 0 / expected_norm, 0 / expected_norm)
        self.assertEqual(result.w, expected.w)
        self.assertEqual(result.x, expected.x)
        self.assertEqual(result.y, expected.y)
        self.assertEqual(result.z, expected.z)

    def test_reverse(self):
        q = Quaternion(3, 4, 0, 0)
        result = q.reverse()
        norm_squared = q.normal() ** 2
        expected = Quaternion(3 / norm_squared, -4 / norm_squared, 0 / norm_squared, 0 / norm_squared)
        self.assertEqual(result.w, expected.w)
        self.assertEqual(result.x, expected.x)
        self.assertEqual(result.y, expected.y)
        self.assertEqual(result.z, expected.z)

    def test_rotate_vector(self):
        q = Quaternion(0.7, 0.7, 0.0, 0.0)
        vector = [0.0, 1.0, 0.0]
        result = q.rotate_vector(vector)
        expected = [0.0, 0.0, 1.0]
        self.assertAlmostEqual(result[0], expected[0])
        self.assertAlmostEqual(result[1], expected[1])
        self.assertAlmostEqual(result[2], expected[2])

    def test_normalize_zero(self):
        q = Quaternion(0, 0, 0, 0)
        with self.assertRaises(ZeroDivisionError):
            q.normalize()

    def test_reverse_zero(self):
        q = Quaternion(0, 0, 0, 0)
        with self.assertRaises(ZeroDivisionError):
            q.reverse()

if __name__ == "__main__":
    unittest.main()