""" Window
"""


import tkinter
import tkinter.ttk

from . import i18n
from . import task


_ = i18n.translate


class Track(tkinter.Frame):  # pylint: disable=too-many-ancestors
    """ Current track
    """

    def __init__(self, master=None):
        super(Track, self).__init__(master)
        self._create_widgets()
        self._layout_widgets()
        return None

    def _create_widgets(self):
        self.label = tkinter.Label(self, text=_("Pmpc"))
        return None

    def _layout_widgets(self):
        self.label.grid(sticky=tkinter.EW)
        self.grid_columnconfigure(0, weight=1)
        return None


class Playback(tkinter.Frame):  # pylint: disable=too-many-ancestors
    """ Playback buttons
    """

    def __init__(self, master=None):
        super(Playback, self).__init__(master)
        self._create_widgets()
        self._layout_widgets()
        return None

    def _create_widgets(self):
        self.previous = tkinter.Button(self, text=_("Previous"))
        self.pause = tkinter.Button(self, text=_("Pause"))
        self.next = tkinter.Button(self, text=_("Next"))
        return None

    def _layout_widgets(self):
        self.previous.grid(row=0, column=0, sticky=tkinter.EW)
        self.pause.grid(row=0, column=1, sticky=tkinter.EW)
        self.next.grid(row=0, column=2, sticky=tkinter.EW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        return None


class Playlist(tkinter.Frame):  # pylint: disable=too-many-ancestors
    """ Playlist
    """

    def __init__(self, master=None):
        super(Playlist, self).__init__(master)
        self._create_widgets()
        self._config_widgets()
        self._layout_widgets()
        return None

    def _create_widgets(self):
        self.scrollbar = tkinter.Scrollbar(self)
        self.tree = tkinter.ttk.Treeview(self, selectmode=tkinter.NONE)
        return None

    def _config_widgets(self):
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.column('#0', width=50, anchor='e', stretch=tkinter.NO)
        self.tree['columns'] = ('artist', 'title')
        self.tree.heading('artist', text=_("Artist"))
        self.tree.heading('title', text=_("Title"))
        self.scrollbar.config(command=self.tree.yview)
        return None

    def _layout_widgets(self):
        self.scrollbar.grid(row=0, column=1, sticky=tkinter.NS)
        self.tree.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        return None


class Frame(tkinter.Frame):  # pylint: disable=too-many-ancestors
    """ Main frame
    """

    def __init__(self, master=None):
        super(Frame, self).__init__(master)
        self._create_widgets()
        self._layout_widgets()
        return None

    def _create_widgets(self):
        self.track = Track(self)
        self.playback = Playback(self)
        self.playlist = Playlist(self)
        return None

    def _layout_widgets(self):
        self.track.grid(row=0, sticky=tkinter.EW)
        self.playback.grid(row=1, sticky=tkinter.EW)
        self.playlist.grid(row=2, sticky=tkinter.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        return None


class Window(task.Task):
    """ Tkinter UI task
    """

    def __init__(self, name):
        self._current_track = {}
        self._create_widgets()
        self._config_widgets()
        self._layout_widgets()
        event_handlers = {
            'track': self._event_handler_track,
            'playlist': self._event_handler_playlist,
            'quit': self._event_handler_quit,
        }
        super(Window, self).__init__(name, event_handlers, threaded=False)
        return None

    def _create_widgets(self):
        self._root = tkinter.Tk()
        self._frame = Frame(master=self._root)
        return None

    def _config_widgets(self):
        self._root.title(_("Pmpc"))
        self._root.protocol('WM_DELETE_WINDOW', self._callback_quit)
        self._notify_event = '<<notify_event>>'
        self._root.bind(self._notify_event, self._interrupt)
        self._frame.playback.pause['command'] = self._callback_pause
        self._frame.playback.next['command'] = self._callback_next
        self._frame.playback.previous['command'] = self._callback_previous
        return None

    def _layout_widgets(self):
        self._frame.grid(sticky=tkinter.NSEW)
        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_rowconfigure(0, weight=1)
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
        self._frame.track.label['text'] = '{} - {}'.format(
            track['artist'],
            track['title'],
        )
        self._current_track = track
        self._highlight_current_track()
        return None

    def _set_current_playlist(self, playlist):
        self._frame.playlist.tree.delete(
            *self._frame.playlist.tree.get_children()
        )
        for track_index, track in enumerate(playlist):
            self._frame.playlist.tree.insert(
                '',  # insert as top level item
                track_index,  # item index
                track['pos'],  # item identifier
                text='{}'.format(track_index + 1),
                values=(
                    track['artist'],
                    track['title'],
                ),
            )
        self._highlight_current_track()
        return None

    def _highlight_current_track(self):
        pos = self._current_track.get('pos', '')
        if self._frame.playlist.tree.exists(pos):
            self._frame.playlist.tree.selection_set(pos)
            self._frame.playlist.tree.see(pos)
        else:
            self._frame.playlist.tree.selection_set('')
        return None


# EOF
