#!/usr/bin/env python3
import requests
import subprocess
import sys
import time

def check_backend():
    """Проверяет статус backend сервера"""
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend (FastAPI) - РАБОТАЕТ на http://localhost:8080")
            return True
        else:
            print(f"❌ Backend - ОШИБКА: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend (FastAPI) - НЕ ЗАПУЩЕН")
        return False
    except Exception as e:
        print(f"❌ Backend - ОШИБКА: {e}")
        return False

def check_frontend():
    """Проверяет статус frontend сервера"""
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend (React) - РАБОТАЕТ на http://localhost:3000")
            return True
        else:
            print(f"❌ Frontend - ОШИБКА: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend (React) - НЕ ЗАПУЩЕН")
        return False
    except Exception as e:
        print(f"❌ Frontend - ОШИБКА: {e}")
        return False

def check_ports():
    """Проверяет какие порты заняты"""
    try:
        result = subprocess.run(['lsof', '-i', ':8080'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📊 Порт 8080 занят (Backend)")
        else:
            print("📊 Порт 8080 свободен")
            
        result = subprocess.run(['lsof', '-i', ':3000'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📊 Порт 3000 занят (Frontend)")
        else:
            print("📊 Порт 3000 свободен")
    except Exception as e:
        print(f"❌ Ошибка проверки портов: {e}")

def main():
    print("🔍 Проверка статуса VidelizerAI...")
    print("=" * 50)
    
    check_ports()
    print("-" * 30)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    print("-" * 30)
    if backend_ok and frontend_ok:
        print("🎉 ВСЕ СЕРВИСЫ РАБОТАЮТ!")
        print("📱 Откройте http://localhost:3000 в браузере")
    elif backend_ok:
        print("⚠️  Backend работает, но Frontend не запущен")
        print("💡 Запустите: cd frontend && npm start")
    elif frontend_ok:
        print("⚠️  Frontend работает, но Backend не запущен")
        print("💡 Запустите: cd backend/Analise && poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --reload")
    else:
        print("❌ Ни один сервис не запущен")
        print("💡 Запустите: ./start.sh")

if __name__ == "__main__":
    main() 