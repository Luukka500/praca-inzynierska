from tkinter import *
from tkinter import messagebox
import pymysql

window=Tk()
window.title('Wyliczacz - Załóż konto')
window.geometry('925x500+300+200')
window.configure(bg='white')
window.resizable(False,False)

def signup():
    username=user.get()
    password=code.get()
    conformPassword=confirmCode.get()
#############------------------------ łączenie z bazą danych
    try:
        connection = pymysql.connect \
            (host="localhost",
             user="root",
             passwd="",
             database="wyliczacv1")
        print("MySQL Database connection successful")
    except:
        print("Coś poszło nie tak")

    mycursor = connection.cursor()
    mycursor.execute('select nazwa from uzytkownicy where nazwa=%s', (user.get()))
    myresult = mycursor.fetchall()

#############------------------------ zakłdanie konta
    try:
        if myresult[0][0] == username:
            messagebox.showerror('Błąd!','Podany login już istnieje')
    except:
        if password==conformPassword:
            print('zakłdam konto, jest dobrze')
            mycursor.execute("INSERT INTO uzytkownicy (nazwa, grupa, haslo, wlaczone) VALUES (%s, 'uzytkownicy', %s, 'n');",(username, password))
            mycursor.execute('select * from uzytkownicy')
            myresult = mycursor.fetchall()
            print(myresult)
            connection.commit()
            messagebox.showinfo('Informacja','Konto założone. Poczekaj aż zostanie włączone przez administratora.')
        else:
            messagebox.showerror('Błąd','Hasła się nie zgadzają')

def sign():
    window.destroy()
    import main

img=PhotoImage(file='dolacz2.png')
Label(window,image=img,border=0,bg='white').place(x=50,y=25)

frame=Frame(window,width=350,height=390,bg='white')
frame.place(x=480,y=50)

heading=Label(frame,text='Załóż konto',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

#############------------------------ wpisz login
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    if user.get()=='':
        user.insert(0,'Login')
user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Login')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
#############------------------------ Podaj hasło
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    if code.get()=='':
        code.insert(0,'Hasło')
code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11),show='*')
code.place(x=30,y=150)
code.insert(0,'Hasło')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
#############------------------------ Powtórz hasło
def on_enter(e):
    confirmCode.delete(0,'end')
def on_leave(e):
    if confirmCode.get()=='':
        confirmCode.insert(0,'Hasło')
confirmCode=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11),show='*')
confirmCode.place(x=30,y=220)
confirmCode.insert(0,'Hasło')
confirmCode.bind('<FocusIn>',on_enter)
confirmCode.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
#############------------------------ Przyciski
Button(frame,width=39,pady=7,text='Załóż konto',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
label=Label(frame,text='Masz już konto?',fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=90,y=340)

signin=Button(frame,width=8,text='Zaloguj się',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=sign)
signin.place(x=190,y=341)

window.mainloop()
