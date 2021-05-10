#!/usr/bin/python3
from model import*
from view import*

class Controller():

    def __init__(self):
        self.root_window = Tk.Tk()
        self.sqlite_model = SqliteAction(self)
        self.view = App(self, self.root_window)

    def run(self):
        self.root_window.mainloop()

    def quit(self):
        self.sqlite_model.close_db() # db_action oder persisten_store_action
        self.root_window.destroy()

    def put_information(self, String):
        self.sqlite_model.put_information(String)

    def get_information(self):
        String = self.sqlite_model.get_information()
        return String

    def insert_task(self, vocable1, vocable2, information):
        self.sqlite_model.insert_task(vocable1, vocable2, information)

    def search_task(self, vocable, selected_language):
        txt = self.sqlite_model.search_task(vocable, selected_language)
        self.view.setText(txt)

    def change_task(self, vocable1, vocable2, selected_language):
        self.sqlite_model.change_task(vocable1, vocable2, selected_language)

    def delete_task(self, String1, String2, selected_language):
        self.sqlite_model.delete_task(String1, String2, selected_language)    
        
    def create_new_table(self):
        self.sqlite_model.create_new_table()    

    def CreateInfoMessageBoxWindow(self, String1, String2):
        self.view.CreateInfoMessageBoxWindow(String1, String2)

    def WriteToFile(self,String):
        self.sqlite_model.WriteIntoFile(String)
