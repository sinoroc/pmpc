""" Window
"""


import tkinter
import tkinter.ttk

from . import i18n
from . import task


_ = i18n.translate


class Frame(tkinter.Frame):  # pylint: disable=too-many-ancestors
    """ Main frame
    """

    def __init__(self, master=None):
        super(Frame, self).__init__(master)  # before creating widgets
        self._create_widgets()
        self.pack()
        return None

    def _create_widgets(self):
        self.current_track_label = tkinter.Label(self, text=_("Pmpc"))
        self.current_track_label.grid(row=0, column=0, columnspan=3)
        self.previous_button = tkinter.Button(self, text=_("Previous"))
        self.previous_button.grid(row=1, column=0)
        self.pause_button = tkinter.Button(self, text=_("Pause"))
        self.pause_button.grid(row=1, column=1)
        self.next_button = tkinter.Button(self, text=_("Next"))
        self.next_button.grid(row=1, column=2)
        self._playlist_frame = tkinter.Frame(self)
        self._playlist_scrollbar = tkinter.Scrollbar(self._playlist_frame)
        self._playlist_scrollbar.grid(
            row=0,
            column=1,
            sticky=(tkinter.N + tkinter.S),
        )
        self.playlist = tkinter.ttk.Treeview(
            self._playlist_frame,
            yscrollcommand=self._playlist_scrollbar.set,
        )
        self.playlist['columns'] = ('artist', 'title')
        self.playlist.column('artist', width=100)
        self.playlist.column('title', width=100)
        self.playlist.heading('artist', text=_("Artist"))
        self.playlist.heading('title', text=_("Title"))
        self._playlist_scrollbar.config(command=self.playlist.yview)
        self.playlist.grid(row=0, column=0)
        self._playlist_frame.grid(row=2, column=0, columnspan=3)
        return None


class Window(task.Task):
    """ Tkinter UI task
    """

    def __init__(self, name):
        self._root = tkinter.Tk()
        self._root.protocol('WM_DELETE_WINDOW', self._callback_quit)
        self._frame = Frame(master=self._root)
        self._notify_event = '<<notify_event>>'
        self._root.bind(self._notify_event, self._interrupt)
        self._frame.pause_button['command'] = self._callback_pause
        self._frame.next_button['command'] = self._callback_next
        self._frame.previous_button['command'] = self._callback_previous
        event_handlers = {
            'track': self._event_handler_track,
            'playlist': self._event_handler_playlist,
            'quit': self._event_handler_quit,
        }
        super(Window, self).__init__(name, event_handlers, threaded=False)
        return None

    def _routine(self):
        """ Override 'task.Task'.
            Execute Tkinter's event loop.
        """
        self._root.mainloop()
        return None

    def _notify(self):
        """ Override 'task.Task'.
            Send notify event to break own Tkinter event loop.
        """
        self._root.event_generate(self._notify_event, when='tail')
        return None

    def _interrupt(self, dummy_tkinter_event):
        """ Receive notify event.
        """
        self._process_event_queue()
        return None

    def _callback_pause(self):
        self._emit({
            'type': 'window.pause',
            'value': None,
        })
        return None

    def _callback_next(self):
        self._emit({
            'type': 'window.next',
            'value': None,
        })
        return None

    def _callback_previous(self):
        self._emit({
            'type': 'window.previous',
            'value': None,
        })
        return None

    def _callback_quit(self):
        self._emit({
            'type': 'window.quit',
            'value': None,
        })
        return None

    def _event_handler_track(self, event):
        self._set_current_track(event['value'])
        return None

    def _event_handler_playlist(self, event):
        self._set_current_playlist(event['value'])
        return None

    def _event_handler_quit(self, dummy_event):
        self.stop()
        self._root.destroy()
        return None

    def _set_current_track(self, track):
        self._frame.current_track_label['text'] = '{} - {}'.format(
            track['artist'],
            track['title'],
        )
        return None

    def _set_current_playlist(self, playlist):
        for track_index, track in enumerate(playlist):
            self._frame.playlist.insert(
                '',
                'end',
                text=_("#{}").format(track_index + 1),
                values=(
                    track['artist'],
                    track['title'],
                ),
            )
        return None


# EOF
