from queries import MySQL
import os

#mydb = MySQL("sqlite:///database/cs50final.db")

# Some testing

# mydb.set_userid(1)
# mydb.catsMenu() # initialize mydb.menu
# cats = mydb.select_cats()
# print(cats)
# print('db Menu')
# menu = mydb.getMenu()
# print(menu)
# for item in menu:
#     print(item['menu_item'])
# mydb.setChecked('Computer SciEnce', False)
# bookmarks = mydb.build_bookmarks(cats)
# for bm in bookmarks:
#     print(bm['category'], bm['visible'])


# For Local use of Heroku 
#mydb = MySQL("postgres://mtztrmkrqbfvgp:1260311e94b8d2608be808433512f8d34dc623526e61ad1f04c2e3336b3a0f8a@ec2-52-202-66-191.compute-1.amazonaws.com:5432/d30b48o0gtbpnp")

# For Heroku deployment
mydb = MySQL(os.getenv("DATABASE_URL"))
         

# enables foreign key constraints at runtime
#db.execute('PRAGMA foreign_keys = ON')


     
