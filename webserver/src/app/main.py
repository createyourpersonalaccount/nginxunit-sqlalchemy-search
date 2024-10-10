from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import psycopg

from litestar import Controller, Litestar, MediaType, Request, Response, get
from litestar.datastructures import CacheControlHeader, State
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_URL = "postgresql+psycopg://myuser:mypass@postgres:5432/mydb"

def generic_exception_handler(_: Request, exc: Exception) -> Response:
    """Default handler for exceptions subclassed from HTTPException."""
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = "Error."
    return Response(
        media_type=MediaType.TEXT,
        content=detail,
        status_code=status_code,
    )


def server_error_404(router: Request, exc: Exception) -> Response:
    """Handler for HTTP 404."""
    del router, exc
    detail = "Not found."
    return Response(
        media_type=MediaType.TEXT,
        content=detail,
        status_code=404
    )


async def search_documents(Session, s):
    stmt = select(literal(1))
    async with Session() as session:
          result = await session.scalar(stmt)
    return result


class MyController(Controller):
    @get("/")
    async def index(self) -> dict[str, str]:
        return dict(
            page="index",
            code="success"
        )

    @get("/search", cache_control=CacheControlHeader(no_store=True))
    async def search(self, state: State, s: str = "") -> dict[str, str]:
        result = "empty"
        if s:
            Session = async_sessionmaker(bind=state.engine)
            result = await search_documents(Session, s)
        return dict(
            page="search",
            code="success",
            result=result
        )


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(DB_URL)
        setattr(app.state, "engine", engine)
    try:
        yield
    finally:
        await engine.dispose()


app = Litestar(
    route_handlers=[MyController],
    openapi_config=None,
    exception_handlers={
        HTTP_404_NOT_FOUND: server_error_404,
        HTTPException: generic_exception_handler,
    },
    lifespan=[db_connection],
)
