#pip install pywin32 -> This will install the libs that are required
from win32gui import IsWindowVisible, GetWindowText, EnumWindows,\
ShowWindow, SetForegroundWindow, SystemParametersInfo

import win32con

#Sub-Functions
def window_enum_handler(hwnd, resultList):
    if IsWindowVisible(hwnd) and GetWindowText(hwnd) != '':
        resultList.append((hwnd, GetWindowText(hwnd)))

#Prime-Functions
def winHide(partial_window_name):
    SystemParametersInfo(8193, 0, 2 | 1)
    handles=[]
    EnumWindows(window_enum_handler, handles)
    for i in handles:
        if str(partial_window_name).upper() in str(i[1]).upper():
            ShowWindow(i[0],  win32con.SW_HIDE)
#            SetForegroundWindow(i[0])
            return True
    print(partial_window_name + " was not found")
    return False

