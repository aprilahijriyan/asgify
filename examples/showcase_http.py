import json
from asgify.app import Asgify
from asgify.context import HTTPContext
from asgify.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_STATUS_CODES,
)


def flatten_headers(ctx: HTTPContext):
    hdrs = {}
    for k in set(ctx.headers.keys()):
        values = ctx.headers.getall(k)
        f_value = ",".join(values)
        hdrs[k] = f_value
    return hdrs


async def http_handler(ctx: HTTPContext):
    # Get path and method
    path = ctx.path
    method = ctx.method

    if path == "/" and method == "GET":
        await ctx.start(HTTP_200_OK, {"content-type": "application/json"})
        await ctx.end(
            json.dumps(
                {
                    "message": "Hello from asgify!",
                    "headers": flatten_headers(ctx),
                    "params": ctx.params,
                }
            ).encode()
        )

    elif path.startswith("/users/") and method == "GET":
        user_id = path.split("/users/")[-1]
        page = ctx.params.get("page", "1")

        await ctx.start(HTTP_200_OK, {"content-type": "application/json"})
        await ctx.end(
            json.dumps({"user_id": user_id, "page": page, "status": "active"}).encode()
        )

    elif path == "/api/data" and method == "POST":
        # Read JSON body
        body = b""
        async for chunk in ctx.read_body():
            body += chunk

        data = json.loads(body.decode())

        await ctx.start(HTTP_201_CREATED, {"content-type": "application/json"})
        await ctx.end(json.dumps({"created": True, "data": data}).encode())

    else:
        await ctx.start(HTTP_404_NOT_FOUND, {"content-type": "text/plain"})
        await ctx.end(HTTP_STATUS_CODES[HTTP_404_NOT_FOUND].encode())


app = Asgify(http=http_handler)
