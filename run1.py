#!/usr/bin/env python3
#imports
import serial
import csv
import requests
import os
import tkinter as tk
import tkinter.scrolledtext as tkT
import time
import tkinter.messagebox as tkMessageBox
from gpiozero import CPUTemperature


def main():
    cpuTemp()
    ROOT.mainloop()
    
def cpuTemp():
    global LABEL_TEMP, TEMP, ROOT
    cpu = CPUTemperature()
    LABEL_TEMP.config(text = "TEMP: "+ str(int(cpu.temperature)), bg='#006', fg='#0f0')
    TEMP = str(int(cpu.temperature))
    LABEL_TEMP.update()
    
def exit1():
    global testZigTerminate, callibrateTerminate, dummyTestTerminate
    testZigTerminate = 1
    callibrateTerminate = 1
    dummyTestTerminate = 1
    exit()
    
def callibrate():
    global testZigTerminate, callibrateTerminate, dummyTestTerminate
    global LABEL_CURRENT, TextBox, LABEL_INTERNET
    END = tk.END
    testZigTerminate = 1
    callibrateTerminate = 0
    dummyTestTerminate = 1
    
    LABEL_CURRENT.config(text = "C: callibrate", bg='#222', fg='#ABC')
    ROOT.update()
    
    TextBox.insert(END,"Checking Temperature ... "+"\n")
    TextBox.yview(END)
    ROOT.update()
    
    time.sleep(2)
    
    cpuTemp()
    TextBox.insert(END,"TEMPERATURE: "+ TEMP + "\n\n")
    TextBox.yview(END)
    ROOT.update()
    if(int(float(str(TEMP))) > 80):
        TextBox.insert(END,"TEMPERATURE IS TOO HIGH, SHUTTING DOWN..." + "\n")
        TextBox.yview(END)
        ROOT.update()
        time.sleep(5)
        exit()
    time.sleep(2)
    TextBox.insert(END,"CHECKING SCANNER & ZIG" + "\n")
    TextBox.yview(END)
    ROOT.update()
    try:
        ser_zig.flush()
        ser_scan.flush()
        ser_write.flush()
        time.sleep(2)
        TextBox.insert(END,"SCANNER & ZIG: OK" + "\n")
        TextBox.yview(END)
        ROOT.update()
    except:
        time.sleep(2)
        TextBox.insert(END,"SCANNER or ZIG: ERROR!!" + "\n" + "check port and reconnect\n\n")
        TextBox.yview(END)
        ROOT.update()
        time.sleep(2)
        TextBox.insert(END,"Restarting Callibration in 20 seconds...\n")
        TextBox.yview(END)
        ROOT.update()
        time.sleep(20)
        callibrate()
    try:
        TextBox.insert(END,"\nCHECKING INTERNET.." + "\n")
        TextBox.yview(END)
        ROOT.update()
        response = requests.get("https://www.google.com", timeout=5)
        print("\033[1;32;40m - - |__~~INTERNET OK~~__|")
        LABEL_INTERNET.config(text = "INTERNET:  OK  ", bg='#000', fg='#ff0')
        ROOT.update()
        TextBox.insert(END,"INTERNET: OK " + "\n")
        TextBox.yview(END)
        ROOT.update()
    except:
        print("\033[1;32;40m - - |__~~INTERNET ERROR!~~__|")
        LABEL_INTERNET.config(text = "INTERNET:  ERROR!  ", bg='#000', fg='#ff0')
        ROOT.update()
        TextBox.insert(END,"NTERNET: ERROR " + "\n")
        TextBox.yview(END)
        ROOT.update()
    TextBox.insert(END,"\nCallibration REPORT: _ status: OK  _" + "\n")
    TextBox.yview(END)
    TextBox.insert(END,"----------------------------" + "\n\n")
    TextBox.yview(END)
    ROOT.update()
    
    
def dummyTest():
    END = tk.END
    global testZigTerminate, callibrateTerminate, dummyTestTerminate
    global LABEL_CURRENT, TextBox
    testZigTerminate = 1
    callibrateTerminate = 1
    dummyTestTerminate = 0
    
    ser_zig.flush()
    ser_scan.flush()
    ser_write.flush()
    
    LABEL_CURRENT.config(text = "C: dummyTest", bg='#222', fg='#ABC')
    ROOT.update()
    
    #Check Always
    i=0
    while(dummyTestTerminate == 0):
        cpuTemp()
        #Scanner Data
        flag = 0
        ROOT.update()
        if ser_scan.in_waiting > 0:
            scan_data = ser_scan.readline().decode('utf-8').rstrip()
            
            TextBox.insert(END, scan_data+"\n")
            TextBox.yview(END)
            ROOT.update()
            
            print("\033[1;32;40m |__~~SCANNED~~__| - - ", scan_data)
            ser_write.write(scan_data.encode())
            flag = 1

        #Zig Data
        while(flag==1 and dummyTestTerminate==0):
            ROOT.update()
            if ser_zig.in_waiting > 0:
                flag = 0
                s_data = ser_zig.readline().decode('utf-8').rstrip()
                TextBox.insert(END, s_data+"\n\n")
                TextBox.yview(END)
                TextBox.pack()
                ROOT.update()
                print("\033[1;37;40m|__~~RECEIVED~~__| - - ", s_data)
                ser_write.write(s_data.encode())
                if isValid(s_data):
                    pass
                else:
                    print("\033[1;31;47m - - |__~~TEST NOT PASSED~~__|")
                    ROOT.update()     
#####################################################################
    
def is_file_empty(file_name):
    try:
        with open(file_name, 'r') as read_obj:
            one_char = read_obj.read(1)
            if not one_char:
               return True
        return False
    except:
        return True
    
#Function to check zig data valid
def isValid(s_data):
    #some data test
    return True

def zigTest():
    END = tk.END
    global  ROOT, LABEL_INTERNET, TextBox, LABEL_CURRENT
    global  testZigTerminate, callibrateTerminate, dummyTestTerminate
    
    LABEL_CURRENT.config(text = "C: zigTest", bg='#222', fg='#ABC')
    ROOT.update()
                        
    testZigTerminate = 0
    callibrateTerminate = 1
    dummyTestTerminate = 1
    
    #Check Always
    i=0
    while(testZigTerminate == 0):
        cpuTemp()
        #Scanner Data
        flag = 0
        ROOT.update()
        if ser_scan.in_waiting > 0:
            scan_data = ser_scan.readline().decode('utf-8').rstrip()
            print("\033[1;32;40m |__~~SCANNED~~__| - - ", scan_data)
            ser_write.write(scan_data.encode())
            
            TextBox.insert(END, "Scan Data: \n"+scan_data +"\n")
            TextBox.yview(END)
            ROOT.update()
            
            flag = 1
            found_flag = 0
            with open("scanner_data.txt", 'r') as scan_file:
                for line in scan_file:  
                    if scan_data+'\n' in line:
                        found_flag = 1
                        break
                    
            if found_flag==0:
                with open("scanner_data.txt", 'a') as out:
                    out.write(scan_data + '\n')
            
            if found_flag==1:
                print("\033[1;24;22m SCAN DATA ALREADY EXISTS",)
                TextBox.insert(END, "SCAN DATA ALREADY EXISTS..Please Rescan New Code\n\n")
                TextBox.yview(END)
                ROOT.update()
                flag = 0
                time.sleep(2)
            

        #Zig Data
        while(flag==1 and testZigTerminate==0):
            ROOT.update()
            if ser_zig.in_waiting > 0:
                flag = 0
                s_data = ser_zig.readline().decode('utf-8').rstrip()
                TextBox.insert(END,"ZIG DATA: \n"+s_data+"\n\n")
                TextBox.yview(END)
                TextBox.pack()
                ROOT.update()
                print("\033[1;37;40m|__~~RECEIVED~~__| - - ", s_data, end="")
                ser_write.write(s_data.encode())
                if isValid(s_data):
                    with open(mainFile, 'a', newline="") as file1:
                        csvwriter1 = csv.writer(file1) 
                        csvwriter1.writerow([scan_data,s_data])
                    
                    try:
                        response = requests.get(s_url+"S_: "+scan_data+"    "+"Z_: "+s_data, timeout=5)
                        print("\033[1;32;40m - - |__~~RESPONSE OK~~__|")
                        LABEL_INTERNET.config(text = "INTERNET:  OK  ", bg='#000', fg='#ff0')
                        LABEL_SYNC.config(text = "", bg='#003', fg='#6a0')
                        ROOT.update()
                        if not is_file_empty(backupFile):
                            with open(backupFile, 'r+', newline="") as read_obj :
                                csv_reader1 = csv.reader(read_obj) 
                                lastLine = read_obj.readlines()[-1]
                                print("\033[1;30;47m Uploading Backup: ",lastLine[:-1])
                                arr = lastLine[:-1].split(',')
                                response = requests.get(s_url+"S_: "+str(arr[0])+"    "+"Z_: "+str(arr[1]),  timeout=5)
                                LABEL_SYNC.config(text = "Syncing Backup..", bg='#003', fg='#6a0')
                                ROOT.update()
                                print("\033[1;32;40m - - |__~~RESPONSE OK~~__|")
                            with open(backupFile, 'r+', newline="") as f:
                                lines = f.readlines()
                                lines.pop()
                            with open(backupFile, 'w+', newline="") as f:
                                f.writelines(lines)
                        if is_file_empty(backupFile):
                            try:
                                os.remove(backupFile)
                            except:
                                pass
                            
                    except Exception as e:
                            LABEL_INTERNET.config(text = "INTERNET: DOWN ",bg='#fff', fg='#f00')
                            ROOT.update()
                            #print("except",e)
                            print("\033[1;30;43m - - |__~~Internet Down.. Backuping~~__|")
                            with open(backupFile, 'a', newline="") as write_obj3 :
                                csvwriter3 = csv.writer(write_obj3) 
                                csvwriter3.writerow([scan_data,s_data])
                else:
                    print("\033[1;31;47m - - |__~~TEST NOT PASSED~~__|")
                    ROOT.update()     
#####################################################################
#GUI CONSTANTS

#ROOT
r = tk.Tk()
r.title('SCA-ZIG DATA-HANDLE PROTOCOL')
r.geometry("480x320")
ROOT = r
#Frame
f = tk.Frame(ROOT)
#MenuButton
menubutton = tk.Menubutton(f, text="Options", fg="blue")   
menubutton.menu = tk.Menu(menubutton)  
menubutton["menu"]= menubutton.menu
menubutton.menu.add_command(label = "Calibration",command = callibrate)  
menubutton.menu.add_command(label = "Dummy Test",command=dummyTest)
menubutton.menu.add_command(label = "Operate",command=zigTest)
menubutton.menu.add_command(label = "Exit",command=exit1) 
menubutton.pack(side='left',padx=10, anchor='nw')
#Label
LABEL_CURRENT = tk.Label(f, text="C: ")
LABEL_CURRENT.pack(side = 'right',padx=10, anchor='nw')
LABEL_INTERNET = tk.Label(f, text="INTERNET: .... ")
LABEL_INTERNET.pack(side='right',padx=10, anchor='nw')
LABEL_TEMP = tk.Label(f, text="dvrblacktech")
LABEL_TEMP.pack(side = 'right',padx=10, anchor='nw')
f.pack()
#TextBox
LABEL_LOGO = tk.Label(ROOT, text="© All rights reserved - dvrblacktech")
LABEL_LOGO.pack(side = 'bottom',padx=10, anchor='s')

LABEL_SYNC = tk.Label(ROOT, text="")
LABEL_SYNC.pack(side = 'bottom',padx=10, anchor='s')

TextBox = tkT.ScrolledText(ROOT, height='100', width='100', wrap=tk.WORD)
TextBox.pack(side='left', anchor='e')

#####################################################################

#####################################################################
#Constants

#AppScript URL to upload DATA
s_url = "https://script.google.com/macros/s/AKfycbzHbV93W5wwXaKzcJJ6j5fRKFTJZ0kQRvEVxo00arqlT3f4Y3VoEUnOEysbt4UuEq0/exec?data="

#File Names
mainFile = 'uploaded_data.csv'
backupFile = 'backup.csv'

#Serial Ports
serialPortScan = '/dev/ttyACM0'
serialPortZig = '/dev/ttyACM0'
serialPortSend = '/dev/ttyACM0'

#Baud Rates
baud_rate_send = 9600
baud_rate_receive_zig = 9600
baud_rate_receive_scan = 9600

#Serial port initialization and flush if any buffer
ser_zig = serial.Serial(serialPortZig, baud_rate_receive_zig, timeout=1000)
ser_scan = serial.Serial(serialPortScan, baud_rate_receive_scan, timeout=1000)
ser_write = serial.Serial (serialPortSend, baud_rate_send, timeout=1000)

ser_zig.flush()
ser_scan.flush()
ser_write.flush()

#Flags
testZigTerminate = 1
callibrateTerminate = 1
dummyTestTerminate = 1

TEMP = ""
#####################################################################


if __name__ == '__main__':
    main()

#####################

