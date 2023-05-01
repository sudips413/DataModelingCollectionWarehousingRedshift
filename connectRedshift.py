import psycopg2
import pandas as pd
import configparser
from psycopg2 import sql

## import from credentials.cfg
config= configparser.ConfigParser()
config.read_file(open('credentials.cfg'))

host=config.get('REDSHIFT','HOST')
port = config.get('REDSHIFT','PORT')
database = config.get('REDSHIFT','DATABASE')
user = config.get('REDSHIFT','USER')
password = config.get('REDSHIFT','PASSWORD')

conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

cursor=conn.cursor()

# check if table movies exists or not in redshift
cursor.execute("SELECT * FROM information_schema.tables WHERE table_name='movies';")
table_exits = bool(cursor.rowcount)
if table_exits:
    cursor.execute("DROP TABLE movies;")
    
    
##create table movies in redshift
cursor.execute("CREATE TABLE movies(title varchar(100),year varchar(20),rating varchar(15),reviews varchar(20),genres varchar(50),runtime varchar(25),gross varchar(20));")

### insert all the data from csv file to redshift from local
df = pd.read_csv('data/moviesv4.csv')
data = [tuple(row) for row in df.values]
sql = 'INSERT INTO movies VALUES %s'
args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in data)
cursor.execute(sql % args_str)
conn.commit()

cursor.execute("SELECT * FROM movies LIMIT 200")
print(cursor.fetchall())





