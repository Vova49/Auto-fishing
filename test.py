import pyautogui
from PIL import ImageGrab
import time
import os
import threading

# Определяем цвет для поиска (в формате (R, G, B))
TARGET_COLOR = (255, 170, 0)

# Определяем координаты области сканирования
TOP_LEFT = (1386, 66)
BOTTOM_RIGHT = (1905, 99)


def find_pixels():
    # Делаем скриншот указанной области
    screenshot = ImageGrab.grab(bbox=(TOP_LEFT[0], TOP_LEFT[1], BOTTOM_RIGHT[0], BOTTOM_RIGHT[1]))
    pixels = screenshot.load()

    width, height = screenshot.size

    for x in range(width):
        for y in range(height):
            if pixels[x, y] == TARGET_COLOR:
                return TOP_LEFT[0] + x, TOP_LEFT[1] + y

    return None


def schedule_shutdown(minutes):
    seconds = minutes * 60
    print(f"Компьютер выключится через {minutes} минут.")
    time.sleep(seconds)

    # Отменим все отложенные выключения, если они были активированы ранее
    os.system("shutdown /a")

    print("Выключение...")
    os.system("shutdown /s /t 0")


if __name__ == "__main__":
    shutdown_choice = input("Выключать ли компьютер после работы программы? (да/нет): ").strip().lower()

    if shutdown_choice == "да":
        try:
            shutdown_minutes = float(input("Через сколько минут выключить компьютер?: "))
            shutdown_thread = threading.Thread(target=schedule_shutdown, args=(shutdown_minutes,))
            shutdown_thread.daemon = True
            shutdown_thread.start()
        except ValueError:
            print("Некорректное значение времени. Продолжение без выключения.")
    else:
        print("Выключение отключено.")

    while True:
        position = find_pixels()
        if position:
            print(f"Найден пиксель цвета {TARGET_COLOR}")
            pyautogui.click(button='right')  # Первый клик ПКМ
            time.sleep(0.5)  # Задержка 0.5 секунды
            pyautogui.click(button='right')  # Второй клик ПКМ
            time.sleep(6.5)  # Ожидание 6.5 секунд перед новой проверкой
        else:
            print("Цвет не найден в указанной области.")
        time.sleep(0.3)
