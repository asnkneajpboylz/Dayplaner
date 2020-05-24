from TimeManager import TimeManager
from Event import Event


class EventManager:
    events = []
    mittagspause = Event(TimeManager.mittagspauseStart, TimeManager.mittagspauseEnde)
    @staticmethod
    def addEvent(event):
        # passe das einzufügende Event an die Lücke an, dh überprüfen ob es überschneidungen gibt, Verknüpfungen
        # erstellen und nicht wie beim VerschiebenNach das andere Event anpassen, sonder das neue Event anpassen
        for oevent in EventManager.events:
            if event.schneiden(oevent):

                if (oevent.startzeit >= event.startzeit and event.endzeit >= oevent.startzeit): # das andere Event liegt im neuen Element, Event wird gekürzt
                    EventManager.verschiebeZeitNach(event, False, oevent.startzeit)
                    EventManager.events.append(event)
                    return
                elif (oevent.startzeit == event.startzeit and oevent.endzeit == event.endzeit): #beide elemente decken sich komplett
                    return
                elif (event.startzeit <= oevent.endzeit and event.endzeit > oevent.endzeit): #Event liegt unterhalb von oevent
                    EventManager.verschiebeZeitNach(event, True, oevent.endzeit)
                    EventManager.events.append(event)

    @staticmethod
    def removeEvent(event):
        #lösche die Verknüpfungen über Vorheriges Element und folgendes Element
        if (event.eventDanach != None):
            event.eventDanach.eventDavor = None
        if (event.eventDavor != None):
            event.eventDanach.eventDanach = None

        EventManager.events.remove(event)

    #Methode um Events zu verschieben
    #Wenn das Event das nachstehende oder vorherstehende Element weiß kann es die Verschiebung weitergeben und
    #aufs nächste Element anweden
    #Falls nicht sucht es noch überschneidenden Elemente und verschiebt diese dann um die fehlende Differenz
    @staticmethod
    def verschiebeEventUm(event, zeit):
        deltaZeit = event.endzeit - event.startzeit
        event.startzeit += zeit
        event.endzeit += zeit

        #Prüft nach ob das Event in eine der verbotenen Bereiche überlappt udn kürzt oder löscht das Event
        if (event.startzeit < TimeManager.aufstehzeit):
            EventManager.verschiebeZeitNach(event, True, TimeManager.aufstehzeit)
        if (event.endzeit > TimeManager.aufstehzeit):
            EventManager.verschiebeZeitNach(event, False,  TimeManager.schlafenszeit)
        if (event.schneiden(EventManager.mittagspause)):
            if (zeit < TimeManager.null):
                if (event.endzeit <= TimeManager.mittagspauseEnde): EventManager.removeEvent(event)
                EventManager.verschiebeZeitNach(event, True, TimeManager.mittagspauseEnde)
            elif (zeit >= TimeManager.null):
                if (event.startzeit >= TimeManager.mittagspauseStart): EventManager.removeEvent(event)
                EventManager.verschiebeZeitNach(event, False, TimeManager.mittagspauseStart)

        #Prüft ob es Anhängende Events gib die leicht verschoben werden können
        if (zeit > TimeManager.null):
            if event.eventDanach != None:
                EventManager.verschiebeEventUm(event.eventDanach, zeit)
                return
        elif (zeit < TimeManager.null):
            if event.eventDavor != None:
                EventManager.verschiebeEventUm(event.eventDavor, zeit)
                return

        #Prüft ob das Event mit anderen Events kollidiert und verschiebt diese entsprechend
        otherEvents = list(filter(lambda x: x != event))
        for oevent in otherEvents:
            if (event.schneiden(oevent)):
                if (oevent.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit): # das Event liegt im neuen Element
                    if (zeit < TimeManager.null):
                        EventManager.verschiebeEventUm(oevent, event.startzeit - oevent.endzeit) #verschiebe Event nach vorne
                        event.eventDavor = oevent
                        oevent.eventDanach = event
                    if (zeit >= TimeManager.null):
                        EventManager.verschiebeEventUm(oevent, event.endzeit - oevent.startzeit) #verschiebe Event nach hinten
                        event.eventDanach = oevent
                        oevent.eventDavor = event
                    break
                elif (oevent.startzeit <= event.startzeit and oevent.endzeit >= event.startzeit): #anderes Event schneidet von oben hinein
                    if (zeit < TimeManager.null):
                        EventManager.verschiebeEventUm(oevent, event.startzeit - oevent.endzeit)
                        event.eventDavor = oevent
                        oevent.eventDanach = event
                    if (zeit >= TimeManager.null):
                        EventManager.verschiebeEventUm(oevent, event.endzeit - oevent.startzeit)
                        oevent.eventDavor = event
                        event.eventDanach = oevent
                    break
                elif (oevent.startzeit > event.startzeit and oevent.endzeit > event.endzeit): #anderes event runtscht von unten hinein
                    if (zeit < TimeManager.null):
                        EventManager.verschiebeEventUm(oevent, event.startzeit - oevent.endzeit)
                        event.eventDavor = oevent
                        oevent.eventDanach = event
                    if (zeit >= TimeManager.null):
                        EventManager.verschiebeEventUm(oevent, event.endzeit - oevent.startzeit)
                        event.eventDanach = oevent
                        oevent.eventDavor = event
                    break

    # Verschiebt eine Zeit, nur falls startzeit vor endzeit liegt
    @staticmethod
    def verschiebeZeitNach(event, istStartzeit, zeit):
        # überprüft ob verschiebung erlaubt
        if istStartzeit:
            if event.endzeit - zeit <= 0: return
            event.startzeit.set(zeit)
        else:
            if zeit - event.startzeit <= 0: return
            event.endzeit.set(zeit)

        # überschneidungen korrigieren, indem die Grenzen strikt neu verändern werden. Anhängende Teile werden nicht
        # verschoben sonder gekürzt
        otherEvents = list(filter(lambda x: x != event))
        for oevent in otherEvents:
            if (event.schneiden(oevent)):
                if (
                        oevent.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit):  # das Event liegt im neuen Element
                    EventManager.removeEvent(oevent)
                    break
                elif (
                        oevent.startzeit <= event.startzeit and oevent.endzeit >= event.startzeit):  # anderes Event schneidet von oben hinein
                    oevent.endzeit.set(event.startzeit)
                    oevent.eventDanach = event
                    event.eventDavor = oevent
                    break
                elif (
                        oevent.startzeit >= event.startzeit and oevent.endzeit >= event.endzeit):  # anderes event runtscht von unten hinein
                    oevent.startzeit.set(event.endzeit)
                    oevent.eventDavor = event
                    event.eventDanach = oevent
                    break

