""" Win32 system tray icon
"""


import win32con
import win32gui
import win32gui_struct


class Win32SystemTrayIcon(object):
    """ Win32 system tray icon
    """

    _CALLBACK_MESSAGE = win32con.WM_USER + 20  # not sure why this value
    _FIRST_ITEM_ID = 1023  # not sure why this value
    _WINDOW_CLASS_NAME = 'Win32SystemTrayIcon'

    def __init__(self, hover, callback):
        # parameters
        self._hover = hover
        self._callback = callback
        # utility attributes
        self._menu_items = {}
        self._current_item_id = 0
        self._popup_handle = None
        self._hicon = None
        self._user_event_handler_map = {
            win32con.WM_RBUTTONUP: self._handle_right_click,
        }
        # initialize
        self._reset_menu_items()
        return None

    def build(self):
        """ Build the icon and the popup.
        """
        self._build_popup()
        self._build_icon()
        return None

    def show(self):  # pylint: disable=no-self-use
        """ Show.
        """
        win32gui.PumpMessages()
        return None

    def show_menu(self, menu_items):
        """ Show a popup menu.
        """
        self._reset_menu_items()
        popup_menu = win32gui.CreatePopupMenu()
        self._build_menu(popup_menu, menu_items)
        cursor_position = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self._popup_handle)
        win32gui.TrackPopupMenu(
            popup_menu,
            win32con.TPM_LEFTALIGN,
            cursor_position[0],
            cursor_position[1],
            0,
            self._popup_handle,
            None,
        )
        return None

    def show_balloon(self, title, info):
        """ Show a notification balloon.
        """
        message = win32gui.NIM_MODIFY
        notify_icon_data = (
            self._popup_handle,
            0,
            win32gui.NIF_INFO,
            self._CALLBACK_MESSAGE,
            self._hicon,
            self._hover,
            info,
            200,
            title,
        )
        win32gui.Shell_NotifyIcon(message, notify_icon_data)
        return None

    def notify(self):
        """ Wake up the message pump with a void message.
        """
        win32gui.PostMessage(self._popup_handle, win32con.WM_NULL, 0, 0)
        return None

    def destroy(self):
        """ Destroy.
        """
        win32gui.DestroyWindow(self._popup_handle)
        return None

    def _handle_menu_item(self, item_id):
        if item_id in self._menu_items:
            self._callback(
                self,
                {
                    'type': 'menu_item',
                    'value': self._menu_items[item_id],
                },
            )
        return None

    def _handle_command(self, hwnd, dummy_msg, wparam, dummy_lparam):
        if hwnd == self._popup_handle:
            item_id = win32gui.LOWORD(wparam)
            self._handle_menu_item(item_id)
        return None

    def _handle_destroy(self, hwnd, dummy_msg, dummy_wparam, dummy_lparam):
        if hwnd == self._popup_handle:
            notification_icon_data = (self._popup_handle, 0)
            win32gui.Shell_NotifyIcon(
                win32gui.NIM_DELETE,
                notification_icon_data,
            )
            win32gui.PostQuitMessage(0)
        return None

    def _handle_right_click(self):
        self._callback(
            self,
            {
                'type': 'right_click',
                'value': None,
            },
        )
        return None

    def _handle_null(self, hwnd, dummy_msg, dummy_wparam, dummy_lparam):
        if hwnd == self._popup_handle:
            self._callback(
                self,
                {
                    'type': 'notify',
                    'value': None,
                },
            )
        return None

    def _handle_user(self, hwnd, dummy_msg, dummy_wparam, lparam):
        if hwnd == self._popup_handle:
            if lparam in self._user_event_handler_map:
                self._user_event_handler_map[lparam]()
        return True

    def _build_menu_item(self, menu_item):  # pylint: disable=no-self-use
        item_id = self._get_next_item_id()
        win32_item, dummy_extras = win32gui_struct.PackMENUITEMINFO(
            text=menu_item['text'],
            wID=item_id,
        )
        self._register_menu_item(
            item_id,
            menu_item,
        )
        return win32_item

    def _build_submenu(self, item, submenu):  # pylint: disable=no-self-use
        win32_item, dummy_extras = win32gui_struct.PackMENUITEMINFO(
            hSubMenu=submenu,
            text=item['text'],
        )
        return win32_item

    def _build_menu(self, popup_menu, menu_items):
        for menu_item in reversed(menu_items):
            if 'menu' in menu_item:
                submenu = win32gui.CreatePopupMenu()
                self._build_menu(submenu, menu_item['menu'])
                win32_item = self._build_submenu(menu_item, submenu)
                win32gui.InsertMenuItem(popup_menu, 0, 1, win32_item)
            else:
                win32_item = self._build_menu_item(menu_item)
                win32gui.InsertMenuItem(popup_menu, 0, 1, win32_item)
        return None

    def _register_menu_item(self, item_id, action):
        self._menu_items[item_id] = action
        return None

    def _build_icon(self):
        """ Build the system tray icon.
        """
        message = win32gui.NIM_ADD
        self._hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        notify_icon_data = (
            self._popup_handle,
            0,
            win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
            self._CALLBACK_MESSAGE,
            self._hicon,
            self._hover,
        )
        win32gui.Shell_NotifyIcon(message, notify_icon_data)
        return None

    def _build_popup(self):
        """ Build the popup window.
        """
        message_map = {
            win32con.WM_DESTROY: self._handle_destroy,
            win32con.WM_COMMAND: self._handle_command,
            self._CALLBACK_MESSAGE: self._handle_user,
            win32con.WM_NULL: self._handle_null,
        }

        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self._WINDOW_CLASS_NAME
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map
        class_atom = win32gui.RegisterClass(window_class)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self._popup_handle = win32gui.CreateWindow(
            class_atom,
            self._WINDOW_CLASS_NAME,
            style,
            0,
            0,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            hinst,
            None,
        )
        win32gui.UpdateWindow(self._popup_handle)
        return None

    def _get_next_item_id(self):
        self._current_item_id = self._current_item_id + 1
        return self._current_item_id

    def _reset_menu_items(self):
        self._current_item_id = self._FIRST_ITEM_ID
        self._menu_items = {}
        return None


# EOF
