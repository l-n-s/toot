import json
import traceback
import urwid

from toot import __version__

from .utils import highlight_keys
from .widgets import Button, EditBox


class StatusSource(urwid.ListBox):
    """Shows status data, as returned by the server, as formatted JSON."""
    def __init__(self, status):
        source = json.dumps(status.data, indent=4)
        lines = source.splitlines()
        walker = urwid.SimpleFocusListWalker([
            urwid.Text(line) for line in lines
        ])
        super().__init__(walker)


class ExceptionStackTrace(urwid.ListBox):
    """Shows an exception stack trace."""
    def __init__(self, ex):
        lines = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        walker = urwid.SimpleFocusListWalker([
            urwid.Text(line) for line in lines
        ])
        super().__init__(walker)


class GotoMenu(urwid.ListBox):
    signals = [
        "home_timeline",
        "public_timeline",
        "hashtag_timeline",
    ]

    def __init__(self):
        self.hash_edit = EditBox(caption="Hashtag: ")

        actions = list(self.generate_actions())
        walker = urwid.SimpleFocusListWalker(actions)
        super().__init__(walker)

    def get_hashtag(self):
        return self.hash_edit.edit_text.strip()

    def generate_actions(self):
        def _home(button):
            self._emit("home_timeline")

        def _local_public(button):
            self._emit("public_timeline", True)

        def _global_public(button):
            self._emit("public_timeline", False)

        def _hashtag(local):
            hashtag = self.get_hashtag()
            if hashtag:
                self._emit("hashtag_timeline", hashtag, local)
            else:
                self.set_focus(4)

        yield Button("Home timeline", on_press=_home)
        yield Button("Local public timeline", on_press=_local_public)
        yield Button("Global public timeline", on_press=_global_public)
        yield urwid.Divider()
        yield self.hash_edit
        yield Button("Local hashtag timeline", on_press=lambda x: _hashtag(True))
        yield Button("Public hashtag timeline", on_press=lambda x: _hashtag(False))


class Help(urwid.Padding):
    def __init__(self):
        actions = list(self.generate_contents())
        walker = urwid.SimpleListWalker(actions)
        listbox = urwid.ListBox(walker)
        super().__init__(listbox, left=1, right=1)

    def generate_contents(self):

        def h(text):
            return highlight_keys(text, "cyan")

        yield urwid.Text(("yellow_bold", "toot {}".format(__version__)))
        yield urwid.Divider()
        yield urwid.Text(("bold", "General usage"))
        yield urwid.Divider()
        yield urwid.Text(h("  [Arrow keys] or [H/J/K/L] to move around and scroll content"))
        yield urwid.Text(h("  [PageUp] and [PageDown] to scroll content"))
        yield urwid.Text(h("  [Enter] or [Space] to activate buttons and menu options"))
        yield urwid.Text(h("  [Esc] or [Q] to go back, close overlays, such as menus and this help text"))
        yield urwid.Divider()
        yield urwid.Text(("bold", "General keys"))
        yield urwid.Divider()
        yield urwid.Text(h("  [Q] - quit toot"))
        yield urwid.Text(h("  [G] - go to - switch timelines"))
        yield urwid.Text(h("  [H] - show this help"))
        yield urwid.Divider()
        yield urwid.Text(("bold", "Status keys"))
        yield urwid.Divider()
        yield urwid.Text("These commands are applied to the currently focused status.")
        yield urwid.Divider()
        yield urwid.Text(h("  [B] - Boost/unboost status"))
        yield urwid.Text(h("  [C] - Compose new status"))
        yield urwid.Text(h("  [F] - Favourite/unfavourite status"))
        yield urwid.Text(h("  [R] - Reply to current status"))
        yield urwid.Text(h("  [S] - Show text marked as sensitive"))
        yield urwid.Text(h("  [T] - Show status thread (replies)"))
        yield urwid.Text(h("  [U] - Show the status data in JSON as received from the server"))
        yield urwid.Text(h("  [V] - Open status in default browser"))
