# Nocturno local — 2026-07-31

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus octubre).
**Branch:** `nocturno/local-2026-07-31-ota-versioning-tests` (pusheado a origin).

## Tarea elegida y por qué
El backlog de branches nocturnos sin mergear es enorme (galgas 6+ noches, ~34 branches en total) y las últimas noches ya construyeron el tooling para **drenarlo** (cola de merge clasificada + auto-resolución de conflictos-docs). Sumar otro "modelo" python de análisis tenía valor marginal.

Buscando trabajo de **software real, verificable offline y NO ya brancheado**, apareció un hueco concreto y de prioridad octubre: la lógica de **versionado OTA del dashboard de galgas** (`compareSemver`, `isVersionNewer`, `getProfileSuffix`, `getMaxSilenceSec`) vivía **inline en `web/src/App.jsx` (1700 líneas) sin un solo test**. Esa lógica decide si una placa en campo baja o no una OTA. Un fallo ahí = placa en **loop de reflasheo** (falso "newer") o **pegada en firmware viejo** (falso "no newer") — exactamente lo que no puede pasar en la parada. "Evidencia o no pasó": no tenía evidencia ninguna.

## Qué hice (quirúrgico, sin cambio de comportamiento)
1. **Extraje** `PP_PROFILES` + las 4 funciones puras a **`web/src/lib/versioning.js`** (ESM, fuente única de verdad) y las **importé de vuelta** en `App.jsx`. Cero lógica nueva, cero cambio de comportamiento — solo mover a un módulo testeable e importable (alineado con la doctrina "una sola fuente de verdad": no duplicar el umbral a mano). Los ~14 call-sites siguen usando los mismos nombres vía import.
2. **Red de tests** `web/src/lib/versioning.test.js` con el runner **nativo de node** (`node --test`) — **cero dependencias nuevas** (el `package.json` ya tiene `"type": "module"`). **18 tests**: el caso que motivó el helper (`"3.2.9" < "3.2.10"`, no lexicográfico), major/minor/patch, nulls/undefined, fallback no-semver, cobertura de todos los suffixes de `PP_PROFILES`, y **dos bordes peligrosos fijados con evidencia** (ver abajo).

## Hallazgo (con test que lo demuestra, NO corregido — generator≠evaluator)
`compareSemver` desempata por comparación de **string** cuando `X.Y.Z` + profile coinciden. Consecuencia: `"3.2.0-B-pmax"` aparece como "newer" que `"3.2.0-A-pmax"` **solo porque `'B' > 'A'`**. El aislamiento real entre placa A y B **no lo da `compareSemver`** sino el filtrado por `device_id`/`device_type`/suffix en el call-site de `App.jsx`. Mientras A y B **compartan el target `emisor`** (que es justo lo que denuncia **QUE_FALTA #5**), ese filtro del call-site es lo único que evita empujar el `.bin` de B a una placa A. Fijar el target por placa en `firmware_versions` cierra el ítem. Anotado en QUE_FALTA #5 para @backend + @firmware. (El orden cross-profile también es lexicográfico arbitrario, mitigado por el filtro same-suffix.)

## Cómo verificarlo (comandos exactos)
```
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-31-ota-versioning-tests
cd web
node --test src/lib/versioning.test.js      # -> tests 18 / pass 18 / fail 0
npm run build                               # -> vite build OK (395 modules, ~4.7s)
```
El warning de "chunks > 500 kB" del build es **preexistente** (bundle del dashboard, no lo introduje).

## Qué quedó sin verificar por hardware
Nada requería hardware: es lógica pura + build del dashboard, todo verificado offline. Lo que **no** hace este branch (fuera de alcance, doctrina): **corregir** el desempate A/B — eso es una decisión de data-model (target por placa) que toca backend+firmware y se valida con las placas reales; queda documentado como hallazgo en QUE_FALTA #5.

## Estado
- Branch `nocturno/local-2026-07-31-ota-versioning-tests` pusheado (2 commits: extracción+tests, y nota en QUE_FALTA).
- `QUE_FALTA.md` de galgas: ítem #5 anotado `EN BRANCH ... (pendiente de merge)`.
- 4 repos intactos salvo el branch de trabajo. `data/field_captures` no tocado.
