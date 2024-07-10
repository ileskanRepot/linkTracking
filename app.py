from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request, nextLink: str = None, msg: str = None):
	if nextLink and msg:
		db.addLink(nextLink, msg)
		return RedirectResponse(nextLink, status_code=302)
	ret = ""
	with open("templates/index.html", "r") as ff:
		ret = ff.read()
	return HTMLResponse(ret)

@app.get("/api/linkGets")
async def linkGets(request: Request, count: int = 5, offset: int = 0):
	return db.getData(offset, count)