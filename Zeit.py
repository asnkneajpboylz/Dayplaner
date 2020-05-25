from Objekt import Objekt


class Zeit(Objekt):
    toleranz = (0, 5)

    # Bestimmt die Zeit aus einem String, kann entweder im Format 12 oder 12:00 gemacht werden
    @staticmethod
    def fromString(text):
        if len(text) == 2:
            try:
                stunde = int(text)
                if 0 <= stunde <= 24:
                    zeit = Zeit(stunde, 0)
                    return zeit
                else:
                    return None
            except ValueError:
                return None
        if len(text) == 5:
            try:
                stunde = int(text[0:2])
                minute = int(text[3:5])
                if 0 <= stunde <= 24 and 0 <= minute <= 60:
                    zeit = Zeit(stunde, minute)
                    return zeit
                else:
                    return None
            except ValueError:
                return None

    def __init__(self, stunde, minute, event=None):
        self.stunde = stunde
        self.minute = minute
        self.event = event
        self.text = f"{self.stunde:02}:{self.minute:02}"
        self.form = []

    def __str__(self):
        if self.event is None:
            return f"Zeit {self.stunde:02}:{self.minute:02}"
        else:
            return f"Zeit {self.stunde:02}:{self.minute:02} zu Event {self.event}"

    def __add__(self, other):
        assert (not (self.event is not None and other.event is not None) or self.event == other.event)
        #assert (self.stunde + other.stunde + (self.minute + other.minute) / 60 <= 24) #achtung, Stunde kann damit > 24 sein!
        stunde = self.stunde + other.stunde
        minute = self.minute + other.minute
        if minute >= 60:
            stunde += 1
            minute -= 60
        if minute < 0:
            stunde -= 1
            minute += 60
        event = self.event
        if event is None:
            event = other.event
        return Zeit(stunde, minute, event)

    def __gt__(self, other):
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute > other.minute: return True
        return False

    def __ge__(self, other):
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute >= other.minute: return True
        return False

    def __lt__(self, other):
        return not (self >= other)

    def __le__(self, other):
        return not (self > other)

    def __sub__(self, other):
        stunde = self.stunde - other.stunde
        minute = self.minute - other.minute
        if minute < 0:
            stunde -= 1
            minute += 60
        if minute > 60:
            stunde += 1
            minute -= 60

        event = self.event
        if event is None:
            event = other.event
        return Zeit(stunde, minute, event)

    def __eq__(self, other):
        if self is None and other is None: return True
        if self is None or other is None: return False
        return self.stunde == other.stunde and self.minute == other.minute

    def setEvent(self, event):
        self.event = event

    def set(self, other):
        self.stunde = other.stunde
        self.minute = other.minute
        self.text = other.text

    def circa(self, zeit):
        if abs(self.stunde - zeit.stunde) <= Zeit.toleranz[0] and abs(self.minute - zeit.minute) <= Zeit.toleranz[1]:
            return True
        return False

    def istStartzeit(self):
        if self.circa(self.event.startzeit): return True

    def istEndzeit(self):
        if self.circa(self.event.endzeit): return True

    def callback_verschiebe(self, event):
        from EventManager import EventManager
        if event.keysym == "Return":
            self.unfokusiere()
            nach = Zeit.fromString(self.text)
            if nach is not None:
                if self.event is not None:
                    EventManager.verschiebeZeitNach(self.event, event.istStartzeit(), nach)
                    # überprüft ob die Zeit die Start oder Endzeit ist wenn sie einem Event zugeordnet ist
                    assert (self.istStartzeit() or self.istEndzeit())
                    assert (not self.istStartzeit() and self.istEndzeit())
                else:
                    self.stunde = nach.stunde
                    self.minute = nach.minute
                    self.text = nach.text
        elif event.keysym == "BackSpace":
            self.text = self.text[:-1]
        elif event.keysym == "Delete":
            self.unfokusiere()
        else:
            self.text += event.char

    def zeichne(self):
        pass

    def zeichneMarkiert(self):
        pass

    def entferne(self):
        pass

    def fokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_bind(str(self), "<Key>", self.callback_verschiebe)

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_unbind(str(self))
