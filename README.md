Třetí projekt Engeto Python akademie. 

"Elevation scraper" 

- sckript slouží k extrakci dat z výsledku voleb v r. 2017
- pracuje s libovolným odkazem na konkrétní obci z tohoto výběru:
https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
- pracuje vždy se dvěma argumenty:
  1. "URL odkaz na obci"
  2. "název_výsledného_souboru.csv"
     
- z URL odkazu postupně vytáhne volební výsledky a následně je uloží do csv souboru pod názvem zvoleným dryhým argumentem

Před spuštěním je nutné nainstalovat knihovny, se kterými skript pracuje - najdete je v souboru requirements.txt

Knihovny nainstalujete v příkazovém řádku pomocí:

    $ pip3 install -r requirements.txt  


Ukázka průběhu scriptu na obci Cheb:
python scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101" "Cheb.csv"

Částečný výstup:
Code	Location	        Registered Voters	Envelopes	Valid Votes	Občanská demokratická strana	Řád národa - Vlastenecká unie ...
554499	Aš        	        9766	            4289	    4254	    276	                            37
554502	Dolní Žandov	    943	                532	        528	        31	                            3
554511	Drmoul	            769	                486	        481	        49	                            2
554529	Františkovy Lázně	4700	            2905	    2886	    340	                            7
...
