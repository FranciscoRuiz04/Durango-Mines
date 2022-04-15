# Durango-Mines
## GUI for SQL queries
Code to create a GUI for a PostgreSQL DB with Durango Mines data using Python 3.
If you want to test the code, I encourage you to download the file named gps_postgredb.py
which is within libs folder because it has the connection script used into DurangoMines.py script.
Also, is necessary to have PostgreSQL within computer where will be run the present scripts to create Durango Mines DB. Script with the records with geographic information in SQL language are in DurangoMinesDB.sql.
## Prepare PostgreSQL Enviroment
Copy the next code whitin snippet in your PostgreSQL.
```sql
CREATE EXTENSION postgis;
```
### Necessary Python Libraries
```python
pip install dotenv
pip install psycopg2
```