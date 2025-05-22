import tkinter as tk
import random as rdm
import time
import keyboard as kb
from tkinter import messagebox
from collections import deque
from enum import Enum
TIEMPO_BIENVENIDA_SEGUNDOS=3
TIEMPO_GENERAL_SEGUNDOS=1
CANT_TRABAJOS_POR_LOTE=5
TIEMPO_MIN_ESTIMADO=5 #cambiar tiempo
TIEMPO_MAX_ESTIMADO=20 #cambiar tiempo
REDONDEO_OPERANDOS=2
BG_FRAMES="gainsboro"
class Operacion(Enum):
    SUMA=1
    RESTA=2
    MULTIPLICACION=3
    DIVISION=4
    MODULO=5
class Trabajo():
    def __init__(self, id, tiempoMaximoEstimado, operacion, resultado, tiempoTranscurrido, estado):
        self.id=id
        self.tiempoMaximoEstimado=tiempoMaximoEstimado
        self.operacion=operacion
        self.resultado=resultado
        self.tiempoTranscurrido=tiempoTranscurrido
        self.estado=estado
def mostrarBienvenida():
    etiquetaBienvenida.pack(expand=True)
    ventanaPrincipal.after(TIEMPO_BIENVENIDA_SEGUNDOS*1000, ocultarBienvenida)
def ocultarBienvenida():
    etiquetaBienvenida.pack_forget()
    mostrarEntryCantTrabajos()
def mostrarEntryCantTrabajos():
    etiquetaCantTrabajos.pack(expand=True)
    entryCantTrabajos.pack(expand=True)
    botonIngresarCantTrabajos.pack(expand=True)
def ocultarEntryCantTrabajos():
    etiquetaCantTrabajos.pack_forget()
    entryCantTrabajos.pack_forget()
    botonIngresarCantTrabajos.pack_forget()
def mostrarVistaProcesamiento():
    ventanaPrincipal.grid_columnconfigure(0, weight=1)
    ventanaPrincipal.grid_columnconfigure(1, weight=1)
    ventanaPrincipal.grid_rowconfigure(0, weight=1)
    ventanaPrincipal.grid_rowconfigure(1, weight=1)
    frameLotesPendientes.grid(row=0, column=0, padx=10, pady=10)
    labelLotesPendientes.pack()
    frameTrabajosPendientes.grid(row=1, column=0, padx=10, pady=10)
    tituloFrameTrabajosPendientes.pack()
    frameTrabajoActual.grid(row=1, column=1, padx=10, pady=10)
    tituloFrameTrabajoActual.pack()
    frameTrabajosTerminados.grid(row=1, column=2, padx=10, pady=10)
    tituloFrameTrabajosTerminados.pack()
    frameContador.grid(row=2, column=0, padx=10, pady=10)
    labelContador.pack()
def obtenerCantTrabajosEntry():
    try:
        cantTrabajos=(int)(entryCantTrabajos.get())
    except ValueError:
        messagebox.showerror("Error de valor", "La cantidad de trabajos deber ser un entero mayor a 0")
    else:
        if(cantTrabajos<=0):
            messagebox.showerror("Error de valor", "La cantidad de trabajos deber ser un entero mayor a 0")
        else:
            ocultarEntryCantTrabajos()
            procesarLotes(cantTrabajos)
def generarLotes(cantLotes, cantTrabajos):
    cantIdsCapturados=1
    cantTrabajosCapturados=0
    lotes=deque()
    for i in range (0, cantLotes):
        trabajos=deque()
        for j in range(0, CANT_TRABAJOS_POR_LOTE):
            if(cantTrabajosCapturados==cantTrabajos):
                break
            idTrabajo=cantIdsCapturados
            tiempoMaximoEstimadoTrabajo=rdm.randint(TIEMPO_MIN_ESTIMADO, TIEMPO_MAX_ESTIMADO)
            selOperacion=rdm.randint(Operacion.SUMA.value, Operacion.MODULO.value)
            operando1=round(rdm.uniform(-100, 100), REDONDEO_OPERANDOS)
            operando2=round(rdm.uniform(-100, 100), REDONDEO_OPERANDOS)
            match selOperacion:
                case Operacion.SUMA.value:
                    resultadoTrabajo=operando1+operando2
                    operacionTrabajo=str(operando1)+" + "+str(operando2)
                case Operacion.RESTA.value:
                    resultadoTrabajo=operando1-operando2
                    operacionTrabajo=str(operando1)+" - "+str(operando2)
                case Operacion.MULTIPLICACION.value:
                    resultadoTrabajo=operando1*operando2
                    operacionTrabajo=str(operando1)+" * "+str(operando2)
                case Operacion.DIVISION.value:
                    operando2=round(rdm.uniform(1, 100), REDONDEO_OPERANDOS)
                    resultadoTrabajo=operando1/operando2
                    operacionTrabajo=str(operando1)+" / "+str(operando2)
                case Operacion.MODULO.value:
                    operando2=round(rdm.uniform(1, 100), REDONDEO_OPERANDOS)
                    resultadoTrabajo=operando1%operando2
                    operacionTrabajo=str(operando1)+" % "+str(operando2)
            trabajos.append(Trabajo(idTrabajo, tiempoMaximoEstimadoTrabajo, operacionTrabajo, resultadoTrabajo, 0, "C"))
            cantIdsCapturados+=1
            cantTrabajosCapturados+=1
        lotes.append(trabajos)
    return lotes    
def gestionarTeclas(event):
    match event.name.upper():
        case 'E':
            if(trabajoActual.estado!='P'):
                trabajoActual.resultado="ERROR"
        case 'P':
            trabajoActual.estado='P'
        case 'I':
            if(trabajoActual.estado!='P'):
                trabajoActual.estado='I'
def procesarLotes(cantTrabajos):
    global trabajoActual
    labelsTrabajosPendientes=deque()
    labelTrabajoActual=tk.Label(frameTrabajoActual)
    labelsTrabajosTerminados=deque()
    trabajosTerminados=deque()
    cantLotes=0
    tiempoGeneral=0
    tiempoTranscurrido=0
    if((cantTrabajos%CANT_TRABAJOS_POR_LOTE)==0):
        cantLotes=(int)(cantTrabajos/CANT_TRABAJOS_POR_LOTE)
    else:
        cantLotes=(int)(cantTrabajos/CANT_TRABAJOS_POR_LOTE)+1
    mostrarVistaProcesamiento()
    lotes=generarLotes(cantLotes, cantTrabajos)
    kb.on_press(gestionarTeclas)
    while(len(lotes)!=0):
        labelLotesPendientes.config(text="Lotes pendientes: "+str(len(lotes)-1))
        loteActual=lotes.popleft()
        for i in range(len(loteActual)):
            labelTrabajoPendiente=tk.Label(frameTrabajosPendientes)
            labelTrabajoPendiente.config(text=f"ID: {loteActual[i].id} | TME: {loteActual[i].tiempoMaximoEstimado} | TT: {loteActual[i].tiempoTranscurrido}")
            labelTrabajoPendiente.pack()
            labelsTrabajosPendientes.append(labelTrabajoPendiente)
        while(len(loteActual)!=0):
            labelsTrabajosPendientes.popleft().pack_forget()
            trabajoActual=loteActual.popleft()
            tiempoTranscurrido=trabajoActual.tiempoTranscurrido
            tiempoRestante=trabajoActual.tiempoMaximoEstimado-trabajoActual.tiempoTranscurrido
            labelTrabajoActual.config(text=f"ID: {trabajoActual.id}\nOpe: {trabajoActual.operacion}\nTME: {trabajoActual.tiempoMaximoEstimado}\nTT: {tiempoTranscurrido}\nTR: {tiempoRestante}")
            labelTrabajoActual.pack()
            while(tiempoTranscurrido<=trabajoActual.tiempoMaximoEstimado):
                if(trabajoActual.resultado=="ERROR"):
                    trabajoActual.tiempoTranscurrido=trabajoActual.tiempoMaximoEstimado
                    break
                elif(trabajoActual.estado=='P'):
                    kb.wait('C')
                    trabajoActual.estado='C'
                elif(trabajoActual.estado=='I'):
                    trabajoActual.estado='C'
                    trabajoActual.tiempoTranscurrido=tiempoTranscurrido-1
                    loteActual.append(trabajoActual)
                    labelTrabajoPendiente=tk.Label(frameTrabajosPendientes)
                    labelTrabajoPendiente.config(text=f"ID: {loteActual[len(loteActual)-1].id} | TME: {loteActual[len(loteActual)-1].tiempoMaximoEstimado} | TT: {loteActual[len(loteActual)-1].tiempoTranscurrido}")
                    labelTrabajoPendiente.pack()
                    labelsTrabajosPendientes.append(labelTrabajoPendiente)
                    break
                labelTrabajoActual.config(text=f"ID: {trabajoActual.id}\nOpe: {trabajoActual.operacion}\nTME: {trabajoActual.tiempoMaximoEstimado}\nTT: {tiempoTranscurrido}\nTR: {tiempoRestante}")
                labelContador.config(text="Contador: "+str(tiempoGeneral))
                ventanaPrincipal.update()
                time.sleep(TIEMPO_GENERAL_SEGUNDOS)
                tiempoTranscurrido+=1
                tiempoRestante-=1
                tiempoGeneral+=1
                trabajoActual.tiempoTranscurrido=tiempoTranscurrido-1
            if((trabajoActual.tiempoTranscurrido==trabajoActual.tiempoMaximoEstimado)):
                trabajosTerminados.append(trabajoActual)
                labelTrabajoTerminado=tk.Label(frameTrabajosTerminados)
                labelTrabajoTerminado.config(text=f"ID: {trabajoActual.id} | Ope: {trabajoActual.operacion} | Res: {trabajoActual.resultado}")
                labelTrabajoTerminado.pack()
                labelsTrabajosTerminados.append(labelTrabajoTerminado)
        labelDivision=tk.Label(frameTrabajosTerminados)
        labelDivision.config(text="-----------------------------------------")
        labelDivision.pack()
        labelsTrabajosTerminados.append(labelDivision)
    labelTrabajoActual.pack_forget()
# Declaración de widgets
ventanaPrincipal=tk.Tk()
etiquetaBienvenida=tk.Label(ventanaPrincipal, text="Bienvenid@")
etiquetaCantTrabajos=tk.Label(ventanaPrincipal, text="Ingresa la cantidad de trabajos que se procesaran: ")
entryCantTrabajos=tk.Entry(ventanaPrincipal)
botonIngresarCantTrabajos=tk.Button(ventanaPrincipal, text="Ingresar", command=obtenerCantTrabajosEntry)
frameLotesPendientes=tk.Frame(ventanaPrincipal, bg=BG_FRAMES, padx=10, pady=10)
labelLotesPendientes=tk.Label(frameLotesPendientes, text="Lotes pendientes: ")
frameTrabajosPendientes=tk.Frame(ventanaPrincipal, bg=BG_FRAMES, padx=10, pady=10)
tituloFrameTrabajosPendientes=tk.Label(frameTrabajosPendientes, text="Trabajos pendientes")
frameTrabajoActual=tk.Frame(ventanaPrincipal, bg=BG_FRAMES, padx=10, pady=10)
tituloFrameTrabajoActual=tk.Label(frameTrabajoActual, text="Trabajo actual")
frameTrabajosTerminados=tk.Frame(ventanaPrincipal, bg=BG_FRAMES, padx=10, pady=10)
tituloFrameTrabajosTerminados=tk.Label(frameTrabajosTerminados, text="Trabajos terminados")
frameContador=tk.Frame(ventanaPrincipal, bg=BG_FRAMES, padx=10, pady=10)
labelContador=tk.Label(frameContador, text="Contador: ")
# Configuración de widgets
ventanaPrincipal.title("Procesamiento por Lotes - Multiprogramación")
ventanaPrincipal.minsize(width=500, height=500)
etiquetaBienvenida.config(font=(20))
etiquetaCantTrabajos.config(font=(15))
entryCantTrabajos.config(font=(15))
botonIngresarCantTrabajos.config(font=(15))
# Ejecución del programa
mostrarBienvenida()
ventanaPrincipal.mainloop()

