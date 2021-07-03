#this file connects sqlite3 with the main scraping project
#this contains the queries of sql sich as create,insert,select

import sqlite3                          #importing packages

def connect(dbname):                    #defining a function and database name as parameter 
    conn = sqlite3.connect("dbname")    #creating a object 'conn'

    conn.execute("CREATE TABLE IF NOT EXISTS OYO_HOTELS (NAME TEXT, ADDRESS TEXT, PRICE INT, AMENITIES TEXT, RATING TEXT)")  #Creating a table

    print("Table created successfully!")
    
    conn.close()                       #closing a function is essential!#
    
def insert_into_table(dbname, values): #defining a function to insert values in tables
    conn = sqlite3.connect(dbname)    

    insert_sql = "INSERT INTO OYO_HOTELS (NAME, ADDRESS, PRICE, AMENITIES, RATING) VALUES (?, ?, ?, ?, ?)" #creating an object to insert values
    
    conn.execute(insert_sql, values)   #using keyword execute,the values been inserted and turned out into a database
    
    conn.commit()
    conn.close()
    
def get_hotel_info(dbname):            #defining a function to get those values
    conn = sqlite3.connect(dbname)    
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM OYO_HOTELS") #using Select to retreive datas

    table_data = cur.fetchall()

    for record in table_data:         #using a forloop print untill the data is none
        print(record)           
        
    conn.close()    
