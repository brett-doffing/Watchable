from tkinter import *
from CamsView import CamsView
from Cameras.CameraMenu import CameraMenu

if __name__ == "__main__":
    root = Tk()
    root.title('Watchful App')
    root.wm_geometry("960x640")
    app = CamsView(root)
    broadcasts = []


    def showCameraMenu():
        CameraMenu(root, broadcasts)


    def shutdown():
        [process.kill() for process in broadcasts]
        root.destroy()

    
    # create a menubar
    menubar = Menu(root)
    root.config(menu=menubar)
    # create a menu
    file_menu = Menu(menubar)
    calibrate_menu = Menu(menubar)
    camera_menu = Menu(menubar)
    # add the File menu to the menubar
    menubar.add_cascade(
        label="File",
        menu=file_menu
    )
    menubar.add_cascade(
        label="Calibration",
        menu=calibrate_menu
    )
    menubar.add_cascade(
        label="Cameras",
        menu=camera_menu
    )
    # add a menu item to the menu
    file_menu.add_command(
        label='Exit',
        command=shutdown
    )
    calibrate_menu.add_command(
        label='Calibrate',
        command=app.calibrate,
    )
    camera_menu.add_command(
        label='Add',
        command=showCameraMenu,
    )
    
    root.mainloop()
