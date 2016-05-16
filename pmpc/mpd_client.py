""" MPD observer
"""


import logging
import uuid

import mpd

from . import fsm_task
from . import i18n


LOG = logging.getLogger(__name__)

_ = i18n.translate


class MpdClient(fsm_task.FsmTask):
    """ Interface to 'music player daemon' server.
    """

    def __init__(self, name, host, port):
        self._host = host
        self._port = port
        self._mpd_client = mpd.MPDClient(use_unicode=True)
        self._status = None
        self._connected = False
        self._notify_channel = str(uuid.uuid4())
        self._notify_message = str(uuid.uuid4())
        states = {
            'initializing': {
                'transitions': {
                    'started': {
                        'next_state': 'connecting',
                    },
                },
                'handlers': {
                    'quit': self._event_handler_quit,
                },
            },
            'connecting': {
                'enter': self._enter_connecting,
                'transitions': {
                    'connected': {
                        'next_state': 'idling',
                    },
                },
                'handlers': {
                    'quit': self._event_handler_quit,
                },
            },
            'idling': {
                'handlers': {
                    'previous': self._event_handler_previous,
                    'next': self._event_handler_next,
                    'pause': self._event_handler_pause,
                    'quit': self._event_handler_quit,
                },
            },
        }
        super(MpdClient, self).__init__(name, states, 'initializing')
        return None

    def _run_pre(self):
        """ Override 'task.Task'
        """
        self.post({
            'type': 'started',
            'value': None,
        })
        return None

    def _run_post(self):
        """ Override 'task.Task'
        """
        self._mpd_client.unsubscribe(self._notify_channel)
        self._mpd_client.close()
        return None

    def _routine(self):
        """ Override 'task.Task'
        """
        if self._connected:
            self._mpd_client.idle()
            if self._woken_by_message():
                self._process_event_queue()
            else:
                self._check_status()
        else:
            self._process_event_queue()
        return None

    def _notify(self):
        """ Override 'task.Task'
        """
        if self._connected:
            client = mpd.MPDClient()
            client.connect(self._host, self._port)
            try:
                client.sendmessage(self._notify_channel, self._notify_message)
            except mpd.CommandError:
                LOG.error(_("Could not notify."))
            client.close()
        return None

    def _woken_by_message(self):
        result = False
        for message in self._mpd_client.readmessages():
            chn = message.get('channel', None)
            msg = message.get('message', None)
            if chn == self._notify_channel and msg == self._notify_message:
                result = True
                break
        return result

    def _check_status(self):
        status = self._mpd_client.status()
        if not self._status or status['songid'] != self._status['songid']:
            track = self._mpd_client.currentsong()
            self._emit({
                'type': 'mpd.track',
                'value': track,
            })
            playlist = self._mpd_client.playlistinfo()
            self._emit({
                'type': 'mpd.playlist',
                'value': playlist,
            })
        self._status = status
        return None

    def _event_handler_previous(self, dummy_event_value):
        self._mpd_client.previous()
        return None

    def _event_handler_next(self, dummy_event_value):
        self._mpd_client.next()
        return None

    def _event_handler_pause(self, dummy_event_value):
        self._mpd_client.pause()
        return None

    def _event_handler_quit(self, dummy_event_value):
        self.stop()
        return None

    def _enter_connecting(self, dummy_event):
        self._mpd_client.connect(self._host, self._port)
        self._mpd_client.subscribe(self._notify_channel)
        self._connected = True
        self._check_status()
        self.post({
            'type': 'connected',
            'value': None,
        })
        return None


# EOF
