#autor: Kacper Grzesik
import datetime
import re
import requests
import os

def usunPlik(do_usuniecia):
    potwierdzenie = "n"

    if do_usuniecia == "n n": return 0

    if not sprawdz_dostepnosc(do_usuniecia):
        potwierdzenie = input(f"\nCzy na pewno chcesz usunąć plik {do_usuniecia} [y] - Tak / [n] - Nie? ")
        if potwierdzenie == "y": 
            if os.path.exists(do_usuniecia + ".faktura"): 
                os.remove(do_usuniecia + ".faktura")
                input(f"\nFaktura [{do_usuniecia}] została usunięta. Naciśnij [Enter], aby kontynuować.\n")
            if os.path.exists(do_usuniecia + ".wplata"):
                os.remove(do_usuniecia + ".wplata")
                input(f"\nWpłata [{do_usuniecia}] została usunięta. Naciśnij [Enter], aby kontynuować.\n")
        else: return 0
    else: input("\nNie znaleziono pliku.\n\n")

def wyswietl(usun, pobierz):
    Lista_faktur = []
    Lista_wplat = []

    Import_dane = []

    for line in os.listdir():
        if line.endswith('.faktura'):
            Lista_faktur.append(line[:-8:])

    for line in os.listdir():
        if line.endswith('.wplata'):
            Lista_wplat.append(line[:-7:])

    if usun:
        do_usuniecia = input(f"\nWybierz plik do usunięcia (wpisz [n n], jeśli chcesz przerwać akcję.):\nFaktury: {Lista_faktur}\nPłatności: {Lista_wplat}\n")
        if do_usuniecia == "n n": return 0
        else: 
            usunPlik(do_usuniecia)
            return 0
        
    elif pobierz:
        wybrana = input(f"\nPobierz z listy faktur:\n{Lista_faktur}\nPobierz z listy płatności:\n{Lista_wplat}\n\n")

    else:
        wybrana = input(f"\nWybierz z listy faktur:\n{Lista_faktur}\n\nWybierz z listy płatności:\n{Lista_wplat}\n\n")

    if wybrana in Lista_faktur:
        nazwa_faktury = wybrana + ".faktura"
        file = open(nazwa_faktury, 'r')
        
        for line in file:
            line = line.strip()
            Import_dane.append(line)

        if pobierz:
            kwota = Import_dane[0]
            waluta = Import_dane[1]
            data = Import_dane[2]

            wartosc = przewalutowanie(kwota, waluta, data)

            print(f"Pomyślnie pobrano fakturę {nazwa_faktury}.\n")

            return [wartosc, 1]

        print(f"\nNazwa faktury: {nazwa_faktury}\nWartość: {Import_dane[0]}\nWaluta: {Import_dane[1]}\nData: {Import_dane[2]}\n")
    
    elif wybrana in Lista_wplat:
        nazwa_wplaty = wybrana + ".wplata"
        file = open(nazwa_wplaty, 'r')

        for line in file:
            line = line.strip()
            Import_dane.append(line)

        if pobierz:
            kwota = Import_dane[0]
            waluta = Import_dane[1]
            data = Import_dane[2]

            wartosc = przewalutowanie(kwota, waluta, data)

            print(f"Pomyślnie pobrano fakturę {nazwa_wplaty}.\n")

            return [wartosc, 0]

        print(f"\nNazwa płatności: {nazwa_wplaty}\nWartość: {Import_dane[0]}\nWaluta: {Import_dane[1]}\nData: {Import_dane[2]}\n")

    else:
        print("\nNie znaleziono pliku.\n")

    input("Naciśnij [Enter], aby kontynuować.\n")


def dane(czyFaktura):
    czy_zapisac = False

    if czyFaktura:
        print("\nWpisz dane faktury\n")
    else:
        print("\nWpisz dane płatności\n")
    
    while True:
        kwota = input("Podaj kwote: ")
        kwota = re.sub("\,", ".", kwota) #zamiana ewentualnego przecinka na kropke

        if kwota_walidacja(kwota): break

    while True:
        waluta = input("Podaj walute [PLN/EUR/USD/GBP]: ")
        waluta = waluta.upper() #przyjmowana jest dowolna wielkosc znakow

        if waluta_walidacja(waluta): break
    
    while True:
        data = input("Wprowadz date [rrrr-mm-dd]: ")

        if data_walidacja(data):
            print("\nPomyślnie wprowadzono dane faktury.\n")
            break

    if czyFaktura:
        while True:
            czy_zapisac = input("Czy chcesz zapisać dane faktury?\n[y] - Tak\n[n] - Nie\n")

            if czy_zapisac.lower() == "y":
                zapis_faktury(kwota, waluta, data, True)
                break

            if czy_zapisac.lower() == "n":
                break

            else: print("\nNie rozpoznano znaku.\n")
    
    else:
        while True:
            czy_zapisac = input("Czy chcesz zapisać dane płatności?\n[y] - Tak\n[n] - Nie\n")

            if czy_zapisac.lower() == "y":
                zapis_faktury(kwota, waluta, data, False)
                break

            if czy_zapisac.lower() == "n":
                break

            else: print("\nNie rozpoznano znaku.\n")

    if waluta != "PLN":
        kwotaPrzed = kwota
        kwota = przewalutowanie(kwota, waluta, data)
        print(f"\nPrzekonwertowano {kwotaPrzed} {waluta} na {kwota} PLN.\n")

    return kwota

def sprawdz_dostepnosc(nazwa):
    for line in os.listdir():
        if str(nazwa).lower() + ".faktura" == line.lower() or str(nazwa).lower() + ".wplata" == line.lower():
            return False
    return True

def zapis_faktury(fKwota, fWaluta, fData, czyFaktura):
    if czyFaktura:
        while True:
            nazwa = input("Wybierz nazwę: ")
            if sprawdz_dostepnosc(nazwa):
                nazwa = nazwa + ".faktura"
                
                if " " in nazwa:
                    print("\nTwoja nazwa nie może zawierać spacji.\n")
                else:
                    f = open(nazwa, "x")
                    f.write(f"{fKwota}\n{fWaluta}\n{fData}")
                    print(f"\nZapisano fakturę pod nazwą: {nazwa}")
                    f.close()
                    return 0
            else: print("\nNazwa niedostępna!\n")
    else:
        while True:
            nazwa = input("Wybierz nazwę: ")
            if sprawdz_dostepnosc(nazwa):
                nazwa = nazwa + ".wplata"
                
                if " " in nazwa:
                    print("\nTwoja nazwa nie może zawierać spacji.\n")
                else:
                    f = open(nazwa, "x")
                    f.write(f"{fKwota}\n{fWaluta}\n{fData}")
                    print(f"\nZapisano płatność pod nazwą: {nazwa}")
                    f.close()
                    return 0
            else: print("\nNazwa niedostępna!\n")

def przewalutowanie(kwota, waluta, data):
    #automatyczne przewalutowanie z pomocą API NBP  /   nie działa, kiedy wybrano dzień, w którym NBP nie zaktualizował dat
    url = 'http://api.nbp.pl/api/exchangerates/tables/A/' + data

    body = requests.get(url)
    response = body.json()

    for rate in response[0]['rates']:
        if waluta == rate['code']:
            wynik = float(kwota) * float(rate['mid'])
            wynik = round(wynik, 2)
            return wynik

def kwota_walidacja(kwota):
    try:
        float(kwota)    

    except ValueError:
        print("Niepoprawny format kwoty. Wprowadź liczbę.")
        return 0
    return 1

def waluta_walidacja(waluta):
    dozwolone = ['PLN', 'USD', 'EUR', 'GBP']

    if waluta in dozwolone: return 1
    else:
        print("Nieobsługiwana waluta.")
        return 0

def data_walidacja(data):
    try:
        datetime.date.fromisoformat(data)
        return 1
    
    except ValueError:
        print("Niepoprawny format daty.")
        return 0

def main():
    suma_faktura = 0
    suma_platnosci = 0

    while True:
        tryb = input("Wybierz działanie:\n[1] - Dodaj/wpisz fakturę ręcznie\n[2] - Pobierz fakturę z pliku\n[3] - Dodaj/wpisz płatność ręcznie\n[4] - Pobierz płatność z pliku\n[5] - Usuwanie załadowanych płatności/faktur\n[6] - Wyświetl pliki\n[7] - Usuwanie plików\n[8] - Zobacz ile zostało do opłacenia\n[0] - Wyjdź\n")

        if int(tryb) in range(9):
            if tryb == "1": #dodawanie i wpisywanie faktury
                suma = dane(1)
            
            if tryb == "2": #pobieranie faktury z pliku
                pobrany = wyswietl(0, 1)
                
                if pobrany[1]:
                    suma_faktura = pobrany[0]
                else:
                    suma_platnosci += pobrany[0]

            if tryb == "3": #dodawanie i wpisywanie platnosci
                platnosc = dane(0)

            if tryb == "4": #pobieranie platnosci z pliku
                print("4")

            if tryb == "5": #usuniecie załadowanej platnosci lub faktury
                print("5")

            if tryb == "6": #wyswietlenie plikow
                wyswietl(0, 0)

            if tryb == "7": #usuwanie plików
                wyswietl(1, 0)

            if tryb == "8": #sprawdzenie ile zostalo do oplacenia
                print("8")

            if tryb == "0": #wyjscie z programu
                tekst = "Program autorstwa: Kacper Grzesik"

                print("-" * len(tekst))
                print(tekst)
                print("-" * len(tekst))
                return 0
        
        else: print("\nNie ropoznano znaku.\n")

if __name__ == "__main__":
    main()