from database import mydb
from helpers import shorten_title
from flask import session

# alternative version, as a function instead as of a method
def catsMenu(view):
        catsMenu = []
        cats = mydb.execute('''select * from menu where user_id = ? order by cat_name''',
           (session['user_id'],))
        for cat in cats:
            catDict = {}
            catDict['name'] = cat['cat_name']
            catDict['checked'] = cat['visible']
            catDict['menu_item'] =  shorten_title(cat['cat_name'], 15)
            if cat['visible'] == 1:
                catDict['status'] = '[ On ]'
            else:
                catDict['status'] = '[ Off ]'
            catsMenu.append(catDict)
        view.setMenu(catsMenu)
        return catsMenu



class View():
    def __init__(self):
        self.menu = []

    def setMenu(self, menu):
        self.menu = menu 

    def getMenu(self):
      return self.menu

    def getItemStatus(self, name):
        for item in self.menu:
            if item['name'].lower() == name.lower():
                return item['checked']

    def setChecked(self, name, truthy):
        for item in self.menu:
            if item['name'].lower() == name.lower():
                item['checked'] = truthy
                if truthy:
                    visible = 1
                else:
                    visible = 0
                print('user_id', session['user_id'])
                print('visible', visible)
                mydb.execute('''update menu set visible = ? where 
                        cat_name = ? and user_id = ?''', 
                        visible, name.lower(), session['user_id'])
                break

    def catsMenu(self):
        catsMenu = []
        cats = mydb.execute('''select * from menu where user_id = ? order by cat_name''',
           (session['user_id'],))
        for cat in cats:
            catDict = {}
            catDict['name'] = cat['cat_name']
            catDict['checked'] = cat['visible']
            catDict['menu_item'] =  shorten_title(cat['cat_name'], 15)
            if cat['visible'] == 1:
                catDict['status'] = 'visibility'
            else:
                catDict['status'] = 'visibility_off'
            catsMenu.append(catDict)
        self.setMenu(catsMenu)
        return catsMenu


    
# instantiate view menu object 
viewMenu = View()


# mydb.set_userid(1) # for testing purposes
# viewMenu = View()
# menu = viewMenu.getMenu()
# for item in menu:
#     print(item['menu_item'])
# viewMenu.setChecked('Computer SciEnce', False)
# menu = viewMenu.getMenu()
# for item in menu:
#     print(item['menu_item'])