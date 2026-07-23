import asyncio

import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request

from config import HOST, PORT

from server.broadcaster import broadcaster
from server.channel_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="web"), name="static")


@app.get("/")
async def index():
    return FileResponse("web/index.html")


async def event_stream(channel: str, queue: asyncio.Queue):

    try:

        while True:

            msg = await queue.get()

            yield f"data:{msg}\n\n"

    except asyncio.CancelledError:
        pass

    finally:

        broadcaster.disconnect(channel, queue)

        await manager.disconnect(channel)


@app.get("/events")
async def events(request: Request):

    channel = request.query_params.get("username")

    if not channel:
        return {"error": "username required"}

    channel = channel.lower()

    queue = broadcaster.connect(channel)

    manager.connect(channel)

    return StreamingResponse(
        event_stream(channel, queue),
        media_type="text/event-stream"
    )


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True
    )