from sqlalchemy import MetaData, Table, Column, inspect
from sqlalchemy.types import Integer, String, Float, DateTime, Boolean
import pandas as pd


class DataUploader:

    def __init__(self, engine):
        self.engine = engine
        self.metadata = MetaData()

    def table_exists(self, table_name):
        return inspect(self.engine).has_table(table_name)
    
    def get_table_info(self, table_name):
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        return {
            'columns': columns,
            'primary_keys': inspector.get_pkconstraint(table_name),
            'foreing_keys': inspector.get_foreign_keys(table_name)
        }
    
    def execute_query(self, query, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(query, params or {})
            conn.commit()
            return result