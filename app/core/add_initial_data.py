from app.permissions.service import Service


async def add_initial_data(service: Service) -> None:
    roles_objects = await service.create_roles()
    for role_object in roles_objects:
        if role_object.name == "user":
            right_1 = await service.create_right(write=True, read=False, only_owner=True, model="user")
            right_2 = await service.create_right(write=True, read=True, only_owner=True, model="advertisement")
            await service.create_role_right(role_object.id, right_1.id)
            await service.create_role_right(role_object.id, right_2.id)
        elif role_object.name == "admin":
            right_1 = await service.create_right(write=True, read=True, only_owner=False, model="user")
            right_2 = await service.create_right(write=True, read=True, only_owner=False, model="advertisement")
            await service.create_role_right(role_object.id, right_1.id)
            await service.create_role_right(role_object.id, right_2.id)
