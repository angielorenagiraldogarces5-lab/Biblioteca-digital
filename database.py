import sqlite3

def inicializar_bd():
    # Esto crea el archivo 'biblioteca.db' en tu carpeta actual
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # 1. Tabla de Sagas
    cursor.execute('''CREATE TABLE IF NOT EXISTS sagas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL UNIQUE
                      )''')

    # 2. Tabla de Libros
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        autor TEXT NOT NULL,
                        sinopsis TEXT,
                        orden_en_saga INTEGER,
                        ruta_portada TEXT,
                        ruta_pdf TEXT,
                        saga_id INTEGER,
                        FOREIGN KEY(saga_id) REFERENCES sagas(id)
                      )''')

    # 3. Tabla de Usuarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        es_admin BOOLEAN DEFAULT 0
                      )''')

    # Índices para búsqueda rápida
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_titulo ON libros(titulo)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_autor ON libros(autor)')

    conn.commit()
    conn.close()
    print("¡Base de datos 'biblioteca.db' creada exitosamente!")

if __name__ == "__main__":
    inicializar_bd()