from functools import wraps

def caching_decorator(cache_depth=10):
    def decorator(func):
        # У каждой функции будет свой кэш и порядок
        cache = {}
        cache_order = []

        @wraps(func)
        def wrapper(*args):
            key = args
            if key in cache:
                print(f"Достаем из кеша для {func.__name__}: {key[0]}")
                # Перемещаем ключ в конец списка (обновляем порядок)
                cache_order.remove(key)
                cache_order.append(key)
                return cache[key]

            print(f"Вычисляем для {func.__name__}: {key[0]}")
            result = func(*args)

            if len(cache_order) >= cache_depth:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]

            cache[key] = result
            cache_order.append(key)
            return result

        return wrapper

    return decorator


@caching_decorator(10)
# Функция, вычисляющая n-ое число в ряду Фибоначчи
def fibo(n):
    if n <= 1:
        return n
    return fibo(n - 1) + fibo(n - 2)

@caching_decorator(10)
# Функция, вычисляющая факториал числа n
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# Тесты
print(fibo(5))
print(fibo(10))

print(factorial(5))
print(factorial(10))
