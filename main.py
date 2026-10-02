from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

app = FastAPI(title="Stats Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/jsonScrap")
def get_json_match_stats(games: str = Query(..., description="ID del partido")):
    """Obtiene directamente las estadísticas JSON de un partido."""
    endpoint = "https://webws.365scores.com/web/game/stats/"
    query = urlencode({
        "appTypeId": 5,
        "langId": 29,
        "timezoneName": "America/Lima",
        "userCountryId": 112,
        "games": games,
    })
    request = Request(
        f"{endpoint}?{query}",
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
    )

    try:
        with urlopen(request, timeout=15) as response:
            jsonResult = json.loads(response.read().decode("utf-8"))

            games_data = jsonResult.get("games", [])
            if isinstance(games_data, list):
                game = games_data[0] if games_data else {}
            elif isinstance(games_data, dict):
                game = games_data
            else:
                game = {}

            home_competitor_id = game.get("homeCompetitor", {}).get("id")
            away_competitor_id = game.get("awayCompetitor", {}).get("id")
            local = {}
            visita = {}

            local["score"] = game.get("homeCompetitor", {}).get("score")
            visita["score"] = game.get("awayCompetitor", {}).get("score")

            fechaCompleta = game.get("startTime")
            fecha = None
            hora = None

            if fechaCompleta:
                fecha_ajustada = datetime.fromisoformat(fechaCompleta) - timedelta(hours=5)
                fecha = fecha_ajustada.date().isoformat()
                hora = fecha_ajustada.time().isoformat()

            statistic_fields = {
                "Posesión": "posesion",
                "Goles esperados": "goles_esperados",
                "Total Remates" : "total_remates",
                "Remates al arco" : "remates_al_arco",
                "Grandes chances" : "grandes_chances",
                "Saques de Esquina" : "saques_de_esquina",
                "Salvadas de Portero" : "salvadas_de_portero",
                "Faltas" : "faltas",
                "Faltas recibidas" : "faltas_recibidas",
                "Tarjetas Amarillas" : "tarjetas_amarillas",
                "Tarjetas Rojas" : "tarjetas_rojas",
                "Pases completados" : "pases_completados",
                "Pases en el propio campo" : "pases_en_el_campo_propio",
                "Pases en el campo contrario" : "pases_en_el_campo_contrario"
            }

            for field_name in statistic_fields.values():
                local[field_name] = "-1"
                visita[field_name] = "-1"

            for statistic in jsonResult.get("statistics", []):
                field_name = statistic_fields.get(statistic.get("name"))
                if field_name is None:
                    continue

                competitor_id = statistic.get("competitorId")
                value = statistic.get("value", "-1")
                if field_name == "posesion":
                    value = str(value).replace("%", "").strip()

                if competitor_id == home_competitor_id:
                    local[field_name] = value
                elif competitor_id == away_competitor_id:
                    visita[field_name] = value

            result = {}
            result["local"] = local
            result["visita"] = visita
            result["fecha"] = fecha
            result["hora"] = hora
            result["estadio"] = game.get("venue", {}).get("name")

            return result
    except HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Scores respondió con HTTP {error.code}.",
        ) from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"No se pudo obtener un JSON válido desde Scores: {error}",
        ) from error

@app.get("/health")
def health():
    return {"status": "alive"}