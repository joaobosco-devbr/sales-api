# Sales API

API REST backend desenvolvida em **Python** com **FastAPI**, seguindo boas práticas de arquitetura, autenticação e containerização com **Docker**.

Este projeto simula um backend real de sistema de vendas, com estrutura modular, persistência de dados e execução em ambiente containerizado.  
Foi desenvolvido com foco em **portfólio profissional** para vagas de estágio/júnior em backend.

---

## 🚀 Funcionalidades

- CRUD de entidades
- Autenticação com JWT
- Validação de dados
- Arquitetura em camadas:
  - Routers
  - Services
  - Repositories
- Integração com banco de dados relacional
- Execução via Docker e Docker Compose

---

## 🛠️ Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Docker
- Docker Compose
- Git

---

## 📁 Estrutura do Projeto

```text
app/
├── main.py
├── routers/
├── services/
├── repositories/
├── models/
├── schemas/
└── core/
```

---

## 🐳 Docker Compose

Exemplo de configuração utilizada para subir a API e o banco de dados:

```yaml
version: "3.9"

services:
  api:
    build: .
    container_name: sales_api
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: mysql:8.0
    container_name: sales_db
    restart: always
    environment:
      MYSQL_DATABASE: sales_db
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"
```

---

## ▶️ Como Executar o Projeto

### Pré-requisitos
- Docker
- Docker Compose

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/joaobosco-devbr/sales-api.git
```

2. Acesse o diretório do projeto:
```bash
cd sales-api
```

3. Suba os containers:
```bash
docker-compose up -d
```

4. Acesse a documentação interativa da API:
```text
http://localhost:8000/docs
```

---

## 👤 Autor

João Bosco Ferreira  
Estudante de Análise e Desenvolvimento de Sistemas (FIAP)  
Backend Developer | Python | FastAPI | SQL
