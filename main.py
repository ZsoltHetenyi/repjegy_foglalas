from abc import ABC, abstractmethod
from datetime import datetime
import random


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar, max_helyek):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.max_helyek = max_helyek
        self.foglalt_helyek = 0  # Foglalt helyek száma

    def van_szabad_hely(self):
        return self.foglalt_helyek < self.max_helyek

    def foglal_hely(self):
        if self.van_szabad_hely():
            self.foglalt_helyek += 1
            return True
        return False

    @abstractmethod
    def tipus(self):
        pass


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, legitarsasag):
        if legitarsasag.ara_kategoria == 'olcso':
            jegyar = random.choice([2500, 5000])
        else:
            jegyar = random.choice([7000, 10000])
        max_helyek = 50  # Belföldi járatokon 50 hely van
        super().__init__(jaratszam, celallomas, jegyar, max_helyek)

    def tipus(self):
        return "Belföldi"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, legitarsasag):
        if legitarsasag.ara_kategoria == 'olcso':
            jegyar = random.choice([20000, 30000, 40000])
        else:
            jegyar = random.choice([50000, 60000, 70000])
        max_helyek = 200  # Nemzetközi járatokon 200 hely van
        super().__init__(jaratszam, celallomas, jegyar, max_helyek)

    def tipus(self):
        return "Nemzetközi"


class Legitarsasag:
    def __init__(self, nev, ara_kategoria):
        self.nev = nev
        self.ara_kategoria = ara_kategoria  # 'olcso' vagy 'dragabb'
        self.jaratok = []

    def add_jarat(self, jarat):
        self.jaratok.append(jarat)

    def get_jaratok(self):
        return self.jaratok


class JegyFoglalas:
    def __init__(self, jarat, utas_neve, datum):
        self.jarat = jarat
        self.utas_neve = utas_neve
        self.datum = datum


def jegy_foglalas(jarat, utas_neve, datum):
    if jarat.foglal_hely():
        return JegyFoglalas(jarat, utas_neve, datum), jarat.jegyar
    else:
        return None, "A járat már teljes!"


def lemondas(foglalasok, utas_neve):
    for foglalas in foglalasok:
        if foglalas.utas_neve == utas_neve:
            foglalas.jarat.foglalt_helyek -= 1  # Hely felszabadítása
            foglalasok.remove(foglalas)
            return f"Foglalás lemondva: {utas_neve}"
    return "Nincs ilyen foglalás."


def listazas(foglalasok):
    for foglalas in foglalasok:
        print(f"Utas: {foglalas.utas_neve}, Járatszám: "
              f"{foglalas.jarat.jaratszam}, Célállomás: "
              f"{foglalas.jarat.celallomas}, Ár: {foglalas.jarat.jegyar} Ft, "
              f"Dátum: {foglalas.datum}")


def main():
    legitarsasagok = [
        Legitarsasag("Ryanair", "olcso"),
        Legitarsasag("Wizzair", "olcso"),
        Legitarsasag("EasyJet", "olcso"),
        Legitarsasag("American Airlines", "dragabb"),
        Legitarsasag("British Airways", "dragabb"),
        Legitarsasag("AirFrance", "dragabb"),
        Legitarsasag("Qatar Airways", "dragabb")
    ]

    # Belföldi városok
    belfoldi_varosok = [
        "Budapest", "Debrecen", "Szeged", "Pécs", "Miskolc",
        "Győr", "Kecskemét", "Nyíregyháza", "Székesfehérvár",
        "Veszprém", "Sopron", "Zalaegerszeg", "Tatabánya",
        "Érd", "Békéscsaba", "Kaposvár", "Kiskunfélegyháza",
        "Eger", "Salgótarján", "Dunaújváros"
    ]

    # Nemzetközi városok
    nemzetkozi_varosok = [
        "London", "New York", "Párizs", "Berlin", "Tokió",
        "Róma", "Madrid", "Brüsszel", "Amszterdam", "Sydney",
        "Toronto", "Los Angeles", "Milánó", "Dubaj", "Prága",
        "Bécs", "Stockholm", "Oslo", "Koppenhága", "Dublin",
        "Zágráb", "Sofia", "Belgrád", "Athén", "Helsinki",
        "Tallinn", "Vilnius", "Riga", "Zürich", "Genf",
        "Bordeaux", "Lille", "Marseille", "Nice", "Malaga",
        "Valencia", "Sevilla", "Bilbao", "San Sebastián",
        "Bratislava", "Ljubljana", "București"
    ]

    # Járatok hozzáadása légitársaságokhoz
    jarat_szamlalo = 1
    for legitarsasag in legitarsasagok:
        # Belföldi járatok
        for _ in range(3):
            if belfoldi_varosok:
                celallomas = belfoldi_varosok.pop(0)
                jaratszam = f"{legitarsasag.nev[:2].upper()}{jarat_szamlalo:03d}"
                legitarsasag.add_jarat(
                    BelfoldiJarat(jaratszam, celallomas, legitarsasag))
                jarat_szamlalo += 1

        # Nemzetközi járatok
        for _ in range(5):
            if nemzetkozi_varosok:
                celallomas = nemzetkozi_varosok.pop(0)
                jaratszam = f"{legitarsasag.nev[:2].upper()}{jarat_szamlalo:03d}"
                legitarsasag.add_jarat(
                    NemzetkoziJarat(jaratszam, celallomas, legitarsasag))
                jarat_szamlalo += 1

    foglalasok = []

    while True:
        print("\n1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válassz egy lehetőséget: ")

        if valasztas == '1':
            nev = input("Add meg a neved: ")

            print("Válassz légitársaságot:")
            for index, legitarsasag in enumerate(legitarsasagok):
                kategoria = 'Olcsó' if legitarsasag.ara_kategoria == 'olcso' \
                    else 'Drágább'
                print(f"{index + 1}. {legitarsasag.nev} - {kategoria}")

            try:
                legitarsasag_index = int(
                    input("Add meg a légitársaság számát: ")) - 1
                legitarsasag = legitarsasagok[legitarsasag_index]
            except (IndexError, ValueError):
                print("Érvénytelen választás!")
                continue

            print("Válassz járatot:")
            for index, jarat in enumerate(legitarsasag.get_jaratok()):
                szabad_helyek = jarat.max_helyek - jarat.foglalt_helyek
                print(f"{index + 1}. {jarat.celallomas} ({jarat.jaratszam}) - "
                      f"Ár: {jarat.jegyar} Ft - Szabad helyek: {szabad_helyek}")

            try:
                jarat_index = int(
                    input("Add meg a járat számát: ")) - 1
                jarat = legitarsasag.get_jaratok()[jarat_index]
            except (IndexError, ValueError):
                print("Érvénytelen választás!")
                continue

            datum = input("Add meg a dátumot (YYYY-MM-DD): ")
            try:
                datetime.strptime(datum, "%Y-%m-%d")
                foglalas, ar = jegy_foglalas(jarat, nev, datum)
                if foglalas:
                    foglalasok.append(foglalas)
                    print(f"Foglalás sikeres! Ár: {ar} Ft")
                else:
                    print(ar)
            except ValueError:
                print("Érvénytelen dátum! Próbáld újra.")

        elif valasztas == '2':
            nev = input("Add meg a neved: ")
            print(lemondas(foglalasok, nev))

        elif valasztas == '3':
            listazas(foglalasok)

        elif valasztas == '4':
            break
        else:
            print("Érvénytelen választás!")


if __name__ == "__main__":
    main()
