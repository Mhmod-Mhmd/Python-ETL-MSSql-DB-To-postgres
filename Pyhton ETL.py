#import needed libraries
from sqlalchemy import create_engine
import pyodbc
import pandas as pd


#sql db details
driver = "{SQL Server}"
server = "DESKTOP-BUN7963\SQL2019"
database = "AdventureWorksDW2019;"
# MS SQL server username and password
pwd = 'etlpass'
uid = 'etl'

# Postgresql db details
pgserver='localhost'
pgdatabase = 'Ad_Works'
# Pgadmin username and password
pwd2='002001'
uid2='postgres'

#extract data from sql server
def extract():
    try:
        src_conn = pyodbc.connect('DRIVER=' + driver + 
                                  ';SERVER=' + server +
                                  ';DATABASE=' + database +
                                  ';UID=' + uid +
                                  ';PWD=' + pwd )
        
        src_cursor = src_conn.cursor()
        # execute query
        src_cursor.execute(""" select  t.name as table_name
                               from sys.tables t 
                               where t.name in (
                                                'DimProduct',
                                                'DimProductSubcategory',
                                                'DimProductCategory',
                                                'DimSalesTerritory',
                                                'DimDate',
                                                'DimCustomer',
                                                'DimEmployee',
                                                'DimSalesReason',
                                                'FactInternetSales',
                                                'FactFinance'
                                                )
                           """)
        src_tables = src_cursor.fetchall()
        for tbl in src_tables:
            #query and load save data to dataframe
            df = pd.read_sql_query(f'select * FROM {tbl[0]}', src_conn)
            load(df, tbl[0])

    except Exception as e:
        print("Data extract error: " + str(e))

    finally:
        src_cursor.close()
        src_conn.close()


#load data to postgres
def load(df, tbl):

    try:
        rows_imported = 0
       
        engine = create_engine(f'postgresql://{uid2}:{pwd2}@{pgserver}:5432/{pgdatabase}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {tbl}')
        # save df to postgres
        df.to_sql(f'stg_{tbl}', engine, if_exists='replace', index=False)
        rows_imported += len(df)
        # add elapsed time to final print out
        print("Data imported successful")

    except Exception as e:
        print("Data load error: " + str(e))

try:
    #call extract function
    extract()

except Exception as e:
    print("Error while extracting data: " + str(e))


# Developed by Eng: Mahmoud Mohamed Ahmed 