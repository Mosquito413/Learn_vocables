# Logger
import logging.config

# Sqlite
import datetime
import sqlite3
from sqlite3 import Error


class SqliteAction():

    def __init__(self, controller):
        """ Constructor """
        self.start_logging()
        self.controller = controller
        #neu
        #self.conn = self.create_connection()
        self.connection = self.create_sql() 
        self.__information = " " 

#################################################################################

    def start_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Start logging!')

#################################################################################

    def put_information(self, info):
        self.__information = info

#################################################################################

    def get_information(self):
        return self.__information   

#################################################################################
    
    def create_sql(self):
        """ Create a new database """
        
        sql_table_german = """CREATE TABLE IF NOT EXISTS German (
                                            ID integer PRIMARY KEY AUTOINCREMENT,
                                            Vocable text NOT NULL,
                                            Info text,
                                            Example_Sentence text,
                                            Date timestamp
                                            );"""
 
        sql_table_english = """CREATE TABLE IF NOT EXISTS English (
                                    ID integer,
                                    Vocable text NOT NULL,
                                    Info text,
                                    Example_Sentence text,
                                    Date timestamp
                                    );"""
 
        #create a database connection
        conn = self.create_connection()
 
        # create tables if not exist
        # falls table schon exestiert muss ich diese nicht erstellen
        if conn is not None:
            self.create_table(conn, sql_table_german)
            self.create_table(conn, sql_table_english)
            #logger.info("Created tables!")
            return conn
        else:
            self.logger.error("Couldn't create connection to database!")

#################################################################################

    def create_new_table(self, table_name):

        table_name=String.get()

        sql_new_table = """CREATE TABLE IF NOT EXISTS %s (ID integer,
                                                          Vocable text NOT NULL,
                                                          Info text,
                                                          Example_Sentence text,
                                                          Date timestamp);""" % (table_name)
 
        # create a database connection
        conn = self.create_connection(self.database)
 

        # create tables if not exist
        if conn is not None:
            self.create_table(conn, sql_new_table)
            return conn
        else:
            # wenn keinen verbindung erstellt wurde
            # entweder abrechen oder nach bestimmter zeit nochmal probieren
            self.logger.error("Couldn't create connection to database!")


#################################################################################

    def create_connection(self):
        """ create connection to SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.database = "sqlite_vocables.db"

        conn = None
        try:
            conn = sqlite3.connect(self.database, timeout=10)
            #logger.info("Created connection to database!")
            return conn
        except Error as e:
            pass
            #logger.info("Not connected to database")
     
#################################################################################

    def create_table(self ,conn, sql_query):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor() 
            c.execute(sql_query)
        except Error as e:
            self.logger.error("%s",e)
         
#################################################################################

    def insert_task(self, String1, String2, information):
        """
        Create a new task
        Check if words have been already added to the database
        :param conn: Connection object
        :param get_value1:
        :param get_value1:
        """

        native_vocable = String1.get()
        to_learn_vocable = String2.get()
        date = datetime.datetime.now()


        # in case both vocables are missing
        if not native_vocable and not to_learn_vocable:
            self.controller.CreateInfoMessageBoxWindow("ERROR1", "Vocables are missing!")
            self.logger.info("Both vocables are missing!")
        # in case one vocable is  missing
        elif not native_vocable or not to_learn_vocable:
            self.controller.CreateInfoMessageBoxWindow("ERROR1", "At least one vocable is missing!")
            self.logger.info("One of the vocables are missing!")
        else:
            self.connection.text_factory = str
            db_cursor = self.connection.cursor()
  
            sql_query=("SELECT German.id, German.Vocable, English.Vocable FROM German INNER JOIN English USING (id) WHERE German.Vocable LIKE ? " ""
                       "UNION SELECT German.id, German.Vocable, English.Vocable FROM German LEFT OUTER JOIN English USING (id) WHERE English.Vocable LIKE ? GROUP BY German.id ") 

            db_cursor.execute(sql_query, (native_vocable, to_learn_vocable,))
            exists = db_cursor.fetchall()
           
            print(exists)
            

            # in case  both or at least one vocable already exist in database
            if exists:
                
                id=0
                flag=False

                for row in exists:
                    # in case both vocables already exist in database
                    if row[1] == native_vocable and row[2] == to_learn_vocable :
                        txt = "Vocable " + str(native_vocable) + " = " + str(to_learn_vocable) + " already exist"
                        self.controller.CreateInfoMessageBoxWindow("Vocable already exist!", txt)
                        self.logger.info(txt)
                        break
                    # in case native vocable exist
                    elif row[1] == native_vocable and row[2] != to_learn_vocable :
                        id=row[0]
                        self.logger.info("Vocable \"%s\" exist in table \"German\", id: %s!", native_vocable, str(row[0]))
                    # in case the english vocable exist    
                    elif row[1] != native_vocable and row[2] == to_learn_vocable :
                        flag=True
                        self.logger.info("Vocable \"%s\" exist in table \"English\" but vocable \"%s\" doesn't exist in table \"German\"!", to_learn_vocable, native_vocable)
               
                if id!=0:
                    sql_query ="INSERT INTO English (ID, Vocable, Info, Date) VALUES (?, ?, ?, ?)"
                    db_cursor.execute(sql_query, (id, to_learn_vocable, self.__information, date,))
                    self.connection.commit()
                    self.logger.info("Add vocable \"%s\" to table \"English\"",to_learn_vocable)

            # 
            # in case both vocables doesn't exist in the database 
            if not exists or flag==True:
                sql_query ="INSERT INTO German (Vocable, Info, Date) VALUES (?, ?, ?)"
                cur = db_cursor.execute(sql_query, (native_vocable, self.__information, date,))
                self.connection.commit()
                sql_query ="INSERT INTO English (ID, Vocable, Info, Date) VALUES (?, ?, ?, ?)"
                db_cursor.execute(sql_query, (cur.lastrowid, to_learn_vocable, self.__information, date,))
                self.connection.commit()
                self.logger.info("Add vocable \"%s\" and vocable \"%s\" to \"German\" and \"English\" table!",native_vocable ,to_learn_vocable)

            
#################################################################################

    def search_task(self, String, selected_language):  
        """
        Search for vocble in database
        :param conn: Connection object
        :param vocable
        """

        vocable = String.get()
        self.connection.text_factory = str
        db_cursor = self.connection.cursor()

        if selected_language == "German -> English":
            sql_query=("SELECT German.Vocable, English.Vocable FROM German INNER JOIN English USING (id) WHERE German.Vocable LIKE ? ") 
        elif selected_language == "English -> German":
            sql_query=("SELECT English.Vocable, German.Vocable FROM English INNER JOIN German USING (id) WHERE English.Vocable LIKE ? ") 


        db_cursor.execute(sql_query, (vocable,))
        exists = db_cursor.fetchall()

        print(exists)

        # in case vocable exist
        if exists:
            for idx, row in enumerate(exists):
                if idx==0:
                    txt = row[1]
                else:
                    txt = txt + ", " + row[1]  
        else:
            txt=  "Vocable does not exist"             

        return txt 

#################################################################################

    # überprüfen
    def change_task(self, String1, String2, selected_language):
        """
        Change or update a vocable in the database. In case the vocable is false written
        :param conn: Connection object
        :param vocable
        """
   
        false_vocable = String1.get()
        correct_vocable = String2.get()

        self.connection.text_factory = str
        db_cursor = self.connection.cursor()

        # fenster mit warn hinweis erstellen aändern von dieser in diese vocable
        if selected_language == "German":
            sql_query= ("UPDATE German SET Vocable=? Where Vocable=? ")
        elif selected_language == "English":
            sql_query= ("UPDATE English SET Vocable=? Where Vocable=? ")
        
        db_cursor.execute(sql_query, (correct_vocable,false_vocable,))
        self.connection.commit()

#################################################################################

    def delete_task(self, String1, String2, selected_language):
        """
        Delete vocable in the database. 
        :param conn: 
        :param vocable:
        """

        native_vocable = String1.get()
        to_learn_vocable = String2.get() 

        self.connection.text_factory = str
        db_cursor = self.connection.cursor()

        # counts the results (in case vocable has more entrys in the database) 
        if selected_language == "German -> English":
            sql_query=("SELECT COUNT (*) FROM German INNER JOIN English USING (id) WHERE German.Vocable LIKE ? ") 
            db_cursor.execute(sql_query, (native_vocable,))
            amount = db_cursor.fetchone()
            sql_query=("SELECT COUNT (*) FROM English WHERE English.Vocable LIKE ? ") 
            db_cursor.execute(sql_query, (to_learn_vocable,))
            amount2 = db_cursor.fetchone()
            sql_query=("SELECT German.id FROM German WHERE German.Vocable LIKE ? ") 
            db_cursor.execute(sql_query, (native_vocable,))
            id = db_cursor.fetchone()
 
        
        if amount[0]>1:
            sql_query=("DELETE FROM English WHERE English.Vocable LIKE ? AND English.id LIKE ?") 
            db_cursor.execute(sql_query, (to_learn_vocable, id[0],))
            self.connection.commit()
            self.logger.info("Delete vocable \"%s\" only from \"English\" table, with ID: %s!", to_learn_vocable, id[0])
        elif amount[0]==1 and amount2[0]!=0:
            sql_query=("DELETE FROM German WHERE German.Vocable LIKE ? AND German.id LIKE ?")
            db_cursor.execute(sql_query, (native_vocable, id[0],))
            self.connection.commit()
            sql_query=("DELETE FROM English WHERE English.Vocable LIKE ? AND English.id LIKE ?")
            db_cursor.execute(sql_query, (to_learn_vocable, id[0],))
            self.connection.commit()
            self.logger.info("Delete vocable \"%s\" and \"%s\" from \"German\" and \"English\" table, with ID: %s!", native_vocable, to_learn_vocable, id[0])
        else:
            self.logger.info("Vocables doesn't exists in database")
        
#################################################################################

    def WriteIntoFile(self, String):
        """
        Search for vocables in database and write them into a txt file
        :param 
        """

        #information = String.get()
        information = String
        self.connection.text_factory = str
        db_cursor = self.connection.cursor()

        # count vocable (in table) for each id (primary key)  
        sql_query=("SELECT English.id, COUNT(English.id) FROM English WHERE English.Info LIKE ? GROUP BY English.id ORDER BY English.id ASC") 
        db_cursor.execute(sql_query, (information,))
        amount = db_cursor.fetchall()
    
        # find vocables (search task info) in table 
        sql_query=("SELECT German.id, German.Vocable, English.Vocable FROM German INNER JOIN English USING (id) WHERE German.Info LIKE ? ORDER BY German.id ASC") 
        db_cursor.execute(sql_query, (information,))
        exists = db_cursor.fetchall()

        file = open('Vocable.txt','w')
        self.logger.info("File open!")

        # if database contains vocable searched for
        if exists:

            # value for how often a vocable exist in the database
            count=0

            # run through each vocable in exists
            for row in exists:    
                # 
                if count==0:
                    for row_amount in amount:    
                        if row_amount[0]==row[0]:
                            count=row_amount[1]    
                            break
                    
                    # vocable exist more than one time
                    if count > 1:
                        txt = row[2]
                        count=count-1
                    # vocable exist one time, then write to file    
                    elif count==1:
                        file.write("{0:30} ==> {1:30}\n".format(row[1],row[2]))  
                        count=0
    
                # vocable exist more than one time
                # get next vocable and append
                elif count!=0:
                    txt = txt + ", " + row[2]
                    count=count-1
                    
                    # if all vocables are appended, write to file and delete vocables in txt
                    if count==0:
                        file.write("{0:30} ==> {1:30}\n".format(row[1],txt))
                        txt=""
   
        else:
            self.logger.info("No vocables, for writting to file, found in database!")
        
        file.close()
        self.logger.info("File closed!") 
   
#################################################################################

    # Hinweis: die letzten beiden funktionen close_db close_connection kann man zu einer zusammenfügen
    def close_db(self):
        if self.connection is not None:
            self.close_connection()
            self.logger.info("Connection to database has been closed")
        else:
            self.logger.error("No sqlite connection")   
    
#################################################################################

    def close_connection(self):
        """ 
        Close database 
        :param conn: Connection object
        """

        if (self.connection):
            self.connection.close()
            self.logger.info("Closed connection to SQLite")
        else:
            self.logger.error("Couldn't close connection to database!")


    
        
        



   
