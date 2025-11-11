# This file is ignored by git to keep credentials private.
# Import the environment-based config from the tracked database_env.py
from app.config.database_env import DB_CONFIG
import os
import platform

# On developer machines (Windows) or when FORCE_LOCAL_DB=1 is set, prefer
# local development database defaults. This keeps production behavior
# unchanged unless explicitly overridden.
if os.getenv("FORCE_LOCAL_DB") == "1" or platform.system() == "Windows":
	DB_CONFIG.update({
		"host": os.getenv("LOCAL_DB_HOST", "localhost"),
		"port": int(os.getenv("LOCAL_DB_PORT", os.getenv("DB_PORT", "3306"))),
		"user": os.getenv("LOCAL_DB_USER", os.getenv("DB_USER", "root")),
		"password": os.getenv("LOCAL_DB_PASSWORD", os.getenv("DB_PASSWORD", "123456")),
		"database": os.getenv("LOCAL_DB_NAME", os.getenv("DB_NAME", "ecomdb")),
	})

# You can still manually override DB_CONFIG here for this machine if needed:
# DB_CONFIG.update({
#     "password": "your_local_password"
# })
