from fastapi import Request

from app.permissions.dependencies import PermServiceDep


def parse_request(request: Request) -> dict[str, str]:
    method = request.method
    spl = request.url.path.split("/")[1:]
    model = spl[0][:-1]
    return {"method": method, "model": model}


async def check_rights(
    request: Request,
    perm_service: PermServiceDep,
    user_id: int,
    obj_id: int | None = None,
) -> None:
    parsed_request = parse_request(request)
    method = parsed_request["method"]
    model = parsed_request["model"]
    await perm_service.check_rights(user_id, method, model, obj_id)