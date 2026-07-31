import sys
from pathlib import Path
import tkinter as tk

# Aseguramos que Python encuentre el paquete 'src' desde la raíz
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

from src.gui.ventana import VentanaPrincipal

def main():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()