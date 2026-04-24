import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_ORIGEN = os.path.join(BASE_DIR, "registros.xlsx") 
DB_NAME = os.path.join(BASE_DIR, "registros.db")

def migrar():
    try:
        print(f"📂 Buscando datos en: {ARCHIVO_ORIGEN}")
        
       
        if not os.path.exists(ARCHIVO_ORIGEN):
            print(f"❌ No encontré 'registros.xlsx'. Archivos reales: {os.listdir(BASE_DIR)}")
            return

        
        try:
            print("📖 Intentando leer como CSV...")
            df = pd.read_csv(ARCHIVO_ORIGEN, low_memory=False)
        except:
            print("📖 No era un CSV, intentando leer como Excel real...")
            df = pd.read_excel(ARCHIVO_ORIGEN)

        
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        
        # Conexión a la base de datos
        conexion = sqlite3.connect(DB_NAME)
        df.to_sql("confirmaciones", conexion, if_exists="replace", index=False)
        conexion.close()
        
        print("-" * 30)
        print(f"✅ ¡ÉXITO TOTAL!")
        print(f"Se creó el archivo: {DB_NAME}")
        print(f"Registros procesados: {len(df)}")
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    migrar()