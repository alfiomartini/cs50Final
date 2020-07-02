# from queries import MySQL
from cs50 import SQL
# from flask import session
import os

mydb = SQL("sqlite:///database/cs50final.db")


# For Local use of Heroku 
#mydb = MySQL("postgres://mtztrmkrqbfvgp:1260311e94b8d2608be808433512f8d34dc623526e61ad1f04c2e3336b3a0f8a@ec2-52-202-66-191.compute-1.amazonaws.com:5432/d30b48o0gtbpnp")

# For Heroku deployment
#mydb = SQL(os.getenv("DATABASE_URL"))
         

# enables foreign key constraints at runtime
#db.execute('PRAGMA foreign_keys = ON')


     
