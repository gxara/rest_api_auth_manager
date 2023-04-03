from src.rest_api_auth_manager import AuthManager
import pytest


def test_token_valido__rotas_validas(auth_manager: AuthManager):
    token = auth_manager.add_user({
        "alias": "NEW_USER",
        "name": "New user",
    })
    auth_manager.add_role_to_user("NEW_USER", "service_orders:get")
    auth_manager.add_role_to_user("NEW_USER", "service_orders:post")
    auth_manager.add_role_to_user("NEW_USER", "service_orders_images:post")
    auth_manager.add_role_to_user("NEW_USER", "service_order:get")

    assert auth_manager.verify_auth(token, "api/service-orders", "GET")
    assert auth_manager.verify_auth(token, "api/service-orders", "POST")
    assert auth_manager.verify_auth(
        token, "api/service-orders/1234/images", "POST")
    assert auth_manager.verify_auth(token, "api/service-orders/12", "GET")


def test_token_valido__rotas_invalidas(auth_manager: AuthManager):
    token = auth_manager.add_user({
        "alias": "NEW_USER",
        "name": "New user",
    })
    auth_manager.add_role_to_user("NEW_USER", "service_orders:post")

    with pytest.raises(AssertionError):
        assert auth_manager.verify_auth(
            token, "api/service-orders/1/testedevefalhar", "GET")


def test_token_invalido(auth_manager: AuthManager):
    token = "TOKEN_FALSO"
    assert auth_manager.verify_auth(
        token, "api/service-orders", "GET") is False
    assert auth_manager.verify_auth(
        token, "api/service-orders", "POST") is False
    assert auth_manager.verify_auth(
        token, "api/service-orders/1234/images", "POST") is False
    assert auth_manager.verify_auth(
        token, "api/service-orders/12", "GET") is False


def test_add_user(auth_manager: AuthManager):

    user = {
        "alias": "NEW_USER",
        "name": "New user",
        "email": "",
        "roles": [],
    }

    token = auth_manager.add_user(user)
    assert auth_manager.verify_auth(
        token, "api/service-orders", "GET") is False


def test_add_role_to_user(auth_manager: AuthManager):
    user = "NEW_USER"
    role = "service_orders:get"
    token = auth_manager.add_user({
        "alias": user,
        "name": "New user",
    })

    auth_manager.add_role_to_user(user, role)
    assert auth_manager.verify_auth(token, "api/service-orders", "GET") is True
