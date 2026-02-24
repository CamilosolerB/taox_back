import requests
import json
from uuid import UUID

BASE_URL = "http://localhost:8000"

# IDs que existen en la BD
ROLE_ID = "e687ff93-cfec-4718-a03d-7bcbdacfef9d"
COMPANY_ID = "b27ce798-2a16-47fa-89c4-0b7f8e46cda0"

# 1️⃣ REGISTRO
print("=" * 60)
print("1️⃣ REGISTRANDO USUARIO...")
print("=" * 60)

register_data = {
    "username": "testuser2024",
    "email": "test2024@example.com",
    "password": "Mypassw0rd@2024",
    "role_id": ROLE_ID,
    "company_id": COMPANY_ID
}

print(f"\nDatos de registro: {json.dumps(register_data, indent=2)}")
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(f"\n✓ Status: {response.status_code}")

if response.status_code == 201:
    print("✓ Registro exitoso!")
    token_data = response.json()
    print(json.dumps(token_data, indent=2))
    token = token_data.get("access_token")
else:
    print("✗ Error en registro:")
    print(json.dumps(response.json(), indent=2))
    token = None

# 2️⃣ LOGIN
print("\n" + "=" * 60)
print("2️⃣ HACIENDO LOGIN...")
print("=" * 60)

login_data = {
    "email": "test2024@example.com",
    "password": "Mypassw0rd@2024"
}

print(f"\nDatos de login: {json.dumps(login_data, indent=2)}")
print(f"Endpoint: POST {BASE_URL}/auth/login")

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"\n✓ Status: {response.status_code}")

if response.status_code == 200:
    print("✓ Login exitoso!")
    print(json.dumps(response.json(), indent=2))
else:
    print("✗ Error en login:")
    print(json.dumps(response.json(), indent=2))

# 3️⃣ TEST CON JWT
if token:
    print("\n" + "=" * 60)
    print("3️⃣ PROBANDO ENDPOINT PROTEGIDO CON JWT...")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        f"{BASE_URL}/providers?company_id={COMPANY_ID}",
        headers=headers
    )
    print(f"\n✓ Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
