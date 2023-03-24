# Az Orbán Viktor beszéd scraper // _The Victor Orban Speech Scraper_

## At ötlet // _The idea_

Orbán Viktor miniszterelnök úr kommunikációs csapata az utóbbi időben elkezdte többé-kevésbé következetesen feltölteni a beszédeit és nyilatkozatait a weboldalára. Úgyhogy csináltam egy webscrapert, ami összeszedi ezeket és egy Pandas adatkeretbe rendezi őket későbbi elemzésre. 
_The communication team of Hungarian Prime Minister Viktor Orban recently started to upload his speeches and statements more or less consistently on his website, so I created a webscraper that gathers these in a Pandas dataframe for further analysis._

## Jövőbeli célok // _Future goals_

Per pillanat általános statisztikákon és szentiment elemzésen dolgozom, meg ezek vizualizációján. Mihelyt írok belőle egy cikket, elérhetővé fogom tenni a kódot mindenki számára. 
_Currently I'm working on general statistics functions and also on sentiment analysis and their visualizations. Once I publish my article I will make the code accessible to everyone._ 

## Használhatom én is a scrapert? // Can I use the scraper?

Természetesen! Annyi, hogy ha újságíróként, tartalomgyártóként, vagy csak simán nagy OV-rajongóként megosztanád az eredményeidet, kérlek, hivatkozz rám egy linkkel ehhez a repóhoz.

A szükséges kód az ov_scrape.py fájlban van (a szükséges függvények az ov_functions csomagban találhatók).
A dataframes mappa egy nagyon alap adatkeretet tartalmaz a jelenleg elérhető beszédekből, az alábbi infókkal: dátum, forrás, cím, szöveg. 

Ha elakadsz, szólj, és segítek szívesen. 

_Absolutely! However, if you are a journalist, content creator or just a fan of the Prime Minister who want to share the results publically, please, quote me with a link pointing at this repository.
The ov_scrape.py contains the necessary code (the functions are stored in the ov_functions package.)
The dataframes folder contains a very basic dataframe of the currently available speeches with the following information: date, source, title, text._ 

If you got stuck, I'm happy to help. 


