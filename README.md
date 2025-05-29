# Space-defender---seminaarityo (Toimiva, mutta jatkan vielä kehittämistä)

# Space Defender -pelisuunnitelma (Python)

## Johdanto

Tämä on suunnitelma yksinkertaisen 2D Space Defender -tyyppisen pelin tekemiseen Pythonilla. Pelissä pelaaja ohjaa avaruusalusta ja ampuu vihollisia. Tavoitteena on selviytyä mahdollisimman pitkään ja saada mahdollisimman korkea pistemäärä.

## Käytettävät Työkalut ja Kirjastot

*   **Python:** Peruskieli, jolla kaikki tehdään. Helppo oppia ja käyttää.
*   **Pygame:** Kirjasto pelien tekemiseen Pythonilla. Hoitaa grafiikan, äänet ja inputin. Pygame on aika suosittu ja siinä on paljon hyviä tutoriaaleja.
*   **(Mahdollisesti) PyOpenGL:** Jos halutaan 3D-efektejä tai jotain vähän hienompaa grafiikkaa, mutta ei välttämätön.
*   **(Mahdollisesti) NumPy:** Jos tarvitaan monimutkaisempaa matematiikkaa, esimerkiksi vektorilaskentaa. Luulen, että Pygame riittää perusjuttuihin.

## Pelin Perusrakenne

1.  **Alustus:**
    *   Pygame alustetaan.
    *   Ikkuna luodaan.
    *   Fontit ja äänet ladataan (jos niitä on).
2.  **Pelisilmukka:**
    *   Pelisilmukka pyörii jatkuvasti, kunnes pelaaja lopettaa pelin.
    *   Pelisilmukassa käsitellään input (näppäimistö, hiiri).
    *   Pelin tila päivitetään (liikutetaan aluksia, ammutaan, tarkistetaan törmäykset).
    *   Peli piirretään ruudulle.
3.  **Inputin Käsittely:**
    *   Pelaajan inputtia (esim. nuolinäppäimet) käytetään aluksen liikuttamiseen ja ampumiseen.
4.  **Pelin Logiikka:**
    *   Viholliset luodaan satunnaisesti.
    *   Ammukset liikkuvat ruudulla.
    *   Törmäykset tarkistetaan (alukset, ammukset).
    *   Pisteet lasketaan.
    *   Pelin loppu, kun pelaajan alus tuhoutuu.
5.  **Piirtäminen:**
    *   Tausta piirretään.
    *   Pelaajan alus piirretään.
    *   Viholliset piirretään.
    *   Ammukset piirretään.
    *   Pisteet piirretään.

## Pelin Komponentit

*   **Pelaajan alus:**
    *   Liikkuu vasemmalle ja oikealle.
    *   Ampuu ammuksia ylöspäin.
    *   Tuhoutuu, kun vihollinen osuu siihen.
*   **Viholliset:**
    *   Liikkuvat ylhäältä alas.
    *   Tuhoutuvat, kun pelaajan ammus osuu niihin.
    *   Saattavat ampua takaisin (lisävaikeutta).
*   **Ammukset:**
    *   Liikkuvat suoraan.
    *   Tuhoutuvat, kun osuvat johonkin.
*   **Tausta:**
    *   Staattinen tai liikkuva.
*   **Pisteet:**
    *   Näytetään ruudulla.
    *   Kasvavat, kun vihollisia tuhotaan.

## Mahdolliset Lisäominaisuudet

*   **Erilaisia vihollisia:** Eri nopeuksilla ja ampumismalleilla.
*   **Power-upit:** Esimerkiksi nopeampi ampuminen tai lisäelämät.
*   **Boss-taistelut:** Vaikeampia vihollisia, jotka vaativat erityistaktiikoita.
*   **Ääniefektit ja musiikki:** Parantavat pelikokemusta.
*   **Pistemäärätaulukko:** Näyttää parhaat tulokset.

## Aikataulu

(Tämä on vain arvio, riippuu paljon siitä, kuinka paljon aikaa on käytettävissä.)

*   **Viikko 1:** Pygamen perusteet, aluksen liikuttaminen.
*   **Viikko 2:** Vihollisten luominen ja liikuttaminen.
*   **Viikko 3:** Ampuminen ja törmäysten tarkistus.
*   **Viikko 4:** Pisteet, pelin loppu, lisäominaisuudet.

## Pelin ohjeet:
*   Peli ajetaan "python space_defender.py" komennolla ja pygame pitää olla asenettuna laitteella.
*   Pelaaja alusta liikutetaan nuoli näppäimillä ja ammutaan SPACE - näppäimellä.
*   Vihollisia ilmestyy satunnaisesti peli ruudun yläreunasta.
*   Tällä hetkellä voi ampua vihollisia ja tuhoutua itse, jos vihollinen osuu pelaajaan, jolloin peli aloitetaan alusta.
