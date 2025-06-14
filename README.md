# API Orders

API REST de gestion des commandes pour un système de microservices, développée avec **FastAPI**, utilisant **MongoDB** comme base de données et **RabbitMQ** pour la communication interservices.

---

## Fonctionnalités

- Authentification via JWT (JSON Web Token)
- CRUD complet des commandes (`POST`, `GET`, `DELETE`)
- Publication de messages RabbitMQ (`order_created`)
- Monitoring Prometheus (`/metrics`)
- CI via GitHub Actions
- Analyse qualité de code via SonarCloud
- Conteneurisée avec Docker

---

## Stack technique

- **Python 3.11**
- **FastAPI**
- **MongoDB**
- **RabbitMQ**
- **Pydantic v2**
- **Uvicorn**
- **Docker**
- **GitHub Actions**
- **SonarCloud**

---

## Arborescence du projet

```
api-orders/
├── app/
│   ├── models/            # Schémas Pydantic (Order)
│   ├── routes/            # Endpoints FastAPI
│   ├── services/          # Logique métier
│   ├── messaging/         # RabbitMQ (publisher)
│   ├── security/          # Authentification JWT
│   ├── db/                # Connexion MongoDB
│   ├── config.py          # Chargement .env
│   └── main.py            # Point d'entrée FastAPI
├── tests/                 # Tests unitaires avec Pytest
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env.example
└── README.md
```

---

## Lancement local

### 1. Cloner le repo

```bash
git clone https://github.com/AdrianeRuggiero/MSPR_4_api-orders.git
cd MSPR_4_api-orders
```

### 2. Créer un `.env` à partir de l’exemple

```bash
cp .env.example .env
```

### 3. Lancer l’API avec Uvicorn

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L’API sera accessible sur : http://localhost:8000

---

## Lancement via Docker

```bash
docker build -t api-orders .
docker run -d -p 8000:8000 --env-file .env api-orders
```

---

## Exemples de requêtes

### Authentification (POST /token)
```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=any"
```

### Créer une commande (POST /orders/)
```json
{
  "client_id": "abc123",
  "products": [
    { "product_id": "p1", "quantity": 2 }
  ],
  "total_price": 49.99
}
```

---

## Lancer les tests

```bash
pytest --cov=app --cov-report=term-missing tests/
```
