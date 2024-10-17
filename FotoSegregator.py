import os
import shutil
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import datetime
import random
import sys

# Funkcja do uzyskania ścieżki
def resource_path(relative_path):
    """Zwraca ścieżkę"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def extract_date_taken(path):
    try:
        image = Image.open(path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    date_str = value.split()[0].replace(':', '-')
                    return date_str
        modification_time = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Błąd podczas pobierania daty z {path}: {e}")
        return None

def organize_photos(source_folder, group_by, include_subfolders):
    if not source_folder or source_folder == "Nie wybrano folderu":
        messagebox.showwarning("Uwaga", "Uwaga! Przenoszę Twoje zdjęcia do kosza... nie wskazałeś folderu, który chcesz segregować :P")
        return

    files_to_process = []
    if include_subfolders:
        for root_dir, dirs, files in os.walk(source_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    files_to_process.append(os.path.join(root_dir, file))
    else:
        for file in os.listdir(source_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                files_to_process.append(os.path.join(source_folder, file))

    for file_path in files_to_process:
        date_taken = extract_date_taken(file_path)
        if date_taken:
            if group_by == "Dzień":
                target_folder = os.path.join(source_folder, date_taken)
            elif group_by == "Miesiąc":
                target_folder = os.path.join(source_folder, date_taken[:7])  
            elif group_by == "Rok":
                target_folder = os.path.join(source_folder, date_taken[:4])  
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            target_path = os.path.join(target_folder, os.path.basename(file_path))
            if not os.path.exists(target_path):
                try:
                    shutil.move(file_path, target_path)
                except Exception as e:
                    print(f"Błąd podczas przenoszenia pliku {file_path}: {e}")

    messagebox.showinfo("Sukces", f"Zdjęcia zostały posegregowane według kryterium: {group_by.lower()}!")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        
        folder_display = "..." + folder_selected[-23:] if len(folder_selected) > 23 else folder_selected
    else:
        folder_display = "Nie wybrano folderu"
    
    folder_label.config(text=folder_display)
    return folder_selected


# Funkcja do losowania ciekawostki
def losuj_ciekawostke():
    ciekawostki = [
    "Pierwsze zdjęcie: \nPierwsza fotografia na świecie została wykonana w 1826 roku przez Nicéphore'a Niépce'a i przedstawiała widok z okna jego domu. Czas naświetlania wynosił aż 8 godzin!",

        "Najstarsze selfie: \nNajstarsze znane selfie zostało zrobione w 1839 roku przez Roberta Corneliusa, amerykańskiego pioniera fotografii.",

        "Aparat z pudełka po butach: \nAparaty typu 'pinhole' można zbudować samodzielnie, wykorzystując zwykłe pudełko po butach i małą dziurkę jako obiektyw.",

        "Fotografia w kosmosie: \nPierwsze zdjęcie Ziemi z kosmosu zostało zrobione w 1946 roku przez rakietę V-2.",

        "Fotografia kolorowa: \nPierwsze zdjęcie kolorowe wykonał James Clerk Maxwell w 1861 roku, fotografując wstążkę w trzech podstawowych kolorach (czerwony, zielony, niebieski).",

        "Najczęściej fotografowane miejsce: \nWedług badań najczęściej fotografowanym miejscem na świecie jest wieża Eiffla w Paryżu.",

        "ISO w fotografii: \nStandard ISO, używany do mierzenia czułości na światło w fotografii, pochodzi od Międzynarodowej Organizacji Normalizacyjnej (ISO).",

        "Zdjęcia z powietrza: \nPierwsza fotografia lotnicza została wykonana w 1858 roku przez fotografa Gasparda-Félixa Tournachona (znanego jako Nadar) z balonu na gorące powietrze.",

        "Najdroższe zdjęcie: \nNajdrożej sprzedane zdjęcie to 'Rhein II' autorstwa Andreasa Gursky'ego, które zostało sprzedane w 2011 roku za 4,3 miliona dolarów.",

        "Kodak i aparat dla mas: \nFirma Kodak wprowadziła na rynek pierwszy aparat dla amatorów w 1888 roku, co zrewolucjonizowało dostępność fotografii dla mas.",

        "Fotografia rentgenowska: \nWilhelm Röntgen odkrył promienie rentgenowskie w 1895 roku, co umożliwiło wykonywanie zdjęć rentgenowskich.",

        "Polaroid: \nPierwszy aparat Polaroid, który wywoływał zdjęcia natychmiast, został wprowadzony na rynek w 1948 roku.",

        "Selfie z kosmosu: \nBuzz Aldrin zrobił pierwsze 'selfie' w kosmosie podczas misji Gemini 12 w 1966 roku.",

        "Fotografia pod wodą: \nPierwsze podwodne zdjęcie zostało zrobione w 1899 roku przez Louisa Boutana, pioniera fotografii podwodnej.",

        "Najwięcej zdjęć: \nSzacuje się, że każdego dnia na całym świecie robi się około 1,4 biliona zdjęć.",

        "Czarno-biała dominacja: \nKolorowa fotografia nie była popularna do lat 70. XX wieku. Wcześniej dominowała fotografia czarno-biała.",

        "Pierwsze zdjęcie Księżyca: \nPierwsze zdjęcie Księżyca zostało wykonane w 1840 roku przez amerykańskiego astronoma Johna W. Drapera.",

        "Migawka w telefonie: \nDźwięk migawki, który słyszysz podczas robienia zdjęć telefonem, to często sztuczny dźwięk, który dodano, aby naśladować dźwięk mechanicznej migawki.",

        "Pierwsze zdjęcie Ziemi z Księżyca: \nAstronauta William Anders wykonał pierwsze zdjęcie Ziemi z powierzchni Księżyca podczas misji Apollo 8 w 1968 roku.",

        "Dagerotypia: \nTechnika dagerotypii, wynaleziona w 1839 roku przez Louisa Daguerre'a, była jedną z pierwszych metod utrwalania obrazów na metalowych płytkach.",

        "Pierwszy aparat cyfrowy: \nPierwszy aparat cyfrowy został stworzony przez Steve'a Sassona, inżyniera Kodaka, w 1975 roku. Ważył około 4 kg i miał rozdzielczość 0,01 megapiksela.",

        "Fotografia w gazetach: \nPierwsze zdjęcie pojawiło się w gazecie w 1880 roku w 'Daily Graphic' w Nowym Jorku.",

        "Fotografia satelitarna: \nPierwsze zdjęcia satelitarne zostały wykonane w latach 60. XX wieku przez satelitę TIROS-1.",

        "Fotografia mobilna: \nPierwszy telefon z wbudowanym aparatem fotograficznym pojawił się w 2000 roku (Sharp J-SH04).",

        "Największe zdjęcie świata: \nW 2015 roku stworzono największą fotografię świata – panoramiczne zdjęcie Mont Blanc o rozdzielczości 365 gigapikseli.",

        "Pierwsze zdjęcie na Instagramie: \nPierwsze zdjęcie opublikowane na Instagramie zostało zrobione w 2010 roku przez współzałożyciela platformy, Kevina Systroma. Przedstawia psa i stopy.",

        "Pierwszy aparat lustrzany: \nPierwsza lustrzanka jednoobiektywowa (SLR) została zaprezentowana przez firmę Nikon w 1959 roku.",

        "Fotografia HDR: \nTechnika HDR (High Dynamic Range) pozwala na uchwycenie większej ilości detali w jasnych i ciemnych obszarach obrazu.",

        "Fotografia cyfrowa vs analogowa: \nAparaty cyfrowe wyparły tradycyjne aparaty na kliszę, a ostatnia rolka filmu Kodachrome została wyprodukowana w 2010 roku.",

        "Fotografia makro: \nFotografia makro pozwala uchwycić najmniejsze detale przedmiotów, które nie są widoczne gołym okiem, takich jak struktura liści czy oczu owadów.",

        "Światło jest kluczowe: \nW fotografii światło jest najważniejszym elementem – to ono decyduje o nastroju, kolorach i szczegółach obrazu.",

        "Fotografia nocna: \nDługie naświetlanie w fotografii nocnej pozwala uchwycić zjawiska niedostępne dla ludzkiego oka, takie jak smugi świetlne samochodów czy ruch gwiazd na niebie.",

        "Zdjęcia panoramiczne: \nTechnika fotografii panoramicznej istnieje od XIX wieku, ale dopiero aparaty cyfrowe zyskały popularność w tworzeniu łatwych i dokładnych zdjęć panoramicznych.",

        "Fotografia w modzie: \nFotografia mody ma swoje początki już w XIX wieku, ale dopiero magazyny takie jak Vogue i Harper's Bazaar zdefiniowały tę gałąź fotografii na początku XX wieku.",

        "Największe archiwum zdjęć: \nNajwiększe archiwum zdjęć na świecie to Getty Images, które posiada ponad 80 milionów zdjęć i ilustracji.",

        "Technika bokeh: \nBokeh to efekt wizualny, który powstaje, gdy tło na zdjęciu jest rozmyte, co podkreśla główny obiekt.",

        "Fotografia czarno-biała: \nCzarno-białe zdjęcia często uchodzą za bardziej artystyczne, ponieważ pozbawienie koloru pozwala skupić się na kompozycji, strukturze i emocjach.",

        "Fotografia lotnicza dronami: \nDrony zrewolucjonizowały fotografię, umożliwiając robienie zdjęć z unikalnych, wcześniej niedostępnych perspektyw.",

        "Zdjęcia duchów: \nW XIX wieku popularne były 'fotografie duchów', na których rzekomo pojawiały się zjawy, ale najczęściej były to efekty podwójnej ekspozycji.",

        "Fotografia uliczna: \nFotografia uliczna zyskała popularność w XX wieku dzięki takim artystom jak Henri Cartier-Bresson, którzy uchwycili codzienne życie w miastach."
        # ciekawostki
    ]
    ciekawostka = random.choice(ciekawostki)
    ciekawostka_podzielona = ciekawostka.split(": ")
    tytul = ciekawostka_podzielona[0]
    tresc = ciekawostka_podzielona[1]
    return f"{tytul}:\n{tresc}"

# Główne okno aplikacji
root = Tk()
root.title("FOTO SEGREGATOR by DebugDuck-quack")
root.geometry("497x535")  # wysokość
root.update_idletasks()  # Aktualizacja wymiarów okna
window_width = root.winfo_width()
window_height = root.winfo_height()

# Pobierz rozmiar ekranu
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Oblicz pozycję x, y aby wyśrodkować okno
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Ustawienie geometrii okna na wyśrodkowaną
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.resizable(False, False)

# Ścieżka do obrazka
img_path = resource_path("data/Foto.png")

# Wczytanie obrazu
try:
    img = Image.open(img_path)
    img = img.resize((120, 140), Image.Resampling.LANCZOS)  
    img_photo = ImageTk.PhotoImage(img)
    img_label = Label(root, image=img_photo, bg='#f0f0f0')
    img_label.grid(row=0, column=2, padx=10, pady=10)  
except Exception as e:
    print(f"Nie udało się wczytać obrazu: {e}")

# Nagłówek
title_label = Label(root, text="Organizator zdjęć według daty", font=("Helvetica", 18), bg='#f0f0f0')
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Ciekawostka
ciekawostka_label = Label(root, text=losuj_ciekawostke(), font=("Helvetica", 12), bg='#f0f0f0', wraplength=400, justify=LEFT, height=6, anchor=N)
ciekawostka_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Funkcja odświeżenia ciekawostki
def odswiez_ciekawostke(event):
    ciekawostka_label.config(text=losuj_ciekawostke())

ciekawostka_label.bind("<Button-1>", odswiez_ciekawostke)

# Komunikat informacyjny
info_label = Label(root, text="Prześlę Twoje zdjęcia do galerii sztuki, no chyba że nie wskażesz folderu!",
                   font=("Helvetica", 10, "italic"), fg='#333333', bg='#f0f0f0', wraplength=300, justify=LEFT)
info_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

# Przycisk do wyboru folderu
select_button = Button(root, text="Wybierz folder", command=select_folder, font=("Helvetica", 12), bg='#00aaff', fg='white')
select_button.grid(row=3, column=0, padx=10, pady=5, sticky=W)

# Etykieta wyświetlająca wybrany folder
folder_label = Label(root, text="Nie wybrano folderu", font=("Helvetica", 10), bg='#f0f0f0')
folder_label.grid(row=3, column=1, padx=10, pady=5, sticky=W)

# Opcje (dzień, miesiąc, rok) 
group_by_var = StringVar(value="Dzień")
day_radio = Radiobutton(root, text="Dzień", variable=group_by_var, value="Dzień", font=("Helvetica", 12), bg='#f0f0f0')
month_radio = Radiobutton(root, text="Miesiąc", variable=group_by_var, value="Miesiąc", font=("Helvetica", 12), bg='#f0f0f0')
year_radio = Radiobutton(root, text="Rok", variable=group_by_var, value="Rok", font=("Helvetica", 12), bg='#f0f0f0')

day_radio.grid(row=4, column=0, padx=5, pady=5, sticky=W)
month_radio.grid(row=4, column=1, padx=5, pady=5, sticky=W)
year_radio.grid(row=4, column=2, padx=5, pady=5, sticky=W)

# Checkbutton do uwzględniania podfolderów
include_subfolders_var = BooleanVar()
include_subfolders_checkbox = Checkbutton(root, text="Działaj w podfolderach", variable=include_subfolders_var, font=("Helvetica", 10), bg='#f0f0f0')
include_subfolders_checkbox.grid(row=5, column=0, padx=10, pady=10, sticky=W)

# Przycisk do rozpoczęcia organizowania zdjęć
organize_button = Button(root, text="Organizuj zdjęcia", command=lambda: organize_photos(folder_label.cget("text"), group_by_var.get(), include_subfolders_var.get()), font=("Helvetica", 12), bg='#00cc66', fg='white')
organize_button.grid(row=6, column=0, padx=10, pady=20, sticky=W)

# Przycisk wyjścia
exit_button = Button(root, text="Wyjdź", command=lambda: root.quit(), font=("Helvetica", 12), bg='#ff6666', fg='white')
exit_button.grid(row=6, column=2, padx=10, pady=20, sticky=E)

# Uruchomienie pętli głównej aplikacji
root.mainloop()
