.PHONY: setup install train seed run test docker-build docker-up clean

setup: install
	cp .env.example .env
	@echo "Edit .env with your credentials, then run: make train seed"

install:
	pip install -r backend/requirements.txt

train:
	cd backend && python -m app.ml_models.train

seed:
	python scripts/seed_db.py

run:
	cd backend && uvicorn app.main:app --reload --port 8000

test:
	pytest tests/ -v

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.db" -delete
