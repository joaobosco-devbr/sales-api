# Sales API (FastAPI + SQLModel + MySQL)

Projeto exemplo pronto para deploy local / server Ubuntu.

## O que tem
- CRUD de produtos
- Autenticação JWT (signup/login)
- Endpoints para criar pedidos
- Docker + Docker Compose (MySQL + app)
- Testes com pytest
- README com exemplos de requests

## Rodando com Docker Compose (recomendado)
1. Ajuste `.env` se necessário.
2. `docker-compose up --build`
3. Acesse docs: http://localhost:8000/docs

## Rodando sem Docker (rápido, usando SQLite para testes)
1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. export DATABASE_URL=sqlite:///./test.db
5. uvicorn app.main:app --reload

## Testes (usando SQLite local)
1. export DATABASE_URL=sqlite:///./test.db
2. pytest -q

## Testes manuais (curl)
# Signup
curl -X POST "http://localhost:8000/signup" -H "Content-Type: application/json" -d '{"username":"me","password":"secret"}'
# Get token
curl -X POST "http://localhost:8000/token" -d "username=me&password=secret"
# Create product (use token from previous step)
curl -X POST "http://localhost:8000/products" -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d '{"name":"Caneca","description":"Caneca legal","price":25.0,"stock":10}'

