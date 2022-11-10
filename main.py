from sdbus import DbusInterfaceCommonAsync, dbus_method_async_override, dbus_property_async_override, dbus_property_async, dbus_signal_async, request_default_bus_name_async
from sdbus.dbus_proxy_async_interfaces import DbusPropertiesInterfaceAsync
from asyncio import get_event_loop
from iface import OrgMprisMediaPlayer2Interface, OrgMprisMediaPlayer2PlayerInterface
import pygame

SHOW = pygame.USEREVENT + 1
HIDE = pygame.USEREVENT + 2

class BaseInterface(OrgMprisMediaPlayer2Interface, OrgMprisMediaPlayer2PlayerInterface, DbusPropertiesInterfaceAsync):
    _playing = True
    _playstate = "Playing"
    _queue = None

    @dbus_method_async_override()
    async def raise_(self):
        pass

    @dbus_method_async_override()
    async def quit(self):
        pass

    @dbus_property_async_override()
    def can_quit(self):
        return False
    
    @dbus_property_async_override()
    def can_set_fullscreen(self):
        return False
    
    @dbus_property_async_override()
    def can_raise(self):
        return False
    
    @dbus_property_async_override()
    def has_track_list(self):
        return False
    
    @dbus_property_async_override()
    def identity(self):
        return "Presentation"
    
    @dbus_property_async_override()
    def supported_uri_schemes(self):
        return ["file"]
    
    @dbus_property_async_override()
    def supported_mime_types(self):
        return ["text/plain"]

    # Player methods.... horrifying

    @dbus_method_async_override()
    async def next(self):
        print("Next")
    
    @dbus_method_async_override()
    async def previous(self):
        print("Prev")
    
    @dbus_method_async_override()
    async def pause(self):
        self._playing = False
        await self.playback_status.set_async("Playing" if self._playing else "Paused")
        pygame.event.post(pygame.event.Event(HIDE))
        print("Pause")
    
    @dbus_method_async_override()
    async def play_pause(self):
        self._playing = not self._playing
        await self.playback_status.set_async("Playing" if self._playing else "Paused")
        pygame.event.post([pygame.event.Event(HIDE), pygame.event.Event(SHOW)][int(self._playing)])
        print("PlayPause", self._playstate, self._playing)
    
    @dbus_method_async_override()
    async def play(self):
        self._playing = True
        await self.playback_status.set_async("Playing" if self._playing else "Paused")
        pygame.event.post(pygame.event.Event(SHOW))
        print("Play")
    
    @dbus_method_async_override()
    async def seek(self, offset: int):
        pass
    
    @dbus_method_async_override()
    async def set_position(self, track_id: str, position: int):
        pass
    
    @dbus_method_async_override()
    async def open_uri(self, uri: str):
        pass
    
    @dbus_property_async_override()
    def playback_status(self):
        return self._playstate
    
    @playback_status.setter
    def pbstatus_setter(self, new: str):
        self._playstate = new
    
    @dbus_property_async_override()
    def rate(self):
        return 1.0
    
    @dbus_property_async_override()
    def metadata(self):
        return {"mpris:trackid": ("o", "/org/present/track"), "xesam:title": ("s", "Presentation")}
    
    @dbus_property_async_override()
    def volume(self):
        return 1.0
    
    @volume.setter
    def vol_setter(self, new: float):
        pass
    
    @dbus_property_async_override()
    def position(self):
        return 0
    
    @dbus_property_async_override()
    def minimum_rate(self):
        return 1.0
    
    @dbus_property_async_override()
    def maximum_rate(self):
        return 1.0
    
    @dbus_property_async_override()
    def can_go_next(self):
        return True
    
    @dbus_property_async_override()
    def can_go_previous(self):
        return True
    
    @dbus_property_async_override()
    def can_play(self):
        return True
    
    @dbus_property_async_override()
    def can_pause(self):
        return True
    
    @dbus_property_async_override()
    def can_seek(self):
        return False
    
    @dbus_property_async_override()
    def can_control(self):
        return True
    

loop = get_event_loop()
import asyncio
def pygame_event_loop(loop, queue):
    while True:
        ev = pygame.event.wait()
        asyncio.run_coroutine_threadsafe(queue.put(ev), loop)


async def handle_events(queue):
    while True:
        ev = await queue.get()
        if ev.type == pygame.QUIT:
            break
        elif ev.type == SHOW:
            screen.fill((0, 0, 0))
            screen.blit(img, (0, 0))
            pygame.display.update()
            print("Show")
        elif ev.type == HIDE:
            screen.fill((0, 0, 0))
            pygame.display.update()
            print("Hide")
    asyncio.get_event_loop().stop()

queue = asyncio.Queue()
pygame.init()
img = pygame.image.load("twil.png")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.blit(img, (0, 0))
pygame.display.update()
pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, queue)
ev_task = asyncio.ensure_future(handle_events(queue))
iface_1 = BaseInterface()
async def start():
    await request_default_bus_name_async('org.mpris.MediaPlayer2.mprispresent')
    iface_1.export_to_dbus('/org/mpris/MediaPlayer2')

loop.run_until_complete(start())
loop.run_forever()
pygame.quit()