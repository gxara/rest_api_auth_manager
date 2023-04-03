from src.rest_api_auth_manager import AuthManager
import pytest


def test_token_valido__rotas_validas(auth_manager: AuthManager):
    token = auth_manager.add_user({
        "alias": "MISTY",
        "name": "MISTY",
    })
    auth_manager.add_role_to_user("MISTY", "pokemons:get")
    auth_manager.add_role_to_user("MISTY", "pokemons:post")
    auth_manager.add_role_to_user("MISTY", "pokemon_images:post")
    auth_manager.add_role_to_user("MISTY", "pokemon:get")

    assert auth_manager.verify_auth(token, "api/pokemon", "GET")
    assert auth_manager.verify_auth(token, "api/pokemon", "POST")
    assert auth_manager.verify_auth(token, "api/pokemon/1234/images", "POST")
    assert auth_manager.verify_auth(token, "api/pokemon/12", "GET")


def test_token_valido__rotas_invalidas(auth_manager: AuthManager):
    token = auth_manager.add_user({
        "alias": "NEW_USER",
        "name": "New user",
    })
    auth_manager.add_role_to_user("NEW_USER", "pokemon:post")

    with pytest.raises(AssertionError):
        assert auth_manager.verify_auth(token, "api/pokemon/1/testedevefalhar", "GET")


def test_token_invalido(auth_manager: AuthManager):
    token = "TOKEN_FALSO"
    assert auth_manager.verify_auth(token, "api/pokemon", "GET") is False
    assert auth_manager.verify_auth(token, "api/pokemon", "POST") is False
    assert auth_manager.verify_auth(token, "api/pokemon/1234/images", "POST") is False
    assert auth_manager.verify_auth(token, "api/pokemon/12", "GET") is False


def test_add_user(auth_manager: AuthManager):

    user = {
        "alias": "NEW_USER",
        "name": "New user",
        "email": "",
        "roles": [],
    }

    token = auth_manager.add_user(user)
    assert auth_manager.verify_auth(token, "api/pokemon", "GET") is False


def test_add_role_to_user(auth_manager: AuthManager):
    user = "NEW_USER"
    token = auth_manager.add_user({
        "alias": user,
        "name": "New user",
    })

    auth_manager.add_role_to_user(user, "pokemons:get")
    assert auth_manager.verify_auth(token, "api/pokemon", "GET") is True
