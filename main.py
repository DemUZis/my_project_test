from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.db_manager import create_all_tables
from app.api import auth, clients, masters, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    
    # Include API routers
    app.include_router(auth.router)
    app.include_router(clients.router)
    app.include_router(masters.router)
    app.include_router(admin.router)
    app.include_router(web.router)
    app.include_router(reviews.router)
    app.include_router(statistics.router)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    return app


# For development/testing purposes
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)