# 1️⃣ Use official Python image
FROM python:3.12-slim

# 2️⃣ Set working directory
WORKDIR /CTRL_API

# 3️⃣ Copy everything
COPY . .

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Expose FastAPI default port
EXPOSE 8000

# 6️⃣ Default command (can be overridden in docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
