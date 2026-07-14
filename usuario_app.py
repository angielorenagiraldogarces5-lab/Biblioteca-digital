import streamlit as st
import sqlite3
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mi Biblioteca Digital", layout="centered")
st.title("📚 Mi Biblioteca Digital")
st.write("Explora y descarga nuestros libros disponibles.")

# --- FUNCIÓN DE LECTURA ---
def obtener_libros():
    if not os.path.exists('biblioteca.db'):
        return []
    
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    try:
        # Seleccionamos los libros
        cursor.execute("SELECT * FROM libros")
        libros = cursor.fetchall()
    except sqlite3.OperationalError:
        libros = []
    finally:
        conn.close()
    return libros

# --- LÓGICA DE VISUALIZACIÓN ---
libros = obtener_libros()

if not libros:
    st.info("Aún no hay libros disponibles. ¡Vuelve pronto!")
else:
    for libro in libros:
        # Según la estructura de tu BD:
        # 0:id, 1:titulo, 2:autor, 3:sinopsis, 4:orden_en_saga, 5:ruta_portada, 6:ruta_pdf, 7:saga_id
        titulo = libro[1]
        autor = libro[2]
        sinopsis = libro[3]
        ruta_portada = libro[5]
        ruta_pdf = libro[6]
        
        # Validación de seguridad
        es_valida = (ruta_portada is not None) and (ruta_pdf is not None)
        
        if es_valida:
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if os.path.exists(ruta_portada):
                        st.image(ruta_portada, use_container_width=True)
                    else:
                        st.warning("Imagen no encontrada")
                
                with col2:
                    st.subheader(titulo)
                    st.write(f"**Autor:** {autor}")
                    st.write(sinopsis)
                    
                    if os.path.exists(ruta_pdf):
                        with open(ruta_pdf, "rb") as f:
                            st.download_button(
                                label="📥 Descargar PDF",
                                data=f,
                                file_name=os.path.basename(ruta_pdf),
                                mime="application/pdf"
                            )
                    else:
                        st.error("Archivo PDF no encontrado")
                
                st.divider()