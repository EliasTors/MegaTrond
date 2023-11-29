# MegaTrond
## Et datainsamlings prosjekt, Teknologi og forskningslære H23

Laget av: Elias, Hedda og Aksel

# Oppgave
Bruk arduino og sensorer for å gjøre undersøkelser og samle inn data. Dataene skal lagres til fil og bearbeides for så å presenteres på en oversiktlig måte.

Resultatet skal presenteres i en skriftlig rapport der problemstillingen og prosessen beskrives, og målingene vises og drøftes. I tillegg skal prosjektet presenteres i en kort presentasjon for klassen.

# Problemstilling
Hvilket klasserom har best læringsmiljø? Finnes det noe korrelasjon mellom hvilke fag som var i et klasserom og hvordan miljøet i klasserommet er?

# Introduksjon
I dette prosjektet har vi valgt å samle miljø-data fra utvalgte klasserom og deretter bruke denne dataen til å finne ut hvilket klasserom som har best læringsmiljø. Vi vil også se hvordan hvilke fag som er i ett klasserom påvirker læringsmiljøet. For å gjøre dette har vi samlet div data med en Arduino Uno og brukt en Raspberry Pi 2B+ for å lagre dataen. Vi valgte å ta i bruk Raspberry Pien for å forenkle logge prossesen og slippe å ha en laptop stående med RPien til alle tider.

Dette prosjektet består av fire hoveddeler
## Innholdsfortegnelse
1. [Introduksjon](#Introduksjon)
2. [Innsamling av data](#Innsamling-av-data)
    1. [Logging av data](#Logging-av-data-med-Arduino)
    2. [Lagring av data](#Lagring-av-data-med-RPi)
3. [Resultater](#Resultater)
    1. [Visualisering](#visualisering)
4. [Drøfting](#drøfting)
    1. [Feilkilder](##feilkilder)
    2. [Korrelasjoner](#korrelasjoner)
    3. [Utvidelser](#Utvidelser)

# Innsamling av data
Innsamling av data er sentralt i dette prosjektet. Vi brukte mye tid på å bestemme hvilke sensorer og metoder vi skulle benytte for å samle inn data. Vi valgte bruke en BME680 som den sentrale sensoren i prosjektet, denne sensoren kan samle inn trykk, temperatur, luftfuktighet og gass. Vi hadde også med en fotoresisitor og en lydmåler. Vi logget datoen fra dette på en Raspberry Pi

# Logging av data med Arduino
Som nevnt bruker vi en Arduino for å samle dataen fra sensorene og aggregere den. For å redusere mengden feilkilder så gjør vi lite prossesering av dataen på arduinoen og vi valgte heller å sende rå data videre så vi kan prossesere den i etterkant. Vi har et ganske enkelt program for å samle inn data. Mesteparten av dataen kommer fra BME680 sensoren som kommuniserer og protokollen I2C. Denne protokollen gjør det veldig lett å samle inn data fra den sensoren. Etter at dataen er hentet fra sensorene skrives det til RPien over serial. Vi skriver det til serial i CSV format for å gjøre det lett å håndtere senere. Arduino programmet kan sees [her](https://github.com/EliasTors/MegaTrond/blob/main/data-collection/MegaTrond-Data-collector/MegaTrond-Data-collector.ino)

# Lagring av data med RPi
Som nevnt i introduksjonen så brukte vi en RPi for å lagre dataen etter at Arduinoen hadde samlet de. Vi valgte å bruke en RPi fordi det er enkeltstående, robust og godt dokumentert. Vi startet med å bruke en RPi Zero 2 der vi skrev dataen direkte til en CSV fil, men vi støttet på problemer med overoppheting etter kort tid. Vi valgte derfor å gå over til å bruke den litt mer robuste Raspberry Pi 2B+. Vi byttet også metoden vår for lagring til SQL lite for å redusere hvor tungt Pien måtte jobbe med prossesen. Etter disse endringene støttet vi ikke på flere problemer. Vi valgte å benytte Rasbian OS lite etter som vi ikke har behov for en GUI og det gjorde det lettere å få Pien stabil. Koden som kjører på RPien kan sees [her](https://github.com/EliasTors/MegaTrond/blob/main/data-collection/data-logger.py). Den er designet for å beholde data selv om Pien plutselig mister strøm. Vi aktiverer den ved å koble til Pien med SSH også bare kjøre det som et annet python program. Det eneste man trenger å installere i tillegg til standard python er biblioteket `pyserial` ettersom det er dette vi bruker for å samle data fra arduinoen over USB serial.

# Korrigering av tidspunkt
Raspberry Pien har ikke noe CMOS batteri og siden den ikke er koblet på nett var datoene den registrerte datoene ofte feil. For å korrigere dette bruker vi funksjonen under.


```python
from data import dataHandler

dataHandler.shift_datetime("serial_data dag 1.db", "2023-11-20T08:00:00")
```

# Resultater
Vi fikk mange resultater i de forskjellige rommene og har valgt a visualisere dem ved hjelp av grafer og korrelasjonsmatriser med hensikten å se sammenhenger mellom forskjellige datapunkter og for å se ulikheter i de forskjellige rommene. 

## Konvertere til CSV
Som nevnt tidligere så valgte vi å samle dataen i SQL format fordi dette var lettere for raspberry Pien å håndtere og det er mer stabilt, men for å gjøre det lett å jobbe med så må vi gjøre det om til CSV. Vi har laget en funksjon for å gjennomføre dette og i tillegg rydde opp i dataen ved å fjerne linjer der arduinoen ikke klarte å samle data eller andre feil.


```python
from data import dataHandler
data = dataHandler.sql_to_csv("data/serial_data sen mon.db")
```

## Visualisering
Vi har valgt hovedsakelig vanlige grafer som vår visualiseringsmetode fordi dette er mest oversiktlig for den type data vi har. Vi kan puttet også to rom på samme graf som gjør at du kan lett se forskjeller i for eksempel temperatur.


```python
from data import estemation

estemation.fill_time_gaps("data/day one.csv").to_csv("data/extrapolatedday1.csv", index=False)
estemation.fill_time_gaps("data/day one.5.csv").to_csv("data/extrapolatedday2.csv", index=False)
```


```python
%matplotlib inline
import matplotlib.pyplot as plt
from plotter import plotter

p = plotter()
p.plot_data(["data/day two.csv", "data/extrapolatedday1.csv", "data/extrapolatedday2.csv"], '1T')
```


    
![png](rapport_files/rapport_9_0.png)
    


# Drøfting
## Feilkilder
 
Feilkildene som kan oppstå går hovedsakelig ut på sensorene; kvaliteten, plasseringen og stabiliteten, samt feil i koden. Kvaliteten på sensorene kan variere, i tillegg til at plasseringen kan gi et feil bilde på miljøet i klasserommet. Dette kan for eksempel skje hvis sensoren blir plassert bakerst i klasserommet, altså at det kan være langt unna det vi vil måle. Vi vil dermed ikke få riktige resultater. Det var begrensede muligheter for plassering av sensorer i klasserom ettersom vi var avhengig av strømuttak og at det skulle være ute av veien så ingen tullet med det. Ustabile koblinger kan føre til at sensoren får feil mengde strøm, og vi får dermed feil resultat tilbake. Ved feil i koden kan vi gjøre en beregningsfeil.
 
## Korrelasjoner

Vi opplevde en hendelse på rom 04 som tydelig kommer til syne på dataen. Vi antar at noen åpnet vinduet bak arduinoen, som førte til at arduinoen falt ned på varmeovnen. Dette vises i dataene ved at temperaturen plutselig øker når sensorene kommer nærmere varmeovnen, gassen synker plutselig som følge av at vinduet åpnes, og lyden øker, samt lyset synker. Da vi hentet arduinoen på slutten av dagen fra rom 04 hang den langs varmeovnen.

## Utvidelser

En mulig utvidelse ville ha vært å måle over flere dager enn vi gjorde, eventuelt i flere uker. Da hadde vi fått et bredere resultat som hadde bidratt til større forståelse for resultatene. Vi ønsket opprinnelig å måle i lengre tid enn det vi endte opp med å gjøre, men det tok tid å få alle sensorene vi trengte. I tillegg ble vi litt forsinket etter feil med utstyret, og vi fikk enda færre dager med måling enn det vi hadde sett for oss. Videre kunne vi ha hatt flere sensorer på forskjellige steder i et rom, for å måle gjennomsnittet i rommet. Det er ikke sikkert at vi hadde fått forskjellig resultat, men det ville muligens ha vært litt mer konkret
