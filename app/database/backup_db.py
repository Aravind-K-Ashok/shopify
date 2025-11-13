import subprocess
from pathlib import Path
from datetime import datetime
from app.config.database import DB_CONFIG

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(__file__).parent.parent / "database_backup"
    backup_dir.mkdir(exist_ok=True)
    
    schema_file = backup_dir / f"schema_{timestamp}.sql"
    subprocess.run([
        "mysqldump",
        "-h", DB_CONFIG["host"],
        "-u", DB_CONFIG["user"],
        f"-p{DB_CONFIG['password']}",
        "--no-data",
        DB_CONFIG["database"],
        "-r", str(schema_file)
    ], check=True)

    data_file = backup_dir / f"data_{timestamp}.sql"
    subprocess.run([
        "mysqldump",
        "-h", DB_CONFIG["host"],
        "-u", DB_CONFIG["user"],
        f"-p{DB_CONFIG['password']}",
        "--no-create-info",
        "--complete-insert",
        DB_CONFIG["database"],
        "-r", str(data_file)
    ], check=True)

    print(f"Backup completed:\nSchema: {schema_file}\nData: {data_file}")

if __name__ == "__main__":
    backup_database()