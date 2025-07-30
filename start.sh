#!/bin/bash

# Запуск backend
echo "Starting backend..."
cd backend/Analise
poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --reload &
BACKEND_PID=$!

# Ждем немного чтобы backend запустился
sleep 3

# Запуск frontend
echo "Starting frontend..."
cd ../../frontend
npm start &
FRONTEND_PID=$!

echo "Backend running on http://localhost:8080"
echo "Frontend running on http://localhost:3000"
echo "Press Ctrl+C to stop both servers"

# Ждем сигнала для остановки
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 