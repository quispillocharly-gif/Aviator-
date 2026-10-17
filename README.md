# ORBIT Aviator — Análisis automático de estadísticas

Web estática **para GitHub Pages** que consulta automáticamente mediciones públicas independientes de Aviator. No pide archivos, multiplicadores ni conexión a la cuenta del casino.

**Datos:** https://clashwatchdog.com/data, API JSON abierta a cualquier origen. Se consultan estadísticas históricas, no el resultado de la próxima ronda. La fuente puede reflejar una demo diferente de la mesa del usuario. Attribution: Clash Watchdog, CC BY 4.0. El proveedor declara 97% de RTP para Aviator.

## Activar el enlace público en GitHub (única configuración inicial)

1. Repositorio creado: `quispillocharly-gif/Aviator-`.
2. Sube a la raíz todo el contenido de este ZIP, conservando la carpeta `.github/workflows` y `scripts`.
3. En **Settings > Pages > Build and deployment**, elige `Deploy from a branch`, rama `main`, carpeta `/(root)` y guarda.
4. En **Actions** habilita los workflows si GitHub lo solicita. El respaldo actualiza `data/latest.json` cada 30 minutos (también se puede ejecutar a mano). En **Settings > Actions > General > Workflow permissions**, permite `Read and write permissions` si tu configuración bloquea los commits de Actions.
5. Abre `https://quispillocharly-gif.github.io/Aviator-/` en Android. No se requieren credenciales ni importaciones.

La interfaz consulta el API directamente cada 30 segundos mientras está abierta. Si falla, intenta usar la última copia `data/latest.json` guardada por GitHub Actions, y finalmente una copia local anterior. Nunca inventa estadísticas, y marca las copias de respaldo como tal.

### Importante

- **No** conecta con la cuenta del casino ni recibe el streaming completo de los vuelos.
- No hay evidencia de que las rondas anteriores permitan pronosticar el próximo multiplicador de Aviator.
- El gráfico de evolución indica aumento en la cantidad de rondas *de la muestra agregada*, no las rondas individuales.
- La API está documentada públicamente, pero su esquema podría cambiar. Si faltan campos, el panel muestra `—` y permite abrir diagnóstico de conexión; no muestra números falsos.
- Si la API o GitHub fallan, el proyecto sigue mostrando que no está conectado en vez de generar rondas simuladas.

## Licencias y fuentes

Datos e indicadores publicados: [Clash Watchdog](https://clashwatchdog.com/data) (CC BY 4.0), [página de Aviator](https://clashwatchdog.com/games/aviator). Marca y producto original Aviator: SPRIBE.