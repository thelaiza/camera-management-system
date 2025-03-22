import os
import sys
import django
from django.db import connection

def test_database_connection():
    if os.environ.get('RUN_MAIN') == 'true': 
        try:
            connection.ensure_connection()
            print("Conexão com o banco de dados estabelecida.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

def main():
    """Função principal para rodar comandos do Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()

    test_database_connection()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
