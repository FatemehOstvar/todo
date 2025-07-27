# ---- Stage 1: Build React frontend ----
FROM node:20-bullseye AS frontend-builder
WORKDIR /frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --verbose
COPY frontend ./
RUN yarn build

# ---- Stage 2: Build FastAPI backend ----
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY app ./app

# Copy frontend dist into backend
COPY --from=frontend-builder /frontend/dist ./frontend/dist



# Start FastAPI with frontend serving
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
