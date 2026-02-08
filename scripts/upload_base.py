import pandas as pd
import numpy as np
import os 
import logging
import argparse
from datetime import datetime
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import (
    BigInteger, Integer, Float, Boolean, DateTime, Text
)

from tqdm import tqdm
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import DataBaseConfig
from utils.database_utils import DataUploader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/upload.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AutomatedDataUploader:
    def __init__(self, db_type='postgresql', chunk_size=10000):
        self.db_type = db_type
        self.chunk_size = chunk_size
        self.engine = None

    def connect(self):
        try:
            self.engine = DataBaseConfig.create_engine(
                db_type=self.db_type,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True
            )

            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            self.uploader = DataUploader(self.engine)
            logger.info(f"Conexão estabelecida com {self.db_type.upper()}")
            return True
        
        except Exception as e:
            logger.error(f"Erro na conexão: {str(e)}")
            return False
        
    def find_data_files(self, data_dir='data/processsed'):
        supported_formats = ['.csv', '.parquet', '.xlsx', '.xls', '.json']
        data_files = []

        for root, dir, files in os.walk(data_dir):
            for file in files:
                if any(file.endswith(ext) for ext in supported_formats):
                    full_path = os.path.join(root, file)
                    data_files.append({
                        'path': full_path,
                        'name': file,
                        'ext': os.path.splitext(file)[1],
                        'table_name': self._generate_table_name(file)
                    })

        logger.info(f"Encontrados {len(data_files)} arquivos de dados")
        return data_files
    
    def _generate_table_name(self, filename):

        name = os.path.splitext(filename)[0]
        name = name.lower()
        name = ''.join(c if c.isalnum() else '_' for c in name)
        name = '_'.join(name.split())
        return name.rstrip('_')
    
    def infer_schema(self, df, table_name):


        from sqlalchemy.dialects.mssql import NVARCHAR

        type_mapping = {
            'int64': BigInteger(),
            'int32': Integer(),
            'float64': Float(),
            'float32': Float(),
            'object': NVARCHAR(length='max'),
            'bool': Boolean(),
            'datetime64[ns]': DateTime(),
            'category': NVARCHAR(length='max')
        }

        schema = {}
        for col in df.columns:
            dtype = str(df[col].dtype)
            schema[col] = type_mapping.get(dtype, NVARCHAR(length='max'))

        return schema
        
    def load_data(self, file_info):
        try:
            ext = file_info['ext'].lower()

            if ext == '.csv':
                df = pd.read_csv(file_info['path'], low_memory=False)
            elif ext == '.parquet':
                df = pd.read_parquet(file_info['path'])
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_info['path'])
            elif ext == '.json':
                df = pd.read_json(file_info['path'])
            else:
                raise ValueError(f"Formato não suportado: {ext}")
            
            df.columns = df.columns.str.lower()
            df.columns = df.columns.str.replace(' ', '_')
            
            logger.info(f"Carregado: {file_info['name']} - {len(df)} registros")
            return df
        
        except Exception as e:
            logger.error(f"Erro ao carregar {file_info['name']}: {str(e)}")
            return None
        
    def upload_dataframe(self, df, table_name, if_exists='replace'):

        try:
            total_rows = len(df)
            df = self._optimize_dataframe(df)
            
            schema = self.infer_schema(df, table_name)

            base_chunk = self.chunk_size

            logger.info(f"Iniciando upload de {table_name} ({total_rows} linhas)")

            with tqdm(total=total_rows, desc=f"Upload {table_name}") as pbar:

                for start in range(0, total_rows, base_chunk):
                    end = min(start + base_chunk, total_rows)
                    chunk = df.iloc[start:end]

                    try:
                        chunk.to_sql(
                            table_name,
                            self.engine,
                            if_exists=if_exists if start == 0 else 'append',
                            index=False,
                            dtype=schema,
                            method='multi',
                            chunksize=1000  
                        )
                        
                        pbar.update(len(chunk))
                        logger.info(f"Chunk {start}:{end} inserido com sucesso")

                    except Exception as e:
                        logger.warning(f"Falha chunk {start}:{end}, tentando fallback menor...")

                        # Fallback automático
                        small_chunk = 200

                        for sub_start in range(start, end, small_chunk):
                            sub_end = min(sub_start + small_chunk, end)
                            sub_chunk = df.iloc[sub_start:sub_end]

                            sub_chunk.to_sql(
                                table_name,
                                self.engine,
                                if_exists='append',
                                index=False,
                                dtype=schema,
                                method='multi',
                                chunksize=200
                            )

                            pbar.update(len(sub_chunk))

                    

                pbar.update(len(chunk))

            logger.info(f"Upload concluído: {table_name}")
            return True

        except Exception:
            logger.exception(f"Erro fatal no upload de {table_name}")
            return False

    
    def _optimize_dataframe(self, df):
        for col in df.select_dtypes(include=['datetime64[ns]']).columns:
            df[col] = pd.to_datetime(df[col])

        df = df.replace([np.inf, -np.inf], np.nan)

        for col in df.select_dtypes(include=['category']).columns:
            df[col] = df[col].astype(str)

        return df
    
    def create_indexes(self, table_name, index_columns=None):
        if not index_columns:
            return
        
        try:
            with self.engine.connect() as conn:
                for col in index_columns:
                    index_name = f"idx_{table_name}_{col}"
                    sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({col})"

                    if self.db_type == 'mysql':
                        sql = f"CREATE INDEX {index_name} ON {table_name} ({col})"

                    conn.execute(text(sql))
                    conn.commit()

                logger.info(f"Indices criados para {table_name}")
            
        except Exception as e:
            logger.warning(f"Não foi possível criar índices: {str(e)}")
    
    def run_upload(self, data_dir='data/processed', if_exists='replace'):
        start_time = datetime.now()
        logger.info("Iniciando upload de dados...")

        if not self.connect():
            return False
        

        data_files = self.find_data_files(data_dir)

        if not data_files:
            logger.warning("Nenhum arquivo de dados encontrados")
            return False
        
        results = []

        for file_info in data_files:

            logger.info(f"Processando: {file_info['name']}")

            df = self.load_data(file_info)

            if df is not None and not df.empty:
                
                print("\n======= DEBUG =======")
                print(df.dtypes)
                print(df.isna().sum())
                print("=====================\n")

                success = self.upload_dataframe(
                    df,
                    file_info['table_name'],
                    if_exists=if_exists
                )

                if success:

                    potencial_index_cols = ['id', 'data', 'codigo', 'timestamp']
                    existing_cols = [col for col in potencial_index_cols if col in df.columns]

                    if existing_cols:
                        self.create_indexes(file_info['table_name'], existing_cols[:2])

                results.append({
                    'arquivo': file_info['name'],
                    'tabela': file_info['table_name'],
                    'registros': len(df),
                    'sucesso': success
                })

                elapsed = datetime.now() - start_time
                self._generate_report(results, elapsed)

        return True
            
    def _generate_report(self, results, elapsed_time):
        report = f"""
        {'='*50} 
        RELATÓRIO DE UPLOAD
        {'='*50}
        Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Tempo total: {elapsed_time}
        {'='*50}

        RESUMO
        Total de arquivos: {len(results)}
        Sucessos: {sum(1 for r in results if r['sucesso'])}
        Falhas: {sum(1 for r in results if not r['sucesso'])}

        DETALHES:
        """

        for result in results:
            status = "OK" if result['sucesso'] else "X"
            
            arquivo = result.get('arquivo', result.get('name', 'Desconhecido'))
            tabela = result.get('table_name', result.get('tabela', 'Desconhecido'))
            registros = result.get('registros', result.get('registro', 0))
            
            report += f"{status} {arquivo} -> {tabela} ({registros} registros)\n"
        
        report += f"\n{'='*50}"

        print(report)

        with open('logs/upload_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"Relatório gerado em logs/upload_report.txt")

def main():
    parser = argparse.ArgumentParser(description="Upload automatizado de dados para banco")

    parser.add_argument('--db-type', default='postgresql',
                        choices=['postgresql', 'mysql', 'sqlite', 'sqlserver'],
                        help='Tipo de banco de dados')

    parser.add_argument('--data-dir', default='data/processed',
                        help='Diretorio com dados processados')
        
    parser.add_argument('--if-exists', default='replace',
                        choices=['replace', 'append', 'fail'],
                        help='Comportamento se tabela existir')
        
    parser.add_argument('--chunk-size', type=int, default=10000,
                        help='Tamanho do chunk para upload')
        
    args = parser.parse_args()

    os.makedirs('logs', exist_ok=True)

    uploader = AutomatedDataUploader(
        db_type=args.db_type,
        chunk_size=args.chunk_size
    )

    sucess = uploader.run_upload(
        data_dir=args.data_dir,
        if_exists=args.if_exists
    )

    if sucess:
        logger.info("Processo concluído com sucesso!")
        sys.exit(0)
    else:
        logger.error("Processo concluído com erros!")
        sys.exit(1)



if __name__ == "__main__":
    main()
