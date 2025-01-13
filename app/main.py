from fastapi import FastAPI
import uvicorn
from app.routers import products, category, auth, permission, reviews


app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(auth.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(permission.router)
app.include_router(reviews.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
