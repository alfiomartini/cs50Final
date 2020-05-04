from cs50 import SQL

class MySQL(SQL):
    def __init__(self, dbpath):
        super().__init__(dbpath)
        self.sql_cats = '''select cat_name from categories 
                    where user_id = ? 
                    order by cat_name'''
        self.sql_bookms = '''select bookmarks.id as bid, cat_name, title, url, description 
                    from users, categories, bookmarks where 
                    users.id = bookmarks.user_id and 
                    bookmarks.categ_name=categories.cat_name  and 
                    categories.cat_name = ? and users.id = ?
                    order by title'''

    def  select_cats(self, user_id):
        categories = []
        cat_names = self.execute(self.sql_cats, user_id)
        for name in cat_names:
            categories.append(name)
        return categories
         

     
