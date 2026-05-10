import traceback
from typing import Final

from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..models.events.absPixelsDiceEvent import AbsPixelsDiceEvent
from ..models.events.pixelsDiceClientConnectedEvent import PixelsDiceClientConnectedEvent
from ..models.events.pixelsDiceClientDisconnectedEvent import PixelsDiceClientDisconnectedEvent
from ..models.events.pixelsDiceRollEvent import PixelsDiceRollEvent
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class PixelsDiceEventHandler(PixelsDiceEventListener):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        baseUrl: str = 'https://127.0.0.1:1337/pixelsDice',
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(baseUrl, str):
            raise TypeError(f'baseUrl argument is malformed: \"{baseUrl}\"')

        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber
        self.__baseUrl: Final[str] = baseUrl

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
        networkClient = await self.__networkClientProvider.get()

        try:
            response = await networkClient.post(
                url = f'{self.__baseUrl}/roll',
                json = {
                    'diceAddress': event.connectedDice.diceAddress,
                    'diceName': event.connectedDice.diceName,
                    'roll': event.roll,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('PixelsDiceEventHandler', f'Encountered unknown network exception ({event=})', e, traceback.format_exc())
            return
        except Exception as e:
            self.__timber.log('PixelsDiceEventHandler', f'Encountered unknown exception ({event=})', e, traceback.format_exc())
            return

        await response.close()
