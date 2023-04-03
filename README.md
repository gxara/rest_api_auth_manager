# rest-api-simple-auth-manager

Simple REST API authentication and authorization manager, designed to operate with token-based security. This package is intended to act as a middleware, providing a secure method for verifying user credentials before granting access to the requested resource.

The current implementation relies on a Redis instance to store and manage credentials. However, we are working on integrating other database options to offer more flexibility and customization.

### Install

```bash
pip install rest_api_auth_manager
```

### Initializing the auth manager

```python
from rest_api_auth_manager import AuthManager, Config

class CustomConfig(Config):
    credentials_database_host = "127.0.0.1"
    environment = "dev"
    password_length = 16

auth_manager = AuthManager(CustomConfig)
```

### Add new user

```python
user = {
    "alias": "ASH_KETCHUM",
    "name": "Ash Ketchum",
    "email": "ash@test.com",
    "roles": [],
}

token = auth_manager.add_user(user)
```

### Granting usage on a specific resource

```python
auth_manager.add_role_to_user("ASH_KETCHUM", "pokemons:get")
```

### Verifying requests authentication and authorization

```python
token = "SUPER_SECRET"
auth_manager.verify_auth(token, "api/pokemon", "GET")
```
