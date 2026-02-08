import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.database import DataBaseConfig
from sqlalchemy import text

print("=" * 50)
print("TESTING CONNECTION WITH SQLSERVER")
print("=" * 50)

if DataBaseConfig.test_connection('sqlserver'):
    print("\n Connection successfully established!")

    try:
        engine = DataBaseConfig.create_engine('sqlserver')
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    TABLE_SCHEMA,
                    TABLE_NAME,
                    TABLE_TYPE
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """))

            tabelas = result.fetchall()
            print(f"\n Banco: ECOMMERCE")
            print(f" Tables found: {len(tabelas)}")

            if tabelas:
                print("\nFirst 5 tables: ")
                for i, tabela in enumerate(tabelas[:5], 1):
                    print(f" {i}. {tabela[0]}.{tabela[1]} ({tabela[2]})")
            else:
                print("\n Empty database -  ready to receive data")
        
    except Exception as e:
        print(f"\n Connected, but error listing tables: {str(e)}")

else:
    print("\n Connection failure. Please check")
    print("  1. SQL Server is running")
    print("  2. Correct instance: DESKTOP-N3CE6QU")
    print("  3. ECOMMERCE database exists")
    print("  4. Windows Authentication is enable")

print("\n " + "=" * 50)
