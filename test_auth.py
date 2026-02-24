import requests
import json
from uuid import UUID

BASE_URL = "http://localhost:8000"

# Primero, necesitas un role_id y company_id que existan en la BD
ROLE_ID = "e687ff93-cfec-4718-a03d-7bcbdacfef9d"  # UUID de rol que existe
COMPANY_ID = "b27ce798-2a16-47fa-89c4-0b7f8e46cda0"  # UUID de empresa que existe

# 1. Crear usuario
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Mypassw0rd@2024",
    "role_id": ROLE_ID,
    "company_id": COMPANY_ID
}

print("📝 Registrando usuario...")
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))