"""
Script para probar los endpoints de autenticación
Usa pytest o ejecuta manualmente con requests
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

class AuthTester:
    """Clase auxiliar para probar autenticación"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_data = {}
    
    def register(self, username: str, email: str, password: str, 
                role_id: str, company_id: str) -> dict:
        """Registra un nuevo usuario"""
        url = f"{self.base_url}/auth/register"
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "role_id": role_id,
            "company_id": company_id
        }
        response = requests.post(url, json=payload)
        print(f"REGISTER: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.user_data = data
        
        return response.json()
    
    def login(self, email: str, password: str) -> dict:
        """Hace login con un usuario existente"""
        url = f"{self.base_url}/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload)
        print(f"LOGIN: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.user_data = data
        
        return response.json()
    
    def get_current_user(self) -> dict:
        """Obtiene la información del usuario actual"""
        if not self.token:
            print("ERROR: No hay token. Primero haz login o registro")
            return {}
        
        url = f"{self.base_url}/auth/me"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        print(f"GET /auth/me: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        return response.json()
    
    def get_users(self) -> dict:
        """Obtiene lista de usuarios (requiere autenticación)"""
        if not self.token:
            print("ERROR: No hay token. Primero haz login o registro")
            return {}
        
        url = f"{self.base_url}/users/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        print(f"GET /users/: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        return response.json()
    
    def create_user(self, username: str, email: str, password: str,
                   role_id: str, company_id: str) -> dict:
        """Crea un nuevo usuario (requiere rol admin)"""
        if not self.token:
            print("ERROR: No hay token. Primero haz login o registro")
            return {}
        
        url = f"{self.base_url}/users/"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "is_active": True,
            "role_id": role_id,
            "company_id": company_id
        }
        response = requests.post(url, json=payload, headers=headers)
        print(f"POST /users/: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        return response.json()


# Ejemplo de uso
if __name__ == "__main__":
    tester = AuthTester()
    
    # Reemplaza estos valores con los UUIDs reales de tu BD
    ADMIN_ROLE_ID = "550e8400-e29b-41d4-a716-446655440000"
    OBSERVER_ROLE_ID = "550e8400-e29b-41d4-a716-446655440001"
    COMPANY_ID = "550e8400-e29b-41d4-a716-446655440002"
    
    print("\n" + "="*60)
    print("1. REGISTRAR UN USUARIO ADMIN")
    print("="*60)
    tester.register(
        username="admin_user",
        email="admin@example.com",
        password="AdminPass123!",
        role_id=ADMIN_ROLE_ID,
        company_id=COMPANY_ID
    )
    
    print("\n" + "="*60)
    print("2. OBTENER INFO DEL USUARIO ACTUAL")
    print("="*60)
    tester.get_current_user()
    
    print("\n" + "="*60)
    print("3. LISTAR USUARIOS (requiere autenticación)")
    print("="*60)
    tester.get_users()
    
    print("\n" + "="*60)
    print("4. CREAR OTRO USUARIO (requiere rol admin)")
    print("="*60)
    tester.create_user(
        username="observer_user",
        email="observer@example.com",
        password="ObserverPass123!",
        role_id=OBSERVER_ROLE_ID,
        company_id=COMPANY_ID
    )
    
    print("\n" + "="*60)
    print("5. LOGOUT E INTENTAR HACER LOGIN CON NUEVO USUARIO")
    print("="*60)
    tester.login(
        email="observer@example.com",
        password="ObserverPass123!"
    )
    
    print("\n" + "="*60)
    print("6. INTENTAR CREAR USUARIO CON ROL OBSERVER (debe fallar)")
    print("="*60)
    tester.create_user(
        username="another_user",
        email="another@example.com",
        password="AnotherPass123!",
        role_id=OBSERVER_ROLE_ID,
        company_id=COMPANY_ID
    )
    
    print("\n" + "="*60)
    print("Pruebas completadas")
    print("="*60)
