Struktura projektu
- app.py – główny kod aplikacji Flask
- templates/index.html – szablon HTML
- Dockerfile – konfiguracja obrazu Docker
- requirements.txt – zależności Pythona
- .github/workflows/docker-pipeline.yml – definicja pipeline GitHub Actions

---

## WeatherApp — Prognoza Pogody

# Opis projektu
Aplikacja webowa napisana w Python Flask, która pozwala sprawdzić aktualną pogodę dla wybranego miasta i kraju.  
Dane pogodowe pobierane są z API OpenWeatherMap.

---

## Jak działa pipeline CI/CD?

- Pipeline uruchamia się automatycznie przy każdym pushu na gałąź `main` lub może być wywołany ręcznie z poziomu interfejsu GitHub.
- Klonuje repozytorium i przygotowuje środowisko buildowe na maszynie wirtualnej.
- Loguje się do GitHub Container Registry (GHCR) oraz do DockerHub (w celu wykorzystania cache).
- Buduje wieloplatformowy obraz Docker (architektury amd64 i arm64) z wykorzystaniem cache i wypycha go do GHCR.
- Skanuje zbudowany obraz pod kątem krytycznych i wysokich podatności (CVE) przy użyciu narzędzia Trivy.
- Jeśli skanowanie zakończy się pomyślnie, wyświetla komunikat potwierdzający poprawne zbudowanie i opublikowanie obrazu.

---

## Jak uruchomić aplikację lokalnie?

1. Zaloguj się do GitHub Container Registry (GHCR):
   docker login ghcr.io -u <github-username> -p <personal-access-token>
2. Pobierz najnowszy obraz:
   docker pull ghcr.io/tobiasz-lab/weatherapp:latest
3. Uruchom kontener na lokalnymporcie 5000:
   docker run -p 5000:5000 ghcr.io/tobiasz-lab/weatherapp:latest
4. Otwórz przeglądarkę i przejdź do adresu:
   http://localhost:5000


