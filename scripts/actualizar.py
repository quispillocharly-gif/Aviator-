"""Consulta fuentes públicas con permiso de acceso. Nunca fabrica estadísticas."""
import datetime
import json
import pathlib
import urllib.request

BASE = 'https://clashwatchdog.com/api/v1/games/aviator/'

def read_json(url):
    request = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'User-Agent': 'ORBIT-Aviator-Statistics/1.0 (GitHub Actions; public aggregated data)'
    })
    with urllib.request.urlopen(request, timeout=18) as response:
        content = response.read(2_000_000)
    value = json.loads(content)
    if not isinstance(value, dict) or 'data' not in value:
        raise ValueError('API sin envoltorio data esperado; no se modifica la copia anterior')
    return value

def main():
    summary = read_json(BASE + 'summary')
    try:
        freshness = read_json(BASE + 'freshness')
    except Exception as exc:
        print('Frescura no disponible:', str(exc)[:220])
        freshness = None
    output = {
        'retrievedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': 'https://clashwatchdog.com/data',
        'summary': summary,
        'freshness': freshness,
    }
    path = pathlib.Path('data/latest.json')
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf8')
    print('Datos públicos guardados en', path)

if __name__ == '__main__':
    main()
