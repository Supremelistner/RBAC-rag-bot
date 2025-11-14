import json
import os

DEFAULT_ROLES = {
    "Finance": ["finance_docs", "general_docs"],
    "Marketing": ["marketing_docs", "general_docs"],
    "HR": ["hr_docs", "general_docs"],
    "Engineering": ["engineering_docs", "general_docs"],
    "C_Level": ["finance_docs", "marketing_docs", "hr_docs", "engineering_docs", "c_level_docs", "general_docs"],
    "Employee": ["general_docs"]
}

ROLES_CONFIG_PATH = os.getenv("ROLES_CONFIG_PATH", "backend/auth/roles_config.json")

def load_roles_config():
    try:
        with open(ROLES_CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_ROLES
    
_roles=load_roles_config()

def allowed_docs(role: str) -> list:
    return _roles.get(role, [])

def access_of_role(role: str, document: str) -> bool:
    return document in allowed_docs(role)
