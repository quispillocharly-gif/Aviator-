# ORBIT Aviator — Análisis automático de estadísticas

Web estática **para GitHub Pages** que consulta automáticamente mediciones públicas independientes de Aviator. No pide archivos, multiplicadores ni conexión a la cuenta del casino.

**Datos:** https://clashwatchdog.com/data, API JSON abierta a cualquier origen. Se consultan estadísticas históricas, no el resultado de la próxima ronda. La fuente puede reflejar una demo diferente de la mesa del usuario. Attribution: Clash Watchdog, CC BY 4.0. El proveedor declara 97% de RTP para Aviator.

## Activar el enlace público en GitHub (único paso pendiente)

Proyecto instalado en: https://github.com/quispillocharly-gif/Aviator-

1. Abre https://github.com/quispillocharly-gif/Aviator-/settings/pages
2. En **Build and deployment > Source**, selecciona **GitHub Actions**.
3. El workflow `.github/workflows/pages.yml` publicará el sitio y actualizará un respaldo estadístico dos veces por hora. Puedes revisar su ejecución en https://github.com/quispillocharly-gif/Aviator-/actions
4. El enlace del analizador será: https://quispillocharly-gif.github.io/Aviator-/

No son necesarios archivos manuales ni ingresar multiplicadores. El navegador consulta la API pública cada 30 segundos mientras está abierto. Si falla, usa el respaldo `data/latest.json` actualizado por GitHub Actions; como última opción muestra los datos locales anteriores y avisa que son antiguos.

### Importante

- **No** conecta con la cuenta del casino ni recibe el streaming completo de los vuelos.
- No hay evidencia de que las rondas anteriores permitan pronosticar el próximo multiplicador de Aviator.
- El gráfico de evolución indica aumento en la cantidad de rondas *de la muestra agregada*, no las rondas individuales.
- La API está documentada públicamente, pero su esquema podría cambiar. Si faltan campos, el panel muestra `—` y permite abrir diagnóstico de conexión; no muestra números falsos.
- Si la API o GitHub fallan, el proyecto sigue mostrando que no está conectado en vez de generar rondas simuladas.

## Licencias y fuentes

Datos e indicadores publicados: [Clash Watchdog](https://clashwatchdog.com/data) (CC BY 4.0), [página de Aviator](https://clashwatchdog.com/games/aviator). Marca y producto original Aviator: SPRIBE.