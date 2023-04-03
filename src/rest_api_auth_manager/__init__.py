import re
from .repository import CredentialsDatabase
from .config import Config
import json
import random
import string
import logging


class AuthManager:

    def __init__(self, config: Config):
        self._config = config
        self._credentials_repository = CredentialsDatabase(config.credentials_database_host)

    def verify_auth(self, token: str, route: str, method: str) -> bool:
        """
        Verify if the user has permission to access the route with the HTTP method
        requested

        args:
            token: the user's token
            route: the route requested
            method: the HTTP method requested

        returns:
            True if the user has permission to access the route with the HTTP method
            requested, False otherwise
        """
        user_name = self._credentials_repository.hget("CREDENTIALS", token)

        if not user_name:
            return False

        user_details = self._credentials_repository.get_user(user_name)
        user_roles = user_details["roles"]
        permission_set = self._build_user_permissions(user_roles)

        if not permission_set:
            logging.debug("User has no permissions")
            return False

        requested_route = route.replace("/", "_").replace("-", "_").lower()
        methods_for_resource = {}

        # Verify if resource is valid using REGEX
        for resource in permission_set:
            if re.search(resource, requested_route):
                methods_for_resource = permission_set[resource]

        if method.lower() in methods_for_resource:
            return True
        return False

    def add_user(self, details: dict) -> str:
        """
        Create a new user and add it to the credentials repository
        """
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters)
                           for _ in range(self._config.password_length))

        token = self._config.environment + "_" + password

        self._credentials_repository.insert_hash("USERS", details["alias"],  json.dumps(details))
        self._credentials_repository.insert_hash("CREDENTIALS", token,  details["alias"])

        return token

    def add_role_to_user(self, user: str, role: str) -> None:
        """
        Assign a role to a user

        args:
            user: the user to which the role will be assigned
            role: the role to be assigned to the user

        Example:
            user: "ASH_KETCHUM"
            role: "pokemon:get"
        """

        user_details = json.loads(self._credentials_repository.hget("USERS", user))

        roles = user_details.get("roles", [])

        self._credentials_repository.insert_hash(
            "USERS", user, json.dumps({**user_details, "roles": [*roles, role]}))

    def add_resource(self, resource: str, path: str) -> None:
        """
        Add a new resource to the resources map
        args:
            resource: the unique name of the resource
            path: the path to the resource (using REGEX syntax)

        Example:
            resource: "pokemon"
            path: "api_pokemon_.[^_]*$"

        """
        resources_map = self._credentials_repository.get_resources_map()
        if resource in resources_map:
            logging.warning(f"Resource {resource} already exists")
            return

        resources_map[resource] = path

        self._credentials_repository.insert("RESOURCES_MAP", resources_map)

    def _build_user_permissions(self, user_roles: set) -> dict:
        user_permissions = {}
        resources_map = self._credentials_repository.get_resources_map()
        for role in user_roles:
            resource = role.split(":")[0]
            resource_path = resources_map.get(resource, None)
            if not resource_path:
                logging.debug(f"Resource {resource} does not exist")
                continue
            method = role.split(":")[1]
            user_permissions.setdefault(resource_path, set()).add(method)
        return user_permissions
