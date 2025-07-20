import os
import hashlib
from Crypto.Cipher import AES

def restore_original_filename(encrypted_name, encrypted_ext):
    """Восстанавливает оригинальное имя файла"""
    original = encrypted_name[:-len(encrypted_ext)]
    parts = original.split('_')
    
    if len(parts) > 1:
        last_part = parts[-1].lower()
        # Проверяем, является ли последняя часть расширением (2-5 символов)
        if 2 <= len(last_part) <= 5 and last_part.isalnum():
            return '_'.join(parts[:-1]) + '.' + last_part
    return original

def main():
    print("[+] Универсальный дешифратор SLocker")

    encrypted_dir = input("[?] Путь к папке с зашифрованными файлами: ").strip()
    if not os.path.isdir(encrypted_dir):
        print("[-] Ошибка: папка не существует!")
        return

    encrypted_ext = input("[?] Расширение вируса (например '.勿卸载软件解密加QQ3135078046bahk10086256' или '_勿卸载软件解密加QQ3135078046bahk10086256'): ").strip()
    try:
        xh = int(input("[?] Код дешифровки (число от вируса): ").strip())
    except ValueError:
        print("[-] Ошибка: код должен быть числом!")
        return

    # Генерация ключа (один раз)
    m = xh + 520
    md5_key = hashlib.md5(str(m).encode()).hexdigest()[8:24]
    iv = b"QQqun 571012706 "  # IV одинаков для всех файлов

    decrypted_count = 0
    for root, _, files in os.walk(encrypted_dir):
        for file in files:
            if file.endswith(encrypted_ext):
                input_path = os.path.join(root, file)
                original_name = restore_original_filename(file, encrypted_ext)
                output_path = os.path.join(root, original_name)

                try:
                    # Чтение данных
                    with open(input_path, 'rb') as f:
                        encrypted_data = f.read()

                    # 🔑 Создаем НОВЫЙ объект AES для каждого файла
                    cipher = AES.new(md5_key.encode(), AES.MODE_CBC, iv)
                    decrypted_data = cipher.decrypt(encrypted_data)

                    # Удаление PKCS7 padding
                    pad_len = decrypted_data[-1]
                    if 0 < pad_len <= AES.block_size:
                        if all(decrypted_data[-i] == pad_len for i in range(1, pad_len + 1)):
                            decrypted_data = decrypted_data[:-pad_len]

                    # Запись
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(decrypted_data)

                    os.remove(input_path)
                    decrypted_count += 1
                    print(f"[✓] Успех: {file} → {original_name}")

                except Exception as e:
                    print(f"[×] Ошибка {file}: {str(e)}")
                    if os.path.exists(output_path):
                        os.remove(output_path)

    print(f"[+] Готово! Расшифровано: {decrypted_count} файлов")

if __name__ == "__main__":
    main()