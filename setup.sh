#!/bin/bash

echo "========================================="
echo "     LLM Knowledge Copilot - Setup"
echo "========================================="

# ------------------------
# Create virtual environment
# ------------------------
echo "[1/7] Creating Python environment..."
python3 -m venv venv
source venv/bin/activate

# ------------------------
# Install backend dependencies
# ------------------------
echo "[2/7] Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# ------------------------
# Build FAISS index if needed
# ------------------------
echo "[3/7] Checking FAISS index..."
if [ ! -f "index.faiss" ]; then
    echo "No FAISS index found. Running init script..."
    python initialize_faiss.py 2>/dev/null || echo "⚠ No FAISS initializer found. Skipping."
else
    echo "FAISS index found."
fi

# ------------------------
# Start backend server
# ------------------------
echo "[4/7] Starting backend server..."
uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend running with PID: $BACKEND_PID"

# ------------------------
# Install frontend dependencies
# ------------------------
echo "[5/7] Installing frontend dependencies..."
cd ..
npm install

# ------------------------
# Start frontend
# ------------------------
echo "[6/7] Starting frontend (Vite)..."
npm run dev &
FRONTEND_PID=$!
echo "Frontend running with PID: $FRONTEND_PID"

# ------------------------
# Completion message
# ------------------------
echo "========================================="
echo " Setup complete! Your app is running at:"
echo " Frontend: http://localhost:5173"
echo " Backend : http://localhost:8000"
echo "========================================="
