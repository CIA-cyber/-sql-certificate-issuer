import sqlite3
from fpdf import FPDF
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "registros.db")
CARPETA_SALIDA = os.path.join(BASE_DIR, "certificados")

def preparar_entorno():
   
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
    return CARPETA_SALIDA

def buscar_en_db(nombre_buscado):
    
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        #
        query = "SELECT * FROM confirmaciones WHERE Nombre_completo LIKE ?"
        cursor.execute(query, ('%' + nombre_buscado + '%',))
        
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            # Mapeo según tabla: [2]Nombre, [6]Padrino, [9]Fecha, [10]Cura
            return {
                "nombre": str(fila[2]).strip(),
                "padrino": str(fila[6]).strip() if fila[6] else "No registrado",
                "fecha": str(fila[9]).strip(),
                "cura": str(fila[10]).strip()
            }
        return None
    except Exception as e:
        print(f"❌ Error al consultar la DB: {e}")
        return None

def crear_pdf(datos, ruta_carpeta):
    """Genera el certificado físico en PDF."""
    try:
       
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        
        
        pdf.set_line_width(1)
        pdf.rect(10, 10, 277, 190)

        # Título
        pdf.set_font("helvetica", "B", 35)
        pdf.set_y(40)
        pdf.cell(0, 20, "CONSTANCIA DE CONFIRMACIÓN", align="C", ln=True)

        # Datos de la persona
        pdf.ln(20)
        pdf.set_font("helvetica", "", 24)
        pdf.cell(0, 15, f"Se certifica que: {datos['nombre']}", align="C", ln=True)
        
        pdf.set_font("helvetica", "", 18)
        pdf.cell(0, 12, f"Recibió el Sacramento el día: {datos['fecha']}", align="C", ln=True)
        pdf.cell(0, 12, f"Oficiante: {datos['cura']}", align="C", ln=True)
        pdf.cell(0, 12, f"Padrino/Madrina: {datos['padrino']}", align="C", ln=True)

        # Guardar archivo
        nombre_archivo = f"Certificado_{datos['nombre'].replace(' ', '_')}.pdf"
        ruta_final = os.path.join(ruta_carpeta, nombre_archivo)
        pdf.output(ruta_final)
        
        print(f"🎯 ¡Certificado creado con éxito en: {ruta_final}")
        return ruta_final
    except Exception as e:
        print(f"❌ Error al crear el PDF: {e}")
        return None

# --- PRUEBA FINAL ---
if __name__ == "__main__":
    print("🚀 Iniciando prueba del Generador SQL...")
    carpeta = preparar_entorno()
    
    
    persona = buscar_en_db("Dionisio")
    
    if persona:
        crear_pdf(persona, carpeta)
    else:
        print("⚠️ No se encontró a la persona en la base de datos.")