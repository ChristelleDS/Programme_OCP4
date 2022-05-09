from view.view import Menu
from controller.controller import Controller

ctr = Controller()
menu = Menu(ctr)
menu.home()
