import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
PASSWORD_ADMIN = "tu_clave"

# --- FUNCIONES DE BASE DE DATOS ---
def guardar_libro_en_db(titulo, autor, sinopsis, ruta_portada, ruta_pdf):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    # Aseguramos estructura de tabla
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, autor TEXT, 
                       sinopsis TEXT, ruta_portada TEXT, ruta_pdf TEXT)''')
    cursor.execute('''INSERT INTO libros (titulo, autor, sinopsis, ruta_portada, ruta_pdf) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (titulo, autor, sinopsis, ruta_portada, ruta_pdf))
    conn.commit()
    conn.close()

def verificar_existencia(titulo):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM libros WHERE titulo = ?", (titulo,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

# --- INTERFAZ ---
st.title("Panel Administrativo")

if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

if not st.session_state.admin_logged:
    clave = st.text_input("Ingrese clave de acceso", type="password")
    if st.button("Acceder"):
        if clave == "Admin123":
            st.session_state.admin_logged = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
else:
    st.success("Acceso concedido")
    
    with st.form("form_carga", clear_on_submit=True):
        titulo = st.text_input("Título del libro")
        autor = st.text_input("Autor")
        sinopsis = st.text_area("Sinopsis")
        portada = st.file_uploader("Portada (Imagen)", type=['jpg', 'png', 'jpeg'])
        pdf = st.file_uploader("Archivo PDF", type=['pdf'])
        
        if st.form_submit_button("Subir libro"):
            if titulo and portada and pdf:
                if verificar_existencia(titulo):
                    st.error(f"El libro '{titulo}' ya existe en la biblioteca.")
                else:
                    # Crear carpetas y guardar
                    os.makedirs("media/portadas", exist_ok=True)
                    os.makedirs("media/libros", exist_ok=True)
                    
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    ruta_portada = f"media/portadas/{ts}_{portada.name}"
                    ruta_pdf = f"media/libros/{ts}_{pdf.name}"
                    
                    with open(ruta_portada, "wb") as f: f.write(portada.getbuffer())
                    with open(ruta_pdf, "wb") as f: f.write(pdf.getbuffer())
                    
                    guardar_libro_en_db(titulo, autor, sinopsis, ruta_portada, ruta_pdf)
                    st.success("¡Libro guardado correctamente!")
            else:
                st.error("Por favor completa todos los campos")