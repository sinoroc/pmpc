""" Systray
"""


from . import i18n
from . import task
from . import win32_system_tray_icon


_ = i18n.translate


class Systray(task.Task):
    """ System tray icon
    """

    def __init__(self, name, menu):
        self._menu = menu
        self._icon = None
        event_handlers = {
            'menu': self._event_handler_menu,
            'balloon': self._event_handler_balloon,
            'quit': self._event_handler_quit,
        }
        super(Systray, self).__init__(name, event_handlers)
        return None

    def _run_pre(self):
        """ Override 'task.Task'.
        """
        self._icon = win32_system_tray_icon.Win32SystemTrayIcon(
            _("Pmpc"),
            self._callback,
        )
        self._icon.build()
        return None

    def _routine(self):
        """ Override 'task.Task'.
        """
        self._icon.show()  # pywin32 message pump
        return None

    def _notify(self):
        """ Override 'task.Task'.
        """
        self._icon.notify()
        return None

    def _callback(self, icon, event):
        if icon is self._icon:
            event_type = event.get('type', None)
            event_value = event.get('value', None)
            if event_type == 'notify':
                self._process_event_queue()
            elif event_type == 'menu_item':
                self._emit({
                    'type': 'icon.menu_item',
                    'value': event_value,
                })
            elif event_type == 'right_click':
                self._emit({
                    'type': 'icon.menu',
                    'value': self._icon,
                })
        return None

    def _event_handler_menu(self, event):
        self._icon.show_menu(event['value'])
        return None

    def _event_handler_balloon(self, event):
        self._icon.show_balloon(
            event['value']['title'],
            event['value']['info'],
        )
        return None

    def _event_handler_quit(self, dummy_event):
        self.stop()
        self._icon.destroy()
        return None


# EOF
