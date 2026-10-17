"""ORBIT: recogida pública y auditoría reproducible; no predice rondas futuras."""
import datetime
import json
import math
import pathlib
import urllib.request

BASE = "https://clashwatchdog.com/api/v1/games/aviator/"
UTC = datetime.timezone.utc
DATA = pathlib.Path("data")

def read_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "ORBIT-Aviator-Research/2.0 (+https://github.com/quispillocharly-gif/Aviator-)"
    })
    with urllib.request.urlopen(req, timeout=18) as response:
        value = json.loads(response.read(2_000_000))
    if not isinstance(value, dict) or not isinstance(value.get("data"), (dict, list)):
        raise ValueError("Respuesta JSON de estructura no reconocida")
    return value

def read_previous(path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return fallback

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def wilson(k, n):
    z = 1.96
    p = k / n
    d = 1 + z*z/n
    center = (p + z*z/(2*n)) / d
    spread = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return [round(max(0, center-spread), 6), round(min(1, center+spread), 6)]

def snapshot(payload):
    d = payload["data"]
    meas = d.get("measurement") or {}
    n = int(meas["rounds"])
    rtp = float(meas["rtp"])
    if n < 1 or not (0 <= rtp <= 2.0):
        raise ValueError("Medición fuera de rango")
    # RTP a salida fija 2x = 2 * proporción de aciertos
    k = round(n * rtp / 2)
    if not (0 <= k <= n):
        raise ValueError("Aciertos implausibles")
    return {"n": n, "winsAt2x": k, "rtpAt2x": rtp,
            "asOf": meas.get("asOf"),
            "p50": (meas.get("quantiles") or {}).get("p50")}

def audit(samples, summary, freshness):
    d = summary["data"]
    current = snapshot(summary)
    claim = float((d.get("claim") or {}).get("rtp", .97))
    p0 = claim/2
    confidence = (d.get("measurement") or {}).get("ci95")
    result = {
        "analysisKind": "backward-looking statistical test",
        "source": "Clash Watchdog: aggregated Aviator demo observations",
        "game": "aviator", "rounds": current["n"],
        "lastRoundAt": d.get("lastRoundAt"),
        "claimRtp": claim,
        "observedRtpAt2x": current["rtpAt2x"],
        "ci95RtpAt2x": confidence,
        "claimInsideObservedCI": (bool(confidence) and len(confidence) == 2
                                  and float(confidence[0]) <= claim <= float(confidence[1])),
        "sampleCount": len(samples), "window": None,
        "status": "insufficient_new_rounds",
        "hasFutureSeed": False,
        "canPredictNextRound": False,
        "limitations": [
            "No official live per-round feed or unrevealed server seed is available.",
            "Rolling windows overlap; statistical flags are exploratory, not proof of bias.",
            "The observations may not match the casino where the user plays."
        ]
    }
    # Locate a recent cumulative snapshot >=500 completed rounds earlier.
    # Incremental wins are estimated from integer counts implied by exact RTP2x.
    older = [s for s in samples[:-1] if current["n"]-s["n"] >= 500
             and 0 <= current["winsAt2x"]-s["winsAt2x"] <= current["n"]-s["n"]]
    if older:
        base = older[-1]  # shortest supported non-overlapping incremental block
        dn = current["n"] - base["n"]
        dk = current["winsAt2x"] - base["winsAt2x"]
        proportion = dk / dn
        z = (proportion - p0) / math.sqrt(p0*(1-p0)/dn)
        pvalue = math.erfc(abs(z)/math.sqrt(2))
        # 0.001 is a screening threshold, NOT a universal test of fairness.
        flagged = pvalue < 0.001
        result["window"] = {
            "fromN": base["n"], "toN": current["n"], "rounds": dn,
            "winsAt2x": dk, "shareReached2x": round(proportion, 6),
            "ci95Reached2x": wilson(dk, dn),
            "expectedReached2x": p0,
            "zScore": round(z, 4), "exploratoryPValue": round(pvalue, 8),
            "screeningThreshold": .001
        }
        result["status"] = "review_anomaly" if flagged else "no_statistical_flag"
    elif current["n"] > 0:
        result["roundsNeededForWindow"] = (
            500 - (current["n"] - samples[0]["n"]) if samples else 500)
    if isinstance(freshness, dict):
        result["sourceStatus"] = (freshness.get("data") or {}).get("status")
    return result

def main():
    now = datetime.datetime.now(UTC).isoformat()
    summary = read_json(BASE + "summary")
    fresh = None
    try:
        fresh = read_json(BASE + "freshness")
    except Exception as exc:
        print("Aviso: sin frescura:", str(exc)[:160])
    fingerprints = None
    try:
        fingerprints = read_json(BASE + "datasets")
    except Exception as exc:
        print("Aviso: sin inventario de huellas diarias:", str(exc)[:160])
    current = snapshot(summary)
    previous = read_previous(DATA / "snapshots.json", [])
    if not isinstance(previous, list):
        previous = []
    previous = [s for s in previous if isinstance(s, dict)
                and isinstance(s.get("n"), int)
                and isinstance(s.get("winsAt2x"), int)
                and s["n"] <= current["n"]]
    if not previous or current["n"] > previous[-1]["n"]:
        previous.append(current)
    previous = previous[-720:]  # ~15 días a ritmo de 30 min
    report = audit(previous, summary, fresh)
    write(DATA / "snapshots.json", previous)
    write(DATA / "audit.json", {
        "computedAt": now, **report,
        "fairnessScope": "Only past-round evidence; not a future-result oracle."
    })
    write(DATA / "latest.json", {
        "retrievedAt": now,
        "source": "https://clashwatchdog.com/data",
        "summary": summary, "freshness": fresh, "datasets": fingerprints
    })
    print("Rondas observadas:", current["n"], "auditoría:", report["status"],
          "incremental:", (report["window"] or {}).get("rounds", 0))

if __name__ == "__main__":
    main()
