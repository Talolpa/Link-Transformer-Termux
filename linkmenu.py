import os
import random
import string
import time
import sys
import datetime
import subprocess
import hashlib

try:
    import requests
except ImportError:
    os.system("pip install requests > /dev/null 2>&1")
    import requests

GREEN = '\033[92m'
BRIGHT_GREEN = '\033[1;92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'

SESSION_HISTORY = []
START_TIME = time.time()
DB_FILE = "saved_passwords.txt"

def clear():
    os.system('clear')

def beep():
    sys.stdout.write('\a')
    sys.stdout.flush()

def copy_to_clipboard(text):
    try:
        subprocess.run(['termux-clipboard-set', text], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def get_honest_online():
    try:
        response = requests.get("https://api.counterapi.dev/v1/lolikpassgen/starts/up", timeout=2)
        if response.status_code == 200:
            return response.json().get("count", 1)
    except:
        return "Offline"
    return 1

def get_uptime():
    elapsed = time.time() - START_TIME
    mins, secs = divmod(int(elapsed), 60)
    return f"{mins:02d}:{secs:02d}"

def draw_header():
    clear()
    print(f"""{BRIGHT_GREEN}
 ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{RESET}
    """)
    
    print(f"{GREEN}┌─────────────────────────┬───────────────────────────────────────┬─────────────┐{RESET}")
    print(f"{GREEN}│ {YELLOW}Owner: Loliik{GREEN}           │ {CYAN}TG: https://t.me/avatatkok{GREEN}             │ {YELLOW}[00] Выход{GREEN}  │{RESET}")
    print(f"{GREEN}└─────────────────────────┴───────────────────────────────────────┴─────────────┘{RESET}\n")

def draw_menu():
    print(f"{GREEN}  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐{RESET}")
    print(f"{GREEN}  │ {CYAN}      Генерация       {GREEN}│  │ {CYAN}     Инструменты     {GREEN}│  │ {CYAN}     База данных     {GREEN}│  │ {CYAN}    Сеть и Система    {GREEN}│{RESET}")
    print(f"{GREEN}  ├───────────────────────┤  ├───────────────────────┤  ├───────────────────────┤  ├───────────────────────┤{RESET}")
    print(f"{GREEN}  │ {YELLOW}[1]{GREEN} Пароль (12)       │  │ {YELLOW}[5]{GREEN} Своя длина        │  │ {YELLOW}[9]{GREEN} Проверить пароль  │  │ {YELLOW}[13]{GREEN} Ping (Сеть)       │{RESET}")
    print(f"{GREEN}  │ {YELLOW}[2]{GREEN} Пароль (16)       │  │ {YELLOW}[6]{GREEN} Passphrase        │  │ {YELLOW}[10]{GREEN} Хэш SHA-256     │  │ {YELLOW}[14]{GREEN} Инфо о канале     │{RESET}")
    print(f"{GREEN}  │ {YELLOW}[3]{GREEN} Пароль (32)       │  │ {YELLOW}[7]{GREEN} API Токен (40)    │  │ {YELLOW}[11]{GREEN} Просмотр сохр.  │  │                       │{RESET}")
    print(f"{GREEN}  │ {YELLOW}[4]{GREEN} PIN-код (6)       │  │ {YELLOW}[8]{GREEN} UUID v4           │  │ {YELLOW}[12]{GREEN} Экспорт в TXT   │  │                       │{RESET}")
    print(f"{GREEN}  └───────────────────────┘  └───────────────────────┘  └───────────────────────┘  └───────────────────────┘{RESET}\n")

def generate_password(length, use_sym=True):
    chars = string.ascii_letters + string.digits
    if use_sym:
        chars += string.punctuation
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        if (any(c.islower() for c in password) and 
            any(c.isupper() for c in password) and 
            any(c.isdigit() for c in password) and 
            (not use_sym or any(c in string.punctuation for c in password))):
            return password

def generate_passphrase():
    words = ["apple", "cloud", "stone", "dark", "light", "fire", "ice", "cyber", "hack", "code", "system", "node", "net", "web", "data", "fox", "wolf", "star", "moon", "sun"]
    return "-".join(random.sample(words, 4)) + str(random.randint(10, 99))

def generate_uuid():
    return f"{random.getrandbits(32):08x}-{random.getrandbits(16):04x}-{random.getrandbits(16):04x}-{random.getrandbits(16):04x}-{random.getrandbits(48):012x}"

def generate_api_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(40))

def save_password(password, p_type="Обычный"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DB_FILE, "a") as file:
        file.write(f"[{now}] [{p_type}] {password}\n")
    SESSION_HISTORY.append(password)
    print(f"\n{GREEN}[+] Данные записаны.{RESET}")

def check_strength(password):
    score = 0
    if len(password) >= 12: score += 1
    if len(password) >= 20: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    
    if score <= 3: return f"{RED}Слабый{RESET}"
    elif score == 4: return f"{YELLOW}Средний{RESET}"
    elif score == 5: return f"{GREEN}Надежный{RESET}"
    else: return f"{CYAN}Максимальный{RESET}"

def main():
    clear()
    print(f"\n{CYAN}   СПАСИБО ЧТО ДОВЕРЯЕТЕ НАМ   {RESET}\n")
    beep()
    time.sleep(1)

    while True:
        draw_header()
        draw_menu()
        
        choice = input(f"{CYAN}[?] Выберите пункт: {RESET}")

        if choice == '00':
            print(f"{RED}[!] Завершение сеанса...{RESET}")
            beep()
            break
            
        elif choice in ['1', '2', '3', '5']:
            length = 12
            if choice == '2': length = 16
            elif choice == '3': length = 32
            elif choice == '5':
                try:
                    length = int(input(f"{CYAN}Длина (от 4 до 100): {RESET}"))
                    if length < 4: length = 4
                except ValueError: 
                    beep()
                    continue

            password = generate_password(length)
            beep()
            print(f"\n{GREEN}[+] Результат: {YELLOW}{password}{RESET}")
            print(f"{CYAN}[i] Надежность: {check_strength(password)}{RESET}")
            
            if copy_to_clipboard(password):
                print(f"{CYAN}[i] Скопировано в буфер{RESET}")
            
            ans = input(f"\n{CYAN}[?] Сохранить? (y/n): {RESET}").lower()
            if ans == 'y': save_password(password)
            else: SESSION_HISTORY.append(password)
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '4':
            pin = ''.join(random.choice(string.digits) for _ in range(6))
            beep()
            print(f"\n{GREEN}[+] PIN: {YELLOW}{pin}{RESET}")
            ans = input(f"{CYAN}[?] Сохранить? (y/n): {RESET}").lower()
            if ans == 'y': save_password(pin, "PIN")
            else: SESSION_HISTORY.append(pin)
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '6':
            phrase = generate_passphrase()
            beep()
            print(f"\n{GREEN}[+] Passphrase: {YELLOW}{phrase}{RESET}")
            ans = input(f"{CYAN}[?] Сохранить? (y/n): {RESET}").lower()
            if ans == 'y': save_password(phrase, "Passphrase")
            else: SESSION_HISTORY.append(phrase)
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '7':
            token = generate_api_token()
            beep()
            print(f"\n{GREEN}[+] API Token: {YELLOW}{token}{RESET}")
            if copy_to_clipboard(token): print(f"{CYAN}[i] Скопировано{RESET}")
            ans = input(f"\n{CYAN}[?] Сохранить? (y/n): {RESET}").lower()
            if ans == 'y': save_password(token, "API-Key")
            else: SESSION_HISTORY.append(token)
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '8':
            beep()
            print(f"\n{GREEN}[+] UUID: {YELLOW}{generate_uuid()}{RESET}")
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '9':
            pwd = input(f"{CYAN}Введите пароль: {RESET}")
            beep()
            print(f"\n{CYAN}[i] Надежность: {check_strength(pwd)}{RESET}")
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '10':
            pwd = input(f"{CYAN}Введите текст: {RESET}")
            beep()
            print(f"\n{GREEN}[+] SHA-256: {YELLOW}{hashlib.sha256(pwd.encode()).hexdigest()}{RESET}")
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '11':
            clear()
            print(f"{YELLOW}--- СОХРАНЕННЫЕ ДАННЫЕ ---{RESET}\n")
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as file:
                    print(file.read())
            else:
                print(f"{RED}Файл пуст.{RESET}")
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '12':
            if os.path.exists(DB_FILE):
                import shutil
                shutil.copy(DB_FILE, "export_backup.txt")
                beep()
                print(f"\n{GREEN}[+] Экспорт в export_backup.txt выполнен.{RESET}")
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '13':
            print(f"\n{YELLOW}[*] Проверка сети (Ping)...{RESET}")
            start = time.time()
            try:
                requests.get("https://google.com", timeout=3)
                ping = int((time.time() - start) * 1000)
                beep()
                print(f"{GREEN}[+] Пинг: {ping} ms{RESET}")
            except:
                print(f"{RED}[-] Сеть недоступна.{RESET}")
            input(f"\n{CYAN}Enter...{RESET}")

        elif choice == '14':
            print(f"\n{CYAN}[i] Канал: {YELLOW}https://t.me/avatatkok{RESET}")
            time.sleep(1.5)
            
        else:
            beep()
            print(f"{RED}[-] Неизвестная команда.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
