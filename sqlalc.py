from sqlalchemy import create_engine

engine = create_engine('mssql://guilherme.breve:84584608Guilherme@10.56.6.56/DW_Vista?driver=SQL Server')

conn = engine.connect()