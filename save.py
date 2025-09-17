import json
from datetime import datetime
import time
from gps3 import gps3
import requests
import os


def save_to_json(data, filename="location_data.json"):
    try:
        # Показываем полный путь к файлу
        full_path = os.path.abspath(filename)
        print(f"Пытаюсь сохранить файл по пути: {full_path}")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Данные сохранены в {filename}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения в JSON: {e}")
        return False


if __name__ == "__main__":
    print("=== Запуск системы определения местоположения ===")
    print(f"Текущая рабочая директория: {os.getcwd()}")
    
    location_data = get_gps_location()
    
    if not location_data:
        print("GPS недоступен, пробуем метод по IP...")
        location_data = get_ip_location()
    
    if location_data:
        # Создаем данные для сохранения
        output_data = {
            "status": "Данные успешно сохранены!",
            "location": {
                "latitude": location_data['latitude'],
                "longitude": location_data['longitude']
            },
            "source": location_data.get('source', 'unknown'),
            "time": location_data['time']
        }
        
        success = save_to_json(output_data)
        if success:
            print("✓ Данные успешно сохранены!")
            print(f"Местоположение: {location_data['latitude']}, {location_data['longitude']}")
            print(f"Источник: {location_data.get('source', 'unknown')}")
            print(f"Время: {location_data['time']}")
            
            # Проверяем, создался ли файл
            if os.path.exists("location_data.json"):
                print("✓ Файл location_data.json успешно создан!")
            else:
                print("✗ Файл location_data.json не создан!")
        else:
            print("✗ Ошибка при сохранении данных")
    else:
        print("✗ Не удалось получить данные о местоположении")
    
    print("=== Завершение работы ===")