"""
Proyecto 26: Agregar marca de tiempo a cada línea
"""

from datetime import datetime

def agregar_timestamp_a_archivo(archivo_entrada, archivo_salida=None):
    """Agrega timestamp a cada línea de un archivo"""
    if archivo_salida is None:
        archivo_salida = f"timestamped_{archivo_entrada}"
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
            lineas = entrada.readlines()
        
        lineas_con_timestamp = []
        timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for i, linea in enumerate(lineas):
            # Crear timestamp único para cada línea (agregando segundos)
            timestamp_linea = datetime.now().replace(second=i % 60).strftime("%Y-%m-%d %H:%M:%S")
            linea_con_timestamp = f"[{timestamp_linea}] {linea.rstrip()}\n"
            lineas_con_timestamp.append(linea_con_timestamp)
        
        with open(archivo_salida, 'w', encoding='utf-8') as salida:
            salida.writelines(lineas_con_timestamp)
        
        return len(lineas), archivo_salida
        
    except FileNotFoundError:
        return None, None

def crear_archivo_ejemplo():
    """Crea un archivo de ejemplo"""
    contenido = """Primera línea del archivo
Segunda línea con más contenido
Tercera línea para pruebas
Cuarta línea final"""
    
    with open('archivo_ejemplo.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'archivo_ejemplo.txt' creado")

def main():
    print("=== AGREGAR TIMESTAMP A LÍNEAS ===")
    
    archivo_entrada = input("Archivo de entrada (o 'ejemplo' para crear uno): ")
    
    if archivo_entrada.lower() == 'ejemplo':
        crear_archivo_ejemplo()
        archivo_entrada = 'archivo_ejemplo.txt'
    
    archivo_salida = input("Archivo de salida (Enter para auto-generar): ").strip()
    if not archivo_salida:
        archivo_salida = None
    
    num_lineas, archivo_generado = agregar_timestamp_a_archivo(archivo_entrada, archivo_salida)
    
    if num_lineas is not None:
        print(f"\nProceso completado:")
        print(f"Líneas procesadas: {num_lineas}")
        print(f"Archivo generado: {archivo_generado}")
        
        # Mostrar resultado
        with open(archivo_generado, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        print(f"\nContenido del archivo con timestamps:")
        print(contenido)
    else:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")

if __name__ == "__main__":
    main()
