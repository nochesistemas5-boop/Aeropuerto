from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

vuelos = [
    {
        "codigo": "AV101",
        "origen": "Bogotá",
        "destino": "Cali",
        "estado": "A tiempo",
        "tipo": "llegada"
    },
    {
        "codigo": "LA202",
        "origen": "Cali",
        "destino": "Medellín",
        "estado": "Embarcando",
        "tipo": "salida"
    },
    {
        "codigo": "IB303",
        "origen": "Madrid",
        "destino": "Cali",
        "estado": "Retrasado",
        "tipo": "llegada"
    },
    {
        "codigo": "AA404",
        "origen": "Cali",
        "destino": "Miami",
        "estado": "A tiempo",
        "tipo": "salida"
    }
]


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "respuesta": ""
        }
    )


@app.post("/preguntar", response_class=HTMLResponse)
async def preguntar(
    request: Request,
    pregunta: str = Form(...)
):

    contexto = f"""
Eres un asistente virtual de un aeropuerto.

Información de vuelos:

{vuelos}

Responde únicamente con la información de estos vuelos.

Pregunta del usuario:
{pregunta}
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": contexto,
                "stream": False
            }
        )

        respuesta = response.json()["response"]

    except Exception as e:

        respuesta = f"Error conectando con Ollama: {e}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "respuesta": respuesta
        }
    )