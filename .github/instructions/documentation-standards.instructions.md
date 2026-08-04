---
description: Use this template when writing documentation in README.md files to ensure clarity and consistency across projects.
applyTo: "docs/**/*.md"
---
# Documentation guidelines for README-files

- Documentation should always follow the same structure and style to ensure consistency across projects and make it easy for readers to find information.
- Use clear, concise danish language and avoid jargon or overly technical terms unless necessary.
- When writing documentation in README.md files, follow this structure, style and examples to ensure clarity and consistency:

# Projektnavn
[**Formål**](#formål) | [**Beskrivelse**](#beskrivelse) | [**Features**](#features) | [**Afhængigheder**](#afh%C3%A6ngigheder) | [**Schedule**](#schedule)

# Formål

Kort beskrivelse af applikationen, herunder formålet med løsningen.

*Eksempel:*
>  Applikationen udstiller et lille HTTP endpoint til at journalisere et *Ambulancebrev* (PDF) i SBSYS. Den modtager en base64-kodet PDF fra X-Flow, finder medarbejderen ud fra et DQ-nummer via Delta, slår medarbejderens personalesager op i SBSYS og journaliserer dokumentet på alle aktive personalesager.
> 
> Hvis der findes et delforløb på personalesagen med titlen **"07 Øvrige"**, journaliseres dokumentet på dette delforløb (ellers journaliseres direkte på sagen).

### Data-flow:

Enkelt linje som beskriver det konkrete dataflow (hvis løsningen er et Airflow- eller ETL-projekt)

*Eksempel:*
> Formular fra X-Flow → CPR træk fra Delta → Journalisering i SBSYS

## Beskrivelse

Detaljeret beskrivelse af den proces som løsningen varetager.

Procesbeskrivelsen opdeles i sektioner hvis løsningen varetager forskellige processer eller flere subprocesser.

Dette afsnit kan erstattes af `## Features`-afsnittet, hvis løsningen er et system frem for en automatiseret proces.

*Eksempel:*
> Applikationen varetager følgende proces:
> 1. Klienten (fx X-Flow) kalder `POST /api/journaliser` med JSON payload:
>    - `user`: streng i formatet `"<fulde navn> - <dq-nummer>"`
>    - `data`: base64-enkodet PDF (string)
> 2. API validerer at payload er til stede, at `data` er base64, og at det dekodede indhold starter med `%PDF`.
> 3. Hvis `TESTING=True`, bruges `TEST_CPR_NUMBER` direkte. Ellers:
>    - DQ-nummer udtrækkes fra `user`
>    - Delta forespørges (OIDC client credentials) for at finde medarbejderens CPR
> 4. SBSYS forespørges på personalesager for CPR-nummeret.
> 5. Kun aktive sager journaliseres (status-id `6`). Hvis der **ingen** aktive sager findes, returnerer API `404`.
> 6. For hver aktiv sag:
>    - SBSYS forespørges på delforløb for sagen
>    - Hvis der findes et delforløb med titlen **"07 Øvrige"**, journaliseres dokumentet på dette delforløb
>    - Ellers journaliseres dokumentet direkte på sagen
> 7. Dokumentet uploades/journaliseres med fast metadata (beskrivelse + dokumentnavn).

## Features

Beskrivelse af applikationens features. Dette afsnit bør kun inkluderes hvis løsningen er et system, eller varetager flere processer.

*Eksempel:*
> #### - CPR-filtrering til at opfange følsomme oplysninger inden afsendelse
> Backend matcher CPR-numre med regex og kan returnere fund via `POST /api/filter`, så klienten kan advare/handle før afsendelse.
> 
> #### - Anonymisering af følsomme oplysninger
> 
> Før beskeder sendes til Azure, bliver følsomt indhold redigeret ud (fx CPR) ved at erstatte fund med placeholders som `[REDACTED #1]`.

## Afhængigheder

Henvisninger til applikationens afhængigheder, kategoriseret og med links til officielle websites.

:key: | Airflow Connections (hvis løsningen er et airflow job)

*Eksempel:*
> **Postgres DB:**
> - **`jobindsats_db`**  
> 
>  **Conn Type**: Postgres
>
>  Bruges som `Connection id` i Airflow til at hente host, database, bruger, adgangskode og port til Postgres DB'en
>
>  *Required felter*:
>  - Connection id, Host, Database, Login, Password and Port (`5432`)

:cloud: | API'er, FTP-servere, CDN'er andre online services som applikationen kommunikerer med. Henvis til relevante miljøvariabler.

*Eksempel:*
> **Delta**
> 
>  Benyttes til udtræk af CPR-numre.
>  - API URL: `DELTA_URL` (`POST api/object/graph-query`)
>  - Auth: `DELTA_AUTH_URL` + `DELTA_REALM` (OIDC token endpoint)
> 
> **SBSYS/SBSIP**
> 
> Benyttes til fremsøgning af personalesager, samt journalisering af dokumenter.
> - SBSYS API URL: `SBSYS_URL(_TEST)`
> - Auth (password grant): `SBSIP_URL(_TEST)`

:heavy_dollar_sign: | Miljøvariabler som forventes at være populeret

*Eksempel*
> Applikationen læser miljøvariabler i [src/utils/config.py](src/utils/config.py).
>
> #### **Generelle variabler**
>
> | Navn | Default | Beskrivelse |
> |---|---:|---|
> | `PORT` | `8080` | Port som Flask kører på |
> | `DEBUG` | `False` | Flask debug + mere logning |
> | `POD_NAME` | `pod_name_not_set` | Bruges som label i readiness-metrics |
> | `TESTING` | `False` | Slår test-mode til (se nedenfor) |
> | `DRY_RUN` | `False` | Simulerer journalisering uden at foretage ændringer |
> 
> #### **SBSYS/SBSIP (production)** *(bruges når `TESTING=False`)*
>
> | Navn | Beskrivelse |
> |---|---|
> | `SBSYS_URL` | Base URL til SBSYS API |
> | `SBSIP_URL` | Base URL til SBSIP auth server |
> | `SBSYS_USERNAME` | Brugernavn til password grant |
> | `SBSYS_PASSWORD` | Password til password grant |
> | `SBSIP_CLIENT_ID` | OIDC client id |
> | `SBSIP_CLIENT_SECRET` | OIDC client secret |

## Udvikling

Beskrivelse af hvordan løsningen startes lokalt.
Overblik over eventuelle API endpoints som løsningen udstiller.
Notering af eventuelle hard-codede værdier, og hvordan værdierne kan ændres.

*Eksempel*:

> ### Lokal udvikling (Windows)
> 
> 1. Opret venv og installer dependencies:
>    ```bat
>    setup-dev-windows.cmd
>    ```
> 2. Start applikationen:
>    ```bat
>    python src\main.py
>    ```
> 3. Kør tests:
>    ```bat
>    pytest
>    ```
> 
> ### Lokal udvikling (Linux/CodeSpace)
> 
> 1. Opret venv og installer dependencies:
>    ```bash
>    source ./setup-dev-linux.sh
>    ```
> 2. Start applikationen:
>    ```bash
>    python src/main.py
>    ```
> 3. Kør tests:
>    ```bash
>    pytest
>    ```
> 
> ### Kørsel med Docker
> 
> - Byg og kør:
>   ```bash
>   docker compose up --build
>   ```
> 
> Applikationen eksponeres som standard på `http://localhost:8080`.
>
> ### API endpoints
> 
> - `GET /healthz` – healthcheck
> - `GET /metrics` – Prometheus metrics
> - `POST /api/journaliser` – journaliser ambulancebrev
> 
> #### Eksempel: kald til `POST /api/journaliser`
>
> **Payload**
>
> ```json
> {
>   "user": "Fornavn Efternavn - dq12345",
>   "data": "<base64-enkodet PDF>"
> }
> ```
> 
> ### Hard-coded værdier (og hvor de ændres)
>
> - **Aktiv sagsstatus**: `SBSYS_SAG_STATUS_ACTIVE = 6` i [src/api_endpoints.py](src/api_endpoints.py).
> - **Delforløb der journaliseres på**: `DELFORLOEB_TARGET_TITLE = "07 Øvrige"` i [src/api_endpoints.py](src/api_endpoints.py).
> - **Metadata ved journalisering** (beskrivelse, dokumentnavn, aktindsigt): fastlagt i `SbsysClient.journalize()` i [src/sbsys_client.py](src/sbsys_client.py).

## Schedule

Beskrivelse af hvornår automatiseringen afvikles. Dette afsnit skal kun inkluderes hvis løsningen er et Airflow-job.

*Eksempel:*
> ## Schedule
> 
> Jobbet er sat op til at køre automatisk på følgende tidspunkter:
> 
> - **Schedule:** `@daily` (kører én gang dagligt)
> - **Startdato:** 2026-04-08 (Europe/Copenhagen)
> - **Catchup:** `false`
> 
> **Retry-policy**
> - **Retries:** 1
> - **Retry delay:** 12 timer
