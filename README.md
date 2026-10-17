# ORBIT Aviator — laboratorio independiente de resultados públicos

**Abrir la web:** https://quispillocharly-gif.github.io/Aviator-/

**Estado:** página web publicada con GitHub Pages y automatización por GitHub Actions, sin Railway. Funciona en Android, sin archivos para importar ni datos manuales en el análisis principal.

## Qué hace realmente

1. Consulta estadísticas públicas independientes de Aviator en https://clashwatchdog.com/data (cada 30 segundos con la página abierta). Son resultados **observados en demos o mesas externas**, no una transmisión de la mesa del usuario.
2. Mantiene copias automáticas en `data/latest.json`, `data/snapshots.json` y `data/audit.json`, actualizadas por el workflow `.github/workflows/pages.yml` dos veces por hora. El historial se crea sin que el usuario introduzca nada.
3. Analiza incrementos comprobables de **al menos 500 rondas nuevas** y compara la proporción que llegó a 2× con el valor teórico bajo el RTP declarado de 97% (p = 0,485). Usa estadístico z y p exploratoria; señala desviaciones con umbral p < 0,001. Como las ventanas pueden solaparse, es un **detector de revisión**, no prueba concluyente de manipulación.
4. Consulta el inventario de huellas SHA-256 de archivos diarios sellados. **No** afirma verificar esos archivos sin acceder a las filas originales.
5. Incluye un verificador *opcional y local al navegador* del compromiso SHA-256 para **una ronda pasada**: requiere el hash publicado **antes** y la semilla revelada **después**. Este verificador no envía esas cadenas a nuestro servidor y no comprueba por sí solo el coeficiente calculado.
6. Los tests en `tests/test_audit.py` se ejecutan antes de cada publicación automatizada.

## Límites de seguridad y honestidad de datos

- El próximo resultado y su duración **no se conocen**: SPRIBE publica un compromiso SHA-256 y solo revela la semilla secreta después de la ronda. Utiliza SHA-512 para el resultado, junto con semillas de los jugadores. Documentación oficial: https://spribe.co/provably-fair
- No se ha identificado un método criptográfico legítimo que permita recuperar la semilla futura a partir del hash público.
- Clash Watchdog no entrega las filas crudas de las rondas mediante su API abierta; se obtienen por solicitud aparte. El análisis automático de la web opera sobre **estadísticas agregadas**, no sobre una secuencia de vuelos en vivo.
- No realiza apuestas, no accede a cuentas de casinos, no utiliza información privada, no ejecuta compras ni sugiere jugar.
- Un valor que cambia por una nueva muestra no es una señal de la siguiente ronda. Tampoco un test de anomalías convierte por sí solo los datos pasados en una predicción.
- Si una fuente falla, el panel lo señala y mantiene la última copia respaldada; nunca simula vuelos.

## Fuentes y licencia

- [Clash Watchdog — datos y API](https://clashwatchdog.com/data). Atribución: Clash Watchdog, CC BY 4.0.
- [Clash Watchdog — Aviator](https://clashwatchdog.com/games/aviator).
- [SPRIBE — Provably Fair](https://spribe.co/provably-fair).
- [GitHub Actions — ejecuciones](https://github.com/quispillocharly-gif/Aviator-/actions).

Proyecto separado de Differ, Rise/Fall y otras IA.
