# from queries import MySQL
from cs50 import SQL
# from flask import session
import os

mydb = SQL("sqlite:///database/cs50final.db")

# enables foreign key constraints at runtime
# mydb.execute('PRAGMA foreign_keys = ON')
