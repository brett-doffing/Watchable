from tkinter import *
from CamsView import CamsView

if __name__ == "__main__":
    root = Tk()
    root.title('Watchful App')
    root.wm_geometry("960x640")
    app = CamsView(root)
    
    # create a menubar
    menubar = Menu(root)
    root.config(menu=menubar)
    # create a menu
    file_menu = Menu(menubar)
    # add a menu item to the menu
    file_menu.add_command(
        label='Exit',
        command=root.destroy
    )
    # add the File menu to the menubar
    menubar.add_cascade(
        label="File",
        menu=file_menu
    )
    
    root.mainloop()
