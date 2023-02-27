from __future__ import print_function
from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
from mailmerge import MailMerge
from datetime import date
from docx2pdf import convert
import os
from time import time, ctime
import math
import os.path

root=Tk()
root.title('Wyliczacz')
root.geometry('925x700+300+50')
root.configure(bg='white')
root.resizable(False,False)
def read_file():
    file_text = open("myfile.txt", "r")
    lines=file_text.readlines()
    lines[0]=(lines[0][:-1])
    return lines
groupe = read_file()

def wyloguj():
    response = messagebox.askyesno("UWAGA!!!", "Czy chcesz wyłączyć program?")

    if response == 1:
        root.destroy()
        import main

def home_page():
    lines = read_file()
    home_frame = Frame(main_frame)
    home_frame.pack(fill = BOTH, expand = True)
    ipadding = {'ipadx': 100, 'ipady': 10}
    label1 = Label(home_frame, text="Witaj " + lines[0] + " w programie Wyliczacz.\nCo będziemy dzisiaj robić?",font=('Bold', 30), bg="#f9f9f9", fg="black")
    label1.pack(**ipadding, fill=X)
    photo = PhotoImage(file='atom.png')
    label4 = Label(home_frame,image=photo,bg='#f9f9f9')
    label4.image = photo
    label4.pack(fill=BOTH)

def categories_page():

    def query_database():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
        except:
            messagebox.showerror("Błąd połączenia", "Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()

        c.execute('SELECT * FROM kategorie')
        records = c.fetchall()

        # dodaj dane do tabeli i wyświetl
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2]), tags=('oddrow',))
            count += 1

        connection.commit()
        connection.close()

    def selec_record(e):
        # wyczyść okienka wprowadzania
        id_entry.delete(0, END)
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

        # wybierz numer rekordu
        selected = my_tree.focus()
        # wybierz wartości
        values = my_tree.item(selected, 'values')

        # wprowadz do ramek wprowadzania
        id_entry.insert(0, values[0])
        fn_entry.insert(0, values[1])
        ln_entry.insert(0, values[2])

    def add_record():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        if fn_entry.get() == '' or ln_entry.get() == '':
            messagebox.showerror("Błąd!", "Wszystkie pola muszą być uzuepłenione")
        else:
            c.execute(
                'INSERT INTO kategorie (nazwa, opis) VALUES(%s, %s)',
                (fn_entry.get(),
                 ln_entry.get(),
                 ))
            id_entry.delete(0, END)
            fn_entry.delete(0, END)
            ln_entry.delete(0, END)
            messagebox.showinfo("Sukces!", "Kategoria dodana")

        connection.commit()
        connection.close()

        my_tree.delete(*my_tree.get_children())
        query_database()

    def update_record():
        selected = my_tree.focus()
        my_tree.item(selected, text='', values=(id_entry.get(), fn_entry.get(), ln_entry.get(),))

        # aktualizacja bazy danych
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        c.execute(
            'UPDATE kategorie SET nazwa=%s, opis=%s WHERE id_kategorii=%s', (

                fn_entry.get(),
                ln_entry.get(),
                id_entry.get(),
            ))
        messagebox.showinfo("Sukces!", "Aktualizacja się powiodła!")
        connection.commit()
        connection.close()

        id_entry.delete(0, END)
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

    def remove_record():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        response = messagebox.askyesno("UWAGA!!!", "Czy chcesz skasować kategorię?")

        # Add logic for message box
        if response == 1:
            kom = "DELETE from kategorie WHERE id_kategorii=" + id_entry.get()
            c.execute(kom)
            messagebox.showinfo("Sukces", "Kategoria usunięta pomyślnie.")
        connection.commit()
        connection.close()
        my_tree.delete(*my_tree.get_children())
        query_database()

    def lookup_records():
        global search_entry, search

        search = Toplevel(root)
        search.title("Wyszukiwanie")
        search.geometry("400x200")

        # Create label frame
        search_frame = LabelFrame(search, text="Nazwa kategorii")
        search_frame.pack(padx=10, pady=10)

        # Add entry box
        search_entry = Entry(search_frame, font=("Helvetica", 18))
        search_entry.pack(pady=20, padx=20)

        # Add button
        search_button = Button(search, text="Szukaj", command=search_records)
        search_button.pack(padx=20, pady=20)

    def search_records():
        lookup_record = search_entry.get()
        print(lookup_record)
        search.destroy()

        for record in my_tree.get_children():
            my_tree.delete(record)

        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        c.execute("SELECT * FROM kategorie WHERE nazwa='" + lookup_record + "'")
        records = c.fetchall()

        # Add our data to the screen
        global count
        count = 0


        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2]),tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2]),tags=('oddrow',))
            count += 1

        # Commit changes
        connection.commit()
        connection.close()

    def reset():
        id_entry.delete(0, END)
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)

        my_tree.delete(*my_tree.get_children())
        query_database()

    categories_frame = Frame(main_frame)
    categories_frame.pack(fill=BOTH, expand=True)
    ipadding = {'ipadx': 100, 'ipady': 10}

    label4 = Label(categories_frame)
    label4.pack(expand=True, fill=BOTH)
    head_frame = Frame(label4)
    head_frame.pack(fill=BOTH)
    groupe = read_file()
    print(groupe)

    # styl tabeli
    style = ttk.Style()
    style.theme_use('default')

    # zmiana kolorów
    style.configure('Treeview',
                    background='#d3d3d3',
                    foreground='black',
                    rowheight=25,
                    fiekdbackground='#d3d3d3')

    # zmiana koloru wybranego rekordu
    style.map('Treeview', background=[('selected', '#347083')])

    # tworzenie ramki dla tabeli
    tree_frame = Frame(head_frame)
    tree_frame.pack(pady=10)

    # tworzenie suwaka
    tree_scrol = Scrollbar(tree_frame)
    tree_scrol.pack(side=RIGHT, fill=Y)

    # tworzenie podglądu
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrol.set, selectmode='extended')
    my_tree.pack()

    # ustawienia suwaka
    tree_scrol.config(command=my_tree.yview)

    # kolumny
    my_tree['columns'] = ('ID', 'Nazwa', 'Opis')

    # format kolumn
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('ID', anchor=CENTER, width=50)
    my_tree.column('Nazwa', anchor=W, width=250)
    my_tree.column('Opis', anchor=W, width=300)

    # nagłówek tabeli
    my_tree.heading('#0', text='', anchor=W)
    my_tree.heading('ID', text='ID', anchor=CENTER)
    my_tree.heading('Nazwa', text='Nazwa', anchor=W)
    my_tree.heading('Opis', text='Opis', anchor=W)

    # dodaj dane

    my_tree.tag_configure('oddrow', background='white')
    my_tree.tag_configure('evenrow', background='lightblue')

    # dodawanie rekordów (ramka)
    data_frame = LabelFrame(head_frame, text='Record')
    data_frame.pack(fill='x', expand='yes', padx=20)
    data_frame.columnconfigure(0, weight=1)
    data_frame.columnconfigure(1, weight=5)


    # pole wprowadzania plus opis dla ID (i tak nie działa, ale cicho ;))
    id_label = Label(data_frame, text='ID')
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    # pole wprowadzania plus opis dla nazwy
    fn_label = Label(data_frame, text='Nazwa')
    fn_label.grid(row=1, column=0, padx=10, pady=10)
    fn_entry = Entry(data_frame)
    fn_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)

    # pole wprowadzania plus opis dla opisu
    ln_label = Label(data_frame, text='Opis')
    ln_label.grid(row=2, column=0, padx=10, pady=10)
    ln_entry = Entry(data_frame)
    ln_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)

    # przyciski ramka
    button_frame = LabelFrame(head_frame, text='Operacje')
    button_frame.pack(fill='x', expand='yes', padx=20)

    # przycisk aktulizacji
    update_button = Button(button_frame, text='Aktualizuj', command=update_record)
    update_button.grid(row=0, column=1, padx=10, pady=10)
    if groupe[1] != 'administratorzy':
        update_button.config(state="disabled")

    # przycisk dodaj
    add_button = Button(button_frame, text='Dodaj nową kategorię', command=add_record)
    add_button.grid(row=0, column=0, padx=10, pady=10)


    # przycisk usun
    remove_button = Button(button_frame, text='Usuń kategorię', command=remove_record)
    remove_button.grid(row=0, column=3, padx=10, pady=10)
    if groupe[1] != 'administratorzy':
        remove_button.config(state="disabled")

    # przycisk szukaj
    select_record_button = Button(button_frame, text='Szukaj', command=lookup_records)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)

    # przycisk reset widoku
    select_record_button = Button(button_frame, text='Wyczyść', command=reset)
    select_record_button.grid(row=0, column=8, padx=10, pady=10)

    my_tree.bind('<ButtonRelease-1>', selec_record)

    # łączenie z bazą danych - funkcja
    query_database()

    # koniec 16:53

def measurements_page():

    def query_database():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()

        c.execute('''SELECT pomiary.id_pomiaru, pomiary.pomiar1, pomiary.pomiar2, pomiary.pomiar3, pomiary.jednostka, kategorie.nazwa, uzytkownicy.nazwa
                    FROM kategorie
                    INNER JOIN pomiary 
                    ON pomiary.id_kat = kategorie.id_kategorii
                    INNER JOIN uzytkownicy
                    ON uzytkownicy.id_uzytkownika = pomiary.id_uzy
                    ''')


        records = c.fetchall()

        # dodaj dane do tabeli i wyświetl
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),  tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))
            count += 1
        connection.commit()
        connection.close()

    def selec_record(e):
        # wyczyść okienka wprowadzania
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        id_entry.delete(0, END)
        sn_entry.delete(0, END)
        gn_entry.delete(0, END)
        hn_entry.delete(0, END)

        # wybierz numer rekordu
        selected = my_tree.focus()
        # wybierz wartości
        values = my_tree.item(selected, 'values')

        # wprowadz do ramek wprowadzania
        fn_entry.insert(0, values[1])
        ln_entry.insert(0, values[2])
        id_entry.insert(0, values[0])
        sn_entry.insert(0, values[3])
        gn_entry.insert(0, values[4])
        hn_entry.insert(0, values[5])

    def cat_down():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()

        c.execute('SELECT id_kategorii, nazwa FROM kategorie')
        records = c.fetchall()
        connection.commit()
        connection.close()
        return records

    def update_record():
        selected = my_tree.focus()
        my_tree.item(selected, text='', values=(
        id_entry.get(), fn_entry.get(), ln_entry.get(), sn_entry.get(), gn_entry.get(), hn_entry.get(),))

        # aktualizacja bazy danych
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()

        c.execute('UPDATE pomiary SET pomiar1=%s, pomiar2=%s, pomiar3=%s, jednostka=%s WHERE id_pomiaru=%s;', (

            fn_entry.get(),
            ln_entry.get(),
            sn_entry.get(),
            gn_entry.get(),
            id_entry.get(),
        ))
        connection.commit()

        c.execute('UPDATE pomiary, kategorie SET pomiary.id_kat = kategorie.id_kategorii WHERE pomiary.id_pomiaru = %s AND kategorie.nazwa=%s',(
            id_entry.get(),
            hn_entry.get(),
        ))
        connection.commit()
        connection.close()

        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        id_entry.delete(0, END)
        fn_entry.delete(0, END)
        sn_entry.delete(0, END)
        gn_entry.delete(0, END)

        my_tree.delete(*my_tree.get_children())
        query_database()


    def add_data():
        selected = my_tree.focus()
        my_tree.item(selected, text='', values=(
            id_entry.get(), fn_entry.get(), ln_entry.get(), sn_entry.get(), gn_entry.get(), hn_entry.get(),))

        # aktualizacja bazy danych
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()

        c.execute('SELECT id_kategorii FROM kategorie WHERE nazwa=%s', (

            hn_entry.get(),
        ))
        connection.commit()
        id_cat = c.fetchall()

        user = read_file()
        comand='SELECT id_uzytkownika FROM uzytkownicy WHERE nazwa="'+user[0]+'"'
        c.execute(comand)
        connection.commit()
        id_user = c.fetchall()

        try:
            c.execute('INSERT INTO pomiary (id_kat, id_uzy, pomiar1, pomiar2, pomiar3, jednostka) VALUES (%s, %s, %s, %s, %s, %s)', (

                id_cat,
                id_user,
                fn_entry.get(),
                ln_entry.get(),
                sn_entry.get(),
                gn_entry.get(),
            ))
            connection.commit()

            connection.close()

            fn_entry.delete(0, END)
            ln_entry.delete(0, END)
            id_entry.delete(0, END)
            sn_entry.delete(0, END)
            gn_entry.delete(0, END)

            my_tree.delete(*my_tree.get_children())
            query_database()
        except:
            messagebox.showerror("Błąd połączenia", "Brak podanych wszystkich wartości")

    def remove_record():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        response = messagebox.askyesno("UWAGA!!!", "Czy chcesz skasować pomiar?")

        # Add logic for message box
        if response == 1:
            kom = "DELETE from pomiary WHERE id_pomiaru=" + id_entry.get()
            c.execute(kom)
            messagebox.showinfo("Sukces", "Pomiar usunięty pomyślnie.")
        connection.commit()
        connection.close()
        my_tree.delete(*my_tree.get_children())
        query_database()

    def obliczenia():

        #łączenie z bazą danych i pobieranie danych do obliczen
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        kom = "SELECT * FROM pomiary WHERE id_pomiaru=" + id_entry.get()
        c.execute(kom)
        records = c.fetchall()
        kom2 = 'SELECT nazwa FROM kategorie WHERE id_kategorii=' + str(records[0][1])
        c.execute(kom2)
        nazwa_kat = c.fetchall()

        #konwersja na zmienno przecinkowe
        pom1 = records[0][3]
        pom2 = records[0][4]
        pom3 = records[0][5]
        pom1=pom1.replace(",", ".")
        pom2=pom2.replace(",", ".")
        pom3=pom3.replace(",", ".")
        try:
            pom1 = float(pom1)
            pom2 = float(pom2)
            pom3 = float(pom3)
        except:
            messagebox.showerror("Błąd!", "Któraś z podanych wartości pomiarowych nie jest liczbą.")
            return 0;
        print(pom1,pom2,pom3)
        # obliczenia od Michała
        # Średnia arytmetyczna
        srednia = (pom1 + pom2 + pom3) / 3
        srednia = float(round(srednia, 4))

        # Bład
        p1r = float(round(abs(pom1 - srednia), 4))
        p2r = float(round(abs(pom2 - srednia), 4))
        pr3 = float(round(abs(pom3 - srednia), 4))

        # Wariacja
        wariacja = (((pom1 - srednia) ** 2) + ((pom2 - srednia) ** 2) + ((pom3 - srednia) ** 2)) / 3
        wariacja = float(round(wariacja, 4))

        # Odchylnie standardowe
        odchs = math.sqrt(wariacja)
        odchs = float(round(odchs, 4))

        # Odchylnie standardowe średniej
        odchss = (odchs / (math.sqrt(3)))
        odchss = float(round(odchss, 4))

        # Współczynnik zmienności (wyrażony w procentach)
        wspzmien = (odchs / srednia) * 100
        wspzmien = float(round(wspzmien, 4))

        # moment 3 rzedu
        m3rz = (((pom1 - srednia) ** 3) + ((pom2 - srednia) ** 3) + ((pom3 - srednia) ** 3)) / 3
        m3rz1 = m3rz**1/3
        m3rz = float(round(m3rz1, 4))

        # wsp aymetrii
        wa = (m3rz / (odchss ** 3))
        wa = float(round(wa, 4))

        #tworzenie raportu
        template = "przykładowy-raport.docx"
        document = MailMerge(template)

        document.merge(
            id_uzytkownika=str(records[0][2]),
            id_pomiaru=str(records[0][0]),
            jed=records[0][6],
            ID_kategorii=str(records[0][1]),
            nazwa_kategorii=nazwa_kat[0][0],
            pomiar_1=str(pom1),
            pomiar_2=str(pom2),
            pomiar_3=str(pom3),
            data='{:%d.%m.%Y}'.format(date.today()),
            srednia=str(srednia),
            odch_stand=str(odchs),
            wspol_zmienn=str(wspzmien),
            mom_cent_3_rzd=str(m3rz),
            wspol_asym=str(wa),
            data_pom=str(records[0][7])

        )
        document.write('Raport.docx')

        t = time()
        a = 'Raport ' + ctime(t) + '.pdf'
        a = a.replace(":", "")
        path = "~\\Documents\\Raporty\\" + a
        full_path = os.path.expanduser(path)

        try:
            os.makedirs(full_path)
        except FileExistsError:
            pass

        convert("Raport.docx", full_path)
        os.remove("Raport.docx")
        messagebox.showinfo("SUKCES!","Raport wygenrowany i zapisany w folderze Dokumenty")

    measurements_frame = Frame(main_frame)
    measurements_frame.pack(fill=BOTH, expand=True)
    ipadding = {'ipadx': 100, 'ipady': 10}

    label4 = Label(measurements_frame)
    label4.pack(expand=True, fill=BOTH)
    head_frame = Frame(label4)
    head_frame.pack(fill=BOTH)
    groupe = read_file()
    # styl tabeli
    style = ttk.Style()
    style.theme_use('default')

    # zmiana kolorów
    style.configure('Treeview',
                    background='#d3d3d3',
                    foreground='black',
                    rowheight=25,
                    fiekdbackground='#d3d3d3')

    # zmiana koloru wybranego rekordu
    style.map('Treeview', background=[('selected', '#347083')])

    # tworzenie ramki dla tabeli
    tree_frame = Frame(head_frame)
    tree_frame.pack(pady=10)

    # tworzenie suwaka
    tree_scrol = Scrollbar(tree_frame)
    tree_scrol.pack(side=RIGHT, fill=Y)

    # tworzenie podglądu
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrol.set, selectmode='extended')
    my_tree.pack()

    # ustawienia suwaka
    tree_scrol.config(command=my_tree.yview)

    # kolumny
    my_tree['columns'] = ('ID', 'Pomiar 1', 'Pomiar 2', 'Pomiar 3', 'Jed.', 'Kategoria', 'Użytkownik')

    # format kolumn
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('ID', anchor=CENTER, width=50)
    my_tree.column('Pomiar 1', anchor=W, width=100)
    my_tree.column('Pomiar 2', anchor=W, width=100)
    my_tree.column('Pomiar 3', anchor=W, width=100)
    my_tree.column('Jed.', anchor=W, width=50)
    my_tree.column('Kategoria', anchor=W, width=100)
    my_tree.column('Użytkownik', anchor=W, width=100)

    # nagłówek tabeli
    my_tree.heading('#0', text='', anchor=W)
    my_tree.heading('ID', text='ID', anchor=CENTER)
    my_tree.heading('Pomiar 1', text='Pomiar 1', anchor=CENTER)
    my_tree.heading('Pomiar 2', text='Pomiar 2', anchor=CENTER)
    my_tree.heading('Pomiar 3', text='Pomiar 3', anchor=CENTER)
    my_tree.heading('Jed.', text='Jed.', anchor=CENTER)
    my_tree.heading('Kategoria', text='Kategoria', anchor=CENTER)
    my_tree.heading('Użytkownik', text='Użytkownik', anchor=CENTER)

    # dodaj dane

    my_tree.tag_configure('oddrow', background='white')
    my_tree.tag_configure('evenrow', background='lightblue')

    # dodawanie rekordów (ramka)
    data_frame = LabelFrame(head_frame, text='Operacje')
    data_frame.pack(fill='x', expand='yes', padx=20)
    data_frame.columnconfigure(0, weight=1)
    data_frame.columnconfigure(1, weight=5)

    # pole wprowadzania plus opis dla ID (i tak nie działa, ale cicho ;))
    id_label = Label(data_frame, text='ID')
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    # pole wprowadzania plus opis dla nazwy
    fn_label = Label(data_frame, text='Pomiar 1')
    fn_label.grid(row=1, column=0, padx=10, pady=10)
    fn_entry = Entry(data_frame)
    fn_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)

    # pole wprowadzania plus opis dla opisu
    ln_label = Label(data_frame, text='Pomiar 2')
    ln_label.grid(row=2, column=0, padx=10, pady=10)
    ln_entry = Entry(data_frame)
    ln_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)

    # pole wprowadzania plus opis dla opisu
    sn_label = Label(data_frame, text='Pomiar 3')
    sn_label.grid(row=3, column=0, padx=10, pady=10)
    sn_entry = Entry(data_frame)
    sn_entry.grid(row=3, column=1, padx=10, pady=10, sticky=EW)

    # pole wprowadzania plus opis dla opisu
    gn_label = Label(data_frame, text='Jednostka')
    gn_label.grid(row=4, column=0, padx=10, pady=10)
    gn_entry = Entry(data_frame)
    gn_entry.grid(row=4, column=1, padx=10, pady=10, sticky=W)

    # pole wprowadzania plus opis dla opisu
    hn_label = Label(data_frame, text='Kategoria')
    hn_label.grid(row=5, column=0, padx=10, pady=10)
    slist = cat_down()
    hn_entry = ttk.Combobox(data_frame, state="readonly", values=[row[1] for row in slist])
    hn_entry.set("Wybierz kategorię")
    hn_entry.grid(row=5, column=1, padx=10, pady=10, sticky=EW)

    # przyciski ramka
    button_frame = LabelFrame(head_frame, text='Operacje')
    button_frame.pack(fill='x', expand='yes', padx=20)

    # przycisk aktulizacji
    update_button = Button(button_frame, text='Aktualizuj', command=update_record)
    update_button.grid(row=0, column=1, padx=10, pady=10)
    if groupe[1] != 'administratorzy':
        update_button.config(state="disabled")

    # przycisk dodaj
    add_button = Button(button_frame, text='Dodaj nową serię pomiarów', command=add_data)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    # przycisk usun
    remove_button = Button(button_frame, text='Usuń pomiar', command=remove_record)
    remove_button.grid(row=0, column=2, padx=10, pady=10)
    if groupe[1] != 'administratorzy':
        remove_button.config(state="disabled")

    raport_button = Button(button_frame, text='Generuj Raport', command=obliczenia)
    raport_button.grid(row=0, column=3, padx=10, pady=10)

    my_tree.bind('<ButtonRelease-1>', selec_record)

    # łączenie z bazą danych - funkcja
    query_database()

def reports_page():

    def query_database():
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            print("Coś poszło nie tak")
        c = connection.cursor()

        c.execute('SELECT id_uzytkownika, nazwa, grupa, wlaczone FROM uzytkownicy')


        records = c.fetchall()

        # dodaj dane do tabeli i wyświetl
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3]),  tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1
        connection.commit()
        connection.close()

    def selec_record(e):
        # wyczyść okienka wprowadzania
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        id_entry.delete(0, END)

        # wybierz numer rekordu
        selected = my_tree.focus()
        # wybierz wartości
        values = my_tree.item(selected, 'values')

        # wprowadz do ramek wprowadzania
        fn_entry.insert(0, values[1])
        ln_entry.insert(0, values[2])
        id_entry.insert(0, values[0])

    def aktywacja_konta():
        selected = my_tree.focus()
        my_tree.item(selected, text='', values=(id_entry.get(), fn_entry.get(), ln_entry.get(),))

        # aktualizacja bazy danych
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            print("Coś poszło nie tak")
        c = connection.cursor()
        c.execute(
            'UPDATE uzytkownicy SET wlaczone="t" WHERE id_uzytkownika=%s', (
                id_entry.get(),
            ))
        messagebox.showinfo("Sukces!", "Konto zostało włączone!")
        connection.commit()
        connection.close()
        my_tree.delete(*my_tree.get_children())
        query_database()


    def deaktywacja_konta():
        selected = my_tree.focus()
        my_tree.item(selected, text='', values=(id_entry.get(), fn_entry.get(), ln_entry.get(),))

        # aktualizacja bazy danych
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        c.execute(
            'UPDATE uzytkownicy SET wlaczone="n" WHERE id_uzytkownika=%s', (
                id_entry.get(),
            ))
        messagebox.showinfo("Sukces!", "Konto zostało wyłączone!")
        connection.commit()
        connection.close()
        my_tree.delete(*my_tree.get_children())
        query_database()

    def zmiana_uprawnien():
        selected = my_tree.focus()
        my_tree.item(selected, text='', values=(id_entry.get(), fn_entry.get(), ln_entry.get(),))

        # aktualizacja bazy danych
        try:
            connection = pymysql.connect \
                (host="localhost",
                 user="root",
                 passwd="",
                 database="wyliczacv1")
            print("MySQL Database connection successful")
        except:
            messagebox.showerror("Błąd połączenia","Nie można połączyć z bazą danych. Spróbuj potem.")
        c = connection.cursor()
        grupa = read_file()
        if grupa[1]=='uzytkownicy':
            c.execute(
                'UPDATE uzytkownicy SET grupa="administratorzy" WHERE id_uzytkownika=%s', (
                    id_entry.get(),
                ))
            messagebox.showinfo("Sukces!", "Nadano uprawnienia administratora")
        else:
            c.execute(
                'UPDATE uzytkownicy SET grupa="uzytkownicy" WHERE id_uzytkownika=%s', (
                    id_entry.get(),
                ))
            messagebox.showinfo("Sukces!", "Zabrano uprawnienia administratora")
        connection.commit()
        c.execute('SELECT nazwa, grupa FROM uzytkownicy')

        records = c.fetchall()
        txtFile = open("myfile.txt", "w")
        txtFile.write(records[0][0] + '\n' + records[0][1])
        txtFile.close()
        grupa = read_file()
        connection.close()
        my_tree.delete(*my_tree.get_children())
        query_database()

    measurements_frame = Frame(main_frame)
    measurements_frame.pack(fill=BOTH, expand=True)
    ipadding = {'ipadx': 100, 'ipady': 10}

    label4 = Label(measurements_frame)
    label4.pack(expand=True, fill=BOTH)
    head_frame = Frame(label4)
    head_frame.pack(fill=BOTH)
    groupe = read_file()

    # styl tabeli
    style = ttk.Style()
    style.theme_use('default')

    # zmiana kolorów
    style.configure('Treeview',
                    background='#d3d3d3',
                    foreground='black',
                    rowheight=25,
                    fiekdbackground='#d3d3d3')

    # zmiana koloru wybranego rekordu
    style.map('Treeview', background=[('selected', '#347083')])

    # tworzenie ramki dla tabeli
    tree_frame = Frame(head_frame)
    tree_frame.pack(pady=10)

    # tworzenie suwaka
    tree_scrol = Scrollbar(tree_frame)
    tree_scrol.pack(side=RIGHT, fill=Y)

    # tworzenie podglądu
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrol.set, selectmode='extended')
    my_tree.pack()

    # ustawienia suwaka
    tree_scrol.config(command=my_tree.yview)

    # kolumny
    my_tree['columns'] = ('ID', 'Login', 'Grupa', 'Aktywne')

    # format kolumn
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('ID', anchor=CENTER, width=50)
    my_tree.column('Login', anchor=W, width=150)
    my_tree.column('Grupa', anchor=W, width=150)
    my_tree.column('Aktywne', anchor=W, width=150)

    # nagłówek tabeli
    my_tree.heading('#0', text='', anchor=W)
    my_tree.heading('ID', text='ID', anchor=CENTER)
    my_tree.heading('Login', text='Login', anchor=CENTER)
    my_tree.heading('Grupa', text='Grupa', anchor=CENTER)
    my_tree.heading('Aktywne', text='Aktywne', anchor=CENTER)

    # dodaj dane

    my_tree.tag_configure('oddrow', background='white')
    my_tree.tag_configure('evenrow', background='lightblue')

    # dodawanie rekordów (ramka)
    data_frame = LabelFrame(head_frame, text='Operacje')
    data_frame.pack(fill='x', expand='yes', padx=20)
    data_frame.columnconfigure(0, weight=1)
    data_frame.columnconfigure(1, weight=5)

    # pole wprowadzania plus opis dla ID (i tak nie działa, ale cicho ;))
    id_label = Label(data_frame, text='ID')
    id_entry = Entry(data_frame)

    # pole wprowadzania plus opis dla nazwy
    fn_label = Label(data_frame, text='Login')
    fn_entry = Entry(data_frame)

    # pole wprowadzania plus opis dla opisu
    ln_label = Label(data_frame,  text='Grupa')
    ln_entry = Entry(data_frame)

    # przyciski ramka
    button_frame = LabelFrame(head_frame, text='Operacje')
    button_frame.pack(fill='x', expand='yes', padx=20)

    # przycisk dodaj
    act_button = Button(button_frame, text='Aktywuj', command=aktywacja_konta)
    act_button.grid(row=0, column=0, padx=10, pady=10)

    # przycisk dodaj
    deac_button = Button(button_frame, text='Dezaktywuj', command=deaktywacja_konta)
    deac_button.grid(row=0, column=1, padx=10, pady=10)

    # nadaj uprawnienia administratora
    up_button = Button(button_frame, text='Zmień uprawnienia', command=zmiana_uprawnien)
    up_button.grid(row=0, column=2, padx=10, pady=10)

    my_tree.bind('<ButtonRelease-1>', selec_record)

    # łączenie z bazą danych - funkcja
    query_database()


def hide_indicators():
    groupe = read_file()
    home_indicate.config(bg='#c3c3c3')
    categories_indicate.config(bg='#c3c3c3')
    measurements_indicate.config(bg='#c3c3c3')
    reports_indicate.config(bg='#c3c3c3')

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def indicate(lb, page):
    hide_indicators()
    lb.config(bg='#158aff')
    delete_pages()
    page()


options_frame=Frame(root, bg='#f1f1f1')

home_btn=Button(options_frame, text='Główna', font=('Microsoft YaHei UI',15),fg='#158aff',bd=0,bg='#f1f1f1',command=lambda: indicate(home_indicate, home_page))
home_btn.place(x=10, y=50)
home_indicate=Label(options_frame,text='',bg='#c3c3c3')
home_indicate.place(x=3,y=50,width=5,height=40)

categories_btn=Button(options_frame, text='Kategorie', font=('Microsoft YaHei UI',15),fg='#158aff',bd=0,bg='#f1f1f1',command=lambda: indicate(categories_indicate, categories_page))
categories_btn.place(x=10, y=100)
categories_indicate=Label(options_frame,text='',bg='#c3c3c3')
categories_indicate.place(x=3,y=100,width=5,height=40)

measurements_btn=Button(options_frame, text='Pomiary', font=('Microsoft YaHei UI',15),fg='#158aff',bd=0,bg='#f1f1f1',command=lambda: indicate(measurements_indicate, measurements_page))
measurements_btn.place(x=10, y=150)
measurements_indicate=Label(options_frame,text='',bg='#c3c3c3')
measurements_indicate.place(x=3,y=150,width=5,height=40)

reports_btn=Button(options_frame, text='Użytkownicy', font=('Microsoft YaHei UI',15),fg='#158aff',bd=0,bg='#f1f1f1',command=lambda: indicate(reports_indicate,reports_page))
reports_btn.place(x=10, y=200)
if groupe[1] != 'administratorzy':
    reports_btn.config(state="disabled")
reports_indicate=Label(options_frame,text='',bg='#c3c3c3')
reports_indicate.place(x=3,y=200,width=5,height=40)

logout_btn=Button(options_frame, text='Wyloguj', font=('Microsoft YaHei UI',15),fg='red',bd=0,bg='#f1f1f1', command=wyloguj)
logout_btn.place(x=10, y=650)

options_frame.pack(side=LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=150,height=700)

main_frame = Frame(root, highlightbackground='#c3c3c5',highlightthickness=2,bg='white')
main_frame.pack(side=LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height=700,width=925)

indicate(home_indicate,home_page)
root.mainloop()