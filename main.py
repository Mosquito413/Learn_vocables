#!/usr/bin/python3
# -*- coding: latin-1 -*-
"""
Created 2020
Each of the Model, View, Controller and SidePanel objects are in their own modules.
The program runs on Python3.
"""
# logger
from logger import*

# model
import datetime
import sqlite3
from sqlite3 import Error

# view
import tkinter as Tk
import tkinter.messagebox as tkMessageBox
from tkinter import ttk

# controller
from controller import*
from model import*
from view import*



if __name__ == '__main__':
    setup_logging() 
    c = Controller()
    c.run()
