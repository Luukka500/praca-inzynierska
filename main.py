from tkinter import *
from tkinter import messagebox
import pymysql

#############------------------------ ustawienia okna
root=Tk()
root.title('Wyliczacz - Logowanie')
root.geometry('925x500+300+200')
root.configure(bg='white')
root.resizable(False,False)

def signin():
    username=user.get()
    password=code.get()
#############------------------------ łączenie z bazą danych
    try:
        connection = pymysql.connect \
            (host="localhost",
             user="root",
             passwd="",
             database="wyliczacv1")
    except:
        messagebox.showerror("Błąd!","Brak połączenia z bazą danych! Spróbuj później.")

    mycursor = connection.cursor()

    mycursor.execute('select nazwa,wlaczone,haslo,grupa from uzytkownicy where nazwa=%s', (user.get()))
    myresult = mycursor.fetchall()

#############------------------------ warunki logowania
    try:
        if myresult[0][0]==username and myresult[0][1] == 't' and myresult[0][2] == password:
            print("Konto włączone, login i hasło działa")
            print('Działa')
            root.destroy()
            txtFile = open("myfile.txt", "w")
            txtFile.write(myresult[0][0]+'\n'+myresult[0][3])
            txtFile.close()
            connection.commit()
            connection.close()
            import wyliczaczMain

        elif myresult[0][0]==username and myresult[0][1] == 'n' and myresult[0][2] == password:
            print("Konto wyłączone")
            messagebox.showerror('Błąd!','Twoje konto jest wyłączone. Skontaktuj się z administratorem w celu jego aktywacji.')
        elif myresult[0][0]!=username and myresult[0][1] == 't' and myresult[0][2] == password:
            messagebox.showerror('Błąd!','Niepoprawny login.')
        elif myresult[0][0]==username and myresult[0][1] == 't' and myresult[0][2] != password:
            messagebox.showerror('Błąd!','Niepoprawne hasło.')
        elif myresult[0][0]!=username and myresult[0][1] == 't' and myresult[0][2] != password:
            messagebox.showerror('Błąd!','Niepoprawne hasło i login.')
        else:
            messagebox.showerror('Bład','Nie wiem co się stało :(')
    except:
        messagebox.showerror('Bład', 'Podany login nie istnieje!')

def signupComand():
    root.destroy()
    import signup

img=PhotoImage(file='login2.png')
Label(root,image=img,bg='white').place(x=5,y=50)

frame=Frame(root,width=350,height=350,bg='white')
frame.place(x=520,y=70)

heading=Label(frame,text='Zaloguj',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=110,y=5)

#############------------------------ wpisz login
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Login')

user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Login')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

#############------------------------ wpisz hasło
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Hasło')
code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11),show='*')
code.place(x=30,y=150)
code.insert(0,'Hasło')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
#############------------------------

Button(frame,width=39,pady=7,text='Zaloguj się',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
label=Label(frame,text='Nie masz konta?',fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=35,y=270)

sign_up=Button(frame,width=8,text='Zarejestruj',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signupComand)
sign_up.place(x=130,y=269)

root.mainloop()
