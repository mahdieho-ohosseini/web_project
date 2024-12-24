from fastapi import FastAPI
from router.user import user_router 
from db.engine import engine, Base



app = FastAPI()
@app.get('/')

@app.lifespan
async def lifespan(app: FastAPI):
    # رویداد startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router,prefix="/user")