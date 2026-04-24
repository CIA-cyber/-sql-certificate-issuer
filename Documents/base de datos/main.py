from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import generador
import os

app = FastAPI(title="API de Certificados SQL")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #
    allow_methods=["*"],
    allow_headers=["*"],
)

class Peticion(BaseModel):
    nombre_buscar: str

@app.post("/crear-certificado")
def api_crear_certificado(peticion: Peticion):
    print(f"📡 Petición recibida: {peticion.nombre_buscar}")
    
    datos_persona = generador.buscar_en_db(peticion.nombre_buscar)
    
    if not datos_persona:
        raise HTTPException(status_code=404, detail="No se encontró en los registros.")
    
    carpeta = generador.preparar_entorno()
    ruta_pdf = generador.crear_pdf(datos_persona, carpeta)
    
    if ruta_pdf and os.path.exists(ruta_pdf):
        return FileResponse(
            ruta_pdf, 
            media_type='application/pdf', 
            filename=f"Certificado_{datos_persona['nombre'].replace(' ', '_')}.pdf"
        )
    else:
        raise HTTPException(status_code=500, detail="Error al generar archivo.")