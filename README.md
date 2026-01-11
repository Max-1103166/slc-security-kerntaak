# Week 5 - Security Opdracht

## Mijn applicatie
Mijn app is symmetrisch: een gebruiker stuurt plaintext door en versleutelt het met een gegenereerde sleutel. Deze sleutel wordt “doorgegeven” en alleen de ontvanger kan het encrypte bericht ontsleutelen met de doorgegeven sleutel.  

Een asymmetrische app zou een gebruiker twee sleutels geven: een publieke en een private sleutel.  
De zender gebruikt de publieke sleutel van de ontvanger om de plaintext te vergrendelen. Alleen de private sleutel van de ontvanger kan het ontsleutelen. Dit maakt key management makkelijker, maar is trager.  

Mijn applicatie bestaat uit:  
- Standaard algoritme Fernet (AES-128)  
- Key Derivation Function (KDF)  
- Hardware Security Module (HSM)  

Volgens Kerckhoff’s Principe mag de veiligheid niet afhangen van het geheim van het algoritme, alleen van de sleutel. Ook als de broncode publiek zichtbaar is, kan een bericht niet ontsleuteld worden zonder toegang tot de HSM.

---

## Installatie

1. Zorg dat je **Python 3.13** hebt geïnstalleerd.
2. Maak een python venv aan in de projectdirectory:
```
python -m venv venv
```
3. Activeer de venv:
   - Windows:
```
 ./venv/Scripts/activate
```
   - macOS/Linux:
```
 source venv/bin/activate
```
4. Installeer de benodigde dependencies
```
   pip install -r requirements.txt
```

## Database en HSM Initialisatie

1. Genereer de database door het script uit te voeren:
```python db_gen.py```
2. Start de HSM (Hardware Security Module) simulatie:
```python hsm.py```

    De HSM moet aanblijven staan om de keys opgeslagen te houden
## Applicatie starten

1. Start de hoofdapplicatie:
   ```python main.py```
2. In de applicatie kun je nu:
   - De **zender** en **ontvanger** selecteren in het bovenste formulier.
   
     Let op: de zender mag niet hetzelfde zijn als de ontvanger.
   - Schrijf een bericht in het tekstvak.
   
![Zender & ontvanger selecteren](readme%20images/sender_reciever.png)

3. Om het bericht te **encrypten**, klik je op de encryptie-knop:

![Encryptie knop](readme%20images/send.png)

4. Wacht een paar seconden; het resultaat van de encryptie verschijnt:

![Encryptie resultaat](readme%20images/encryption_result.png)

5. Om een bericht te decrypten, selecteer je de gebruiker naar wie het bericht is gestuurd.
   Wacht enkele seconden en het resultaat verschijnt naast het bericht:

![Decryptie bericht](readme%20images/decrypt_message.png)
![Voorbeeld](readme%20images/img.png)


## Applicatieproces
1. Een gebruiker maakt een bericht en stuurt dit als een request door.  
2. Mijn applicatie genereert een salt (een willekeurige string van 16 bytes met `secrets.token_bytes()`). Deze salt is uniek voor elk bericht.  
3. De HSM wordt aangeroepen met zenders- en ontvangers-id + de salt wordt doorgegeven. In de HSM wordt een random string van 32 bytes gegenereerd (ook met`secrets.token_bytes`). Deze key wordt opgeslagen in het “geheugen” van de HSM (een Python Dictionary).  
   - De dictionary key bestaat uit: zenders-id + ontvangers-id + salt  
   - De value is de gegenereerde 32 bytes sleutel  
4. De key (32 bytes) wordt teruggegeven aan het main script, waar deze door een KDF wordt gehaald. De key wordt met de eerst gegenereerde salt “gestretched” (key stretching).  
5. Deze gestretchte key wordt gebruikt met Fernet om het bericht te encrypten.  
6. Het encrypte bericht wordt samen met de salt opgeslagen in de database met de verzender- en ontvanger-id.  

### Decryptieproces
1. De ontvanger stuurt zijn id.  
2. Er wordt een query uitgevoerd om het laatst verzonden bericht voor deze id op te halen.  
3. De zender-id + ontvanger-id + salt worden naar de HSM gestuurd.  
4. De HSM zoekt de key in zijn geheugen. Als de juiste key is gevonden, wordt deze teruggestuurd naar het main script.  
5. In het main script wordt de key weer door de KDF gehaald met de salt en vervolgens met Fernet gedecrypt.

---

## Mijn keuzes

- AES-128 via Fernet:  
  - Snelheid is belangrijk.  
  - Key uitwisseling gebeurt via mijn mock HSM.  
  - Fernet gebruikt een Initialization Vector (IV), dus plaintext is altijd anders geencrypt.  
  - Elke token heeft een timestamp en een Authentication Tag, zodat de data niet ongemerkt kan worden aangepast.  
  - OWASP geeft aan dat AES-128 voldoende is, maar het zou ideaal zijn om AES-256 te gebruiken, want AES-256 is een stuk effectiever en veiliger in het encrypten van data.

- KDF:  
  - PBKDF2HMAC met SHA-256 en 100.000 iteraties.  
  - Dit maakt brute-force aanvallen moeilijker en kost meer rekenwerk.  
  - Cryptography.io beveelt PBKDF2HMAC aan als geschikte KDF.

- HSM:  
  - De sleutel wordt fysiek beschermd in echte HSM’s. (nu is het een mock HSM) 
  - Mijn applicatie gebruikt een mock HSM, maar dit simuleert dat alleen geautoriseerde gebruikers de sleutel kunnen ophalen.  
  - Hiermee wordt Kerckhoff’s principe toegepast: het algoritme mag publiek zijn, de sleutel blijft geheim.

- Secrets module:  
  - Gebruikt voor het genereren van cryptografisch veilige willekeurige bytes.  
  - Aanbevolen door OWASP.

---

## Architectuur
- HSM-script draait op poort 5000.  
- Main-script draait op poort 8000.  
- Dit simuleert dat de HSM op een aparte server draait.

---

## Reflectie
- Ik zou meer aandacht willen besteden aan het mocken van een HSM, bijvoorbeeld door softHSM te gebruiken. Nu is het alleen een dictionary in een apart script op een andere poort.  
- Ik wil in de toekomst meer validatie toevoegen bij het ontvangen van berichten, 
bijvoorbeeld door een sessiebeheer te implementeren. Daarnaast zou ik overwegen om de requests zelf ook te encrypten, zodat niet alleen het bericht in de database veilig is, maar ook de communicatie tussen client en server beschermd wordt.
- ook wil ik dat deze applicatie logischer opgebouwd is, nu zit de database technisch gezien aan de "client" kant van de applicatie. maar realistisch moet het aan de server net als de HSM kant zitten van de applicatie.
  hierdoor is er duidelijk scheiding tussen client en server zijn en de beveiliging beter gesimuleerd kan worden.
---

## Bronnen
- [Repository](https://github.com/Max-1103166/opdracht-week-5-security)  
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)  
- [Principe van Kerckhoffs - Wikipedia](https://nl.wikipedia.org/wiki/Principe_van_Kerckhoffs)  
- [Cryptography.io - KDFs](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/)  
- [Cryptography.io - PBKDF2HMAC](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC)  
- [Symmetrische vs. Asymmetrische encryptie](https://www.encryptionconsulting.com/nl/opleidingscentrum/symmetrische-versus-asymmetrische-encryptie/)
