from abc import ABC, abstractmethod
from datetime import datetime


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    @abstractmethod
    def tipus(self):
        pass


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas):
        # Ár véletlenszerűen: 2500 Ft (negyed ár) vagy 5000 Ft (fél ár)
        import random
        jegyar = random.choice([2500, 5000])
        super().__init__(jaratszam, celallomas, jegyar)

    def tipus(self):
        return "Belföldi"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas):
        # Változatos árak a nemzetközi járatokhoz
        import random
        jegyar = random.choice([20000, 30000, 40000])
        super().__init__(jaratszam, celallomas, jegyar)

    def tipus(self):
        return "Nemzetközi"


class Legitarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def add_jarat(self, jarat):
        self.jaratok.append(jarat)

    def get_jaratok(self):
        return self.jaratok


class JegyFoglalas:
    foglalt_jegyek = 0

    def __init__(self, jarat, utas_neve, datum):
        self.jarat = jarat
        self.utas_neve = utas_neve
        self.datum = datum
        JegyFoglalas.foglalt_jegyek += 1


def jegy_foglalas(jarat, utas_neve, datum):
    if JegyFoglalas.foglalt_jegyek < 5:  # Például maximum 5 foglalás
        return JegyFoglalas(jarat, utas_neve, datum), jarat.jegyar
    else:
        return None, "A járat már teljes!"


def lemondas(foglalasok, utas_neve):
    for foglalas in foglalasok:
        if foglalas.utas_neve == utas_neve:
            foglalasok.remove(foglalas)
            JegyFoglalas.foglalt_jegyek -= 1
            return f"Foglalás lemondva: {utas_neve}"
    return "Nincs ilyen foglalás."


def listazas(foglalasok):
    for foglalas in foglalasok:
        print(f"Utas: {foglalas.utas_neve}, Járatszám: {foglalas.jarat.jaratszam}, "
              f"Célállomás: {foglalas.jarat.celallomas}, Ár: {foglalas.jarat.jegyar} Ft, "
              f"Dátum: {foglalas.datum}")


def main():
    legitarsasag = Legitarsasag("AirExample")

    # Belföldi városnevek
    belfoldi_varosok = [
        "Budapest", "Debrecen", "Szeged", "Pécs", "Miskolc",
        "Győr", "Kecskemét", "Nyíregyháza", "Székesfehérvár", "Veszprém",
        "Sopron", "Zalaegerszeg", "Tatabánya", "Érd", "Békéscsaba",
        "Kaposvár", "Kiskunfélegyháza", "Eger", "Salgótarján", "Dunaújváros"
    ]

    # Nemzetközi városnevek
    nemzetkozi_varosok = [
        "London", "New York", "Párizs", "Berlin", "Tokió",
        "Róma", "Madrid", "Brüsszel", "Amszterdam", "Sydney",
        "Toronto", "Los Angeles", "Milánó", "Dubaj", "Prága",
        "Bécs", "Stockholm", "Oslo", "Koppenhága", "Dublin",
        "Zágráb", "Sofia", "Belgrád", "Athén", "Helsinki",
        "Tallinn", "Vilnius", "Riga", "Zürich", "Genf",
        "Bordeaux", "Lille", "Marseille", "Nice", "Malaga",
        "Valencia", "Sevilla", "Bilbao", "San Sebastián", "Bratislava",
        "Ljubljana", "București"
    ]

    # Járatok hozzáadása
    for celallomas in belfoldi_varosok:
        legitarsasag.add_jarat(BelfoldiJarat(f"AE{123 + len(legitarsasag.get_jaratok())}", celallomas))

    for celallomas in nemzetkozi_varosok:
        legitarsasag.add_jarat(NemzetkoziJarat(f"AE{123 + len(legitarsasag.get_jaratok())}", celallomas))

    foglalasok = []

    while True:
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válassz egy lehetőséget: ")

        if valasztas == '1':
            nev = input("Add meg a neved: ")
            print("Válassz célállomást:")
            for index, jarat in enumerate(legitarsasag.get_jaratok()):
                print(f"{index + 1}. {jarat.celallomas} ({jarat.jaratszam}) - Ár: {jarat.jegyar} Ft")

            jarat_index = int(input("Add meg a választott járat számát: ")) - 1
            if 0 <= jarat_index < len(legitarsasag.get_jaratok()):
                datum = input("Add meg a dátumot (YYYY-MM-DD): ")
                try:
                    datetime.strptime(datum, "%Y-%m-%d")  # Dátum érvényesség ellenőrzése
                    jarat = legitarsasag.get_jaratok()[jarat_index]
                    foglalas, ar = jegy_foglalas(jarat, nev, datum)
                    if foglalas:
                        foglalasok.append(foglalas)
                        print(f"Foglalás sikeres! Ár: {ar} Ft")
                    else:
                        print(ar)
                except ValueError:
                    print("Érvénytelen dátum formátum! Kérlek, próbáld újra.")
            else:
                print("Érvénytelen választás!")

        elif valasztas == '2':
            nev = input("Add meg a neved: ")
            print(lemondas(foglalasok, nev))

        elif valasztas == '3':
            listazas(foglalasok)

        elif valasztas == '4':
            break


if __name__ == "__main__":
    main()
