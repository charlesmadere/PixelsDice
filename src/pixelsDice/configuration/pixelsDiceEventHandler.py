from typing import Final

from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..models.events.absPixelsDiceEvent import AbsPixelsDiceEvent
from ..models.events.pixelsDiceClientConnectedEvent import PixelsDiceClientConnectedEvent
from ..models.events.pixelsDiceClientDisconnectedEvent import PixelsDiceClientDisconnectedEvent
from ..models.events.pixelsDiceRollEvent import PixelsDiceRollEvent
from ...timber.timberInterface import TimberInterface


class PixelsDiceEventHandler(PixelsDiceEventListener):

    def __init__(
        self,
        timber: TimberInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: Final[TimberInterface] = timber

    async def onNewPixelsDiceEvent(self, event: AbsPixelsDiceEvent):
        if not isinstance(event, AbsPixelsDiceEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('PixelsDiceEventHandler', f'Received new Pixels Dice event ({event=})')

        if isinstance(event, PixelsDiceClientConnectedEvent):
            await self.__handleConnectedEvent(
                event = event,
            )

        elif isinstance(event, PixelsDiceClientDisconnectedEvent):
            await self.__handleDisconnectedEvent(
                event = event,
            )

        elif isinstance(event, PixelsDiceRollEvent):
            await self.__handleRollEvent(
                event = event,
            )

        else:
            self.__timber.log('PixelsDiceEventHandler', f'Received unhandled pixels dice event ({event=})')

    async def __handleConnectedEvent(self, event: PixelsDiceClientConnectedEvent):
        # this method is currently intentionally empty
        pass

    async def __handleDisconnectedEvent(self, event: PixelsDiceClientDisconnectedEvent):
        # this method is currently intentionally empty
        pass

    async def __handleRollEvent(self, event: PixelsDiceRollEvent):
        # this method is currently intentionally empty
        pass
