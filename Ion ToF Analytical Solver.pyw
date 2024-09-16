'''
Ion ToF Analytical Solver.pyw: Solves kinematics equations for an ion by approximating the ToF setup as parallel plates with constant E-fields between them

Author: Rick Mattish
'''

import math
from tkinter import *


font1 = ('Helvetica', 16)
font2 = ('Helvetica', 12)
font3 = ('Helvetica', 18)
font4 = ('Helvetica', 14)

#Opens About Window with description of software
def About():
    helpMessage ='Ion ToF Analytical Solver solves\n kinematics equations for an ion by\n approximating the ToF setup as\n parallel plates with constant\n E-fields between them.'
    t = Toplevel(root)
    t.wm_title("About")
    t.configure(background='lightgreen')
    l = Label(t, text = helpMessage, bg='lightgreen', font = font2)
    l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    
#Opens Settings Window, which allows the user to change the persistent global variables V and R
def Settings():
	global root
	global d1
	global d2
	global d3

	t = Toplevel(root)
	t.geometry('400x300')
	t.wm_title("Settings")
	t.configure(bg='grey95')

	L0 = Label(t, text = 'Settings', font = font3)
	L0.place(relx=0.5, rely=0.15, anchor = CENTER)
	L1 = Label(t, text = 'd1:', font = font4)
	L1.place(relx=0.4, rely=0.3, anchor = E)
	E1 = Entry(t, font = font4, width = 10)
	E1.insert(0,str(round(1000*d1,1)))
	E1.place(relx=0.4, rely=0.3, anchor = W)
	L2 = Label(t, text = 'mm', font = font4)
	L2.place(relx=0.64, rely=0.3, anchor = W)

	L3 = Label(t, text = 'd2:', font = font4)
	L3.place(relx=0.4, rely=0.425, anchor = E)
	E2 = Entry(t, font = font4, width = 10)
	E2.insert(0,str(round(1000*d2,1)))
	E2.place(relx=0.4, rely=0.425, anchor = W)
	L4 = Label(t, text = 'mm', font = font4)
	L4.place(relx=0.64, rely=0.425, anchor = W)

	L5 = Label(t, text = 'd3:', font = font4)
	L5.place(relx=0.4, rely=0.55, anchor = E)
	E3 = Entry(t, font = font4, width = 10)
	E3.insert(0,str(round(100*d3,2)))
	E3.place(relx=0.4, rely=0.55, anchor = W)
	L6 = Label(t, text = 'cm', font = font4)
	L6.place(relx=0.64, rely=0.55, anchor = W)

	b1 = Button(t, text = 'Update', relief = 'raised', background='lightblue', activebackground='blue', font = font1, width = 10, height = 1,\
			command = lambda: [updateSettings(float(E1.get()),float(E2.get()),float(E3.get())),t.destroy()])
	b1.place(relx=0.75, rely=0.8, anchor = CENTER)

	b2 = Button(t, text = 'Reset', relief = 'raised', background='pink', activebackground='red', font = font1, width = 10, height = 1, command = lambda: [updateSettings(10.3,10.3, 55.88),t.destroy()])
	b2.place(relx=0.25, rely=0.8, anchor = CENTER)

#Updates the persistent global variables V and R, as well as store which elements the user has selected for calibration
def updateSettings(E1, E2, E3):
	global d1
	global d2
	global d3
	global root
	d1 = E1/1000
	d2 = E2/1000
	d3 = E3/100
	f = open("variables",'w')
	f.write('d1='+str(d1)+'\n'+'d2='+str(d2)+'\n'+'d3='+str(d3))
	f.close()
	makeDrawing()

def makeDrawing():
	global W
	try:
		w.destroy()
	except:
		pass
	#Creates a Drawing of the Experimental Setup
	w = Canvas(root, width=1000, height=350)
	w.place(relx = 0.5, rely = 0.4, anchor = CENTER)

	#Creates Ion Trajectory Line
	w.create_line(55, 155, 945, 155, fill="red", dash=(4, 4))


	#Creates First Potential Plate
	w.create_rectangle(5, 5, 55, 305, fill='lightblue')
	w.create_text(30, 155, text='V1', font=font2)

	#Creates Second Potential Plate (Skimmer)
	w.create_rectangle(155, 5, 205, 145, fill='lightblue')
	w.create_rectangle(155, 165, 205, 305, fill='lightblue')
	w.create_text(180, 70, text='V2', font=font2)
	w.create_text(180, 235, text='V2', font=font2)

	#Creates Distance 1 Label
	w.create_line(55, 330, 155, 330)
	w.create_line(55, 315, 55, 345)
	w.create_line(155, 315, 155, 345)
	w.create_text(105, 320, text=f'{round(1000*d1,1)} mm', font = font2)


	#Creates Third Potential Plate (Second Skimmer)
	w.create_rectangle(305, 5, 355, 145, fill='lightblue')
	w.create_rectangle(305, 165, 355, 305, fill='lightblue')
	w.create_text(330, 70, text='0 V', font=font2)
	w.create_text(330, 235, text='0 V', font=font2)


	#Creates Distance 2 Label
	w.create_line(205, 330, 305, 330)
	w.create_line(205, 315, 205, 345)
	w.create_line(305, 315, 305, 345)
	w.create_text(255, 320, text=f'{round(1000*d2,1)} mm', font = font2)


	#Creates Detector
	w.create_rectangle(945,80, 995, 230, fill='lightyellow')
	w.create_text(970, 155, text='CEM', font = font2)


	#Creates Distance 3 Label
	w.create_line(355, 330, 945, 330)
	w.create_line(355, 315, 355, 345)
	w.create_line(945, 315, 945, 345)
	w.create_text(650, 320, text=f'{round(100*d3,2)} cm', font = font2)

#Calculates the acceleration of both bodies from Newton's Second Law of Motion and Law of Gravitation and returns both values as an acceleration vector
def calcAccel(V1, V2, d1, d2, q, m):
    a1 = (q*(V1-V2))/(m*d1)
    a2 = (q*V2)/(m*d2)
    aVector = [a1, a2]
    return aVector


#Calculates the new velocities of both bodies from equation of motion and returns the values as a velocity vector
def calcNewVel(vi, a, t):
    vf = vi + a*t
    return vf


def calcNewTime(vi, a, d):
    t = (((-2*vi)/(a))+math.sqrt(pow(((-2*vi)/a),2)-4*((-2*d)/a)))/2
    return t

def convertMass(m):
    newM = m*1.6603145*pow(10,-27)
    return newM

def convertCharge(q):
    newQ = q*1.602*pow(10,-19)
    return newQ


def Calculate():
	global d1
	global d2
	global d3
	V1 = float(entry1.get())
	V2 = float(entry5.get())
	q = convertCharge(float(entry4.get()))
	m = convertMass(float(entry6.get()))
	vi1 = 0

	aVector = calcAccel(V1, V2, d1, d2, q, m)

	a1 = aVector[0]
	a2 = aVector[1]

	t1 = calcNewTime(vi1, a1, d1)
	vi2 = calcNewVel(vi1, a1, t1)

	t2 = calcNewTime(vi2, a2, d2)
	v = calcNewVel(vi2, a2, t2)

	t3 = d3/v

	ToF = round((t1 + t2 + t3)/(1*pow(10,-6)),3)
	
	ToFMessage = "The Time of Flight is " + str(ToF) + " μs"
	messageVar = Message(root, text = ToFMessage, font = font1, width = 500)
	messageVar.config(bg='yellow')
	messageVar.place(relx = 0.6, rely = 0.3, anchor = CENTER)
        
	
#Loads the variables V and R from the variables file, and creates the file if none exists
try:
	f = open('variables', 'r')
	variables = f.readlines()
	f.close()
	d1 = float(variables[0].split('=')[1])
	d2 = float(variables[1].split('=')[1])
	d3 = float(variables[2].split('=')[1])
except:
    d1 = 0.0103
    d2 = 0.0103
    d3 = 0.5588
    f = open("variables",'w')
    f.write('d1='+str(d1)+'\n'+'d2='+str(d2)+'\n'+'d3='+str(d3))
    f.close()
    
root = Tk() 
menu = Menu(root) 
root.config(menu=menu)

root.title("Time of Flight Analytical Solver")
root.geometry("1280x768")

#Creates single line text entries
text1 = Label(root, text='Potential 1:', font = font1).grid(row=0)
entry1 = Entry(root, font = font1)
entry1.grid(row=0,column=1)

text2 = Label(root, text='V', font = font1).grid(row=0, column=2)
text3 = Label(root, text='V', font = font1).grid(row=1, column=2)




text4 = Label(root, text='\tIon Charge:', font = font1).grid(row=0, column=3)
entry4 = Entry(root, font = font1)
entry4.grid(row=0,column=4)

text5 = Label(root, text='Potential 2:', font = font1).grid(row=1)
entry5 = Entry(root, font = font1)
entry5.grid(row=1,column=1)

text6 = Label(root, text='\tIon Mass:', font = font1).grid(row=1, column=3)
entry6 = Entry(root, font = font1)
entry6.grid(row=1, column=4)

text7 = Label(root, text='e', font = font1).grid(row=0, column=5)
text8 = Label(root, text='amu', font = font1).grid(row=1, column=5)


#Creates drop down menus
filemenu = Menu(menu) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_command(label='New')
filemenu.add_command(label='Open...') 
filemenu.add_separator()
filemenu.add_command(label='Settings', command= lambda: Settings())
filemenu.add_command(label='Exit', command=root.destroy)


helpmenu = Menu(menu) 
menu.add_cascade(label='Help', menu=helpmenu) 
helpmenu.add_command(label='About', command= lambda: About())


#Creates an Exit Button
b1 = Button(text = "Exit", relief = "raised", activebackground='red', font = font1, width = 15, height = 3, command = root.destroy)
b1.place(relx = 0.6, rely = 0.7, anchor = CENTER)

#Creates a Simulate Button
b2 = Button(text = 'Calculate ToF', relief = 'raised', activebackground='blue', font = font1, width = 15, height = 3, command = lambda: Calculate())
b2.place(relx = 0.4, rely = 0.7, anchor = CENTER)


#Creates Copyright Notice
helpMessage ='Copyright © 2019 Richard Mattish All Rights Reserved.' 
messageVar = Message(root, text = helpMessage, font = font2, width = 600) 
#messageVar.config(bg='lightgreen')
messageVar.place(relx = 0, rely = 1, anchor = SW)

makeDrawing()





root.mainloop() 
