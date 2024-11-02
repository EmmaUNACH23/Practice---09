import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

ardiPort = 'COM3'
baudrate =  9600
arduino = None 

def Conectar():
    global arduino
    try:
        arduino = serial.Serial(ardiPort, baudrate)
        time.sleep(2)
        lbConnection.config(text="Estado: Conectado", fg="green")
        messagebox.showinfo("Conexión", "Conexión establecida.")
        ReadTheThing()
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino. Verifique sus puertos")


def Desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConnection.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("Conexión", "Conexión terminada.")
    else:
        messagebox.showwarning("Abvertencia", "No hay conexión activa.")

def Enviar_Limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbTempLim.get()
            if limite.isdigit(): 
                arduino.write(f"{limite}\n".encode())
                arduino.flush()
                messagebox.showinfo("Enviado", f"Límite de temperatura ({limite} °C) se ha enviado")
            else:
                messagebox.showerror("Error", "Ingrese un valor numérico para el límite de temperatura: ")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el límite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conéctese al Arduino antes de enviar el limite de temperatura")

def readFromArduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()
            if "Temperatura" in data:
                print(data)
                tempValue = data.split(":")[1].strip()
                lbTemp.config(text=f"{tempValue} grados Celsius")
                time.sleep(1)
        except Exception as e:
            print(f"Ha ocurrido algo. No se pueden leer los datos: {e}")
            break

def ReadTheThing():
    thread = threading.Thread(target=readFromArduino)
    thread.daemon = True
    thread.start()


window = tk.Tk()
window.title("Interfaz de Monitoreo de Temperatura")
window.geometry("400x300")

lbTitleTemp = tk.Label(window, text="Temperatura Actual", font=("Arial", 12))
lbTitleTemp.pack(pady=10)

lbTemp = tk.Label(window, text="-- °C", font=("Arial", 24))
lbTemp.pack()

lbConnection = tk.Label(window, text="Estado: Desconectado", fg="red", font=("Arial", 12))
lbConnection.pack(pady=5)

lbTempLimit = tk.Label(window, text="Límite de temperatura: ")
lbTempLimit.pack(pady=5)
tbTempLim = tk.Entry(window, width=10)
tbTempLim.pack(pady=5)

btnSend = tk.Button(window, text="Enviar límite", command=Enviar_Limite, font=("Arial", 12))
btnSend.pack()

btnConnect = tk.Button(window, text="Conectar", command=Conectar, font=("Arial", 12))
btnConnect.pack(pady=5)

btnDisconnect = tk.Button(window, text="Desconectar", command=Desconectar, font=("Arial", 12))
btnDisconnect.pack(pady=5)

window.mainloop()
