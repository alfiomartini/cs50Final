from cs50 import SQL
from helpers import shorten_title

class MySQL(SQL):
    def __init__(self, dbpath):
        super().__init__(dbpath)
        self.sql_cats = '''select cat_name from categories 
                    where user_id = ? 
                    order by cat_name'''
        self.sql_bookms = '''select bookmarks.id as bid, cat_name, 
                    title, url, description 
                    from users, categories, bookmarks where 
                    users.id = bookmarks.user_id and 
                    bookmarks.categ_name=categories.cat_name  and 
                    categories.cat_name = ? and users.id = ?
                    order by title'''

    def set_userid(self, user_id):
        self.user_id = user_id

    def  select_cats(self):
        categories = []
        cat_names = self.execute(self.sql_cats, self.user_id)
        for name in cat_names:
            categories.append(name)
        return categories

    def build_bookmarks(self, categories):
        sql_bookms = '''select bookmarks.id as bid, cat_name, title, url, description 
                from users, categories, bookmarks where 
                users.id = bookmarks.user_id and 
                bookmarks.categ_name=categories.cat_name  and 
                categories.cat_name = ? and users.id = ?
                order by title'''
        bookmarks = []
        for cat in categories:
            rows = self.execute(sql_bookms, (cat['cat_name'], self.user_id))
        
            for row in rows:
                row['short_title'] = shorten_title(row['title'], 25)
                row['tooltip'] = '<em><u>Category</u></em> : ' + cat['cat_name']\
                                + '\n' + '<em><u>Title</u></em> : ' + row['title']\
                                + '\n' + '<em><u>Description</u></em> : ' + row['description']\
                               # + '\n' + '<em><u>Id</u></em>: ' + str(row['bid'])
            #print(rows)
            dict = {}
            dict['category'] = shorten_title(cat['cat_name'].lower(), 15)
            dict['rows'] = rows
            if rows:
                bookmarks.append(dict)
        return bookmarks

         

     
