#!/usr/bin/python3

# Logger
import logging.config

# Tkinder
import tkinter as Tk
import tkinter.messagebox as tkMessageBox
from tkinter import ttk  

APP_WIN_WIDTH = 550
APP_WIN_HEIGHT = 400
APP_WIN_TITLE = 'Learn Vocabulary'


class App():
    # Constructor
    def __init__(self, controller, root_window):
        self.start_logging()
        self.controller = controller
        self.root_window = root_window
        self.root_window.title(APP_WIN_TITLE)
        self.root_window.geometry("550x400")
        #
        self.tab_parent = ttk.Notebook(self.root_window)
        self.tab_save = self.SetTab("Save Vocable")
        self.tab_search = self.SetTab("Search Vocable")
        self.tab_change = self.SetTab("Change Vocable")
        self.tab_delete = self.SetTab("Delete Vocable")
        #
        self.CreateMenu()
        self.SaveTab()
        self.SearchTab()
        self.ChangeTab()
        self.DeleteTab()
        self.Exit_Frame()


    # Destructor
    def __del__(self):
        pass

#################################################################################

    def start_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Start logging!')

#################################################################################

    def CreateInfoMessageBoxWindow(self, window_txt, info_txt):
        tkMessageBox.showerror(window_txt, info_txt)

#################################################################################

    def SetTab(self, txt):
        tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(tab, text= txt)
        self.tab_parent.pack(expand=1, fill=Tk.BOTH)
        return tab

#################################################################################

    def CreateInformationWindow(self):
        """ 
        Create window to put extra information to db_file
        """
        top=Tk.Toplevel() 
        top.title("Information")
        frame_info = Tk.LabelFrame(top, text = "Extra Info")
        frame_info.pack(fill=Tk.BOTH, padx=10, pady=10)
        info = Tk.Entry(master=frame_info, bd=5, width=40) 
        info.pack(side=Tk.RIGHT) 
        frame_button = Tk.LabelFrame(top)
        frame_button.pack(fill=Tk.BOTH, padx=10, pady=10)

        ok_button = Tk.Button(master=frame_button, 
                           text="Save", 
                           command=  lambda: [self.controller.put_information(info.get()), 
                                              top.destroy(), 
                                              self.CheckThat()])
        ok_button.pack(side=Tk.RIGHT, padx=5, pady=5)
        
        cancel_button = Tk.Button(master=frame_button, 
                               text="Cancel", 
                               command=top.destroy)
        cancel_button.pack(side=Tk.RIGHT, padx=5, pady=5)

#################################################################################

    def PrintInformationWindow(self):
        """ 
        Create window
    
        """
        # suchen nach datum angeben
        # und bei info sollen alle infos die in datei sind angezeigt werden
        # compobox
        # bei dtum bruache ich nur den tag zeit brauche ich nicht

        top=Tk.Toplevel() 
        top.title("Write vocables to file")
        frame_info = Tk.LabelFrame(top, text = "Extra Info")
        frame_info.pack(fill=Tk.BOTH, padx=10, pady=10)
        info = Tk.Entry(master=frame_info, bd=5, width=40) 
        info.pack(side=Tk.RIGHT) 
        frame_button = Tk.LabelFrame(top)
        frame_button.pack(fill=Tk.BOTH, padx=10, pady=10)

        ok_button = Tk.Button(master=frame_button, 
                              text="Write", 
                              command=  lambda: [self.controller.WriteToFile(info.get()), 
                                                 top.destroy()])
        ok_button.pack(side=Tk.RIGHT, padx=5, pady=5)
        
        cancel_button = Tk.Button(master=frame_button, 
                                  text="Cancel", 
                                  command=top.destroy)
        cancel_button.pack(side=Tk.RIGHT, padx=5, pady=5)

#################################################################################   

    def CreateMenu(self):
        menu = Tk.Menu(self.root_window)

        # create menu names
        file_menu = Tk.Menu(menu, tearoff=0)
        edit_menu = Tk.Menu(menu, tearoff=0)

        # Menu values
        file_menu.add_command(label="Write vocables to file", command=(lambda: self.PrintInformationWindow()))
        file_menu.insert_separator
        file_menu.add_command(label="Exit", command=(lambda: self.controller.quit()))
        edit_menu.add_command(label="Create Table", command=(lambda: self.controller.create_new_table()))

        # Create menu bar 
        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Edit", menu=edit_menu)

        # Pass menu bar to the root_window
        self.root_window.config(menu=menu)  
        self.logger.info("Created Menu")

#################################################################################
    # für frame noch klasse bilden
    ######################################################
    def SaveTab(self):
        self.frame_settings = Tk.LabelFrame(self.tab_save, text = "Settings")
        self.frame_settings.pack(fill=Tk.BOTH, padx=5, pady=5)
        self.InformationFrame()
        self.SaveFrame()

#################################################################################    

    def InformationFrame(self):

        self.CheckVarInfoYes = Tk.BooleanVar()
        self.CheckVarInfoNo = Tk.BooleanVar()

        frame = Tk.LabelFrame(master = self.tab_save, relief="flat")
        frame.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label = Tk.Label(frame, 
                              text="Information Set:", 
                              anchor=Tk.NW, 
                              justify=Tk.LEFT)
        self.label.pack(side=Tk.LEFT)

        
        self.setinformation = Tk.Checkbutton(master=frame, 
                                          text="Yes",
                                          variable= self.CheckVarInfoYes,                                
                                          command= (lambda: self.CreateInformationWindow()))
        self.setinformation.pack(side=Tk.LEFT)                            


        self.withoutinformation = Tk.Checkbutton(master=frame, 
                                                text="No",
                                                variable=self.CheckVarInfoNo,
                                                command= lambda: [self.controller.put_information(" "),
                                                                  self.CheckThat()])
        self.withoutinformation.pack(side=Tk.LEFT) 
        self.withoutinformation.select()                   

        self.showInformation = Tk.Label(frame, 
                                        text= "",
                                        justify=Tk.LEFT)
        self.showInformation.pack(side=Tk.LEFT, padx=40)

        self.CheckThat()

#################################################################################
    
    def CheckThat(self):

        value = self.controller.get_information()

        if value.strip()=="":
            uptdateInformation="Not set"
            self.setinformation.deselect()
            self.withoutinformation.select()
        else:
            uptdateInformation=self.controller.get_information()
            self.setinformation.select()
            self.withoutinformation.deselect()

        self.showInformation.configure(text="Information Set to: " + uptdateInformation)

#################################################################################

    def SaveFrame(self):
        
        frame_vocabulary = Tk.LabelFrame(self.tab_save, text = "Vocabulary")
        frame_vocabulary.pack(fill=Tk.BOTH, padx=5, pady=5)
        frame_put_vocabulary = Tk.LabelFrame(frame_vocabulary)
        frame_put_vocabulary.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_put_vocabular = Tk.Label(master=frame_put_vocabulary, 
                                            text="German:",
                                            anchor=Tk.W, 
                                            justify=Tk.LEFT)
        self.label_put_vocabular.pack(side=Tk.LEFT)
        put_vocabular = Tk.Entry(master=frame_put_vocabulary, bd=5, width=40) 
        put_vocabular.pack(side=Tk.RIGHT)

        frame_get_vocabulary = Tk.LabelFrame(frame_vocabulary)
        frame_get_vocabulary.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_get_vocabular = Tk.Label(master=frame_get_vocabulary,  
                                            text="English: ",
                                            anchor=Tk.W, 
                                            justify=Tk.LEFT
                                            )
        self.label_get_vocabular.pack(side=Tk.LEFT)
        get_vocabular = Tk.Entry(master=frame_get_vocabulary, bd=5, width=40)                   
        get_vocabular.pack(side=Tk.RIGHT)

        # Create Buttons
        frame_button_vocabulary = Tk.LabelFrame(frame_vocabulary, relief="flat")
        frame_button_vocabulary.pack(fill=Tk.BOTH, padx=5, pady=5)

        info = self.controller.get_information
        add_button = Tk.Button(master=frame_button_vocabulary, 
                            text="Add", 
                            command= lambda: self.controller.insert_task(put_vocabular, 
                                                                         get_vocabular, 
                                                                         info),
                            bd=5, width=5)
        add_button.pack(side=Tk.RIGHT)

#######################################################################################

    def SearchTab(self):
        frame_search = Tk.LabelFrame(self.tab_search, text = "Search Vocable")
        frame_search.pack(fill=Tk.BOTH, padx=5, pady=5)
             
        frame_chose_language = Tk.LabelFrame(frame_search)
        frame_chose_language.pack(fill=Tk.BOTH, padx=5, pady=5)
     
        self.label_chose_language = Tk.Label(master=frame_chose_language, 
                                               text="Language:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_chose_language.pack(side=Tk.LEFT)
        
        #Create Combobox
        self.n = Tk.StringVar() 
        self.n = ('German -> English',
                  'English -> German')
        language_select_combobox = ttk.Combobox(master=frame_chose_language, 
                                                     width = 39, 
                                                     textvariable = self.n,
                                                     state="readonly")

        language_select_combobox.config(values=self.n)
        language_select_combobox.pack(side=Tk.RIGHT) 
        language_select_combobox.current(0) 
                                 
        
        # first Label
        frame_search_vocabulary = Tk.LabelFrame(frame_search)
        frame_search_vocabulary.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_search_vocabular = Tk.Label(master=frame_search_vocabulary, 
                                               text="Search for Vocable:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_search_vocabular.pack(side=Tk.LEFT)
        vocable = Tk.Entry(master=frame_search_vocabulary, bd=5, width=40) 
        vocable.pack(side=Tk.RIGHT)

        frame_result_vocable = Tk.LabelFrame(frame_search)
        frame_result_vocable.pack(fill=Tk.BOTH, padx=5, pady=5)


        self.label_result_vocable = Tk.Label(master=frame_result_vocable,  
                                               text="Result: ",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_result_vocable.pack(side=Tk.LEFT)
       
        self.result_vocable = Tk.Entry(master=frame_result_vocable, bd=5, width=40)                   
        self.result_vocable.pack(side=Tk.RIGHT)

        # Buttons 
        frame_button_search = Tk.LabelFrame(frame_search, relief="flat")
        frame_button_search.pack(fill=Tk.BOTH, padx=5, pady=5)

        search_button = Tk.Button(master=frame_button_search, 
                                  text="Translate", 
                                  command= lambda: self.controller.search_task(vocable, language_select_combobox.get()),
                                  bd=5, width=5)
        search_button.pack(side=Tk.RIGHT)

#################################################################################

    def setText(self, txt):
        self.result_vocable.delete(0,"end")
        self.result_vocable.insert(0, txt)

#################################################################################

    def ChangeTab(self):
        frame_change = Tk.LabelFrame(self.tab_change, text = "Change Vocable")
        frame_change.pack(fill=Tk.BOTH, padx=5, pady=5)

        frame_change_vocable = Tk.LabelFrame(frame_change)
        frame_change_vocable.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_change_vocable = Tk.Label(master=frame_change_vocable, 
                                               text="Language:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_change_vocable.pack(side=Tk.LEFT)
        
        #Create Combobox
        self.n = Tk.StringVar() 
        self.n = ('German',
                  'English')
        language_select_combobox = ttk.Combobox(master=frame_change_vocable, 
                                                     width = 39, 
                                                     textvariable = self.n,
                                                     state="readonly")

        language_select_combobox.config(values=self.n)
        language_select_combobox.pack(side=Tk.RIGHT) 
        language_select_combobox.current(0)

        frame_chose_vocable = Tk.LabelFrame(frame_change)
        frame_chose_vocable.pack(fill=Tk.BOTH, padx=5, pady=5)


        self.label_change_vocable = Tk.Label(master=frame_chose_vocable, 
                                               text="Change:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_change_vocable.pack(side=Tk.LEFT)
        false_vocable = Tk.Entry(master=frame_chose_vocable, bd=5, width=40) 
        false_vocable.pack(side=Tk.RIGHT)

        frame_to_vocable = Tk.LabelFrame(frame_change)
        frame_to_vocable.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_to_vocable = Tk.Label(master=frame_to_vocable, 
                                               text="To:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_to_vocable.pack(side=Tk.LEFT)
        correct_vocable = Tk.Entry(master=frame_to_vocable, bd=5, width=40) 
        correct_vocable.pack(side=Tk.RIGHT)
        
        # Buttons #
        frame_button_change = Tk.LabelFrame(frame_change, relief="flat")
        frame_button_change.pack(fill=Tk.BOTH, padx=5, pady=5)

        change_button = Tk.Button(master=frame_button_change, 
                                  text="Change",
                                  command= lambda: self.controller.change_task(false_vocable, correct_vocable, language_select_combobox.get()),
                                  bd=5, width=5)
        change_button.pack(side=Tk.RIGHT)

#################################################################################

    def DeleteTab(self):
        frame_delete = Tk.LabelFrame(self.tab_delete, text = "Delete Vocable")
        frame_delete.pack(fill=Tk.BOTH, padx=5, pady=5)

        frame_delete_vocable = Tk.LabelFrame(frame_delete)
        frame_delete_vocable.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_delete_vocable = Tk.Label(master=frame_delete_vocable, 
                                               text="Language:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_delete_vocable.pack(side=Tk.LEFT)
              
        #Create Combobox
        self.n = Tk.StringVar() 
        self.n = ('German -> English',)
        language_select_combobox = ttk.Combobox(master=frame_delete_vocable, 
                                                width = 39, 
                                                textvariable = self.n,
                                                state="readonly")

        language_select_combobox.config(values=self.n)
        language_select_combobox.pack(side=Tk.RIGHT) 
        language_select_combobox.current(0)

        frame_delete_vocable1 = Tk.LabelFrame(frame_delete)
        frame_delete_vocable1.pack(fill=Tk.BOTH, padx=5, pady=5)


        self.label_delete_vocable1 = Tk.Label(master=frame_delete_vocable1, 
                                               text="First:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_delete_vocable1.pack(side=Tk.LEFT)
        vocable1 = Tk.Entry(master=frame_delete_vocable1, bd=5, width=40) 
        vocable1.pack(side=Tk.RIGHT)

        frame_delete_vocable2 = Tk.LabelFrame(frame_delete)
        frame_delete_vocable2.pack(fill=Tk.BOTH, padx=5, pady=5)

        self.label_delete_vocable2 = Tk.Label(master=frame_delete_vocable2, 
                                               text="Second:",
                                               anchor=Tk.W, 
                                               justify=Tk.LEFT)
        self.label_delete_vocable2.pack(side=Tk.LEFT)
        vocable2 = Tk.Entry(master=frame_delete_vocable2, bd=5, width=40) 
        vocable2.pack(side=Tk.RIGHT)
        
        # Buttons #
        frame_button_delete = Tk.LabelFrame(frame_delete, relief="flat")
        frame_button_delete.pack(fill=Tk.BOTH, padx=5, pady=5)

        delete_button = Tk.Button(master=frame_button_delete, 
                                  text="Delete",
                                  command= lambda: self.controller.delete_task(vocable1, vocable2, language_select_combobox.get()), 
                                  bd=5, width=5)
        delete_button.pack(side=Tk.RIGHT)
        
#################################################################################
    
    def Exit_Frame(self):
        frame_exit = Tk.LabelFrame(self.root_window, relief="flat")
        frame_exit.pack(side=Tk.RIGHT, fill=Tk.X, padx=5, pady=5)
        exit_button = Tk.Button(master=frame_exit, 
                                text="Quit", 
                                command=(lambda: self.controller.quit()))
        exit_button.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)


