import mysql.connector
from tkinter import *
import tkinter.font as tkfont
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import ttk




# Connection parameters
host = 'localhost'
user = 'root'
password = 'Sinaaaan'
database = 'miniproj'

# Create a connection
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
# Create a cursor
mycursor = mydb.cursor()



    
        
#fuelprice() used to get the fuel price for the current date
def fuelprice():
    mycursor.execute("select fuel_name,fuel_price from fuel;")
    fuel_price=mycursor.fetchall()
    fuel=[]
    price=[]
    for i in fuel_price:
        fuel.append(i[0])
        price.append(i[1])
    text=f"Current fuel Price:\n"
    for fuel_type, fuel_price in zip(fuel, price):
        add = f"{fuel_type}: ₹{fuel_price:.2f}\n"
        text += add
    messagebox.showinfo("current price",text)


#fuelavailability() used to get the availability of fuel in the pump
def fuelavailability():
    mycursor.execute("select fuel,available_space from tank;")
    fuel_availability=mycursor.fetchall()
    fuel=[]
    availability=[]
    for i in fuel_availability:
        fuel.append(i[0])
        availability.append(i[1])
    text=f"Current fuel Availability:\n"
    for fuel_type, fuel_availability in zip(fuel, availability):
        add = f"{fuel_type}: {fuel_availability:.2f} l\n"
        text += add
    messagebox.showinfo("current availability",text)
        
        


   
    



#signup() is used to get code to signup page and check the code if correct it will go to signup page else it gives access denied message
def signup():
    global signupWindow
    global secretcode_entry
    signupWindow=Toplevel()
    signupWindow.title("user signup")

    secretlabel=Label(signupWindow,text="ENTER SECRET CODE")
    secretlabel.pack()
    secretcode_entry= Entry(signupWindow)
    secretcode_entry.pack()
    clickbutton=Button(signupWindow,text="check code",command=checksecretcode)
    clickbutton.pack()
def checksecretcode():
    secretcode=secretcode_entry.get()
    if secretcode=='1234':
        messagebox.showinfo("code verified","ready to signup")
        signupPage()
        signupWindow.withdraw()
    else:
        messagebox.showinfo("invalid","ACCESS DENIED")


#this is the signup page which is used to get new worker from user side
def signupPage():
    global password_entry
    global username
    global password1
    global phoneNo
    global userdesc_combobox
    global email
    global show_password
    global signupWindow1
    
    signupWindow1=Toplevel()
    signupWindow1.title("SIGNUP")
    signupWindow1.geometry("600x500")
    Label(signupWindow1,text="username").pack()
    username=Entry(signupWindow1)
    username.pack()
    
    Label(signupWindow1,text="password").pack()
    password_entry=Entry(signupWindow1, show="*")
    password_entry.pack()
    show_password = BooleanVar()
    show_password_button = Checkbutton(signupWindow1, text="Show Password", variable=show_password, command=toggle_password_visibility)
    show_password_button.pack()
    
    Label(signupWindow1,text="confirm password").pack()
    password1=Entry(signupWindow1,show="*")
    password1.pack()
    
    Label(signupWindow1,text="phone number").pack()
    phoneNo=Entry(signupWindow1)
    phoneNo.pack()
    
    Label(signupWindow1, text="User Description:").pack()
    userdesc_options = ["sales", "transport"]
    userdesc_combobox = ttk.Combobox(signupWindow1, values=userdesc_options)
    userdesc_combobox.pack()
    
    Label(signupWindow1,text="email").pack()
    email=Entry(signupWindow1)
    email.pack()

    signup_button = Button(signupWindow1, text="Signup",command=signupUser)
    signup_button.pack()


#this is used to show password of the signup page
def toggle_password_visibility():
    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

#this function checks the username if present in the user table if present we cannot add user else we can add user
def signupUser():
    user=username.get()
    passw=password_entry.get()
    pass1=password1.get()
    phone=phoneNo.get()
    userDesc=userdesc_combobox.get()
    email1=email.get()
    text="select username from user;"
    mycursor.execute(text)
    rows=mycursor.fetchall()
    flag=0
    for i in rows:
        if i[0]==user:
            messagebox.showerror("ERROR", "USERNAME ALREADY PRESENT")
            flag=1
            break
    if(flag!=1):
        if(pass1!=passw):
            messagebox.showerror("ERROR", "PASSWORDS ARE DIFFERENT")
        else:
            text="insert into user values(%s,%s,%s,%s,%s)"
            data=(user,passw,phone,userDesc,email1)
            mycursor.execute(text,data)
            mydb.commit()
            messagebox.showerror("DONE", "USER INSERTED SUCCESSFULLY")
            signupWindow1.withdraw()
            
        
#this is a login page for workers
def login():
    global username_entry
    global password_entry
    global loginWindow
    
    loginWindow=Toplevel()
    loginWindow.title("WORKER LOGIN PAGE")
    loginWindow.geometry("600x500")

    # Username label and entry
    username_label = Label(loginWindow, text="Username:")
    username_label.pack(pady=10)
    username_entry = Entry(loginWindow)
    username_entry.pack(pady=5)

    # Password label and entry
    password_label = Label(loginWindow, text="Password:")
    password_label.pack(pady=10)
    password_entry = Entry(loginWindow, show="*")
    password_entry.pack(pady=5)

    # Login button
    login_button = Button(loginWindow, text="Login", command=checklogin)
    login_button.pack(pady=20)

    loginWindow.mainloop()
    
#this function checks the login username and password are matching
def checklogin():
    username = username_entry.get()
    password = password_entry.get()
    query="select username,password from user;"
    mycursor.execute(query)
    rows=mycursor.fetchall()
    A=[False,False]
    for i in rows:
        if i[0]==username:
            if i[1]==password:
                A=[True,True]  

    if A==[True,True]:
        messagebox.showerror("Login Success", "LOGIN SUCCESFULL")
        query1="select userDesc from user where username='"+username+"';"
        mycursor.execute(query1)
        typeuser=mycursor.fetchall()
        for i in typeuser:
            if i[0]=="admin":
                adminPage()
            elif i[0]=="sales":
                salesPage()
            elif i[0]=="transport":
                transportPage()

        
        
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

#if the login username is of admin then addmin page will load
#****************************************************************************************************************
def adminPage():
    loginWindow.withdraw()
    

    adminWindow=Toplevel()
    adminWindow.title("ADMIN PAGE")
    adminWindow.geometry("600x500")

    
    signupbutton=Button(adminWindow,text="MANAGE WORKERS",command=manageWorkers)
    loginbutton=Button(adminWindow,text="SALES DETAILS",command=salesAccount)
    pricedetail=Button(adminWindow,text="UPDATE FUEL PRICE",command=updatefuel)
    loads=Button(adminWindow,text="MAINTAIN LOADS",command=maintainloads)
    deleteload=Button(adminWindow,text="DELETE OLD LOADS",command=deleteloads)
    message=Button(adminWindow,text="MESSAGES",command=showMsg)
    getfuelprice1=Button(adminWindow,text="GET FUEL PRICE OF PARTICULAR DAY",command=getfuelprice)
    availibility=Button(adminWindow,text="CHECK FUEL AVAILIBILITY",command=fuelavailability)
    

    signupbutton.pack()
    loginbutton.pack()
    pricedetail.pack()
    loads.pack()
    deleteload.pack()
    availibility.pack()
    getfuelprice1.pack()
    message.pack()

#this is a part of admin page this function is used to get the fuel price a particular day
def getfuelprice():
    getfuel=Toplevel()
    getfuel.title("get fuel price")
    getfuel.geometry("600x500")
    global fueldateentry
    global fuelnameentry
    
    label1=Label(getfuel,text="enter date of which you need to find the fuel price(yyyy-mm-dd)")
    label1.pack()
    fueldateentry=Entry(getfuel)
    fueldateentry.pack()
    label2=Label(getfuel,text="enter fuel name")
    label2.pack()
    fuel_options = ["Petrol", "diesel","oil","power petrol"]
    fuelnameentry=ttk.Combobox(getfuel, values=fuel_options)
    fuelnameentry.pack()

    button1=Button(getfuel,text="get price",command=getprice)
    button1.pack()

def getprice():
    date=fueldateentry.get()
    fuelname=fuelnameentry.get()
    text="SELECT price FROM fuelprice_history WHERE fuelName ='"+fuelname+"' AND till >= '"+date+"' ORDER BY till ASC LIMIT 1;"
    mycursor.execute(text)
    rows=mycursor.fetchone()
    messagebox.showinfo("detail","fuel price on "+date+" is : "+str(rows[0]))
    
#this function is part of admin page used to get the sales details between two dates
def salesAccount():                        
    global dateentry1
    global dateentry2
    salesDetails=Toplevel()
    salesDetails.title("ACCOUNTS")
    salesDetails.geometry("600x500")

    label1=Label(salesDetails,text="get sale details between date")
    label1.pack()
    label2=Label(salesDetails,text="from date(YYYY-MM-DD)")
    label2.pack()
    dateentry1=Entry(salesDetails)
    dateentry1.pack()
    label3=Label(salesDetails,text="to date(YYYY-MM-DD)")
    label3.pack()
    dateentry2=Entry(salesDetails)
    dateentry2.pack()
    button1=Button(salesDetails,text="get details",command=getsaledetails)
    button1.pack()

    

def getsaledetails():
    date1=dateentry1.get()
    date2=dateentry2.get()

    query1="select fuel_type,sum(sale_amount),sum(sale_litres) from sales where sale_date>='"+date1+"' and sale_date<='"+date2+"' group by fuel_type;"
    mycursor.execute(query1)
    rows=mycursor.fetchall()
    text=""
    for i in rows:
        sale=str(i[1])
        litres=str(i[2])
        text=text+i[0]+":\n total sale amount="+sale+"  total litres sold="+litres+"\n"
    messagebox.showinfo("details",text)
        
    
    
#this is a part of admin page,this function is used to manage other workers of the petrol pump,we can insert a worker or delete a worker
def manageWorkers():
    manageWorker=Toplevel()
    manageWorker.title("manage workers")
    manageWorker.geometry("600x500")
    button1=Button(manageWorker,text="INSERT WORKER",command=signupPage)
    button1.pack()
    button2=Button(manageWorker,text="REMOVE WORKER",command=removeWorker)
    button2.pack()

#remove worker page
def removeWorker():
    global entry1
    RemoveWorker=Toplevel()
    RemoveWorker.title("remove a worker")
    RemoveWorker.geometry("600x500")
    label1=Label(RemoveWorker,text="Enter worker username")
    label1.pack()
    entry1=Entry(RemoveWorker)
    entry1.pack()
    button1=Button(RemoveWorker,text="remove",command=remove)
    button1.pack()

#this function checks whether there is a user present if present it will delete else error message
def remove():
    username=entry1.get()
    text="select username from user;"
    mycursor.execute(text)
    rows=mycursor.fetchall()
    flag=0
    for i in rows:
        if i[0]==username:
            text1="delete from user where username='"+username+"';"
            mycursor.execute(text1)
            mydb.commit()
            text2=username+" removed from worker's list"
            flag=1
            messagebox.showinfo("user found",text2)

    if flag==0:
        messagebox.showerror("ERROR","user doesnt found in the worker's list")

    

#this is a message of admin page which will show messages,if fuel availability is low it will show message here
def showMsg():
    global messages
    if messages==[]:
        messagebox.showinfo("MESSEGES","no message")
    else:   
        for i in messages:
            text=i+"\n"
        messagebox.showinfo("MESSEGES",text)
        messages=[]

    
#this is part of admin page
def updatefuel():
    global fuelentry
    global priceentry
    global fuelUpdate
    fuelUpdate=Toplevel()
    fuelUpdate.title("update fuel price")
    fuelUpdate.geometry("600x500")

    label1=Label(fuelUpdate,text="ENTER FUEL")
    label1.pack()
    fuel_options = ["Petrol", "diesel","oil","power petrol"]
    fuelentry=ttk.Combobox(fuelUpdate, values=fuel_options)
    fuelentry.pack()
    label2=Label(fuelUpdate,text="ENTER UPDATED PRICE")
    label2.pack()
    priceentry=Entry(fuelUpdate)
    priceentry.pack()
    button1=Button(fuelUpdate,text="SUBMIT",command=fuelupdate)
    button1.pack()

def fuelupdate():#done
    l=[]
    text=fuelentry.get()
    l.append(text)
    text=priceentry.get()
    l.append(text)

    text2="updated "+l[0]+" price to : "+l[1]
    messagebox.showinfo("sales",text2)
    text1="update fuel set fuel_price="+l[1]+" where fuel_name='"+l[0]+"';"
    mycursor.execute(text1)
    mydb.commit()

    fuelUpdate.withdraw()
    
    
#******************************************************************************************************************
    

    



def salesPage():#done
    loginWindow.withdraw()
    salesWindow=Toplevel()
    salesWindow.title("SALES PAGE")
    salesWindow.geometry("600x500")
    global fuel_entry
    global amount_entry
    label1=Label(salesWindow,text="enter fuel name")
    label1.pack()
    fuel_options = ["Petrol", "diesel","oil","power petrol"]
    fuel_entry=ttk.Combobox(salesWindow, values=fuel_options)
    fuel_entry.pack()
    label2=Label(salesWindow,text="enter amount")
    label2.pack()
    amount_entry=Entry(salesWindow)
    amount_entry.pack()
    clickbutton=Button(salesWindow,text="submit",command=insertsale)
    clickbutton.pack()
    

def insertsale():#done
    l=[]
    ins=fuel_entry.get()
    l.append(ins)
    ins=amount_entry.get()
    l.append(ins)
    try:
        text1="insert into sales (fuel_type, sale_amount) values('"+l[0]+"',"+l[1]+");"
        mycursor.execute(text1)
        mydb.commit()
        text=l[0]+" for "+l[1]+" done"
        messagebox.showinfo("sales",text)
        fuel_options = ["Petrol", "diesel","oil","power petrol"]
        for i in fuel_options:
            text="select available_space from tank where fuel='"+i+"';"
            mycursor.execute(text)
            rows=mycursor.fetchall()
            for j in rows:
                k=j[0]
            if k<5.00:
                text1="low availibility of "+i
                messages.append(text1)
    except mysql.connector.Error as e:
        messagebox.showerror("Error", str(e))
    
    
    

#***************************************************************************************************************************

def transportPage():
    loginWindow.withdraw()
    transportWindow=Toplevel()
    transportWindow.title("TRANSPORT PAGE")
    transportWindow.geometry("600x500")

    button1=Button(transportWindow,text="add load",command=addloads)
    button1.pack()
    button2=Button(transportWindow,text="maintain loads",command=maintainloads)
    button2.pack()
    button3=Button(transportWindow,text="delete old loads",command=deleteloads)
    button3.pack()


def deleteloads():
    deleteloads=Toplevel()
    deleteloads.title("delete loads")
    deleteloads.geometry("600x500")
    global deletedateentry
    
    label1=Label(deleteloads,text="enter date to which we have to delete loads")
    label1.pack()
    deletedateentry=Entry(deleteloads)
    deletedateentry.pack()
    button1=Button(deleteloads,text="delete",command=deleteentry)
    button1.pack()

def deleteentry():
    date=deletedateentry.get()
    text="DELETE FROM loads WHERE start_date <'"+date+"';"
    mycursor.execute(text)
    mydb.commit()
    messagebox.showinfo("detail","entries deleted upto date="+date)
    

def addloads():
    loadsadd=Toplevel()
    loadsadd.title("add load")
    loadsadd.geometry("600x500")
    global driverentry
    global numberentry
    global fueltypeentry
    global startdateentry
    global tankerentry
    

    label1=Label(loadsadd,text="enter driver's name")
    label1.pack()
    driverentry=Entry(loadsadd)
    driverentry.pack()
    label2=Label(loadsadd,text="enter driver no")
    label2.pack()
    numberentry=Entry(loadsadd)
    numberentry.pack()
    label3=Label(loadsadd,text="enter fuel type")
    label3.pack()
    fueltypeentry=Entry(loadsadd)
    fueltypeentry.pack()
    label4=Label(loadsadd,text="enter start date(YYYY-MM-DD)")
    label4.pack()
    startdateentry=Entry(loadsadd)
    startdateentry.pack()
    label5=Label(loadsadd,text="enter fuel in tanker(litre)")
    label5.pack()
    tankerentry=Entry(loadsadd)
    tankerentry.pack()
    button1=Button(loadsadd,text="submit",command=adddetails)
    button1.pack()

def adddetails():
    name=driverentry.get()
    number=numberentry.get()
    fuel=fueltypeentry.get()
    date=startdateentry.get()
    avail=tankerentry.get()

    query="insert into loads(driver_name,driver_no,fuel_type,start_date,fuel_in_tank) values(%s,%s,%s,%s,%s);"
    data=(name,number,fuel,date,avail)
    mycursor.execute(query,data)
    mydb.commit()
    messagebox.showinfo("details","load details entered successfully")

def maintainloads():
    global maintainloads_window
    maintainloads_window = Toplevel()
    maintainloads_window.title("Maintain Loads")
    maintainloads_window.geometry("600x500")

    global fuelentry1
    global fuelbutton

    label1 = Label(maintainloads_window, text="Enter the fuel to load")
    label1.pack()

    fuel_options = ["petrol", "diesel", "oil", "power petrol"]
    fuelentry1 = ttk.Combobox(maintainloads_window, values=fuel_options)
    fuelentry1.pack()

    fuelentry1.bind("<FocusOut>", on_combobox_focus_out)

    global fuelbutton
    fuelbutton = Button(maintainloads_window, text="Get Details", command=fetchdata, state="disabled")
    fuelbutton.pack()

def on_combobox_focus_out(event):
    # Enable the fuelbutton when the combobox loses focus
    fuelbutton.config(state="normal")

def fetchdata():
    maintainloads_window.withdraw()
    global fetched
    fetched=Toplevel()
    fetched.title("data fetched")
    fetched.geometry("600x500")
    
    
    fuel = fuelentry1.get()

    # Create a Treeview widget to display data
    columns = ("loadid", "name", "phoneNo", "fuel type", "start date","fuel_in_litres")  # Replace with your actual column names
    treeview = ttk.Treeview(fetched, columns=columns, show="headings")

    # Set column headings
    for col in columns:
        treeview.heading(col, text=col)

    # Place the Treeview widget on the window
    treeview.pack(padx=10, pady=10)

    for item in treeview.get_children():
        treeview.delete(item)

    # Execute a sample query
    query = f"SELECT * FROM loads WHERE fuel_type = '{fuel}';"
    mycursor.execute(query)

    # Fetch all rows
    rows = mycursor.fetchall()
    for row in rows:
        treeview.insert("", "end", values=[str(value) + "\t" for value in row])

    global loadentry1
    label1=Label(fetched,text="enter load id of the tanker to use")
    label1.pack()
    loadentry1=Entry(fetched)
    loadentry1.pack()
    button1=Button(fetched,text="fill tank",command=filltank)
    button1.pack()
    
    fuelbutton.config(state="disabled")  # Disable the button after fetching data


def filltank():
    loadid=loadentry1.get()
    fuelname=fuelentry1.get()

    text="select total_space,available_space from tank where fuel='"+fuelname+"';"
    mycursor.execute(text)
    row=mycursor.fetchone()

    text1="select fuel_in_tank from loads where loadid="+loadid+";"
    mycursor.execute(text1)
    row1=mycursor.fetchone()

    value=row[0]
    value1=row[1]
    value2=row1[0]

    temp=value-value1    
    
    if float(value2)>=temp:
        text="update tank set available_space="+str(value)+" where fuel='"+fuelname+"';"
        mycursor.execute(text)
        mydb.commit()
        value2=value2-temp
        text1="update loads set fuel_in_tank=%s where loadid=%s;"
        mycursor.execute(text1,(value2,loadid))
        mydb.commit()
    else:
        value1=value1+value2
        text="update tank set available_space=%s where fuel=%s;"
        mycursor.execute(text,(value1,fuelname))
        mydb.commit()
        text1="update loads set fuel_in_tank=0 where loadid="+loadid+" ;"
        mycursor.execute(text1)
        mydb.commit()

    messagebox.showinfo("details","value added succesfully")
        
#**************************************************************************************************************************   

    
    

    


    
    



#MAIN PROGRAM

root=Tk()
root.title("PETROL PUMP MANAGEMENT SYSTEM")
root.geometry("600x500")



welcomelabel=Label(root,text="WELCOME TO INDUS PETROLEUM",font=tkfont.Font(weight="bold"))
welcomelabel.pack()
global messages
messages=[]

signupbutton=Button(root,text="SIGNUP AS WORKER",command=signup)
loginbutton=Button(root,text="LOGIN",command=login)
pricedetail=Button(root,text="CHECK TODAYS FUEL PRICE",command=fuelprice)
availibilitybutton=Button(root,text="CHECK AVAILIBILITY OF FUEL",command=fuelavailability)


signupbutton.pack()
loginbutton.pack()
pricedetail.pack()
availibilitybutton.pack()



                

root.mainloop()



