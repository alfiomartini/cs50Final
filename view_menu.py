from database import mydb
from helpers import shorten_title
class View():
    def __init__(self):
        # {name:cat, checked:bool}
        self.menu = self.catsMenu()

    def catsMenu(self):
        catsMenu = []
        cats = mydb.select_cats()
        # print(cats)
        for cat in cats:
            catDict = {}
            catDict['name'] = cat['cat_name']
            catDict['checked'] = True 
            catDict['menu_item'] =  shorten_title(cat['cat_name'], 15)
            catDict['status'] = '[ On ]'
            catsMenu.append(catDict)
        return catsMenu

    def setChecked(self, name, truthy):
        for item in self.menu:
            if item['name'].lower() == name.lower():
                item['checked'] = truthy
                if truthy:
                    item['status'] = '[ On ]'
                else:
                    item['status'] = '[ Off ]'
                break

    def getMenu(self):
        return self.menu

    def getItemStatus(self, name):
        for item in self.menu:
            if item['name'].lower() == name.lower():
                return item['checked']
        return False # have to think about it


# mydb.set_userid(1) # for testing purposes
# viewMenu = View()
# menu = viewMenu.getMenu()
# for item in menu:
#     print(item['menu'])
# viewMenu.setChecked('Computer SciEnce', False)
# menu = viewMenu.getMenu()
# for item in menu:
#     print(item['menu'])