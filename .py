from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

    pregunta_lower = pregunta.lower()

    respuesta = "No encontré información."

    for vuelo in vuelos:

        codigo = vuelo["codigo"].lower()

        if codigo in pregunta_lower:

            respuesta = (
                f"Vuelo {vuelo['codigo']} | "
                f"Origen: {vuelo['origen']} | "
                f"Destino: {vuelo['destino']} | "
                f"Estado: {vuelo['estado']}"
            )

    if "salidas" in pregunta_lower:

        lista = []

        for v in vuelos:

            if v["tipo"] == "salida":

                lista.append(
                    f"{v['codigo']} → {v['destino']} ({v['estado']})"
                )

        respuesta = "<br>".join(lista)

    elif "llegadas" in pregunta_lower:

        lista = []

        for v in vuelos:

            if v["tipo"] == "llegada":

                lista.append(
                    f"{v['codigo']} ← {v['origen']} ({v['estado']})"
                )

        respuesta = "<br>".join(lista)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "respuesta": respuesta
        }
    )