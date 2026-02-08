import os
from dotenv import load_dotenv 
from sqlalchemy import create_engine

load_dotenv()

class DataBaseConfig:

#Configurar o banco de dados

    DATABASE_TYPES= {
        'postgresql' : 'PostGreSQL',
        'mysql' : 'MySQL',
        'sqlite': 'SQLite',
        'sqlserver': 'SQL Server',  
        'mssql': 'SQL Server' 

    }

    @staticmethod
    def get_connection_string(db_type = 'postgresql'):

        if db_type == 'postgresql':
            return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"\
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        
        elif db_type == 'mysql':
            return f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"\
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        
        elif db_type == 'sqlite':
            return f"sqlite:///{os.getenv('DB_PATH', 'data/database.db')}"
        
        elif db_type in ['sqlserver', 'mysql']:
                # STRING SUPER SIMPLES que FUNCIONA
            return "mssql+pyodbc://DESKTOP-N3CE6QU/ECOMMERCE?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

            """
            host = os.getenv('SQLSERVER_HOST', 'localhost')
            database = os.getenv('SQLSERVER_DB', 'master')
            driver = os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 17 for SQL Server')

            if not os.getenv('SQLSERVER_USER'):
            
                connection_string = (
                    f"DRIVER={{{driver}}};"
                    f"SERVER={host};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )

                import urllib.parse
                params = urllib.parse.quote_plus(connection_string)
        
                return f"mssql+pyodbc:///?odbc_connect={params}"
            
            else:

                return(
                    f"mssql+pyodbc://{os.getenv('SQLSERVER_USER')}:"
                    f"{os.getenv('SQLSERVER_PASS')}@"
                    f"{os.getenv('SQLSERVER_HOST')}:"
                    f"{os.getenv('SQLSERVER_PORT', '1433')}/"
                    f"{os.getenv('SQLSERVER_DB')}?"
                    f"driver={driver.replace(' ', '+')}&"
                    f"TrustServerCertificate=yes"
                )
            """
        
        else:
            raise ValueError(f"Database type not supported: {db_type}")
        
    @staticmethod
    def create_engine(db_type='sqlserver', **kwargs):
        connection_string = DataBaseConfig.get_connection_string(db_type)

        default_kwargs = {}

        if db_type in ['sqlserver', 'mysql']:

            default_kwargs = {
                'fast_executemany': True,
                'pool_pre_ping': True,
                'pool_size': 10,
                'max_overflow': 20,
                'pool_recycle': 3600,
                'echo': False,
                'isolation_level': 'READ COMMITTED'
            }

        elif db_type == 'postgresql':
            default_kwargs = {
                'pool_size': 10,
                'max_overflow': 20,
                'pool_pre_ping': True

            } 

        elif db_type == 'mysql':
            default_kwargs = {
                'pool_size': 10,
                'pool_pre_ping': True
            }

        default_kwargs.update(kwargs)

        import warnings
        from sqlalchemy import exc
        warnings.filterwarnings('ignore', category=exc.SAWarning)

        return create_engine(connection_string, **default_kwargs)
    
    @staticmethod
    def test_connection(db_type='postgresql'):
       
        try:
            from sqlalchemy import text  # IMPORTANTE!
            engine = DataBaseConfig.create_engine(db_type)
        
            with engine.connect() as conn:
                if db_type in ['sqlserver', 'mssql']:
                    # SEMPRE use text() para queries no SQLAlchemy 2.0+
                    result = conn.execute(text("SELECT @@SERVERNAME as server, DB_NAME() as db"))
                    row = result.fetchone()
                    print(f"✅ SQL Server conectado!")
                    print(f"   Servidor: {row.server}")
                    print(f"   Banco: {row.db}")
                    return True
                else:
                    # Outros bancos
                    conn.execute(text("SELECT 1"))
                    print(f"✅ {db_type.upper()} conectado!")
                    return True
                
        except Exception as e:
            print(f"❌ Erro {db_type.upper()}: {str(e)[:100]}")
            return False
        
    @staticmethod
    def get_available_odbc_drivers():
        try:
            import pyodbc
            drivers = pyodbc.drivers()
            print("Available ODBC drivers:")
            for i, driver in enumerate(drivers, 1):
                print(f"  {i}. {driver}")
            return drivers
        except ImportError:
            print("pyodbc not installed. Install with: pip install pyodcb")
            return []