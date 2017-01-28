# Catcher

## todo

* vytvorit dokumentaci, kam napisu zakladni info o aplikaci a dam do nej rest api doc
* implementovat zmenu hesla (bude to obyc angularjs formular bez modals)
* podívat se na formulář pro vytváření turnaje a podle toho zkontrolovat tabulku tournament
* vymyslet třídu tournament, zda to bude spíš fasáda nebo nejaká složitější třída
* nasadit
* dat do kupy README
* otestovat nainstalovani balicku v cistem envu nebo idealne na cistem systemu

### nice to have (az po odevzdani mipyt)

* http -> https
* ukladat hesla hashovane se soli
* neposilat heslo emailem, ale poslat mu pouze link na adresu, kde si heslo nastavi
  * stejne tak nachystat backend pro obnovu hesla
* implementovat cron pro mazani neaktivnich api klicu
* logovani od urovne WARN logovat do souboru abych vedel o pripadnych problemech
* rozhodnout se, jestli pouzivat json, ujson nebo simplejson

### DB

* kazda tabulka bude mit nakonec svoje id, zadne ide


### web klient

* celkove doladit
    * po aktualizovani stranky vratit do spravneho tabu
    * oznacovat povinna pole
    * apod.


## important

* uzivatel bude moci vytvorit team, ktery mu bude patrit
* misto club a organizer bude pouze user (aby se mohly role prolinat)
* slozku env jsem musel vytahnout z projektu vyse, protoze test runner v setup.py chtel volat testy
i v nainstalovanych balicich


## sqlalchemy

* select: `_session.query(User).filter(User.id == 0).first()`


## testing

* http://falcon.readthedocs.io/en/stable/api/testing.html

## virtualenv

* aktivace: `$ . env/bin/activate`
* instalace balíčků: `(env)$ python -m pip install requests click`
* přehled balíčků: `python -m pip freeze`
* vypnutí: `(env)$ deactivate`
* nastavení PyCharmu: http://stackoverflow.com/questions/19885821/how-do-i-import-modules-in-pycharm

## setup.py

* instalace v dev režimu: `python setup.py develop`

## Zadání semestrální práce

Ve všech případech (kromě případných explicitních výjimek) musí práce splňovat tyto požadavky:

- [x] musí být napsaná v jazyce Python verze 3.3 nebo vyšší (Cython se samozřejmě také počítá),
- [ ] musí splnit zadání, na kterém jsme se dohodli,
- [x] musí být v gitovém repozitáři,
- [x] kód musí splňovat konvence,
- [ ] kód, komentáře i dokumentace musí být v angličtině,
- [x] commity musí obsahovat vhodně atomické změny a mít vysvětlující message,
- [x] kód musí být dostatečně pokryt testy (nechceme stanovovat číselnou hranici,
      použijte selský rozum),
- [x] projekt musí být zabalen jako pythonní balíček (za zveřejnění na PyPI
      pod svobodnou licencí jsou body navíc),
- [x] projekt by měl stavět na nějakém tématu probraném v předmětu MI-PYT.

### Obsahem mé semestrální práce:
- [x] Vytvoření nové větve, kde bude aplikace vytvořená od nuly. Na mnoha místech sice
      využiji původní myšlenku nebo nápad, ale myslím si, že ve většině případů nenechám
      kámen na kameni.
- [ ] Bude splňovat všechny náležitosti pro semestrální práci (Python 3, PEP8, dokumentace,
      testy, balíček).
- [ ] Aplikace bude umět (stará aplikace tohle skoro všechno už umí, ale z toho starého
      kódu by opravdu téměř nic nezůstalo):
    - [x] registrace a přihlášení uživatelů (tokeny s omezenou platností)
    - [ ] autorizace uživatelů (vytvářet turnaj nemůže každý apod.)
    - [ ] vytvoření turnaje (zápasy, skupiny, rozpis, hřiště) - na pozadí je docela
          dost logiky, i když se to nemusí na první pohled znát
    - [x] vytvoření, editace a smazání týmů
    - [x] logování do konzole

Pokud by na to byla kapacita, aplikace by dál měla umět:
- [ ] zadávání výsledků k zápasům a logika, která s nimi dál pracuje
      (např. posune vítěze do dalšího zápasu)
- [ ] zadávání hodnocení SOTG k zápasům (něco jako hodnocení fairplay soupeře)
