import os
from collections import deque
import time

CANT_PROCESOS_POR_LOTE=5
SEGUNDOS_REALES_DE_ESPERA=1

class Proceso:
    def __init__(self, nombreProgramador, operacion, operando1, operando2, resultadoOperacion, tiempoMaximoEstimado, id):
        self.nombreProgramador=nombreProgramador
        self.operacion=operacion
        self.operando1=operando1
        self.operando2=operando2
        self.resultadoOperacion=resultadoOperacion
        self.tiempoMaximoEstimado=tiempoMaximoEstimado
        self.id=id

def limpiarConsola():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system("clear")

def obtenerOperando(numOperando):
    while True:
        try:
            operando=float(input("Ingresa el operando "+numOperando+": "))
        except ValueError:
            print("El operando no es valido. Debe de ser un numero real.")
        else:
            break
    return operando

def obtenerDividendo():
    while True:
        try:
            dividendo=float(input("Ingresa el dividendo: "))
        except ValueError:
            print("El divisor no es valido. Debe de ser un numero real.")
        else:
            break
    return dividendo

def obtenerDivisor():
    while True:
        try:
            divisor=float(input("Ingresa el divisor: "))
        except ValueError:
            print("El divisor no es valido. Debe de ser un numero real.")
        else:
            if(divisor==0):
                print("El divisor no puede ser 0.")
            else:
                break
    return divisor

def imprimirTabla4ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante):
    limpiarConsola()
    print("No. de lotes pendientes: "+str(cantidadLotesPendientes))
    print("Procesos pendientes de ejecutar | Proceso en ejecución | Procesos terminados ")
    print("Nombre | Tiempo máximo estimado | Nombre: ", end="")
    if(len(procesoActual.nombreProgramador)<=12):
        print(f"{procesoActual.nombreProgramador:12} |   ID   |   Operación  | Resultado")
    else:
        for i in range(0, 12):
            print(procesoActual.nombreProgramador[i], end="")
        print(" | ID | Operación | Resultado")
    if(len(procesosPendientes[0].nombreProgramador)<=6):
        print(f"{procesosPendientes[0].nombreProgramador:6} | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[0].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    if(len(procesoActual.id)<=16):
        print(f"{procesoActual.id:16} | ", end="")
    else:
        for i in range(0, 16):
            print(procesoActual.id[i], end="")
        print(" | ", end="")
    cantidadProcesosTerminados=len(procesosTerminados)
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    if(len(procesosPendientes[1].nombreProgramador)<=6):
        print(f"{procesosPendientes[1].nombreProgramador:6} | {str(procesosPendientes[1].tiempoMaximoEstimado):22} | Ope: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[1].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[1].tiempoMaximoEstimado):22} | Ope: ", end="")
    operacion=str(procesoActual.operando1)+" "+procesoActual.operacion+" "+str(procesoActual.operando2)
    print(f"{operacion:15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    if(len(procesosPendientes[2].nombreProgramador)<=6):
        print(f"{procesosPendientes[2].nombreProgramador:6} | {str(procesosPendientes[2].tiempoMaximoEstimado):22} | TME: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[2].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[2].tiempoMaximoEstimado):22} | TME: ", end="")
    print(f"{str(procesoActual.tiempoMaximoEstimado):15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    if(len(procesosPendientes[3].nombreProgramador)<=6):
        print(f"{procesosPendientes[3].nombreProgramador:6} | {str(procesosPendientes[3].tiempoMaximoEstimado):22} | TT: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[3].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[3].tiempoMaximoEstimado):22} | TT: ", end="")
    print(f"{str(tiempoTranscurrido):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TR: {str(tiempoRestante):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    while(cantidadProcesosTerminados!=0):
        for i in range(0, 54):
            print(" ", end="")
        print(f' | ', end="")
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1

def imprimirTabla3ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante):
    limpiarConsola()
    print("No. de lotes pendientes: "+str(cantidadLotesPendientes))
    print("Procesos pendientes de ejecutar | Proceso en ejecución | Procesos terminados ")
    print("Nombre | Tiempo máximo estimado | Nombre: ", end="")
    if(len(procesoActual.nombreProgramador)<=12):
        print(f"{procesoActual.nombreProgramador:12} |   ID   |   Operación  | Resultado")
    else:
        for i in range(0, 12):
            print(procesoActual.nombreProgramador[i], end="")
        print(" | ID | Operación | Resultado")
    if(len(procesosPendientes[0].nombreProgramador)<=6):
        print(f"{procesosPendientes[0].nombreProgramador:6} | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[0].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    if(len(procesoActual.id)<=16):
        print(f"{procesoActual.id:16} | ", end="")
    else:
        for i in range(0, 16):
            print(procesoActual.id[i], end="")
        print(" | ", end="")
    cantidadProcesosTerminados=len(procesosTerminados)
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    if(len(procesosPendientes[1].nombreProgramador)<=6):
        print(f"{procesosPendientes[1].nombreProgramador:6} | {str(procesosPendientes[1].tiempoMaximoEstimado):22} | Ope: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[1].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[1].tiempoMaximoEstimado):22} | Ope: ", end="")
    operacion=str(procesoActual.operando1)+" "+procesoActual.operacion+" "+str(procesoActual.operando2)
    print(f"{operacion:15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    if(len(procesosPendientes[2].nombreProgramador)<=6):
        print(f"{procesosPendientes[2].nombreProgramador:6} | {str(procesosPendientes[2].tiempoMaximoEstimado):22} | TME: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[2].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[2].tiempoMaximoEstimado):22} | TME: ", end="")
    print(f"{str(procesoActual.tiempoMaximoEstimado):15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TT: {str(tiempoTranscurrido):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TR: {str(tiempoRestante):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    while(cantidadProcesosTerminados!=0):
        for i in range(0, 54):
            print(" ", end="")
        print(f' | ', end="")
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1

def imprimirTabla2ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante):
    limpiarConsola()
    print("No. de lotes pendientes: "+str(cantidadLotesPendientes))
    print("Procesos pendientes de ejecutar | Proceso en ejecución | Procesos terminados ")
    print("Nombre | Tiempo máximo estimado | Nombre: ", end="")
    if(len(procesoActual.nombreProgramador)<=12):
        print(f"{procesoActual.nombreProgramador:12} |   ID   |   Operación  | Resultado")
    else:
        for i in range(0, 12):
            print(procesoActual.nombreProgramador[i], end="")
        print(" | ID | Operación | Resultado")
    if(len(procesosPendientes[0].nombreProgramador)<=6):
        print(f"{procesosPendientes[0].nombreProgramador:6} | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[0].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    if(len(procesoActual.id)<=16):
        print(f"{procesoActual.id:16} | ", end="")
    else:
        for i in range(0, 16):
            print(procesoActual.id[i], end="")
        print(" | ", end="")
    cantidadProcesosTerminados=len(procesosTerminados)
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    if(len(procesosPendientes[1].nombreProgramador)<=6):
        print(f"{procesosPendientes[1].nombreProgramador:6} | {str(procesosPendientes[1].tiempoMaximoEstimado):22} | Ope: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[1].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[1].tiempoMaximoEstimado):22} | Ope: ", end="")
    operacion=str(procesoActual.operando1)+" "+procesoActual.operacion+" "+str(procesoActual.operando2)
    print(f"{operacion:15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TME: {str(procesoActual.tiempoMaximoEstimado):15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TT: {str(tiempoTranscurrido):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TR: {str(tiempoRestante):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    while(cantidadProcesosTerminados!=0):
        for i in range(0, 54):
            print(" ", end="")
        print(f' | ', end="")
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1

def imprimirTabla1ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante):
    limpiarConsola()
    print("No. de lotes pendientes: "+str(cantidadLotesPendientes))
    print("Procesos pendientes de ejecutar | Proceso en ejecución | Procesos terminados ")
    print("Nombre | Tiempo máximo estimado | Nombre: ", end="")
    if(len(procesoActual.nombreProgramador)<=12):
        print(f"{procesoActual.nombreProgramador:12} |   ID   |   Operación  | Resultado")
    else:
        for i in range(0, 12):
            print(procesoActual.nombreProgramador[i], end="")
        print(" | ID | Operación | Resultado")
    if(len(procesosPendientes[0].nombreProgramador)<=6):
        print(f"{procesosPendientes[0].nombreProgramador:6} | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    else:
        for i in range(0, 6):
            print(procesosPendientes[0].nombreProgramador[i], end="")
        print(f" | {str(procesosPendientes[0].tiempoMaximoEstimado):22} | ID: ", end="")
    if(len(procesoActual.id)<=16):
        print(f"{procesoActual.id:16} | ", end="")
    else:
        for i in range(0, 16):
            print(procesoActual.id[i], end="")
        print(" | ", end="")
    cantidadProcesosTerminados=len(procesosTerminados)
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    operacion=str(procesoActual.operando1)+" "+procesoActual.operacion+" "+str(procesoActual.operando2)
    print(f"       |                        | Ope: {operacion:15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TME: {str(procesoActual.tiempoMaximoEstimado):15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TT: {str(tiempoTranscurrido):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TR: {str(tiempoRestante):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    while(cantidadProcesosTerminados!=0):
        for i in range(0, 54):
            print(" ", end="")
        print(f' | ', end="")
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1

def imprimirTabla0ProcesosPendientes(cantidadLotesPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante):
    limpiarConsola()
    print("No. de lotes pendientes: "+str(cantidadLotesPendientes))
    print("Procesos pendientes de ejecutar | Proceso en ejecución | Procesos terminados ")
    print("Nombre | Tiempo máximo estimado | Nombre: ", end="")
    if(len(procesoActual.nombreProgramador)<=12):
        print(f"{procesoActual.nombreProgramador:12} |   ID   |   Operación  | Resultado")
    else:
        for i in range(0, 12):
            print(procesoActual.nombreProgramador[i], end="")
        print(" | ID | Operación | Resultado")
    print("       |                        | ID: ", end="")
    if(len(procesoActual.id)<=16):
        print(f"{procesoActual.id:16} | ", end="")
    else:
        for i in range(0, 16):
            print(procesoActual.id[i], end="")
        print(" | ", end="")
    cantidadProcesosTerminados=len(procesosTerminados)
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    operacion=str(procesoActual.operando1)+" "+procesoActual.operacion+" "+str(procesoActual.operando2)
    print(f"       |                        | Ope: {operacion:15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TME: {str(procesoActual.tiempoMaximoEstimado):15} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TT: {str(tiempoTranscurrido):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    print(f"       |                        | TR: {str(tiempoRestante):16} | ", end="")
    if(cantidadProcesosTerminados!=0):
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1
    else:
        print("")
    while(cantidadProcesosTerminados!=0):
        for i in range(0, 54):
            print(" ", end="")
        print(f' | ', end="")
        print(f'{procesosTerminados[cantidadProcesosTerminados-1].id:6} | ', end="")
        operacion=str(procesosTerminados[cantidadProcesosTerminados-1].operando1)+" "+procesosTerminados[cantidadProcesosTerminados-1].operacion+" "+str(procesosTerminados[cantidadProcesosTerminados-1].operando2)
        print(f'{operacion:12} | {procesosTerminados[cantidadProcesosTerminados-1].resultadoOperacion}')
        cantidadProcesosTerminados-=1

limpiarConsola()
print("PROCESAMIENTO POR LOTES\n")
while True:
    try:
        cantidadProcesos=int(input("Ingresa la cantidad de procesos que quieres capturar: "))
    except ValueError:
        print("La cantidad de procesos no es valida.")
    else:
        if(cantidadProcesos>0):
            break
        print("La cantidad de procesos debe ser mayor a 0.")

idsIngresados=[]
cantidadProcesosIngresados=0

if((int(cantidadProcesos)%CANT_PROCESOS_POR_LOTE)!=0):
    cantidadLotes=int(int(cantidadProcesos)/CANT_PROCESOS_POR_LOTE)+1
else:
    cantidadLotes=int(int(cantidadProcesos)/CANT_PROCESOS_POR_LOTE)

lotes=deque()
for i in range(0, cantidadLotes):
    procesos=deque()
    for j in range(0, CANT_PROCESOS_POR_LOTE):
        if(cantidadProcesosIngresados<cantidadProcesos):
            limpiarConsola()
            print("PROCESAMIENTO POR LOTES - INGRESANDO PROCESO "+str(j+1)+"/"+str(CANT_PROCESOS_POR_LOTE)+" DEL LOTE "+str(i+1)+"/"+str(cantidadLotes)+"\n")
            while True:
                nombreProgramador=input("Ingresa el nombre del programador: ")
                if(len(nombreProgramador)<=0):
                    print("El nombre del programador debe contener al menos 1 caracter.")
                else:
                    break
            while True:
                operacion=input("Ingresa una operación (+, -, *, /, %): ")
                if (operacion not in ("+", "-", "*", "/", "%")):
                    print("Ingresa una operación de la lista.")
                else:
                    break
            match operacion:
                case "+":
                    operando1=obtenerOperando("1")
                    operando2=obtenerOperando("2")
                    resultadoOperacion=operando1+operando2
                case "-":
                    operando1=obtenerOperando("1")
                    operando2=obtenerOperando("2")
                    resultadoOperacion=operando1-operando2
                case "*":
                    operando1=obtenerOperando("1")
                    operando2=obtenerOperando("2")
                    resultadoOperacion=operando1*operando2
                case "/":
                    operando1=obtenerDividendo()
                    operando2=obtenerDivisor()
                    resultadoOperacion=operando1/operando2
                case "%":
                    operando1=obtenerDividendo()
                    operando2=obtenerDivisor()
                    resultadoOperacion=operando1%operando2
            while True:
                try:
                    tiempoMaximoEstimado=int(input("Ingresa el tiempo máximo estimado: "))
                except ValueError:
                    print("El tiempo máximo estimado debe de ser un número entero.")
                else:
                    if(tiempoMaximoEstimado<=0):
                        print("El tiempo máximo estimado debe ser mayor a 0.")
                    else:
                        break
            while True:
                id=input("Ingresa ID: ")
                if(len(id)<=0):
                    print("El ID debe contener al menos un caracter.")
                elif id in (idsIngresados):
                    print("El ID ingresado ya existe.")
                else:
                    idsIngresados.append(id)
                    break
            procesos.append(Proceso(nombreProgramador, operacion, operando1, operando2, resultadoOperacion, tiempoMaximoEstimado, id))
            cantidadProcesosIngresados+=1
        else:
            break
    lotes.append(procesos)

tiempoGeneral=0
cantidadLotesPendientes=cantidadLotes-1
procesosTerminados=deque()
while(cantidadLotesPendientes>=0):
    procesosPendientes=lotes.popleft()
    cantidadProcesosPendientes=len(procesosPendientes)-1
    while(cantidadProcesosPendientes!=-1):
        match cantidadProcesosPendientes:
            case 4:
                procesoActual=procesosPendientes.popleft()
                tiempoTranscurrido=0
                tiempoRestante=procesoActual.tiempoMaximoEstimado
                while(tiempoTranscurrido<=procesoActual.tiempoMaximoEstimado):
                    imprimirTabla4ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante)
                    print("Contador: "+str(tiempoGeneral))
                    tiempoGeneral+=1
                    tiempoTranscurrido+=1
                    tiempoRestante-=1
                    time.sleep(SEGUNDOS_REALES_DE_ESPERA)
                cantidadProcesosPendientes-=1
                procesosTerminados.append(procesoActual)
            case 3:
                procesoActual=procesosPendientes.popleft()
                tiempoTranscurrido=0
                tiempoRestante=procesoActual.tiempoMaximoEstimado
                while(tiempoTranscurrido<=procesoActual.tiempoMaximoEstimado):
                    imprimirTabla3ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante)
                    print("Contador: "+str(tiempoGeneral))
                    tiempoGeneral+=1
                    tiempoTranscurrido+=1
                    tiempoRestante-=1
                    time.sleep(SEGUNDOS_REALES_DE_ESPERA)
                cantidadProcesosPendientes-=1
                procesosTerminados.append(procesoActual)
            case 2:
                procesoActual=procesosPendientes.popleft()
                tiempoTranscurrido=0
                tiempoRestante=procesoActual.tiempoMaximoEstimado
                while(tiempoTranscurrido<=procesoActual.tiempoMaximoEstimado):
                    imprimirTabla2ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante)
                    print("Contador: "+str(tiempoGeneral))
                    tiempoGeneral+=1
                    tiempoTranscurrido+=1
                    tiempoRestante-=1
                    time.sleep(SEGUNDOS_REALES_DE_ESPERA)
                cantidadProcesosPendientes-=1
                procesosTerminados.append(procesoActual)
            case 1:
                procesoActual=procesosPendientes.popleft()
                tiempoTranscurrido=0
                tiempoRestante=procesoActual.tiempoMaximoEstimado
                while(tiempoTranscurrido<=procesoActual.tiempoMaximoEstimado):
                    imprimirTabla1ProcesosPendientes(cantidadLotesPendientes, procesosPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante)
                    print("Contador: "+str(tiempoGeneral))
                    tiempoGeneral+=1
                    tiempoTranscurrido+=1
                    tiempoRestante-=1
                    time.sleep(SEGUNDOS_REALES_DE_ESPERA)
                cantidadProcesosPendientes-=1
                procesosTerminados.append(procesoActual)
            case 0:
                procesoActual=procesosPendientes.popleft()
                tiempoTranscurrido=0
                tiempoRestante=procesoActual.tiempoMaximoEstimado
                while(tiempoTranscurrido<=procesoActual.tiempoMaximoEstimado):
                    imprimirTabla0ProcesosPendientes(cantidadLotesPendientes, procesoActual, procesosTerminados, tiempoTranscurrido, tiempoRestante)
                    print("Contador: "+str(tiempoGeneral))
                    tiempoGeneral+=1
                    tiempoTranscurrido+=1
                    tiempoRestante-=1
                    time.sleep(SEGUNDOS_REALES_DE_ESPERA)
                cantidadProcesosPendientes-=1
                procesosTerminados.append(procesoActual)
            case _:
                print("no hay xd")
    cantidadLotesPendientes-=1