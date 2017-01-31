# Catcher

## Zadání semestrální práce

Ve všech případech (kromě případných explicitních výjimek) musí práce splňovat tyto požadavky:

- [x] musí být napsaná v jazyce Python verze 3.3 nebo vyšší (Cython se samozřejmě také počítá),
- [ ] musí splnit zadání, na kterém jsme se dohodli,
- [x] musí být v gitovém repozitáři,
- [x] kód musí splňovat konvence,
- [x] kód, komentáře i dokumentace musí být v angličtině,
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
- [x] Bude splňovat všechny náležitosti pro semestrální práci (Python 3, PEP8, dokumentace,
      testy, balíček).
- [ ] Aplikace bude umět (stará aplikace tohle skoro všechno už umí, ale z toho starého
      kódu by opravdu téměř nic nezůstalo):
    - [x] registrace a přihlášení uživatelů (tokeny s omezenou platností)
    - [x] autorizace uživatelů (vytvářet turnaj nemůže každý apod.)
    - [ ] vytvoření turnaje (zápasy, skupiny, rozpis, hřiště) - na pozadí je docela
          dost logiky, i když se to nemusí na první pohled znát
    - [x] vytvoření, editace a smazání týmů
    - [x] logování do konzole

Pokud by na to byla kapacita, aplikace by dál měla umět:
- [ ] zadávání výsledků k zápasům a logika, která s nimi dál pracuje
      (např. posune vítěze do dalšího zápasu)
- [ ] zadávání hodnocení SOTG k zápasům (něco jako hodnocení fairplay soupeře)

## Usage

Install the package:

```
python setup.py install
```

Test the package:

```
python setup.py test
```

For deploy you will need `python3-dev` because of UWSGi probably.

```
Usage: catcher [OPTIONS] COMMAND [ARGS]...

  Catcher app

Options:
  --help  Show this message and exit.

Commands:
  local  Run UWSGi in local mode
  run    Run UWSGi in production mode
```

## Docs

Catcher use Sphinx doc where is detailed described REST API.

```
cd /catcher/docs/
make html
```

Then html result is available in `/catcher/docs/_build/html/index.html`.

## My personal notes

* kazda tabulka bude mit svoje id, zadne ide

### web client
  
* celkove doladit:
  * po aktualizovani stranky vratit do spravneho tabu
  * oznacovat povinna pole
  * apod.
* implementovat zmenu hesla (bude to obyc angularjs formular bez modals)

### sqlalchemy

* select: `_session.query(User).filter(User.id == 0).first()`

### depenencies

* pro dokumentaci: sphinxcontrib-httpdomain (pip)
* pro databazi: mysql

### falcon testing

* http://falcon.readthedocs.io/en/stable/api/testing.html

### virtualenv

* aktivace: `$ . env/bin/activate`
* instalace balíčků: `(env)$ python -m pip install requests click`
* přehled balíčků: `python -m pip freeze`
* vypnutí: `(env)$ deactivate`
* nastavení PyCharmu: http://stackoverflow.com/questions/19885821/how-do-i-import-modules-in-pycharm

### setup.py

* instalace v dev režimu: `python setup.py develop`
