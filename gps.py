import json
from datetime import datetime
import time
from gps3 import gps3
import requests
import os

def get_gps_location():
    try:
        print("Подключаемся к GPS-демону...")
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        
        gps_socket.connect()
        gps_socket.watch()
        
        print("Ожидаем данные от GPS...")
        timeout = 30
        start_time = time.time()
        
        for new_data in gps_socket:
            if time.time() - start_time > timeout:
                print("Таймаут ожидания GPS данных")
                return None
                
            if new_data:
                data_stream.unpack(new_data)
                
                if (hasattr(data_stream, 'TPV') and 
                    data_stream.TPV.get('lat') not in ['n/a', None] and 
                    data_stream.TPV.get('lon') not in ['n/a', None]):
                    
                    location_data = {
                        'latitude': float(data_stream.TPV['lat']),
                        'longitude': float(data_stream.TPV['lon']),
                        'time': datetime.now().isoformat(),
                        'altitude': float(data_stream.TPV.get('alt', 0)) if data_stream.TPV.get('alt') not in ['n/a', None] else 0,
                        'speed': float(data_stream.TPV.get('speed', 0)) if data_stream.TPV.get('speed') not in ['n/a', None] else 0,
                        'source': 'gps'
                    }
                    
                    print(f"GPS данные получены: {location_data}")
                    return location_data
                    
    except Exception as e:
        print(f"Ошибка получения GPS данных: {e}")
        return None

def get_ip_location():
    try:
        print("Используем метод определения по IP...")
        response = requests.get('https://ipinfo.io/json', timeout=10)
        data = response.json()
        
        # Парсим координаты из ответа
        loc = data.get('loc', '').split(',')
        if len(loc) == 2:
            location_data = {
                'latitude': float(loc[0]),
                'longitude': float(loc[1]),
                'time': datetime.now().isoformat(),
                'source': 'ip',
                'city': data.get('city', ''),
                'country': data.get('country', '')
            }
            return location_data
        return None
        
    except Exception as e:
        print(f"Ошибка получения местоположения по IP: {e}")
        return None

if __name__ == "__main__":
    print("=== Запуск системы определения местоположения ===")
    print(f"Текущая рабочая директория: {os.getcwd()}")
    
    location_data = get_gps_location()
    
    if not location_data:
        print("GPS недоступен, пробуем метод по IP...")
        location_data = get_ip_location()
    
    print("=== Завершение работы ===")