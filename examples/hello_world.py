from asgify.app import Asgify
from asgify.context import HTTPContext
from asgify.status import HTTP_200_OK
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan():
    print("🚀 Starting up the application...")
    # Initialize any resources, databases, etc.
    yield {"message": "Hello World 🎉"}
    print("🛑 Shutting down the application...")
    # Clean up resources, close connections, etc.


async def http_entrypoint(ctx: HTTPContext):
    """Entrypoint function for HTTP requests in your ASGI application.

    This function handles incoming HTTP requests and provides a simple
    response. It demonstrates basic usage of the HTTPContext for
    reading application state and sending HTTP responses.

    Args:
        ctx (HTTPContext): The HTTP context object containing request
            information and methods for handling the HTTP response.
            Provides access to request headers, body, and response
            methods like start(), write(), and end().
    """

    # Get the app state from the context
    message: str = ctx.state.get("message", "No message available")
    # Set response headers for plain text
    await ctx.start(HTTP_200_OK, {"content-type": "text/plain; charset=utf-8"})
    # Write the lifespan state message as plain text response
    await ctx.end(message.encode())


app = Asgify(lifespan=lifespan, http=http_entrypoint)
