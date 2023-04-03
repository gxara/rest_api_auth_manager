from src.rest_api_auth_manager import AuthManager
from src.rest_api_auth_manager.config import Config
from src.rest_api_auth_manager.repository import CredentialsDatabase
import pytest
import logging


class TestConfig(Config):
    credentials_database_host = "127.0.0.1"
    environment = "dev"
    password_length = 16


@pytest.fixture(scope="session", autouse=True)
def populate_database(servicos_compose):
    logging.info("********** Populating database for tests  **********")
    auth_manager = AuthManager(TestConfig)

    # Adding resources
    resources_map = {
        "pokemon": "api_pokemon_.[^_]*$",
        "pokemons": "api_pokemon$",
        "pokemon_images": "api_pokemon_.*_images$",
    }

    for k, v in resources_map.items():
        auth_manager.add_resource(k, v)


@pytest.fixture()
def auth_manager():
    return AuthManager(TestConfig)


@pytest.fixture(scope="session", autouse=True)
def servicos_compose(docker_ip, docker_services):
    """Garante que os serviços estejam no ar antes de rodar os testes"""

    def redis_is_responsive(config):
        redis_server = CredentialsDatabase(
            host=config.credentials_database_host)
        return True if redis_server.is_alive() else False

    docker_services.wait_until_responsive(
        timeout=10,
        pause=2,
        check=lambda: redis_is_responsive(Config)
    )
