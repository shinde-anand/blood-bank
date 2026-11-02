
import os
import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3307")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get(
            "DB_NAME", "blood_bank_management"
        ),
        connection_timeout=20,
        ssl_ca=os.environ.get("DB_SSL_CA"),
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )

    return connection
