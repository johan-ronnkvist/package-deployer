import uvicorn
import fastapi
from fastapi.responses import RedirectResponse

from pkgdeployer.api.packages import router as packages_router

app = fastapi.FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health():
    return {'result': 'ok'}


app.include_router(packages_router)

if __name__ == '__main__':
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
