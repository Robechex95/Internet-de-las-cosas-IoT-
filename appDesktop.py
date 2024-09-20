import tkinter as tk
import requests
from tkinter import messagebox
from datetime import datetime
import socket

# URL de tu recurso en MockAPI
url = "https://66ed9630380821644cdd64b6.mockapi.io/IoTCarStatus"

def obtener_ip_cliente():
    """Obtiene la IP local del cliente."""
    try:
        hostname = socket.gethostname()
        ip_cliente = socket.gethostbyname(hostname)
        return ip_cliente
    except:
        return "0.0.0.0"

def enviar_registro():
    status = entry_status.get()
    name = entry_name.get()

    if status and name:
        datos = {
            "status": status,
            "date": datetime.now().isoformat(),  # Fecha actual en formato ISO
            "ipClient": obtener_ip_cliente(),  # IP del cliente
            "name": name
        }

        # Enviar los datos a MockAPI
        try:
            respuesta = requests.post(url, json=datos)
            if respuesta.status_code == 201:
                messagebox.showinfo("Éxito", "Registro enviado correctamente")
            else:
                messagebox.showerror("Error", f"Error al enviar el registro: {respuesta.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar con MockAPI: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa todos los datos")

def obtener_registros():
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            registros = respuesta.json()
            ultimos_registros = registros[-10:]

            # Mostrar registros en un cuadro de texto
            text_registros.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            for registro in ultimos_registros:
                text_registros.insert(tk.END,
                                      f"ID: {registro['id']} - Status: {registro['status']}, Fecha: {registro['date']}, IP: {registro['ipClient']}, Nombre: {registro['name']}\n")
        else:
            messagebox.showerror("Error", f"Error al obtener los registros: {respuesta.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar con MockAPI: {e}")

# Configuración de la ventana
app = tk.Tk()
app.title("Inyección de Registros IoTCarStatus")

# Etiquetas y campos de entrada
label_status = tk.Label(app, text="Estado del coche:")
label_status.pack()
entry_status = tk.Entry(app)
entry_status.pack()

label_name = tk.Label(app, text="Nombre del propietario:")
label_name.pack()
entry_name = tk.Entry(app)
entry_name.pack()

# Botones para enviar y mostrar registros
boton_enviar = tk.Button(app, text="Enviar Registro", command=enviar_registro)
boton_enviar.pack()

boton_mostrar = tk.Button(app, text="Mostrar Últimos 10 Registros", command=obtener_registros)
boton_mostrar.pack()

# Cuadro de texto para mostrar los registros
text_registros = tk.Text(app, height=10, width=80)
text_registros.pack()

# Ejecutar la aplicación
app.mainloop()
