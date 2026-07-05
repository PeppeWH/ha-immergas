# Immergas Smartech Plus — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Integrazione non ufficiale per caldaie **Immergas** con gateway **Smartech Plus** per Home Assistant.

Comunica direttamente con il cloud `smartechplus.immergas.com` — nessuna modifica hardware, nessun accesso alla rete locale della caldaia.

## Funzionalità

- 🌡️ Temperatura ambiente in tempo reale
- 🌤️ Temperatura esterna rilevata dal gateway
- 🎯 Setpoint — imposta la temperatura desiderata
- 🔥 Stato riscaldamento (fiamma accesa/spenta)
- 🔄 Modalità termostato — Manuale / Automatico
- 🏠 Modalità caldaia — Inverno / Estate / Spento / Raffrescamento
- 🧭 Supporto multi-zona — una entità climate per ogni zona esposta dal gateway Smartech Plus
- ✅ Compatibile con Apple HomeKit tramite HomeKit Bridge

## Installazione tramite HACS

1. Apri HACS in Home Assistant
2. Vai su **Integrazioni** → menu `⋮` → **Repository personalizzati**
3. Aggiungi `https://github.com/PeppeWH/ha-immergas` come tipo **Integrazione**
4. Cerca "Immergas" e installa
5. Riavvia Home Assistant

## Configurazione

L'integrazione richiede i cookie di sessione del portale `smartechplus.immergas.com`. Si ottengono in 30 secondi:

### Come ottenere i token di autenticazione

1. Apri **Safari** (o Chrome) sul tuo Mac o PC
2. Vai su `https://smartechplus.immergas.com` e fai login con email e password
3. Una volta nella dashboard, apri gli **Strumenti Sviluppatore**:
   - Safari: menu **Sviluppo → Mostra Inspector Web** oppure `⌥⌘I`
   - Chrome: tasto destro → **Ispeziona** → tab **Console**
4. Nella tab **Console** digita questo comando e premi Invio:
   ```javascript
   document.cookie
   ```
5. Apparirà una stringa con tutti i cookie. Cerca e copia i valori di:
   - `tokenA=...`
   - `tokenB=...`
   - `PHPSESSID=...`

### Aggiungere l'integrazione in Home Assistant

1. Vai su **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**
2. Cerca **Immergas Smartech Plus**
3. Inserisci i tre valori copiati
4. L'integrazione rileva automaticamente il gateway e crea le entità

> **Nota:** I token hanno lunga durata (mesi). Se l'integrazione smette di funzionare, ripeti la procedura per ottenere nuovi token.

### Impianti multi-zona

Se il gateway Smartech Plus espone più zone, l'integrazione crea automaticamente una entità `climate` per ogni voce presente in `info` nella risposta `getDevices`. Ogni zona usa lo stesso `thingId` del gateway e il proprio indice `deviceN`, quindi i comandi di temperatura e modalità vengono inviati alla zona corretta.

Il nome visualizzato della zona viene preso dal campo `name` restituito dall'API. Se il nome non è disponibile, viene usato un fallback come `Immergas zona 1`.

## Entità create

| Entità | Tipo | Descrizione |
|--------|------|-------------|
| `climate.immergas_*` | Climate | Termostato con setpoint, modalità e preset caldaia; negli impianti multi-zona viene creata una entità per zona |
| `sensor.immergas_*_temperatura_ambiente` | Sensor | Temperatura ambiente in °C |
| `sensor.immergas_*_temperatura_esterna` | Sensor | Temperatura esterna in °C |
| `binary_sensor.immergas_*_riscaldamento_attivo` | Binary Sensor | Fiamma accesa/spenta |

## Integrazione con Apple HomeKit

Aggiungi `climate.immergas_*` all'integrazione **HomeKit Bridge** di Home Assistant. Il termostato apparirà in Apple Casa con temperatura attuale, soglia e modalità.

## Compatibilità

Testato con:
- Immergas Victrix Tera con gateway Smartech Plus
- Home Assistant OS 2026.x su HA Green

## Disclaimer

Integrazione non ufficiale, non affiliata né supportata da Immergas.

