# Catcher

## todo

* kazda tabulka bude mit nakonec svoje id, zadne ide -> kazdy objekt bude mit id nebo tournament_id, takze se muzu dopodivat na to, komu ten turnaj patri (pro privileges.isowner)
* rozhodnout se, jestli pouzivat json, ujson nebo simplejson
* angularu stale neposilam spolecne s pozadavky hlavicku auth, proto mi nefunguje overovani uzivatelu
* implementovat zmenu hesla (bude to obyc angularjs formular bez modals)
* dokončit privileges u rest api
* podívat se na formulář pro vytváření turnaje a podle toho zkontrolovat tabulku tournament
* vymyslet třídu tournament, zda to bude spíš fasáda nebo nejaká složitější třída
* nasadit
* http -> https
* ukladat hesla hashovane se soli
* doladit klienta (po aktualizovani stranky vratit do spravneho tabu, oznacovat povinna pole apod.)
* neposilat heslo emailem, ale poslat mu pouze link na adresu, kde si heslo nastavi
  * stejne tak nachystat backend pro obnovu hesla
* implementovat cron pro mazani neaktivnich api klicu
* na travisu vytvorit testovani repa => opravit testy
* mrknout na sdileni session mezi metodama, asi by stacilo mit globalne jednu session napric behem aplikace

## important

* uzivatel bude moci vytvorit team, ktery mu bude patrit
* misto club a organizer bude pouze user (aby se mohly role prolinat)


## sqlalchemy

* select: `_session.query(User).filter(User.id == 0).first()`


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
- [ ] kód musí být dostatečně pokryt testy (nechceme stanovovat číselnou hranici,
      použijte selský rozum),
- [ ] projekt musí být zabalen jako pythonní balíček (za zveřejnění na PyPI
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
