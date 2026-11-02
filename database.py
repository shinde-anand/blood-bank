
import os
import tempfile
import mysql.connector


def get_db_connection():
    ssl_ca = os.environ.get("DB_SSL_CA")

    # Render: Read certificate content from environment variable
    ssl_ca_content = os.environ.get("DB_SSL_CA_CONTENT")

    if ssl_ca_content:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".pem",
            delete=False
        ) as cert_file:
            cert_file.write(ssl_ca_content)
            ssl_ca = cert_file.name

    connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3307")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get(
            "DB_NAME", "blood_bank_management"
        ),
        connection_timeout=20,
        ssl_ca=ssl_ca,
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )

    return connection
