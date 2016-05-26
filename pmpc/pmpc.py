""" Pmpc
"""


from . import i18n
from . import mpd_client
from . import systray
from . import task
from . import window


_ = i18n.translate


class Pmpc(task.Task):
    """ GUI client for 'music player daemon'
    """

    _MENU = [{
        'text': _("Pause"),
        'action': 'pause',
    }, {
        'text': _("Next"),
        'action': 'next',
    }, {
        'text': _("Previous"),
        'action': 'previous',
    }, {
        'text': _("Quit"),
        'action': 'quit',
    }]

    def __init__(self, name, host, port):
        self._mpc = mpd_client.MpdClient('mpc', host, port)
        self._systray = systray.Systray('systray', self._MENU)
        self._window = window.Window('window')
        event_handlers = {
            'mpd.track': self._event_handler_mpd_track,
            'mpd.playlist': self._event_handler_mpd_playlist,
            'icon.menu': self._event_handler_icon_menu,
            'icon.menu_item': self._event_handler_icon_menu_item,
            'window.pause': self._event_handler_pause,
            'window.next': self._event_handler_next,
            'window.previous': self._event_handler_previous,
            'window.quit': self._event_handler_quit,
        }
        super(Pmpc, self).__init__(name, event_handlers)
        return None

    def run_ui_task(self):
        """ Start the UI task.
            Tkinter does not want to run in a thread.
        """
        self._window.start()
        return None

    def _run_pre(self):
        """ Override 'task.Task'
        """
        self._mpc.start()
        self._systray.start()
        return None

    def _run_post(self):
        """ Override 'task.Task'
        """
        self._mpc.join()
        self._systray.join()
        return None

    def _event_handler_mpd_track(self, event):
        track = _read_track(event['value'])
        self._systray.post({
            'type': 'balloon',
            'value': {
                'title': track['title'],
                'info': track['artist'],
            },
        })
        self._window.post({
            'type': 'track',
            'value': track,
        })
        return None

    def _event_handler_mpd_playlist(self, event):
        raw_playlist = event['value']
        playlist = []
        for raw_track in raw_playlist:
            track = _read_track(raw_track)
            playlist.append(track)
        self._window.post({
            'type': 'playlist',
            'value': playlist,
        })
        return None

    def _event_handler_icon_menu(self, dummy_event):
        self._systray.post({
            'type': 'menu',
            'value': self._MENU,
        })
        return None

    def _event_handler_icon_menu_item(self, event):
        action = event['value'].get('action', None)
        if action == 'quit':
            self._event_handler_quit(event)
        elif action == 'pause':
            self._event_handler_pause(event)
        elif action == 'next':
            self._event_handler_next(event)
        elif action == 'previous':
            self._event_handler_previous(event)
        return None

    def _event_handler_pause(self, dummy_event):
        self._mpc.post({
            'type': 'pause',
            'value': None,
        })
        return None

    def _event_handler_next(self, dummy_event):
        self._mpc.post({
            'type': 'next',
            'value': None,
        })
        return None

    def _event_handler_previous(self, dummy_event):
        self._mpc.post({
            'type': 'previous',
            'value': None,
        })
        return None

    def _event_handler_quit(self, dummy_event):
        quit_event = {
            'type': 'quit',
            'value': None,
        }
        self._emit(quit_event)
        self.stop()
        return None


def _read_track(raw_track):
    track = {
        'artist': raw_track.get('artist', ""),
        'title': raw_track.get('title', ""),
        'pos': raw_track.get('pos', ""),
    }
    return track


# EOF
