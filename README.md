# Catcher

## virtualenv

* aktivace: `$ . env/bin/activate`
* instalace balíčků: `(env)$ python -m pip install requests click`
* přehled balíčků: `python -m pip freeze`
* vypnutí: `(env)$ deactivate`
* nastavení PyCharmu: http://stackoverflow.com/questions/19885821/how-do-i-import-modules-in-pycharm

## Zadání semestrální práce

Ve všech případech (kromě případných explicitních výjimek) musí práce splňovat tyto požadavky:

- [ ] musí být napsaná v jazyce Python verze 3.3 nebo vyšší (Cython se samozřejmě také počítá),
- [ ] musí splnit zadání, na kterém jsme se dohodli,
- [ ] musí být v gitovém repozitáři,
- [ ] kód musí splňovat konvence,
- [ ] kód, komentáře i dokumentace musí být v angličtině,
- [ ] commity musí obsahovat vhodně atomické změny a mít vysvětlující message,
- [ ] kód musí být dostatečně pokryt testy (nechceme stanovovat číselnou hranici,
      použijte selský rozum),
- [ ] projekt musí být zabalen jako pythonní balíček (za zveřejnění na PyPI
      pod svobodnou licencí jsou body navíc),
- [ ] projekt by měl stavět na nějakém tématu probraném v předmětu MI-PYT.

### Obsahem mé semestrální práce:
- [ ] Vytvoření nové větve, kde bude aplikace vytvořená od nuly. Na mnoha místech sice
      využiji původní myšlenku nebo nápad, ale myslím si, že ve většině případů nenechám
      kámen na kameni.
- [ ] Bude splňovat všechny náležitosti pro semestrální práci (Python 3, PEP8, dokumentace,
      testy, balíček).
- [ ] Aplikace bude umět (stará aplikace tohle skoro všechno už umí, ale z toho starého
      kódu by opravdu téměř nic nezůstalo):
    - [ ] registrace a přihlášení uživatelů (tokeny s omezenou platností)
    - [ ] autorizace uživatelů (vytvářet turnaj nemůže každý apod.)
    - [ ] vytvoření turnaje (zápasy, skupiny, rozpis, hřiště) - na pozadí je docela
          dost logiky, i když se to nemusí na první pohled znát
    - [ ] vytvoření, editace a smazání týmů
    - [ ] logování do konzole

Pokud by na to byla kapacita, aplikace by dál měla umět:
- [ ] zadávání výsledků k zápasům a logika, která s nimi dál pracuje
      (např. posune vítěze do dalšího zápasu)
- [ ] zadávání hodnocení SOTG k zápasům (něco jako hodnocení fairplay soupeře)
