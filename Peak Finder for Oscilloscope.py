import pyvisa
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from tkinter import *
import statistics
import nidaqmx
from decimal import Decimal

save_dir = 'C:\\Users\\group\\Desktop\\Rick Mattish\\Save Data\\' # directory to save data
font1 = ('Helvetica', 16)
font2 = ('Helvetica', 12)

'''
#Opens About Window with description of software
def results(peakNum_Average, Pirani, CC, PKR):
    Message1 = 'Average Pressures:'
    Message2 = 'Pirani: ' + '%.2E' % Decimal(str(Pirani)) + ' torr' + '\nCC: ' + '%.2E' % Decimal(str(CC)) + ' torr' + '\nPKR: ' + '%.2E' % Decimal(str(PKR)) + ' torr'
    Message3 = 'The Average Number of Peaks is ' + str(peakNum_Average)
    t = Toplevel(root)
    t.wm_title("Results")
    t.configure(background='lightgreen')
    text1 = Label(t, text = Message1, bg = 'lightgreen', font = font1)
    text2 = Label(t, text = Message2, bg = 'lightgreen', font = font2)
    text3 = Label(t, text = Message3, bg='lightgreen', font = font1)
    text1.pack(side="top", fill="both", expand=True, padx=100, pady=1)
    text2.pack(side="top", fill="both", expand=True, padx=100, pady=10)
    text3.pack(side="top", fill="both", expand=True, padx=100, pady=20)
'''

#Opens About Window with description of software
def results(peakNum_Average, Pirani, CC, PKR, run):
    Message1 = 'Average Pressures:'
    Message2 = 'Pirani: ' + '%.2E' % Decimal(str(Pirani)) + ' torr' + '\nCC: ' + '%.2E' % Decimal(str(CC)) + ' torr' + '\nPKR: ' + '%.2E' % Decimal(str(PKR)) + ' torr'
    Message3 = 'The Average Number of Peaks is ' + str(peakNum_Average)
    t = Toplevel(root)
    t.wm_title("Results " + str(run))
    text1 = Label(t, text = Message1, font = font1)
    text2 = Label(t, text = Message2, font = font2)
    text3 = Label(t, text = Message3, font = font1)
    text1.pack(side="top", fill="both", expand=True, padx=100, pady=1)
    text2.pack(side="top", fill="both", expand=True, padx=100, pady=10)
    text3.pack(side="top", fill="both", expand=True, padx=100, pady=20)

def pressure_single():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev8/ai3',terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,max_val=10, min_val=-10)
        V1 = task.read()
    P1 = 10**(V1 - 5.625)
    print(P1)

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev8/ai2',terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,max_val=10, min_val=-10)
        V2 = task.read()
    P2 = 10**(1.25*V2 - 12.875)
    print(P2)

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev8/ai1',terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,max_val=10, min_val=-10)
        V3 = task.read()
    P3 = 10**(1.667*V3 - 11.46)
    print(P3)

    pressure = [P1, P2, P3]
    return pressure


def pressure_continuous():
    
    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev8/ai3',terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,max_val=10, min_val=-10)
        V1 = task.read()
    P1 = 10**(V1 - 5.625)

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev8/ai2',terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,max_val=10, min_val=-10)
        V2 = task.read()
    P2 = 10**(1.25*V2 - 12.875)

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev8/ai1',terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,max_val=10, min_val=-10)
        V3 = task.read()
    P3 = 10**(1.667*V3 - 11.46)
        
    press_data = np.append(press_data,[[P1,P2,P3,time.time()-t0]], axis=0)

    global b_pc
    b_pc.config(text='Stop', command=stop_prun, font=ft, foreground='red')
    f_press.after(1000, pressure_c)

    
def peakFinder(dataList2,minValue):
    peakNum = 0

    i = 1
    while i < len(dataList2)-1:

        if float(dataList2[i]) > minValue and float(dataList2[i]) > float(dataList2[i-1]) and float(dataList2[i]) > float(dataList2[i+1]):
            peakNum = peakNum + 1 
            
        i = i + 1
    return peakNum


def dataLengthChecker(length, voltage):
    if float(length) != len(voltage):

        errorMessage = "Error: Not all data points were recorded from the oscilloscope."

        label_e = Label(root, text = errorMessage, font = font2, bg = 'firebrick1')
        label_e.place(relx = 0.5, rely = 0.75, anchor = CENTER)



def acquireData(Threshold, runNum):

    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0x0699::0x03A3::C041030::INSTR')

    dataList = []
    Pirani = []
    CC = []
    PKR = []
    
    i = 0
    while i < runNum:
        inst.timeout = 7000

        # reset and autoset scope
        inst.write('*rst')

        # scope settings
        inst.write('ch1:scale 2')
        inst.write('horizontal:scale 2E-04') # set time/div, if you change this make sure data:resolution doesn't change
        inst.write('trigger:a:level 3') # trigger level V
        inst.write('select:ch2 on') # set ch2
        inst.write('ch2:scale 1') # set V/div
        inst.write('acquire:state off')
        inst.write('acquire:stopafter sequence')
        inst.write('data:source ch2') # data on ch 1
        inst.write('data:resolution full')
        length = inst.query('WFMOUTPRE:RECORDLENGTH?')
        inst.write('data:start 1') #check the length of the data available if something goes wrong (should be 100k points)
        inst.write('data:stop ' + str(length))

        time.sleep(1)

        yscale = float(inst.query('wfmoutpre:ymult?'))

        xscale = float(inst.query('wfmoutpre:xincr?'))

        inst.write('acquire:state on')

        time.sleep(.1)

        inst.query('*OPC?')

        time.sleep(.1)

        rawData = inst.query_binary_values('curve?', datatype='b', is_big_endian=True)

        pressure = pressure_single()
        Pirani.append(pressure[0])
        CC.append(pressure[1])
        PKR.append(pressure[2])
        

        j = 0
        voltage = []
        timevar = []
        timeadjust = (1E-3)/xscale
        timetemp = range(len(rawData))
        while j < len(rawData):
            
            voltage.append(-yscale*rawData[j])
            timevar.append(timeadjust*xscale*timetemp[j])
            j = j + 1

        dataLengthChecker(length, voltage)
            

        rundata = [timevar, voltage]

        dataList.append(rundata)

        i = i + 1

    dataVector = [dataList, Pirani, CC, PKR]

    return dataVector

            
        


def plotData(data, peakNum):
    timevar = data[0]
    voltage = data[1]

    fig, ax = plt.subplots()
    plt.plot(timevar,voltage)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (V)')
    plt.title('Number of peaks: ' + str(peakNum))
    #plt.text(0.5,0.8, '# of peaks = ' + str(peakNum), horizontalalignment = 'center', verticalalignment = 'center', transform = ax.transAxes)
    plt.show()


#Writes the data in "data" to a text file named "datafile"
def writeListToFile(data):
    date = datetime.datetime.now().strftime("%m%d%y_%H%M")
    datafile = open(save_dir + 'data_' + date + '.txt', 'w')
    datafile.write('time (ms)\tvoltage (V)\n')
  
    for i in range(0,len(data)-1):
        datafile.write(str(data[i]) + '\t' + str(data[i]) + '\n')
        
    datafile.close()



def mainProgram():
    global run
    run = run + 1
    Threshold = float(e_threshold.get())
    runNum = int(e_runNum.get())
    
    dataVector = acquireData(Threshold, runNum)
    dataList = dataVector[0]
    Pirani = statistics.mean(dataVector[1])
    CC = statistics.mean(dataVector[2])
    PKR = statistics.mean(dataVector[3])
    
    


    if runNum == 1:
        data = dataList[0]
        peakNum = peakFinder(data[1],Threshold)
        print('# of peaks = ' + str(peakNum))
        plotData(data, peakNum)
        writeListToFile(data)
        
        
    else:
        peakNumList = []
        j = 0
        while j < len(dataList):
            peakNum = peakFinder(dataList[j][1],Threshold)
            peakNumList.append(peakNum)
            print(peakNum)
            j = j + 1
        peakNum_Average = statistics.mean(peakNumList)
        results(peakNum_Average,Pirani,CC,PKR,run)
            



global run
run = 0
#This is the GUI for the software
root = Tk() 
menu = Menu(root) 
root.config(menu=menu)

root.title("Peak Finder")
root.geometry("600x400")


e_threshold = Entry(root, font=font1, width = 10)
e_threshold.insert(0,'0.05')
e_threshold.place(relx = 0.5, rely = 0.2, anchor = W)



label1 = Label(root, text = 'Voltage threshold:', font = font1)
label1.place(relx = 0.5, rely = 0.2, anchor = E)

label2 = Label(root, text = 'V', font = font1)
label2.place(relx = 0.71, rely = 0.2, anchor = W)



e_runNum = Entry(root, font=font1, width = 10)
e_runNum.insert(0,'1')
e_runNum.place(relx = 0.5, rely = 0.3, anchor = NW)



label3 = Label(root, text = 'Number of Data Runs:', font = font1)
label3.place(relx = 0.5, rely = 0.3, anchor = NE)



#Creates a "Collect Data" Button
b1 = Button(text = 'Collect Data', font = font1, relief = 'raised', activebackground='lightgreen', width = 17, height = 3, command = lambda: mainProgram())
b1.place(relx = 0.5, rely = 0.55, anchor = CENTER)




#Creates Copyright Notice
helpMessage ='Copyright © 2019 Richard Mattish All Rights Reserved.' 
messageVar = Message(root, text = helpMessage, font = font2, width = 600) 
messageVar.place(relx = 0, rely = 1, anchor = SW)


root.mainloop()




