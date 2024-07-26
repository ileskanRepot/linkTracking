from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request, nextURL: str = None, msg: str = None):
	if nextURL and msg:
		db.addLink(nextURL, msg)
		return RedirectResponse(nextURL, status_code=302)
	ret = ""
	with open("templates/index.html", "r") as ff:
		ret = ff.read()
	return HTMLResponse(ret)

@app.get("/api/linkGets")
async def linkGets(request: Request, count: int = 5, offset: int = 0):
	ret = db.getData(max(offset - count, 0), count)
	return ret

@app.get("/api/count")
async def linkGets(request: Request):
	ret = db.getDataLen()
	return ret