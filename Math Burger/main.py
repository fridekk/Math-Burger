from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cmath
from typing import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")





def calculate_equation(x, coefficients, operations):
    result = coefficients[0] * x
    for i in range(1, len(coefficients)):
        if operations[i - 1] == '+':
            result += coefficients[i] * x
        elif operations[i - 1] == '-':
            result -= coefficients[i] * x
    return result

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "outputx": "", "outputqe": "", "outputineq": ""})

@app.post("/calculate")
async def calculate_x(request: Request, coefficients: List[int] = Form(...), operations: List[str] = Form(...), x: int = Form(...)):
    result = coefficients[0] * x
    for i in range(1, len(coefficients)):
        if operations[i - 1] == '+':
            result += coefficients[i] * x
        elif operations[i - 1] == '-':
            result -= coefficients[i] * x
    return templates.TemplateResponse("index.html", {"request": request, "outputx": result, "outputqe": "", "outputineq": ""})

@app.post("/quadratic")
def solve_quadratic(request: Request, a: float = Form(...), b: float = Form(...), c: float = Form(...)):
    D = b ** 2 - 4 * a * c
    vieta = ""
    if D > 0:
        x1 = (-b + cmath.sqrt(D)) / (2 * a)
        x2 = (-b - cmath.sqrt(D)) / (2 * a)
        solution = f'У уравнения два решения: {x1} и {x2}'
        vieta = f'Проверка через теорему Виета: Сумма корней: {-b / a}, Произведение корней: {c / a}'
    elif D == 0:
        x = -b / (2 * a)
        solution = f'У уравнения одно решение: {x}'
        vieta = f'Проверка через теорему Виета: Сумма корней: {-b / a}, Произведение корней: {c / a}'
    else:
        solution = 'У уравнения нет реальных решений'
    return templates.TemplateResponse("index.html", {"request": request, "output-x": "", "outputqe": solution, "outputvieta": vieta, "outputineq": ""})


@app.post("/inequality")
def solve_inequality(request: Request, a: float = Form(...), b: float = Form(...), c: float = Form(...), inequality: str = Form(...)):
    D = b ** 2 - 4 * a * c
    solution = ""
    if D >= 0:
        x1 = (-b - cmath.sqrt(D)) / (2 * a)
        x2 = (-b + cmath.sqrt(D)) / (2 * a)
        if a > 0:
            if inequality == '>':
                solution = f'x < {x1} или x > {x2}'
            else:
                solution = f'{x1} < x < {x2}'
        else:
            if inequality == '>':
                solution = f'{x1} < x < {x2}'
            else:
                solution = f'x < {x1} или x > {x2}'
    else:
        solution = 'Неравенство не имеет решений в действительных числах'
    return templates.TemplateResponse("index.html", {"request": request, "output-x": "", "output-qe": "", "outputineq": solution})

