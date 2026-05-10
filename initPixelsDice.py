import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.pixelsDice.configuration.pixelsDiceEventHandler import PixelsDiceEventHandler
from src.pixelsDice.listeners.pixelsDiceEventListener import PixelsDiceEventListener
from src.pixelsDice.machine.pixelsDiceMachine import PixelsDiceMachine
from src.pixelsDice.machine.pixelsDiceMachineInterface import PixelsDiceMachineInterface
from src.pixelsDice.mappers.pixelsDiceStateMapper import PixelsDiceStateMapper
from src.pixelsDice.mappers.pixelsDiceStateMapperInterface import PixelsDiceStateMapperInterface
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = BackgroundTaskHelper(
    eventLoop = eventLoop,
)

timber: Final[TimberInterface] = Timber()

cookieJarProvider: Final[AioHttpCookieJarProvider] = AioHttpCookieJarProvider(
    eventLoop = eventLoop,
)

networkClientProvider: Final[NetworkClientProvider] = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = cookieJarProvider,
    timber = timber,
)

pixelsDiceEventListener: Final[PixelsDiceEventListener] = PixelsDiceEventHandler(
    networkClientProvider = networkClientProvider,
    timber = timber,
    baseUrl = 'https://127.0.0.1:1337/pixelsDice',
)

pixelsDiceStateMapper: Final[PixelsDiceStateMapperInterface] = PixelsDiceStateMapper()

pixelsDiceMachine: Final[PixelsDiceMachineInterface] = PixelsDiceMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    pixelsDiceEventListener = pixelsDiceEventListener,
    pixelsDiceStateMapper = pixelsDiceStateMapper,
    timber = timber,
    pixelsDiceName = 'Dice Boi',
)

async def main():
    timber.log('initPixelsDice', 'Starting...')
    pixelsDiceMachine.start()

    while True:
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
