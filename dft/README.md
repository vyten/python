# DFT – Distans Fart Tid

Räknar ut distans, fart eller tid till sjöss i terminalen. Du väljer vad du vill räkna ut, skriver in de två andra värdena och får svaret direkt.

Det här är fjärde versionen av programmet. De tidigare är skrivna i VB6, C# (Windows Forms) och PHP (webbsida med TinyMVC).

## Formler

Tiden räknas i minuter, därav 60.

| Räkna ut | Formel | Enhet |
|---|---|---|
| Distans | (Fart × Tid) / 60 | nm (distansminuter) |
| Fart | (Distans / Tid) × 60 | knop |
| Tid | (Distans / Fart) × 60 | h och minuter |

## Kör

```bash
cd dft
python3 dft.py
```

Första gången väljer du språk: 1 = Svenska, 2 = English, 3 = český. Språket sparas i `dft_lang.txt` bredvid skriptet, och nästa gång kommer du direkt till menyn. I menyn väljer du 1 = Distans, 2 = Fart, 3 = Tid, 4 = Byt språk eller 0 = Avsluta. När du byter språk står det nuvarande inom hakparenteser, till exempel `[2]`, och Enter behåller det. Decimaltal kan skrivas med punkt eller komma, till exempel `5.5` eller `5,5`. Ctrl+C avslutar också.

Fönsterversionen startas med:

```bash
python3 dft_gui.py
```

Fönstret har tre sidor, som webbsidan i PHP-versionen:

1. **Språksidan** med tre flaggor. Den visas bara första gången.
2. **Startsidan** med knapparna Distans, Fart och Tid, samt Avsluta.
3. **Uträkningssidan** med de fält som behövs, knappen Beräkna, Tillbaka och tre små flaggor som byter språk. Det du har skrivit i fälten följer med vid språkbyte.

Svaret visas i gult. Fel visas i gult på rött, och fältet som är fel blir rött. Fönstret och terminalen delar samma sparade språk i `dft_lang.txt`.

Felaktig inmatning loggas till `dft.log` i samma katalog som skriptet, från både terminalen och fönstret. Namnet ändras i konstanten `LOG_FILE_NAME` i `dft.py` och `dft_gui.py`.

## Filer

| Fil | Innehåll |
|---|---|
| `dft.py` | Huvudskriptet: meny, inmatning och utskrift |
| `dft_gui.py` | Samma program i ett fönster (tkinter). Tre sidor som i PHP-versionen: flaggor, startsida och uträkning |
| `img/` | Flaggorna för språkvalet, från PHP-versionen |
| `dft_functions.py` | Uträkningarna: `calculate_distance()`, `calculate_speed()`, `calculate_time()` och hjälpfunktionerna `to_minutes()` och `to_hours_and_minutes()` |
| `lang_se.py` | Svenska texter, för både terminalen och fönstret |
| `lang_en.py` | Engelska texter |
| `lang_cz.py` | Tjeckiska texter (rader märkta TODO är fortfarande på svenska) |

Färgerna hämtas från [`common/terminal_colors.py`](../common/README.md).

Kör `python3 dft_functions.py` för att testa uträkningarna. Den skriver `All tests OK`, eller stoppar med `AssertionError` och visar vilket svar som är fel.

## Utvärdering

Synpunkter från en kodgranskning av programmet.

### Övergripande

- **Uträkningarna är skilda från användargränssnittet.** `dft_functions.py` räknar bara och skriver aldrig ut något, och `dft.py` sköter frågor och svar. Därför kan ett GUI senare använda samma funktioner utan ändringar.
- **Funktionerna är små och gör en sak var.** `to_minutes()` och `to_hours_and_minutes()` används av de andra i stället för att samma uträkning upprepas.
- **Felet med 60 minuter från C#-versionen är borta.** `divmod(round(...), 60)` ger alltid minuter mellan 0 och 59.
- **Uträkningarna testar sig själva** med `assert` när `dft_functions.py` körs direkt, så ett fel syns utan att man behöver läsa av svaren.

### dft.py

- **Inmatningen tål både punkt och komma** som decimaltecken, och negativa tal stoppas. `nan` och `inf`, som `float()` också godtar, stoppas med `math.isfinite()`.
- **Division med noll fångas** innan uträkningen, med ett eget felmeddelande för tid 0 och fart 0.
- **Ctrl+C och Ctrl+D avslutar lugnt** med hej då på valt språk, i stället för en lång Python-felutskrift.
- **Språken ligger i en tabell** (`LANGUAGES`). Ett nytt språk kräver bara en ny språkfil och en rad.
- **Språket sparas** i `dft_lang.txt`, och en trasig eller saknad fil leder till språkvalet i stället för en krasch.

### Språkfilerna

- **Alla tre filerna har samma nycklar**, och tal formateras i själva texten (`{distance:.1f}`), så varje språk kan placera talet där det passar.

### dft_gui.py

- **Inga uträkningar är skrivna en gång till.** Fönstret använder `dft_functions.py` för uträkningarna och `dft.py` för språken och det sparade språket, så terminalen och fönstret räknar alltid likadant.
- **Sidorna byggs från en tabell** (`CALCULATIONS`). De tre uträkningssidorna delar samma kod, och bara fälten skiljer.
- **Felen syns där de är:** fältet som är fel blir rött och får markören.
- **Färgerna och typsnitten är konstanter** överst i filen, med samma värden som i PHP-versionens `w3.css`.
- **Två klassiska tkinter-fällor är undvikna:** bilderna sparas i en variabel så att de inte försvinner, och `lambda number=number:` ger varje flagga sitt eget språk.

### Att förbättra

- **Kontrollen av tal finns två gånger:** `ask_number()` i `dft.py` och `read_number()` i `dft_gui.py` gör samma sak. Kontrollen skulle kunna flyttas till en gemensam funktion i `dft_functions.py`, som returnerar talet eller vilket fel det är.
- **`dft_gui.py` importerar hela `dft.py`** för att komma åt språken. Då följer terminaldelar som `subprocess` och `terminal_colors` med. `LANGUAGES`, `load_language()` och `save_language()` skulle kunna ligga i en egen fil, till exempel `dft_language.py`, som båda använder.
- **Enter räknar inte ut i fönstret,** utan man måste klicka på Beräkna. Det går att lägga till med `window.bind('<Return>', ...)`.
- **Fönstret testas för hand.** Uträkningarna har `assert`, men sidorna och knapparna har inga egna tester.

- **Nio rader i `lang_cz.py` är fortfarande på svenska** och väntar på översättning.
