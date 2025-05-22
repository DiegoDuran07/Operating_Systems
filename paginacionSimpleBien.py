import tkinter as tk
import random as rdm
import time
import threading
from tkinter import ttk, messagebox
from collections import deque
from enum import Enum

# Constants
PROCESSING_WINDOW_LABELS_FONT_TYPE='Arial'
PROCESSING_WINDOW_LABELS_FONT_SIZE=12
MIN_SERVICE_TIME=5
MAX_SERVICE_TIME=20
MIN_OPERAND_VALUE=-100
MAX_OPERAND_VALUE=100
OPERAND_ROUND=2
TIME_STEP_SECONDS=1
THOUSAND=1000
MAX_PROCESSES_MEMORY=5
MAX_BLOCKED_TIME=7
WINDOW_HEIGHT=750
WINDOW_WIDTH=1000  # Increased width for better layout
FRAME_LENGTH=5
FRAME_AMOUNT=48
OPERATIVE_SISTEM_MEM_SIZE=4

# Operators Enum Class
class Operators(Enum):
    ADDITION=1
    SUBSTRACTION=2
    MULTIPLICATION=3
    DIVISION=4
    MODULE=5

# Colors Enum Class
class Colors(Enum):
    OPERATIVE_SISTEM='gray1'
    READY='cyan'
    EMPTY='snow'
    BLOCKED='purple1'
    EXECUTING='red'

# Frame class
class Frame():
    # Constructor
    def __init__(self, root, column, row, num):
        self.num=num
        self.occupiedCells=0
        self.generalFrame=tk.Frame(root, borderwidth=1, relief='solid')
        self.cells=[]
        for i in range(FRAME_LENGTH):
            subFrame=tk.Frame(self.generalFrame)
            subFrame.grid(column=i, row=0)
            subFrameLabel=tk.Label(subFrame, text='', width=2, bg=Colors.EMPTY.value)
            subFrameLabel.grid()
            self.cells.append((subFrame, subFrameLabel))
        self.generalFrame.grid(column=column, row=row)
    
    # Set occupiedCells
    def setOcuppiedCells(self, occupiedCells):
        self.occupiedCells=occupiedCells

    # Set color
    def setColor(self, color):
        for i in range(self.occupiedCells):
            self.cells[i][1].config(bg=color)

    # Check if the frame is empty
    def isEmpty(self):
        return self.occupiedCells==0

    # Check if the frame is full
    def isFull(self):
        return self.occupiedCells==5

# Memory class
class Memory():
    # Constructor
    def __init__(self, root):
        self.frames=[]

        # Widgets

        # Main frame
        mainFrame=ttk.Frame(root)
        mainFrame.grid(padx=10, pady=10)

        # Header configuration
        noFrameFrame1=tk.Frame(mainFrame, borderwidth=1, relief='solid')
        noFrameFrame1.grid(column=0, row=0)
        noFrameLabel1=tk.Label(noFrameFrame1, text='No.',width=5)
        noFrameLabel1.pack()

        emptyFrame1=tk.Frame(mainFrame, borderwidth=1, relief='solid')
        emptyFrame1.grid(column=1, row=0)
        emptyFrameLabel1=tk.Label(emptyFrame1, text='', width=15)
        emptyFrameLabel1.pack()

        noFrameFrame2=tk.Frame(mainFrame, borderwidth=1, relief='solid')
        noFrameFrame2.grid(column=2, row=0)
        noFrameLabel2=tk.Label(noFrameFrame2, text='No.', width=5)
        noFrameLabel2.pack()

        emptyFrame2=tk.Frame(mainFrame, borderwidth=1, relief='solid')
        emptyFrame2.grid(column=3, row=0)
        emptyFrameLabel2=tk.Label(emptyFrame2, text='', width=15)
        emptyFrameLabel2.pack()

        # Numeration configuration
        number=0
        for i in range(0, 4, 2):
            for j in range(int(48/2)):
                numFrame=tk.Frame(mainFrame, borderwidth=1, relief='solid')
                numFrame.grid_propagate(False)
                numFrame.grid(column=i, row=j+1)
    
                numFrameLabel=tk.Label(numFrame, text=str(number), width=5)       
                numFrameLabel.pack()
    
                number+=1

        # Generating frames
        k=0
        for i in range(1, 5, 2):
            for j in range(int(FRAME_AMOUNT/2)):
                self.frames.append(Frame(mainFrame, i, j+1, k))
                k+=1

# Process class
class Process():
    def __init__(self, id, state, operation, result, serviceTime, size):
        self.id=id
        self.state=state
        self.operation=operation
        self.result=result
        self.serviceTime=serviceTime
        self.elapsedTime=0
        self.remainingTime=serviceTime
        self.blockedTime=0
        self.arrivalTime=0
        self.finalizationTime=0
        self.returnTime=0
        self.waitTime=0
        self.responseTime='N/A'
        self.quantumTime=0
        self.hasBeenExecuted=False
        self.memSize=size
        self.ocuppiedFrames=[]

# Algorithm program class
class RR():
    # Constructor
    def __init__(self):
        # Calling the start window first
        self.startWindow()

        # Global variables
        
        # Misc data
        self.startWindow
        self.processingWindow
        self.memoryWindow
        self.bcpWindow
        self.pageWindow
        self.processesAmount
        self.quantumSize
        self.idsCount
        self.generalTime
        self.quantum

        # Memory
        self.memory

        # Deques
        self.newProcesses
        self.readyProcesses
        self.executionProcess
        self.blockedProcesses
        self.finishedProcesses

        # Events
        self.paused
        self.bcpShowing
        self.pageShowing

    # Start window function
    def startWindow(self):

        # Window setup
        self.startWindow=tk.Tk()
        self.startWindow.title('Round Robin')
        self.startWindow.geometry('400x400')
        self.startWindow.resizable(False, False)

        # Data
        self.processesAmount=tk.StringVar()
        self.quantumSize=tk.StringVar()

        # Widgets
        mainFrame=ttk.Frame(self.startWindow)
        mainFrame.pack(expand=True)

        # Processes widgets
        processesLabel=ttk.Label(mainFrame, text='Ingresa la cantidad de procesos: ', font=('Arial', 15))
        processesLabel.pack(pady=10)

        processesEntry=ttk.Entry(mainFrame, textvariable=self.processesAmount)
        processesEntry.pack(pady=10)

        # Quantum widgets
        quantumLabel=ttk.Label(mainFrame, text='Ingresa el tamaño del quantum: ', font=('Arial', 15))
        quantumLabel.pack(pady=10)

        quantumEntry=ttk.Entry(mainFrame, textvariable=self.quantumSize)
        quantumEntry.pack(pady=10)

        continueButton=ttk.Button(mainFrame, text='Continuar', command=self.checkInputs)
        continueButton.pack(pady=10)

        # Run
        self.startWindow.mainloop()

    # Check inputs (processesAmount and quantum)
    def checkInputs(self):
        if self.isPositiveInteger(self.processesAmount.get(), "la cantidad de procesos") and \
           self.isPositiveInteger(self.quantumSize.get(), "el quantum"):
            self.processingWindow()

    # Check if value is a positive integer, fieldName is used in a messagebox to give error feedback
    def isPositiveInteger(self, value, fieldName):
        try:
            number=int(value)
            if number > 0:
                return True
            else:
                messagebox.showerror('Error de valor', 
                                    f'{fieldName.capitalize()} debe ser mayor que 0.')
                return False
        except ValueError:
            messagebox.showerror('Error de valor', 
                                f'{fieldName.capitalize()} debe ser un entero.')
            return False

    # Processing window function
    def processingWindow(self):

        ''' Tkinter configuration '''

        # Hiding start window
        self.startWindow.withdraw()

        # Window setup
        self.processingWindow=tk.Toplevel()
        self.processingWindow.title('Paginación Simple')
        startPosX=int((self.processingWindow.winfo_screenwidth()/2)-(WINDOW_WIDTH/2))
        startPosY=int((self.processingWindow.winfo_screenheight()/2)-(WINDOW_HEIGHT/2))
        self.processingWindow.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{startPosX}+{startPosY}')
        self.processingWindow.resizable(False, False)
        self.processingWindow.configure(bg='light gray')

        # Grid configure
        self.processingWindow.grid_rowconfigure(0, weight=1)
        self.processingWindow.grid_rowconfigure(1, weight=1)
        self.processingWindow.grid_columnconfigure(0, weight=1)
        self.processingWindow.grid_columnconfigure(1, weight=1)
        self.processingWindow.grid_columnconfigure(2, weight=1)

        # Event binding
        self.processingWindow.bind("e", self.ePressed)
        self.processingWindow.bind("p", self.pPressed)
        self.processingWindow.bind("c", self.cPressed)
        self.processingWindow.bind("n", self.nPressed)
        self.processingWindow.bind("i", self.iPressed)
        self.processingWindow.bind("b", self.bPressed)
        self.processingWindow.bind("t", self.tPressed)

        ''' Memory configuration '''

        # Memory window setup
        self.memoryWindow=tk.Toplevel()
        self.memoryWindow.title('Memoria')

        # Initializing memory
        self.memory=Memory(self.memoryWindow)

        for i in range(OPERATIVE_SISTEM_MEM_SIZE):
            if self.memory.frames[i].isEmpty():
                self.memory.frames[i].setOcuppiedCells(5)
                self.memory.frames[i].setColor(Colors.OPERATIVE_SISTEM.value)

        ''' OS configuration '''

        # Deque definition
        self.newProcesses=deque()
        self.readyProcesses=deque()
        self.executionProcess=deque()
        self.blockedProcesses=deque()
        self.finishedProcesses=deque()

        # Data
        self.quantum=int(self.quantumSize.get())

        # Widgets 

        # Quantum value widgets
        quantumValueFrame=ttk.Frame(self.processingWindow)
        quantumValueFrame.grid(row=0, column=2, sticky='ne', padx=10, pady=10)
        quantumValueLabel=ttk.Label(quantumValueFrame, 
                                    text=f'Quantum: {self.quantumSize.get()} | Contador: 0', 
                                    font=(PROCESSING_WINDOW_LABELS_FONT_TYPE, 
                                          PROCESSING_WINDOW_LABELS_FONT_SIZE))
        quantumValueLabel.pack()

        # Create new processes
        self.createNewProcesses()

        # Create events
        self.paused=threading.Event()
        self.bcpShowing=threading.Event()
        self.pageShowing=threading.Event()

        # Create frames for each process state
        self.createProcessStateFrames()

        # Create and run threads
        timerThread=threading.Thread(target=self.timer, args=(quantumValueLabel,))
        newThread=threading.Thread(target=self.newProcessesManagement)
        readyThread=threading.Thread(target=self.readyProcessesManagement)
        blockedThread=threading.Thread(target=self.blockedProcessesManagement)
        executionThread=threading.Thread(target=self.executionProcessManagement)
        finishedThread=threading.Thread(target=self.finishedProcessesManagement)

        timerThread.start()
        newThread.start()
        readyThread.start()
        blockedThread.start()
        executionThread.start()
        finishedThread.start()

        # Run
        self.processingWindow.mainloop()

    def createProcessStateFrames(self):
        # Frame for new processes
        new_frame = ttk.LabelFrame(self.processingWindow, text="Procesos Nuevos", padding=10)
        new_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.new_text = tk.Text(new_frame, height=10, width=30, state='disabled')
        self.new_text.pack(fill='both', expand=True)

        # Frame for ready processes
        ready_frame = ttk.LabelFrame(self.processingWindow, text="Procesos Listos", padding=10)
        ready_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.ready_text = tk.Text(ready_frame, height=10, width=30, state='disabled')
        self.ready_text.pack(fill='both', expand=True)

        # Frame for execution process
        exec_frame = ttk.LabelFrame(self.processingWindow, text="Proceso en Ejecución", padding=10)
        exec_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.exec_text = tk.Text(exec_frame, height=10, width=30, state='disabled')
        self.exec_text.pack(fill='both', expand=True)

        # Frame for blocked processes
        blocked_frame = ttk.LabelFrame(self.processingWindow, text="Procesos Bloqueados", padding=10)
        blocked_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.blocked_text = tk.Text(blocked_frame, height=10, width=30, state='disabled')
        self.blocked_text.pack(fill='both', expand=True)

        # Frame for finished processes
        finished_frame = ttk.LabelFrame(self.processingWindow, text="Procesos Terminados", padding=10)
        finished_frame.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky="nsew")
        self.finished_text = tk.Text(finished_frame, height=20, width=40, state='disabled')
        self.finished_text.pack(fill='both', expand=True)

    # Create and append new processes to the deque
    def createNewProcesses(self):
        self.idsCount=1
        for i in range(int(self.processesAmount.get())):
            self.newProcesses.append(self.createProcess())

    # Create one new process
    def createProcess(self):
        id=self.idsCount
        self.idsCount+=1
        operator=rdm.randint(Operators.ADDITION.value, Operators.MODULE.value)
        operand1=round(rdm.uniform(MIN_OPERAND_VALUE, MAX_OPERAND_VALUE), OPERAND_ROUND)
        if operator!=Operators.DIVISION.value or operator!=Operators.MODULE.value:
            operand2=round(rdm.uniform(MIN_OPERAND_VALUE, MAX_OPERAND_VALUE), OPERAND_ROUND)
        else:
            operand2=round(rdm.uniform(1, MAX_OPERAND_VALUE), OPERAND_ROUND)
        match operator:
            case Operators.ADDITION.value:
                result=round(operand1+operand2, OPERAND_ROUND)
                operation=str(operand1)+' + '+str(operand2)
            case Operators.SUBSTRACTION.value:
                result=round(operand1-operand2, OPERAND_ROUND)
                operation=str(operand1)+' - '+str(operand2)
            case Operators.MULTIPLICATION.value:
                result=round(operand1*operand2, OPERAND_ROUND)
                operation=str(operand1)+' * '+str(operand2)
            case Operators.DIVISION.value:
                result=round(operand1/operand2, OPERAND_ROUND)
                operation=str(operand1)+' / '+str(operand2)
            case Operators.MODULE.value:
                result=round(operand1%operand2, OPERAND_ROUND)
                operation=str(operand1)+' % '+str(operand2)
        serviceTime=rdm.randint(MIN_SERVICE_TIME, MAX_SERVICE_TIME)
        state='NUEVO'
        size=rdm.randint(6, 26)
        return Process(id, state, operation, result, serviceTime, size)

    # General timer function
    def timer(self, label):
        # Data
        self.generalTime=0

        # Label
        label.config(text=f'Quantum: {self.quantum} | Contador: {self.generalTime}')
        time.sleep(TIME_STEP_SECONDS)
        self.generalTime=1
        while self.getProcessesInMemoryAmount()!=0:
            # Checking if paused
            if not self.paused.is_set():
                time.sleep(TIME_STEP_SECONDS)

                # Incrementing self.generalTime
                self.generalTime+=1

                # Updating GUI
                label.config(text=f'Quantum: {self.quantum} | Contador: {self.generalTime}')
            time.sleep(TIME_STEP_SECONDS)

        self.showBcp()
                
    # Get actual in-memory processes amount
    def getProcessesInMemoryAmount(self):
        return len(self.readyProcesses)+len(self.executionProcess)+len(self.blockedProcesses)

    # Function to manage new procceses deque behavior
    def newProcessesManagement(self):
        while True:
            # Update new processes text
            self.new_text.config(state='normal')
            self.new_text.delete(1.0, tk.END)
            text = f"Cantidad: {len(self.newProcesses)}\n\n"
            for process in self.newProcesses:
                text += f"ID: {process.id}\nTamaño: {process.memSize}\n"
            self.new_text.insert(tk.END, text)
            self.new_text.config(state='disabled')
            
            # Checking if there's new processes
            if len(self.newProcesses):
                # Letting the new processes entry the ready deque
                for i in range(len(self.newProcesses)):
                    framesReserved=[]
                    neededFrames=0
                    # Always checking for the first new process 
                    processMemSize=self.newProcesses[0].memSize
                    freeFrames=0
                    canStorage=False
                    # Calculating needed frames
                    while True:
                        neededFrames+=1
                        processMemSize-=FRAME_LENGTH
                        if processMemSize<=0:
                            break
                    # Determining if canStorage is True
                    for l in range(len(self.memory.frames)):
                        if self.memory.frames[l].isEmpty():
                            freeFrames+=1
                            framesReserved.append(self.memory.frames[l])
                        if freeFrames==neededFrames:
                            canStorage=True
                            break
                    if canStorage:
                        # Setting occupied frames
                        nonFrameLenghtMultipleFrames=((processMemSize*-1)-FRAME_LENGTH)*-1
                        if nonFrameLenghtMultipleFrames<5:
                            for k in range(len(framesReserved)-1):
                                framesReserved[k].setOcuppiedCells(FRAME_LENGTH)
                            k+=1
                            framesReserved[k].setOcuppiedCells(nonFrameLenghtMultipleFrames)
                        else:
                            for k in range(len(framesReserved)):
                                framesReserved[k].setOcuppiedCells(FRAME_LENGTH)
                        # Coloring
                        for m in range(len(framesReserved)):
                            framesReserved[m].setColor(Colors.READY.value)
                        # Deque logic
                        self.newProcesses[0].ocuppiedFrames=framesReserved
                        self.newProcesses[0].state='LISTO'
                        self.newProcesses[0].arrivalTime=self.generalTime
                        self.readyProcesses.append(self.newProcesses.popleft())
            time.sleep(TIME_STEP_SECONDS/2)

    # Function to manage ready processes deque behavior
    def readyProcessesManagement(self):
        while True:
            # Update ready processes text
            self.ready_text.config(state='normal')
            self.ready_text.delete(1.0, tk.END)
            text = f"Cantidad: {len(self.readyProcesses)}\n\n"
            for process in self.readyProcesses:
                text += f"ID: {process.id}\nTME: {process.serviceTime}\nTT: {process.elapsedTime}\nTR: {process.remainingTime}\n"
            self.ready_text.insert(tk.END, text)
            self.ready_text.config(state='disabled')
            time.sleep(TIME_STEP_SECONDS/2)

    # Function to manage blocked processes deque behavior
    def blockedProcessesManagement(self):
        while True:
            # Checking if paused
            if not self.paused.is_set():
                time.sleep(TIME_STEP_SECONDS)

                # Update blocked processes text
                self.blocked_text.config(state='normal')
                self.blocked_text.delete(1.0, tk.END)
                text = f"Cantidad: {len(self.blockedProcesses)}\n\n"
                for process in self.blockedProcesses:
                    text += f"ID: {process.id}\nTTB: {process.blockedTime}/{MAX_BLOCKED_TIME}\n"
                self.blocked_text.insert(tk.END, text)
                self.blocked_text.config(state='disabled')

                # Checking if there's blocked processes
                if len(self.blockedProcesses):
                    # Cheking first blocked process is ready
                    if self.blockedProcesses[0].blockedTime==MAX_BLOCKED_TIME:
                        # Memory management
                        for i in range(len(self.blockedProcesses[0].ocuppiedFrames)):
                            self.blockedProcesses[0].ocuppiedFrames[i].setColor(Colors.READY.value)
                        self.blockedProcesses[0].blockedTime=0
                        self.blockedProcesses[0].state='LISTO'
                        self.readyProcesses.append(self.blockedProcesses.popleft())
                    # Incrementing processe's blocked and wait time
                    for i in range(len(self.blockedProcesses)):
                        self.blockedProcesses[i].blockedTime+=1
                        self.blockedProcesses[i].waitTime+=1
            time.sleep(TIME_STEP_SECONDS/2)

    # Function to manage ready processes deque behavior
    def executionProcessManagement(self):
        while True:
            # Checking if paused
            if not self.paused.is_set():
                time.sleep(TIME_STEP_SECONDS)

                # Update execution process text
                self.exec_text.config(state='normal')
                self.exec_text.delete(1.0, tk.END)
                if len(self.executionProcess):
                    process = self.executionProcess[0]
                    text = f"ID: {process.id}\n"
                    text += f"Operación: {process.operation}\n"
                    text += f"TME: {process.serviceTime}\n"
                    text += f"TT: {process.elapsedTime}\n"
                    text += f"TR: {process.remainingTime}\n"
                    text += f"Quantum: {process.quantumTime}/{self.quantum}\n"
                    text += f"Tamaño: {process.memSize}"
                else:
                    text = "Ningún proceso en ejecución"
                self.exec_text.insert(tk.END, text)
                self.exec_text.config(state='disabled')

                # Checking if actual process has ended, if so, it appends to finishedProcesses
                if len(self.executionProcess) and self.executionProcess[0].elapsedTime>=self.executionProcess[0].serviceTime:
                    # Memory management
                    for i in range(len(self.executionProcess[0].ocuppiedFrames)):
                        self.executionProcess[0].ocuppiedFrames[i].setColor(Colors.EMPTY.value)
                        self.executionProcess[0].ocuppiedFrames[i].setOcuppiedCells(0)
                    # Deque management
                    self.executionProcess[0].state='TERMINADO'
                    self.executionProcess[0].finalizationTime=self.generalTime
                    self.finishedProcesses.append(self.executionProcess.popleft())

                # If there is a process in readyProcesses, and executionProcess is empty, then it gets into executionProcess
                if len(self.readyProcesses) and len(self.executionProcess)==0:
                    self.executionProcess.append(self.readyProcesses.popleft())
                    self.executionProcess[0].state='EJECUTANDO'
                    # Memory management
                    for i in range(len(self.executionProcess[0].ocuppiedFrames)):
                        self.executionProcess[0].ocuppiedFrames[i].setColor(Colors.EXECUTING.value)

                # Cheking if there's a processes to be executed:
                if len(self.executionProcess):
                        # Managing response time the first time the process executes 
                        if self.executionProcess[0].hasBeenExecuted==False:
                            self.executionProcess[0].hasBeenExecuted=True
                            self.executionProcess[0].responseTime=self.generalTime-self.executionProcess[0].arrivalTime

                        # Checking if process's quantum has ended
                        if self.executionProcess[0].quantumTime>=self.quantum and len(self.readyProcesses):
                            # If so, moving process
                            # Memory management
                            for i in range(len(self.executionProcess[0].ocuppiedFrames)):
                                self.executionProcess[0].ocuppiedFrames[i].setColor(Colors.READY.value)
                            self.executionProcess[0].quantumTime=0
                            self.executionProcess[0].state='LISTO'
                            self.readyProcesses.append(self.executionProcess.popleft())
                            self.executionProcess.append(self.readyProcesses.popleft())
                            # Memory management
                            for i in range(len(self.executionProcess[0].ocuppiedFrames)):
                                self.executionProcess[0].ocuppiedFrames[i].setColor(Colors.EXECUTING.value)
                            self.executionProcess[0].state='EJECUTANDO'
                        else:
                            # Manage process times
                            self.executionProcess[0].elapsedTime+=1
                            self.executionProcess[0].remainingTime-=1
                            self.executionProcess[0].quantumTime+=1
            time.sleep(TIME_STEP_SECONDS/2)

    # Function to manage finished procceses deque behavior
    def finishedProcessesManagement(self):
        while True:
            # Update finished processes text
            self.finished_text.config(state='normal')
            self.finished_text.delete(1.0, tk.END)
            text = f"Cantidad: {len(self.finishedProcesses)}\n\n"
            for process in self.finishedProcesses:
                text += f"ID: {process.id}\n"
                text += f"Operación: {process.operation}\n"
                text += f"Resultado: {process.result}\n"
                text += f"Estado: {process.state}\n\n"
            self.finished_text.insert(tk.END, text)
            self.finished_text.config(state='disabled')
            time.sleep(TIME_STEP_SECONDS/2)

    # Function called when e key is pressed
    def ePressed(self, event):
        if not self.paused.is_set() and len(self.executionProcess):
            self.executionProcess[0].result='ERROR'
            self.executionProcess[0].state='ERROR'
            self.executionProcess[0].elapsedTime=self.executionProcess[0].serviceTime
            self.executionProcess[0].remainingTime=0

    # Function called when p key is pressed
    def pPressed(self, event):
        self.paused.set()

    # Function called when c key is pressed
    def cPressed(self, event):
        self.paused.clear()

        # BCP managing
        if self.bcpShowing.is_set():
            self.bcpShowing.clear()
            self.bcpWindow.destroy()
        elif self.pageShowing.is_set():
            self.pageShowing.clear()
            self.pageWindow.destroy()

    # Function called when n key is pressed
    def nPressed(self, event):
        self.newProcesses.append(self.createProcess())

    # Function called when i key is pressed
    def iPressed(self, event):
        if len(self.executionProcess):
            # Memory management
            for i in range(len(self.executionProcess[0].ocuppiedFrames)):
                self.executionProcess[0].ocuppiedFrames[i].setColor(Colors.BLOCKED.value)
            self.executionProcess[0].state='BLOQUEADO'
            self.blockedProcesses.append(self.executionProcess.popleft())

    # Function called when b key is pressed
    def bPressed(self, event):
        self.paused.set()
        time.sleep(1)
        self.bcpShowing.set()
        self.showBcp()

    # Function called when T key is pressed
    def tPressed(self, event):
        self.paused.set()
        time.sleep(1)
        self.pageShowing.set()
        self.showPage()

    def showBcp(self):
        # BCP window setup
        self.bcpWindow=tk.Toplevel()
        self.bcpWindow.title('BCP')
        self.bcpWindow.geometry(f'{self.bcpWindow.winfo_screenwidth()}x{self.bcpWindow.winfo_screenheight()}')

        # BCP setup
        bcp=ttk.Treeview(self.bcpWindow, columns=("ID", "Estado", "OPE", "TL", "TF", "TRet", "TE", "TS", "TRest", "TResp"), show="headings", height=100)
        bcp.heading("ID", text="ID")
        bcp.heading("Estado", text="Estado")
        bcp.heading("OPE", text="OPE")
        bcp.heading("TL", text="TL")
        bcp.heading("TF", text="TF")
        bcp.heading("TRet", text="TRet")
        bcp.heading("TE", text="TE")
        bcp.heading("TS", text="TS")
        bcp.heading("TRest", text="TRest")
        bcp.heading("TResp", text="TResp")
        bcp.column("ID", width=10)
        bcp.column("Estado", width=150)
        bcp.column("OPE", width=150)
        bcp.column("TL", width=50)
        bcp.column("TF", width=50)
        bcp.column("TRet", width=50)
        bcp.column("TE", width=50)
        bcp.column("TS", width=50)
        bcp.column("TRest", width=50)
        bcp.column("TResp", width=50) 

        # Inserting data
        for i in range(len(self.finishedProcesses)):
            bcp.insert(parent="", index=tk.END, values=(self.finishedProcesses[i].id,
                                                        self.finishedProcesses[i].state,
                                                        f'{self.finishedProcesses[i].operation}={self.finishedProcesses[i].result}',
                                                        self.finishedProcesses[i].arrivalTime,
                                                        self.finishedProcesses[i].finalizationTime,
                                                        self.finishedProcesses[i].finalizationTime-self.finishedProcesses[i].arrivalTime,
                                                        self.finishedProcesses[i].finalizationTime-self.finishedProcesses[i].arrivalTime-self.finishedProcesses[i].elapsedTime,
                                                        self.finishedProcesses[i].serviceTime,
                                                        self.finishedProcesses[i].remainingTime,
                                                        self.finishedProcesses[i].responseTime))
        for i in range(len(self.blockedProcesses)):
            bcp.insert(parent="", index=tk.END, values=(self.blockedProcesses[i].id,
                                                        f'{self.blockedProcesses[i].state} | TRB: {MAX_BLOCKED_TIME-self.blockedProcesses[i].blockedTime}',
                                                        self.blockedProcesses[i].operation,
                                                        self.blockedProcesses[i].arrivalTime,
                                                        "N/A",
                                                        "N/A",
                                                        self.generalTime-self.blockedProcesses[i].arrivalTime-self.blockedProcesses[i].elapsedTime,
                                                        self.blockedProcesses[i].elapsedTime,
                                                        self.blockedProcesses[i].remainingTime,
                                                        self.blockedProcesses[i].responseTime))
        if(len(self.executionProcess)):                                                     
            bcp.insert(parent="", index=tk.END, values=(self.executionProcess[0].id,
                                                        self.executionProcess[0].state,
                                                        self.executionProcess[0].operation,
                                                        self.executionProcess[0].arrivalTime,
                                                        "N/A",
                                                        "N/A",
                                                        self.generalTime-self.executionProcess[0].arrivalTime-self.executionProcess[0].elapsedTime,
                                                        self.executionProcess[0].elapsedTime,
                                                        self.executionProcess[0].remainingTime,
                                                        self.executionProcess[0].responseTime))
        for i in range(len(self.readyProcesses)):
            bcp.insert(parent="", index=tk.END, values=(self.readyProcesses[i].id,
                                                        self.readyProcesses[i].state,
                                                        self.readyProcesses[i].operation,
                                                        self.readyProcesses[i].arrivalTime,
                                                        "N/A",
                                                        "N/A",
                                                        self.generalTime-self.readyProcesses[i].arrivalTime-self.readyProcesses[i].elapsedTime,
                                                        self.readyProcesses[i].elapsedTime,
                                                        self.readyProcesses[i].remainingTime,
                                                        self.readyProcesses[i].responseTime))
        for i in range(len(self.newProcesses)):
            bcp.insert(parent="", index=tk.END, values=(self.newProcesses[i].id,
                                                        self.newProcesses[i].state,
                                                        self.newProcesses[i].operation,
                                                        "N/A",
                                                        "N/A",
                                                        "N/A",
                                                        "N/A",
                                                        self.newProcesses[i].elapsedTime,
                                                        self.newProcesses[i].remainingTime,
                                                        'N/A'))

        bcp.pack()

        # BCP window run
        bcp.mainloop()

    def showPage(self):
        blockedValues=[]
        executionValues=[]
        readyValues=[]
        self.pageWindow=tk.Toplevel(self.processingWindow)
        self.pageWindow.title('Tabla de páginas')
        # Page setup
        page=ttk.Treeview(self.pageWindow, columns=('Info_Proceso', 'NumPagina', 'NumFrame'), show="headings", height=100)
        page.heading("Info_Proceso", text="Info Proceso")
        page.heading("NumPagina", text="Num Pagina")
        page.heading("NumFrame", text="Num Frame")
        page.pack()
        for i in range(len(self.blockedProcesses)):
            info=f'ID: {self.blockedProcesses[i].id} | Tmñ: {self.blockedProcesses[i].memSize}'
            for j in range(len(self.blockedProcesses[i].ocuppiedFrames)):
                blockedValues.append((info, j+1, self.blockedProcesses[i].ocuppiedFrames[j].num))
        for i in range(len(self.executionProcess)):
            info=f'ID: {self.executionProcess[i].id} | Tmñ: {self.executionProcess[i].memSize}'
            for j in range(len(self.executionProcess[i].ocuppiedFrames)):
                executionValues.append((info, j+1, self.executionProcess[i].ocuppiedFrames[j].num))
        for i in range(len(self.readyProcesses)):
            info=f'ID: {self.readyProcesses[i].id} | Tmñ: {self.readyProcesses[i].memSize}'
            for j in range(len(self.readyProcesses[i].ocuppiedFrames)):
                readyValues.append((info, j+1, self.readyProcesses[i].ocuppiedFrames[j].num))
        for i in range(len(blockedValues)):
            page.insert(parent="", index=tk.END, values=(blockedValues[i]))
        for i in range(len(executionValues)):
            page.insert(parent="", index=tk.END, values=(executionValues[i]))
        for i in range(len(readyValues)):
            page.insert(parent="", index=tk.END, values=(readyValues[i]))

if __name__ == "__main__":
    RR()