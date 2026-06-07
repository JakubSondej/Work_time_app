# DOKUMENTACJA PROJEKTU - Ewidencja Czasu Pracy
**Aplikacja (live):** https://work-time-app.onrender.com/accounts/login/

---

## 1. OPIS

### 1.1 Cel Systemu

Aplikacja webowa do **rejestracji, zarządzania i rozliczania czasu pracy** dla pracowników i studentów. System umożliwia:

- Pracownikom: dodawanie dni pracy z wieloma przedziałami czasowymi, edycja niezatwierdzonych wpisów, przeglądanie podsumowań miesięcznych, export raportów
- Szefom: przegląd wpisów wszystkich pracowników, zatwierdzanie dni pracy, filtrowanie i generowanie raportów zespołu
- Automatyzację obliczeń wynagrodzeń na podstawie godzin pracy i stawki 

### 1.2 Główne Funkcje

#### Dla Pracownika:
1. **Dodawanie czasu pracy** - pracownik wybiera datę i dodaje przedziały czasowe (np. 08:00-12:00, 14:00-17:30)
2. **Edycja niezatwierdzonych wpisów** - zmiana przedziałów czasowych przed zatwierdzeniem przez szefa
3. **Podsumowanie miesięczne** - system automatycznie oblicza:
   - Łączne godziny pracy
   - Wynagrodzenie (godziny × stawka_hourly_rate)
   - Wyświetla tabelę dni pracy z statusem (zatwierdzone/oczekujące)
4. **Export CSV** - pracownik może pobrać raport w formacie CSV z raportem miesięcznym
5. **Przegląd historii** - lista wszystkich dni pracy z możliwością sortowania

#### Dla Szefa (Manager):
1. **Panel zarządzania** - przegląd wszystkich wpisów wszystkich pracowników
2. **Zatwierdzanie wpisów** - szef może zatwierdzić lub cofnąć zatwierdzenie dnia pracy
3. **Filtrowanie** - możliwość filtrowania po:
   - Miesiącu i roku
   - Konkretnym pracowniku
4. **Podsumowania** - automatyczne wyliczenie sumy godzin dla całego zespołu w wybranym okresie
5. **Export raportów** - szef może pobrać raport CSV dla całej grupy lub wybranego pracownika

#### Automatyzacja Systemu:
-  Automatyczne sumowanie przedziałów czasowych (obsługa pracy nocnej - np. 22:00-01:00)
- Automatyczne wyliczanie wynagrodzeń na podstawie godzin i stawki
- Blokada zatwierdzonych wpisów - pracownik nie może edytować/usuwać zatwierdzonego dnia
-   Automatyczny deployment - zmiana w GitHub automatycznie deployuje na Render

### 1.3 Role Użytkowników

| Rola | Uprawnienia | Dostęp do |
|------|-----------|----------|
| **Pracownik** | Dodawanie własnych dni pracy, edycja niezatwierdzonych, przeglądanie podsumowania | /tracker/work-days/, /tracker/monthly-summary/, /tracker/reports/employee/csv/ |
| **Szef (Manager)** | Przeglądanie wszystkich wpisów, zatwierdzanie, filtrowanie, export raportów zespołu | /tracker/manager/, /tracker/reports/manager/csv/ |
| **Admin** | Pełny dostęp do Django Admin, zarządzanie użytkownikami i uprawnieniami | /admin/ |

### 1.4 Testowe Dane

Aplikacja zawiera 3 domyślnych użytkowników:

| Login | Hasło | Rola | Opis |
|-------|-------|------|------|
| `john` | `john123` | Pracownik | Testowanie dodawania dni pracy, podsumowań |
| `boss` | `boss123` | Szef (Manager) | Testowanie panelu szefa, zatwierdzania |
| `admin` | `admin123` | Admin (Superuser) | Dostęp do Django Admin |

Wszyscy użytkownicy mają stawkę godzinową: **30 zł/h**

---

## 2. ARCHITEKTURA TECHNICZNA

### 2.1 Stack Technologiczny

| Warstwa | Technologia | Wersja | Cel |
|---------|-------------|--------|-----|
| **Backend** | Django | 6.0.5 | Framework webowy, logika biznesowa |
| **Język** | Python | 3.13.9 | Język programowania |
| **Frontend** | Bootstrap | 5.3.6 | Framework CSS, responsywność |
| **Markup** | HTML5 | - | Struktura stron |
| **Skrypty** | JavaScript | ES6 | Dynamiczne elementy formularzy |
| **Baza danych (DEV)** | SQLite | - | Lokalna baza do testowania |
| **Baza danych (PROD)** | PostgreSQL | - | Produkcyjna baza na Render |
| **Serwer aplikacji** | Gunicorn | 23.0.0 | WSGI server, obsługa requesta |
| **Static files** | WhiteNoise | 6.6.0 | Serwowanie CSS, JS, obrazów |
| **Env variables** | python-decouple | 3.8 | Zarządzanie zmiennymi środowiska |
| **DB connector** | dj-database-url | 2.1.0 | Parsing DATABASE_URL |
| **ORM** | Django ORM | - | Mapowanie obiektów na bazę |
| **VCS** | Git / GitHub | - | Kontrola wersji, hosting kodu |
| **Hosting** | Render.com | - | Platform as a Service |
| **CI/CD** | Render auto-deploy | - | Automatyczne wdrażanie |

### 2.2 Modele Danych

#### WorkDay (Dzień Pracy)
```
- user (ForeignKey → User)           # Pracownik
- date (DateField)                    # Data pracy
- description (TextField, optional)   # Dodatkowy opis
- approved (BooleanField)             # Czy zatwierdzone przez szefa
- created_at (DateTimeField)          # Data utworzenia wpisu
```

#### WorkPeriod (Przedział Czasowy)
```
- work_day (ForeignKey → WorkDay)    # Powiązany dzień pracy
- start_time (TimeField)             # Godzina startu (np. 08:00)
- end_time (TimeField)               # Godzina końca (np. 12:00)
# Metoda: duration_minutes() - oblicza różnicę czasu w minutach
```

#### UserProfile (Profil Pracownika)
```
- user (OneToOneField → User)        # Użytkownik Django
- hourly_rate (DecimalField)         # Stawka godzinowa w PLN (np. 30.00)
```

### 2.3 Przepływ Danych

```
PRACOWNIK                           SZEF
    ↓                                ↓
Logowanie (Django Auth)         Logowanie (Django Auth)
    ↓                                ↓
Przegląd dni pracy              Panel szefa (view wszystkie wpisy)
    ↓                                ↓
Dodaj dzień + przedziały        Filtruj (miesiąc, rok, pracownik)
    ↓                                ↓
System oblicza: godziny         Przegląda tabele wpisów
    ↓                                ↓
Czeka na zatwierdzenie          Zatwierdza/cofa zatwierdzenie
    ↓                                ↓
Podsumowanie miesięczne         Generuje raport CSV
(automatycznie wylicza)
    ↓
Export CSV
```

### 2.4 Walidacja Danych

**Walidacje w formularzach:**

1. **Godzina końca > Godzina startu**
   - ❌ Błąd: 14:00 - 13:00
   - ✅ OK: 08:00 - 12:00
   - ✅ OK (praca nocna): 22:00 - 01:00 (system obsługuje automatycznie)

2. **Przedziały nie mogą się nakładać**
   - ❌ Błąd: Przedział 1: 08:00-12:00, Przedział 2: 11:00-15:00
   - ✅ OK: Przedział 1: 08:00-12:00, Przedział 2: 13:00-17:00

3. **Data nie może być w przyszłości**
   - ❌ Błąd: data = 2099-12-31
   - ✅ OK: data = dzisiaj lub wcześniej

4. **Praca nocna obsługiwana**
   - ✅ OK: 22:00 - 01:00 = 3 godziny (system automatycznie uznaje przeskok dnia)

### 2.5 Bezpieczeństwo

- ✅ **CSRF Protection** - `{% csrf_token %}` na wszystkich formularzach POST
- ✅ **Role-based Access Control** - pracownik widzi tylko swoje wpisy, szef widzi wszystkich
- ✅ **Autentykacja** - Django Auth System z grupami (Manager)
- ✅ **SECRET_KEY** - zarządzany przez zmienne środowiskowe (.env)
- ✅ **DEBUG** - wyłączony w produkcji
- ✅ **HTTPS** - wymuszony na Render (SECURE_SSL_REDIRECT)
- ✅ **Session Security** - SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE w produkcji

---

## 3. RENDER - PLATFORMA CLOUD

### 3.1 Czym Jest Render?

**Render** to platforma **Platform as a Service (PaaS)** - czyli usługa hostingowa, która umożliwia wdrażanie aplikacji webowych w chmurze bez konieczności zarządzania infrastrukturą serwerową.

**Główne cechy:**
- Hosting aplikacji webowych (Node.js, Python, Ruby, Go, etc.)
- Bazy danych PostgreSQL, MySQL, Redis
- Automatyczne skalowanie
- SSL/HTTPS
- Custom domains
- Automatyczny deployment z GitHub
- Darmowy plan (Free tier)

### 3.2 Jak Render Pracuje

```
Workflow:
1. Kod na GitHub (push)
   ↓
2. Render obserwuje GitHub (webhook)
   ↓
3. Render clonuje repo
   ↓
4. Render uruchamia build.sh
   ↓
5. Render instaluje zależności (pip install -r requirements.txt)
   ↓
6. Render uruchamia migracje (python manage.py migrate)
   ↓
7. Render uruchamia aplikację (gunicorn config.wsgi)
   ↓
8. Aplikacja dostępna na URL: https://work-time-app.onrender.com
```

### 3.3 Komponenty Render Używane w Projekcie

#### 1. **PostgreSQL Database**
- **Nazwa:** work-time-db
- **Plan:** Free
- **Region:** Frankfurt (blisko Polski)
- **Funkcja:** Przechowywanie danych (użytkownicy, dni pracy, przedziały czasowe)
- **URL:** postgresql://postgress:PASSWORD@dpg-xxxx.frankfurt-postgres.render.com:5432/work_time_db

#### 2. **Web Service**
- **Nazwa:** work-time-app
- **Plan:** Free
- **Region:** Frankfurt
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn config.wsgi --log-file -`
- **Funkcja:** Uruchomienie aplikacji Django
- **URL:** https://work-time-app.onrender.com

### 3.4 Zmienne Środowiskowe na Render

W Render Dashboard ustawione:

```
SECRET_KEY = django-secret-key-string
DEBUG = False
ALLOWED_HOSTS = work-time-app.onrender.com
DATABASE_URL = postgresql://postgress:PASSWORD@host/db
PYTHON_VERSION = 3.13.9
```

---

## 4. IMPLEMENTACJA NA RENDER - KROK PO KROKU

### 4.1 Przygotowanie Lokalnego Projektu

#### Kroki 1-2: Konfiguracja Django
```
config/settings.py:
- SECRET_KEY pobierany z .env (decouple)
- DEBUG zarządzany z .env
- ALLOWED_HOSTS konfigurowany dla produkcji
- DATABASES obsługuje DATABASE_URL z Render
- STATIC_ROOT = /staticfiles
- STATICFILES_STORAGE = WhiteNoise
```

#### Krok 3: Pliki Konfiguracyjne
```
.env.example → Template zmiennych (do repozytorium)
.env → Lokalne zmienne (NIE do repozytorium)
.gitignore → Ignoruje venv, .env, db.sqlite3, staticfiles
```

#### Krok 4: Build & Start Scripts
```bash
# build.sh (uruchamiany przez Render przy deployu)
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python setup_db.py

# Procfile / start command
gunicorn config.wsgi --log-file -
```

#### Krok 5: Requirements.txt
```
Django==6.0.5
psycopg2-binary==2.9.12          # PostgreSQL driver
gunicorn==23.0.0                  # Production server
whitenoise==6.6.0                 # Static files
python-decouple==3.8              # Environment variables
dj-database-url==2.1.0            # Parse DATABASE_URL
```

### 4.2 Wdrożenie na Render

#### Faza 1: Przygotowanie GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/work-time-app.git
git push origin main
```

#### Faza 2: Stworzenie PostgreSQL
1. Render Dashboard → New → PostgreSQL
2. Settings:
   - Name: work-time-db
   - Database: work_time_db
   - Region: Frankfurt
3. Skopiuj DATABASE_URL

#### Faza 3: Stworzenie Web Service
1. Render Dashboard → New → Web Service
2. Wybierz GitHub repo
3. Settings:
   - Name: work-time-app
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi --log-file -`
4. Environment Variables:
   ```
   SECRET_KEY = [wygeneruj silne hasło]
   DEBUG = False
   ALLOWED_HOSTS = work-time-app.onrender.com
   DATABASE_URL = [skopiuj z PostgreSQL]
   PYTHON_VERSION = 3.13.9
   ```
5. Kliknij "Create Web Service"

#### Faza 4: Deploy Process (automatyczny)
```
Render:
1. Clone repo z GitHub
2. Zainstaluj Python 3.13
3. Uruchomi build.sh:
   - pip install -r requirements.txt
   - python manage.py collectstatic
   - python manage.py migrate (tworzy tabele)
   - python setup_db.py (tworzy użytkowników)
4. Uruchomi gunicorn
5. Nasłuchuje na porcie 10000
6. Expose na URL: https://work-time-app.onrender.com
```

### 4.3 Co Się Dzieje Przy Każdym Git Push

```
Developer:
git push origin main
    ↓
GitHub:
Webhook notifiuje Render
    ↓
Render:
1. Pull latest code
2. Detects changes in:
   - Python files
   - requirements.txt
   - build.sh
    ↓
3. Build process:
   - pip install -r requirements.txt
   - python manage.py collectstatic
   - python manage.py migrate
   ↓
4. Restart:
   - gunicorn reload
   - Nowa wersja live ✅
```

---

## 5. STRUKTURA PROJEKTU

```
work-time-app/
│
├── config/                     # Django Project Config
│   ├── settings.py            # Ustawienia (ENV variables, DATABASES, STATIC_ROOT)
│   ├── urls.py                # Root URL router
│   ├── wsgi.py                # WSGI app entry
│   └── asgi.py                # ASGI app entry
│
├── tracker/                    # Główna Aplikacja Django
│   ├── models.py              # WorkDay, WorkPeriod, UserProfile
│   ├── views.py               # 8 widoków (list, create, update, delete, summary, manager, approve, export)
│   ├── forms.py               # WorkDayForm, WorkPeriodForm, WorkPeriodFormSet
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Django Admin registration
│   ├── apps.py                # App config
│   ├── migrations/            # Database schema migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_workday_workperiod.py
│   │   └── 0003_userprofile.py
│   └── templates/
│       ├── registration/
│       │   └── login.html     # Django Auth login page
│       └── tracker/
│           ├── work_day_list.html              # Lista dni pracy
│           ├── work_day_form.html              # Formularz dodawania/edycji
│           ├── work_day_confirm_delete.html    # Potwierdzenie usunięcia
│           ├── monthly_summary.html            # Podsumowanie miesięczne
│           ├── manager_dashboard.html          # Panel szefa
│           └── entry_*.html                    # Stare szablony (deprecated)
│
├── docs/                       # Dokumentacja
│   ├── PROJECT_DOCUMENTATION.md
│   ├── APP_DESCRIPTION.md
│   └── IMPROVEMENTS_PROPOSAL.md
│
├── manage.py                   # Django CLI
├── requirements.txt            # Zależności Python
├── Procfile                    # Render process file
├── build.sh                    # Build script (Render)
├── setup_db.py                 # Setup bazy i test users
├── .env.example                # Template zmiennych
├── .gitignore                  # Pliki ignorowane
├── README.md                   # Dokumentacja projektu
└── db.sqlite3                  # Baza SQLite (dev tylko)
```

---

## 6. PRZEPŁYW LOGOWANIA I AUTENTYKACJI

```
1. Użytkownik wchodzi na https://work-time-app.onrender.com/accounts/login/
   ↓
2. Django auth system wyświetla formularz logowania
   ↓
3. Użytkownik wpisuje username i password
   ↓
4. Django waliduje credentials w bazie (tabela auth_user)
   ↓
5. Jeśli OK → Ustawia session cookie
   ↓
6. Redirect na /tracker/work-days/ (dla pracownika)
   lub /tracker/manager/ (jeśli manager)
   ↓
7. Middleware @login_required chroni widoki
   ↓
8. Jeśli nie zalogowany → redirect na /accounts/login/
```

---

## 7. BEZPIECZEŃSTWO DOSTĘPU NA RENDER

### 7.1 Sieć
- ✅ HTTPS (SSL/TLS) - wymuszony
- ✅ Domain: work-time-app.onrender.com

### 7.2 Baza Danych
- ✅ PostgreSQL hasło - secure random
- ✅ Baza dostępna TYLKO ze Web Service (internal network)
- ✅ Połączenie: postgresql://user:pass@host:port/db

### 7.3 Aplikacja
- ✅ SECRET_KEY - 50 losowych znaków
- ✅ DEBUG = False (nie wyświetla stacktrace'u)
- ✅ ALLOWED_HOSTS = work-time-app.onrender.com
- ✅ CSRF_COOKIE_SECURE = True
- ✅ SESSION_COOKIE_SECURE = True

### 7.4 Zmienne Środowiskowe
- ✅ Nie w kodzie (w .env, które jest w .gitignore)
- ✅ Ustawiane w Render Dashboard
- ✅ Czytane przez python-decouple

---

## 8. MONITOROWANIE NA RENDER

### Dostępne narzędzia:
- **Logs** - stdout/stderr z aplikacji
- **Metrics** - CPU, memory, requests
- **Deploy History** - historia deployów
- **Events** - build status, restarts

### Typowe problemy i diagnostyka:
```
500 Error → Sprawdź logs
Connection refused → Sprawdź DATABASE_URL
ModuleNotFoundError → Brakuje pakietu w requirements.txt
Permission denied → Sprawdź build.sh permissions
```

---

## 9. KOSZTY NA RENDER (Free Plan)

| Komponent | Free Plan | Limit |
|-----------|-----------|-------|
| Web Service | ✅ Darmowy | 0.5 CPU, 512 MB RAM |
| PostgreSQL | ✅ Darmowy | 1 GB storage |
| Bandwidth | ✅ Darmowy | Nieograniczony |
| SSL Certificate | ✅ Darmowy | Automatyczny |
| Auto-deploy | ✅ Darmowy | Unlimited |

**Uwaga:** Free plan ma limity zasobów, ale wystarczający do prototypu/szkoły.

---

## 10. TESTOWE DANE I INSTRUKCJA UŻYTKOWANIA

### Zaloguj się jako:

**Pracownik:**
```
Login: john
Hasło: john123
Dostęp do: dodawanie dni, edycja, podsumowanie, export CSV
```

**Szef:**
```
Login: boss
Hasło: boss123
Dostęp do: panel szefa, zatwierdzanie, raport zespołu
```

**Admin:**
```
Login: admin
Hasło: admin123
Dostęp do: Django Admin (/admin/)
```

### Testowanie:

1. **Pracownik:**
   - Zaloguj się jako `john`
   - Przejdź do `/tracker/work-days/new/`
   - Dodaj dzień pracy z kilkoma przedziałami
   - Przejdź do `/tracker/monthly-summary/`
   - Sprawdź automatycznie wyliczone wynagrodzenie
   - Export CSV

2. **Szef:**
   - Zaloguj się jako `boss`
   - Przejdź do `/tracker/manager/`
   - Zauważ wpisy od `john`
   - Zatwierdź dzień pracy
   - Export raportu zespołu

---

## 11. LINKI I ZASOBY

| Zasób | Link |
|-------|------|
| Aplikacja (live) | https://work-time-app.onrender.com/accounts/login/ |
| GitHub (kod) | https://github.com/YOUR_USERNAME/work-time-app |
| Render Dashboard | https://dashboard.render.com |
| Django Docs | https://docs.djangoproject.com/ |
| PostgreSQL | https://www.postgresql.org/docs/ |

---

## 12. PODSUMOWANIE

### Projekt:
✅ System do ewidencji czasu pracy  
✅ Pełna funkcjonalność pracownik/szef  
✅ Automatyczne obliczanie wynagrodzeń  
✅ Raportowanie (CSV)  
✅ Walidacja danych  
✅ Bezpieczeństwo (CSRF, role-based access)  

### Technologie:
✅ Django 6.0.5  
✅ PostgreSQL  
✅ Bootstrap 5.3  
✅ Gunicorn  
✅ WhiteNoise  

### Render:
✅ Web Service (aplikacja Django)  
✅ PostgreSQL (baza danych)  
✅ Auto-deploy z GitHub  
✅ HTTPS  
✅ Free plan  


