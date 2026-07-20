import secrets
import sys
from pathlib import Path
from typing import Annotated

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from env import CSV_PREFIX, HISTORY_YEARS, WEBAPP_PASSWORD, WEBAPP_USERNAME
from file_io import (
    add_exclusion,
    add_participant,
    load_exclusions,
    load_participants,
    load_year,
    remove_exclusion,
    remove_participant,
)
from main import run_draw
from utils import get_last_n_years

app = FastAPI(title="Random Christmas Bot")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

security = HTTPBasic(auto_error=False)


def require_auth(credentials: Annotated[HTTPBasicCredentials | None, Depends(security)]):
    if not WEBAPP_USERNAME or not WEBAPP_PASSWORD:
        return  # auth disabled — no credentials configured
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    valid_user = secrets.compare_digest(credentials.username, WEBAPP_USERNAME)
    valid_pass = secrets.compare_digest(credentials.password, WEBAPP_PASSWORD)
    if not (valid_user and valid_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/")
def dashboard(request: Request, _: None = Depends(require_auth)):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "participants": load_participants(),
            "exclusions": sorted(load_exclusions()),
            "csv_prefix": CSV_PREFIX,
        },
    )


@app.post("/participants/add")
def participants_add(name: str = Form(...), email: str = Form(...), _: None = Depends(require_auth)):
    add_participant(name.strip(), email.strip())
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/participants/remove")
def participants_remove(name: str = Form(...), _: None = Depends(require_auth)):
    remove_participant(name)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/exclusions/add")
def exclusions_add(giver: str = Form(...), receiver: str = Form(...), _: None = Depends(require_auth)):
    add_exclusion(giver.strip(), receiver.strip())
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/exclusions/remove")
def exclusions_remove(giver: str = Form(...), receiver: str = Form(...), _: None = Depends(require_auth)):
    remove_exclusion(giver, receiver)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/history")
def history(request: Request, _: None = Depends(require_auth)):
    years = get_last_n_years(HISTORY_YEARS)
    year_data = [(year, load_year(year)) for year in years]
    return templates.TemplateResponse(
        request,
        "history.html",
        {"year_data": year_data},
    )


@app.post("/draw/run")
def draw_run(request: Request, _: None = Depends(require_auth)):
    try:
        new_draw = run_draw()
        error = None
    except Exception as exc:  # draw can legitimately fail (not enough participants, etc.)
        new_draw = []
        error = str(exc)
    return templates.TemplateResponse(
        request,
        "draw_result.html",
        {"new_draw": new_draw, "error": error},
    )
