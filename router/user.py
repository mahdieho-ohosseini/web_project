from fastapi import APIRouter

user_router = APIRouter()


@user_router.post("/log")
async def register():
    ...

@user_router.post("/login")
async def login():
    ...


@user_router.get("/login")
async def get_user_profile():
    ...

@user_router.put("/login")
async def user_update_profile():
    ...