import sqlite3
from datetime import date
from datetime import timedelta
import config
import tkinter as tk
from PIL import Image, ImageTk    #Use "pip install Pillow" in the terminal to install PIL Library
config.events = []

class evenement:
    def __init__(self, titre, types, genre, duree, date, heure, employee):
        self.titre = titre
        self.genre = genre
        self.types = types
        self.duree = duree
        self.date = date
        self.heure = heure
        self.employee = employee 

def creer_bd():
    conn = sqlite3.connect('evenement.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS EVENEMENT")

    #Creation table evenement
    sql ='''CREATE TABLE evenement(
        titre CHAR(20) NOT NULL,
        genre CHAR(20),
        types CHAR(20),
        duree INT,
        date TEXT,
        heure TEXT,
        employee CHAR(20)

    )'''

    c.execute(sql)

    print("Table created successfully........")
    conn.commit()
    conn.close()

def update_event(event):
    conn = sqlite3.connect('evenement.db')
    c = conn.cursor()
    c.execute("""
       UPDATE evenement
       SET titre=(?), types=(?), genre=(?), duree=(?), date=(?), heure=(?), employee=(?)
       WHERE titre=(?)
        """, (event.titre, event.genre,event.types, event.duree, event.date, event.heure, event.employee, event.titre,))
    conn.commit()
    conn.close()

def insert_event(event):
    conn = sqlite3.connect('evenement.db')
    c = conn.cursor()
    print("Connexion réussie à SQLite")
    sql = "INSERT INTO evenement (titre, genre, types, duree, date, heure, employee) VALUES (?, ?, ?, ?, ?, ?,?)"
    value = (event.titre, event.genre,event.types, event.duree, event.date, event.heure, event.employee)
    c.execute(sql, value)
    conn.commit()
    print("Evenement inséré avec succès dans la table evenement")
    c.close()
    conn.close()
    print("Connexion SQLite est fermée")

def delete_event(titre):
    conn = sqlite3.connect('evenement.db')
    c = conn.cursor()
    print("Connexion réussie à SQLite")
    sql = "DELETE FROM evenement WHERE titre = ?"
  
    id = (titre)
    c.execute(sql, (id, ))
    conn.commit()
    print("Evenement supprimé avec succès")
  
    c.close()
    conn.close()
    print("Connexion SQLite est fermée")


def search_event(date1,date2):
    conn = sqlite3.connect('evenement.db')
    c = conn.cursor()
    print("Connexion réussie à SQLite")
    if date1 == 9:
        c.execute("SELECT * FROM evenement")
    else:
        
        c.execute("SELECT * FROM evenement WHERE date BETWEEN '{}' AND '{}' ".format(date1,date2))
    config.events = c.fetchall()
    print("Evenement affiché avec succès")
    c.close()
    conn.close()
    print("Connexion SQLite est fermée")


def select_period(indice):
    today = date.today()
    if indice == 1 : 
        day1 = today - timedelta(days=3)
        day2 = today.strftime("%Y-%m-%d")
        day1 = day1.strftime("%Y-%m-%d")
        #trois derniers jours

    elif indice == 2 : 
        day2 = today + timedelta(days=6)
        day1 = today.strftime("%Y-%m-%d")
        day2 = day2.strftime("%Y-%m-%d")
        #la semaine en cours

    elif indice == 3 : 
        day1 = today + timedelta(days=7)
        day2 = today + timedelta(days=14)
        day1 = day1.strftime("%Y-%m-%d")
        day2 = day2.strftime("%Y-%m-%d")
        #la semaine prochaine
    elif indice == 4 : 
        day1 = today
        day2 = today + timedelta(days=30)
        day1 = day1.strftime("%Y-%m-%d")
        day2 = day2.strftime("%Y-%m-%d")
        #le mois prochain
    elif indice == 5 : 
        return (9,9)
        #pall
    return (day1,day2)


def delete_page(current_page):
    for i in current_page:
        i.grid_forget()
    button_retour.grid_forget()
    button_Acceuil.grid_forget()
    
    

def show_previous_page():
    if config.previous_page == Modes: 
        page_Mode()
    elif config.previous_page == choix_p:
        page_choix()
    elif config.previous_page == eventsp:
        page_events()
    elif config.previous_page == supp:
        page_modify()

def select_events(indice):
    period=select_period(indice)
    date1 = period[0]
    date2 = period[1]
    search_event(date1,date2)
    page_events()

def add_db():

    titre=titre_var.get()
    genre=genre_var.get()
    type=type_var.get()
    duree=duree_var.get()
    date=str(date_var.get())
    print(date)
    heure=heure_var.get()
    employe=employe_var.get()

    event = evenement(titre,genre,type,duree,date,heure,employe)
    insert_event(event) 

def modifier_event():
    config.titre = listevents.get(listevents.curselection())[0]
    page_update()

def supprimer_event():
    titre = listevents.get(listevents.curselection())
    index = listevents.curselection()
    listevents.delete(index)
    delete_event(titre[0])


def miseajour_event():
    titre = config.titre 
    genre=genre_var.get()
    type=type_var.get()
    duree=duree_var.get()
    date=date_var.get()
    heure=heure_var.get()
    employe=employe_var.get()

    event = evenement(titre,genre,type,duree,date,heure,employe)
    update_event(event)

def page_Acceuil():
    delete_page(config.current_page)

    label_title1.grid(columnspan=16,column=2,row=1)
    label_subtitle1.grid(columnspan=10,column=5,row=2)
    button_outil.grid(columnspan=9,column=1,row=10)
    button_planning.grid(columnspan=7,column=11,row=10)

    config.current_page = Acceuil

def page_Mode():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)

    label_title2.grid(columnspan=17,column=2,row=1)
    label_subtitle2.grid(columnspan=10,column=6,row=2)
    button_Consultation.grid(columnspan=10,column=6,rowspan=2,row=6)
    button_Modification.grid(columnspan=13,column=5,rowspan=2,row=8)
    button_ajout.grid(columnspan=10,column=6,rowspan=2,row=10)
    config.current_page = Modes

def page_Planning():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)

    text_planning.grid(columnspan=15, column=3, row=0)

    config.current_page = Planning

def page_choix():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)
    button_retour.grid(column=19,row=16)

    label_title3.grid(columnspan=10,column=7,row=1)
    button_consultation_3j.grid(columnspan=9,column=8,row=4)
    button_consultation_sem_en_cours.grid(columnspan=9,column=8,row=5)
    button_consultation_sem_a_venir.grid(columnspan=9,column=8,row=6)
    button_consultation_mois_a_venir.grid(columnspan=9,column=8,row=7)
    button_consultation_all_event.grid(columnspan=9,column=8,row=8)

    config.previous_page = config.current_page
    config.current_page = choix_p

def page_events():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)
    button_retour.grid(column=19,row=16)

    label_title4.grid(column=2,row=1)
    listevent.delete(0, tk.END)
    listevent.insert(0,*config.events)
    listevent.grid(columnspan=17,column=1,row=3)
    config.previous_page = config.current_page
    config.current_page = eventsp

def page_add():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)
    button_retour.grid(column=19,row=16)

    choix_ajouter.grid(columnspan=16,column=0,row=0)
    Label1.grid(column=0, row=2, sticky='w')
    Champ.grid(column=1, row=2, sticky='w', columnspan=2, padx=10)
    Label2.grid(column=0, row=3, sticky='w')
    Champ2.grid(column=1, row=3, sticky='w', columnspan=2, padx=10)
    Label3.grid(column=0, row=4, sticky='w')
    Champ3.grid(column=1, row=4, sticky='w', columnspan=2, padx=10)
    Label4.grid(column=0, row=5, sticky='w')
    Champ4.grid(column=1, row=5, sticky='w', columnspan=2, padx=10)
    Label5.grid(column=0, row=6, sticky='w')
    Champ5.grid(column=1, row=6, sticky='w', columnspan=2, padx=10)
    Label6.grid(column=0, row=7, sticky='w')
    Champ6.grid(column=1, row=7, sticky='w', columnspan=2, padx=10)
    Label7.grid(column=0, row=8, sticky='w')
    Champ7.grid(column=1, row=8, sticky='w', columnspan=2, padx=10)
    Label8.grid(column=4, row=6, sticky='w')
    Label9.grid(column=4, row=7, sticky='w')
    button_valider.grid(column=1,row=9)

    config.previous_page = config.current_page
    config.current_page = add

def page_update():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)
    button_retour.grid(column=19,row=16)
    Label10 = tk.Label(root, text = '{}'.format(config.titre))

    choix_ajouter.grid(columnspan=16,column=0,row=0)
    Label1.grid(column=0, row=2, sticky='w')
    Label10.grid(column=1, row=2, sticky='w', columnspan=2, padx=10)
    Label2.grid(column=0, row=3, sticky='w')
    Champ2.grid(column=1, row=3, sticky='w', columnspan=2, padx=10)
    Label3.grid(column=0, row=4, sticky='w')
    Champ3.grid(column=1, row=4, sticky='w', columnspan=2, padx=10)
    Label4.grid(column=0, row=5, sticky='w')
    Champ4.grid(column=1, row=5, sticky='w', columnspan=2, padx=10)
    Label5.grid(column=0, row=6, sticky='w')
    Champ5.grid(column=1, row=6, sticky='w', columnspan=2, padx=10)
    Label6.grid(column=0, row=7, sticky='w')
    Champ6.grid(column=1, row=7, sticky='w', columnspan=2, padx=10)
    Label7.grid(column=0, row=8, sticky='w')
    Champ7.grid(column=1, row=8, sticky='w', columnspan=2, padx=10)
    Label8.grid(column=4, row=6, sticky='w')
    Label9.grid(column=4, row=7, sticky='w')
    button_update.grid(column=1,row=9)

    config.previous_page = config.current_page
    update.append(Label10)
    config.current_page = update

def page_modify():
    delete_page(config.current_page)
    button_Acceuil.grid(column=20,row=16)
    button_retour.grid(column=19,row=16)

    period=select_period(5)
    day1 = period[0]
    day2 = period[1]
    search_event(day1,day2)
    listevents.delete(0, tk.END)
    listevents.insert(0,*config.events)

    choix_modification1.grid(columnspan=16,column=0,row=0)
    button_modifier.grid(column=20,rowspan=1,row=1)
    button_supprimer.grid(column=20,rowspan=1,row=2)
    listevents.grid(columnspan=17,column=0,row=3)
    config.previous_page = config.current_page
    config.current_page = supp



root = tk.Tk()
root.title("Gestion de CinemaClub")
canvas = tk.Canvas(root, width=1000, height=600)
canvas.grid(columnspan=20, rowspan=16) 
path="images.jpg"
load = Image.open(path)
photo = ImageTk.PhotoImage(load)
label = tk.Label(root, image=photo)
label.image = photo
label.place(x=0, y=0) 

button_retour = tk.Button(root, text="Retour", font=('Arial',20), bg='white', fg='black', command=lambda: show_previous_page())
button_Acceuil = tk.Button(root, text="Acceuil", font=('Arial',20), bg='white', fg='black', command=lambda: page_Acceuil())
#Page Acceuil
label_title1 = tk.Label(root, text="Gestion de CinemaClub", font=("Arial", 40), fg='black')
label_subtitle1 = tk.Label(root, text='Choisissez le mode de gestion ?', font=('Arial',25), fg='black')
button_outil = tk.Button(root, text="Gestion des évènements", font=('Arial',25), bg='white', fg='black', command =lambda: page_Mode())
button_planning = tk.Button(root, text="Gestion de planning", font=('Arial',25), bg='white', fg='black', command =lambda: page_Planning())
Acceuil = [label_title1,label_subtitle1,button_outil,button_planning]
#Page de gestion de planning
text_planning = tk.Label(root, text="Sevice en cours de développement..", font="Arial", fg='black')
Planning = [text_planning]
#Page choix de mode de gestion de l'outil
label_title2 = tk.Label(root, text="Vous avez choisi la gestion des évènements", font=("Arial", 30), fg='black')
label_subtitle2 = tk.Label(root, text='Que voulez vous faire ?', font=('Arial',25), fg='black')
button_Consultation = tk.Button(root, text="Consultation du programme", font=('Arial',25), bg='white', fg='black', command= lambda: page_choix())
button_Modification = tk.Button(root, text="Modification/suppression du programme", font=('Arial',25), bg='white', fg='black',command= lambda: page_modify())
button_ajout = tk.Button(root, text="Ajout au programme", font=('Arial',25), bg='white', fg='black', command= lambda: page_add())
Modes = [label_title2,label_subtitle2,button_Consultation,button_Modification,button_ajout]
#Page de choix de période
label_title3=tk.Label(root, text='Sur quelle période ?', font=('Arial',25), fg='black')
button_consultation_3j= tk.Button(root, text="Trois derniers jours", font=('Arial',25), bg='white', fg='black',command= lambda: select_events(1))
button_consultation_sem_en_cours= tk.Button(root, text="Semaine en cours", font=('Arial',25), bg='white', fg='black',command= lambda: select_events(2))
button_consultation_sem_a_venir= tk.Button(root, text="Semaine à venir", font=('Arial',25), bg='white', fg='black',command= lambda: select_events(3))
button_consultation_mois_a_venir= tk.Button(root, text="Mois à venir", font=('Arial',25), bg='white', fg='black',command= lambda: select_events(4))
button_consultation_all_event= tk.Button(root, text="Tous les évènements", font=('Arial',25), bg='white', fg='black',command= lambda: select_events(5))
choix_p = [label_title3,button_consultation_3j,button_consultation_sem_en_cours,button_consultation_sem_a_venir,button_consultation_mois_a_venir,button_consultation_all_event]
#Page de consultaion des évènements
label_title4 = tk.Label(root, text='Voici les évènements programés pour la période sélectionnée', font=('Arial',25), fg='black')
listevent = tk.Listbox(root,height=20,width=100,font=('Arial',14))
eventsp = [label_title4,listevent]
#Page d'ajout évènement
titre_var=tk.StringVar()
genre_var=tk.StringVar()
type_var=tk.StringVar()
duree_var=tk.StringVar()
date_var=tk.StringVar()
heure_var=tk.StringVar()
employe_var=tk.StringVar()
choix_ajouter=tk.Label(root, text="Ajouter un événement", font=("Arial", 40), fg='black')
Label1 = tk.Label(root, text = 'Titre : ')
Label2 = tk.Label(root, text = 'Genre : ')
Label3 = tk.Label(root, text = 'Type : ')
Label4 = tk.Label(root, text = 'Durée : ')
Label5 = tk.Label(root, text = 'Date : ')
Label6 = tk.Label(root, text = 'Heure : ')
Label7 = tk.Label(root, text = 'Employé : ')
Label8 = tk.Label(root, text = 'Format de date aaaa-mm-jj')
Label9 = tk.Label(root, text = 'Format heure hh:mm')
Champ = tk.Entry(root, width=31, textvariable=titre_var, font=('calibre',10,'normal'))
Champ.focus_set()
Champ2 = tk.Entry(root, width=31,textvariable=genre_var, font=('calibre',10,'normal'))
Champ2.focus_set()
Champ3 = tk.Entry(root, width=31,textvariable=type_var, font=('calibre',10,'normal'))
Champ3.focus_set()
Champ4 = tk.Entry(root, width=31,textvariable=duree_var, font=('calibre',10,'normal'))
Champ4.focus_set()
Champ5 = tk.Entry(root, width=31,textvariable=date_var, font=('calibre',10,'normal'))
Champ5.focus_set()
Champ6 = tk.Entry(root, width=31,textvariable=heure_var, font=('calibre',10,'normal'))
Champ6.focus_set()
Champ7 = tk.Entry(root, width=31,textvariable=employe_var, font=('calibre',10,'normal'))
Champ7.focus_set()
button_valider=tk.Button(root, text="Ajouter", font=('Arial',25), bg='white', fg='black',command =lambda: add_db())
add=[choix_ajouter,Label1,Champ,Label2,Champ2,Label3,Champ3,Label4,Champ4,Label5,Champ5,Label6,Champ6,Label7,Label8,Label9,Champ7,button_valider]
#Page de suppression
choix_modification1 = tk.Label(root, text="veuillez choisir l'événement que vous voulez modifier ou supprimer", font=("Arial",25), fg='black')
button_modifier = tk.Button(root, text="Modifier", font=('Arial',25), bg='white', fg='black', command =lambda: modifier_event())
button_supprimer = tk.Button(root, text="Supprimer", font=('Arial',25), bg='white', fg='black',command =lambda: supprimer_event())
listevents = tk.Listbox(root,height=20,width=100,font=('Arial',14))
supp = [listevents,choix_modification1,button_modifier,button_supprimer]
#Page update
button_update=tk.Button(root, text="Mise a jour", font=('Arial',25), bg='white', fg='black',command = lambda: miseajour_event())
update=[choix_ajouter,Label1,Label2,Champ2,Label3,Champ3,Label4,Champ4,Label5,Champ5,Label6,Champ6,Label7,Label8,Label9,Champ7,button_update]

config.current_page = Acceuil 
page_Acceuil()

root.mainloop()