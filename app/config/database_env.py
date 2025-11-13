"""
Environment-based database configuration that can be safely committed.
This module reads database settings from environment variables and provides
a consistent DB_CONFIG dict for database connections.
"""

import os
from typing import Dict, Any
from urllib.parse import urlparse, parse_qs
from pymysql.cursors import DictCursor

def _parse_database_url(url: str) -> Dict[str, Any]:
    """Parse a DATABASE_URL into PyMySQL connection parameters."""
    parsed = urlparse(url)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 3306,
        "user": parsed.username or "root",
        "password": parsed.password or "",
        "database": parsed.path.lstrip('/') if parsed.path else "ecomdb",
        "cursorclass": DictCursor,
    }

def get_db_config() -> Dict[str, Any]:
    """
    Get database configuration from environment variables.
    Priority:
    1. DATABASE_URL if set
    2. Individual DB_* variables
    3. Default local development values
    """
    if database_url := os.getenv("DATABASE_URL"):
        config = _parse_database_url(database_url)
    else:
        config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "ecomdb"),
            "cursorclass": DictCursor,
        }

    if ssl_ca := os.getenv("DB_SSL_CA"):
        config["ssl"] = {"ca": ssl_ca}
    
    return config

DB_CONFIG = get_db_config()