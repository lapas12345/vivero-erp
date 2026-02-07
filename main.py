from database import init_database
from ui.main_window import MainWindow

def main():
    # Inicializar base de datos
    print("Inicializando base de datos...")
    init_database()
    print("✅ Base de datos lista")
    
    # Iniciar aplicación
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()