__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2021, GPS"
__credits__ = "GPS"

__version__ = "1.0.2"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()   

class Connection:
    """
    Conect Python to PostgreSQL.
    Use the function <<query>> to get records from your database
    """
    def __init__(self, db, server = os.getenv('server'), port = os.getenv('port'), usr = os.getenv('usr'), pwd = os.getenv('pwd')):
        """
        Constructor
        """
        self.db = db
        self.server = server
        self.port = port
        self.usr = usr
        self.pwd = pwd





    def opendb(function):
        """
        Create the connection with a DB in 
        PostgreSQL to make a query into the database.
        """
        
        def wrap(self, *arg, **args):
            try:
                con = psycopg2.connect(
                    database = self.db,
                    user = self.usr,
                    password = self.pwd,
                    host = self.server,
                    port = self.port
                )
            except:
                print('\033[1;31mConnection failed\033[0;31m')
            
            else:
                #Create a cursor
                curdb = con.cursor()

                query = function(*arg, **args)  #Function to decorated
                try:
                    curdb.execute(query)    #Execute query
                except:
                    raise ValueError('Can not excecute query')
                else:
                    #Parse what kind of query is
                    if query.find('SELECT') != -1:
                        records = curdb.fetchall()  #Get all the records fetched
                        
                        if len(records) == 0:
                            return 'There is no one record'
                        else:
                            return records
                            
                    else:
                        con.commit()            #Save changes
                finally:
                    curdb.close()           #Close cursor
                    con.close()             #Close database
        return wrap



    @opendb
    def query2(query):
        """
        Write functions upper cases
        """
        return query



    @opendb
    def desc2(table, type = True, isnullable = True):
        """
        Check column structures from every table that you want.
        __________________________________________________________________________

        <<table>>: Table Name. OBLIGATORY.
        <<type>>: See what data type is within table.
        """
        
        query = 'SELECT column_name'
        if type == True:
            query += ', data_type'
        if isnullable == True:
            query += ', is_nullable'
        query += f" FROM information_schema.columns WHERE table_name = '{table}';"
        return query



    @opendb
    def select2(table, *columns, **conditions):
        """
        Make simple queries using basic conditions.
        __________________________________________________________________________

        <<table>>
        Table name. OBLIGATORY

        <<*columns>> 
        Takes column names that you want. 
        If no one value is enter in, automatically
        takes all columns from the table.

        <<**conditions>>
        Takes all conditions that you want to use for your query.


        Example:

        select2('tabname', 'column1', 'column2', ... column1 = x, column2 = y ... )        
        """


        query = 'SELECT '
        if len(columns) == 0:
            query += '*' + ' FROM ' + table
        else:
            attributes = ','.join(columns)
            query += attributes + ' FROM ' + table

        for i, (key, value) in enumerate(conditions.items()):
            if i == 0:
                query += (' WHERE {}={}').format(key,value)
            else:
                query += (' AND {}={}').format(key, value)

        return query
    


    @opendb
    def insert2(table, *records):
        """
        Insert new records into a table wanted.
        __________________________________________________________________________
        
        <<table>>
        Takes table name. OBLIGATORY.

        <<*records>>
        Takes every value you want to insert into the table wanted.
        """
        lis = str(tuple(records))
        query = 'INSERT INTO ' + table + ' VALUES ' + lis + ';'
        
        return query
    
    
    
    def __str__(self):
        return ('DB: %s\nUser: %s\nPassword: %s\nServer: %s\nPort: %s' % 
        (self.db, self.usr, self.pwd, self.server, self.port))