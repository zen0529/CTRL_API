# 🔨 Build and run containers fresh
up:
	docker-compose up --build

# 🚀 Start containers without rebuilding (faster)
start:
	docker-compose up

# 💣 Stop and remove all containers, networks, and volumes
down:
	docker-compose down

# 🔁 Rebuild everything from scratch (forces rebuild)
rebuild:
	docker-compose down
	docker-compose up --build

# 🧼 Clean up everything including dangling images/volumes
clean:
	docker system prune -af
