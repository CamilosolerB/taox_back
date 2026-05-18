import requests
import json
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

print("=== Full Debug Login Test ===\n")

url = "http://127.0.0.1:8000/auth/login"
data = {"email": "test@example.com", "password": "Mypassw0rd@2024"}

print(f"Request URL: {url}")
print(f"Request Data: {json.dumps(data)}")
print()

try:
    # Make request with full logging
    response = requests.post(url, json=data, timeout=10)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"Error Response: {e.response.text}")

print("\n=== Test Direct DB Verification ===")

# Verify directly in Python
from app.core.security import verify_password, create_access_token
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.user_orm_repository import UserORMRepository
from datetime import timedelta

session = next(get_session())
repo = UserORMRepository(session)

user = repo.get_user_by_email("test@example.com")
if user:
    print(f"\nUser from DB: {user.username}")
    print(f"User email: {user.email}")
    print(f"User password hash: {user.password[:50]}...")
    print(f"User is_active: {user.is_active}")
    
    # Test password
    test_pwd = "Mypassw0rd@2024"
    pwd_valid = verify_password(test_pwd, user.password)
    print(f"\nPassword verification: {pwd_valid}")
    
    if pwd_valid:
        # Generate token manually
        token_data = {
            "sub": str(user.id_user),
            "username": user.username,
            "email": user.email,
            "role_id": str(user.role_id),
            "company_id": str(user.company_id),
            "is_active": user.is_active
        }
        token = create_access_token(token_data, timedelta(minutes=30))
        print(f"\nGenerated Token: {token[:50]}...")
        print("\nMANUAL TOKEN GENERATION SUCCESSFUL")
else:
    print("\nUser not found in DB!")

session.close()