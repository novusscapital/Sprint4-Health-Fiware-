from dash import Dash, html, dcc, Output, Input
import requests
import random

external_stylesheets =[
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
]

# ==========================
# CONFIGURAÇÕES BÁSICAS
# ==========================

# Cores do tema
COLORS = {
    "header_bg": "#008000",   # verde
    "header_text": "#FFFFFF", # branco
    "page_bg": "#FFFFFF",     # branco
    "card_border": "#008000", # verde
    "card_label": "#008000",  # verde
    "card_value": "#333333"   # cinza escuro (texto)
}

# URL do FIWARE / Orion (AJUSTAR DEPOIS)
ORION_BASE_URL = "http://20.63.91.180:1026"
ENTITY_ID = "HealthUser:dev-esp32-001"

FIWARE_SERVICE = "health"
FIWARE_SERVICE_PATH = "/"

def fetch_data():
    """
    Busca os dados reais do Orion/FIWARE.
    Cai para valores mock se der erro (404, timeout, etc.).
    """
    url = f"{ORION_BASE_URL}/v2/entities/{ENTITY_ID}"
    headers = {
        "Fiware-Service": FIWARE_SERVICE,
        "Fiware-ServicePath": FIWARE_SERVICE_PATH,
    }
    params = {"options": "keyValues"}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=3)
        resp.raise_for_status()
        data = resp.json()
        print("DEBUG ORION:", data)  # pra você ver no terminal o que está vindo

        # Suporta tanto nomes bonitos quanto t/h/d
        temp = data.get("bodyTemperature", data.get("t", 0))
        hr   = data.get("heartRate", data.get("h", 0))
        dist = data.get("distanceKm", data.get("d", 0))

        return {
            "bodyTemperature": float(temp),
            "heartRate": int(hr),
            "distanceKm": float(dist),
        }

    except Exception as e:
        print("Erro ao buscar dados do Orion:", e)

        # MOCK pra não quebrar enquanto algo der errado
        return {
            "bodyTemperature": 30.0,
            "heartRate": 50,
            "distanceKm": 0.148,
        }


# ==========================
# DASH APP
# ==========================

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={
        "backgroundColor": COLORS["page_bg"],
        "minHeight": "100vh",
        "padding": "24px",
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        # HEADER
        html.Div(
            style={
                "backgroundColor": COLORS["header_bg"],
                "color": COLORS["header_text"],
                "padding": "18px 24px",
                "fontSize": "26px",
                "fontWeight": "bold",
                "borderRadius": "12px",
                "marginBottom": "24px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
            },
            children=[
                html.Div(
                    children=[
                        html.I(
                            className="fa-solid fa-heart-pulse",
                            style={"marginRight": "12px", "fontSize": "26px"},
                        ),
                        "Health Monitor – ESP32",
                    ]
                ),
                html.Div(
                    "FIWARE Sprint 4",
                    style={
                        "fontSize": "14px",
                        "opacity": 0.9,
                        "fontWeight": "normal",
                    },
                ),
            ],
        ),

        # CARDS
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
            },
            children=[
                # Temperatura
                html.Div(
                    id="card-temp",
                    style={
                        "flex": "1",
                        "minWidth": "240px",
                        "backgroundColor": COLORS["page_bg"],
                        "border": f"2px solid {COLORS['card_border']}",
                        "borderRadius": "16px",
                        "padding": "18px 20px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.06)",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "marginBottom": "10px",
                            },
                            children=[
                                html.I(
                                    className="fa-solid fa-temperature-half",
                                    style={
                                        "color": COLORS["card_label"],
                                        "fontSize": "26px",
                                        "marginRight": "10px",
                                    },
                                ),
                                html.Span(
                                    "Temperatura Corporal (°C)",
                                    style={
                                        "color": COLORS["card_label"],
                                        "fontWeight": "bold",
                                        "fontSize": "16px",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-temp",
                            style={
                                "color": COLORS["card_value"],
                                "fontSize": "34px",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                ),

                # Batimentos
                html.Div(
                    id="card-hr",
                    style={
                        "flex": "1",
                        "minWidth": "240px",
                        "backgroundColor": COLORS["page_bg"],
                        "border": f"2px solid {COLORS['card_border']}",
                        "borderRadius": "16px",
                        "padding": "18px 20px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.06)",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "marginBottom": "10px",
                            },
                            children=[
                                html.I(
                                    className="fa-solid fa-heart-pulse",
                                    style={
                                        "color": COLORS["card_label"],
                                        "fontSize": "26px",
                                        "marginRight": "10px",
                                    },
                                ),
                                html.Span(
                                    "Frequência Cardíaca (bpm)",
                                    style={
                                        "color": COLORS["card_label"],
                                        "fontWeight": "bold",
                                        "fontSize": "16px",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-hr",
                            style={
                                "color": COLORS["card_value"],
                                "fontSize": "34px",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                ),

                # Distância
                html.Div(
                    id="card-dist",
                    style={
                        "flex": "1",
                        "minWidth": "240px",
                        "backgroundColor": COLORS["page_bg"],
                        "border": f"2px solid {COLORS['card_border']}",
                        "borderRadius": "16px",
                        "padding": "18px 20px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.06)",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "marginBottom": "10px",
                            },
                            children=[
                                html.I(
                                    className="fa-solid fa-person-running",
                                    style={
                                        "color": COLORS["card_label"],
                                        "fontSize": "26px",
                                        "marginRight": "10px",
                                    },
                                ),
                                html.Span(
                                    "Distância Percorrida (km)",
                                    style={
                                        "color": COLORS["card_label"],
                                        "fontWeight": "bold",
                                        "fontSize": "16px",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-dist",
                            style={
                                "color": COLORS["card_value"],
                                "fontSize": "34px",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                ),
            ],
        ),

        # Intervalo de atualização
        dcc.Interval(
            id="interval-update",
            interval=5_000,  # 5000 ms = 5 s
            n_intervals=0,
        ),
    ],
)



# ==========================
# CALLBACK – atualiza cards
# ==========================

@app.callback(
    Output("value-temp", "children"),
    Output("value-hr", "children"),
    Output("value-dist", "children"),
    Input("interval-update", "n_intervals"),
)
def update_cards(_):
    data = fetch_data()

    temp_txt = f"{data['bodyTemperature']:.1f} °C"
    hr_txt = f"{data['heartRate']} bpm"
    dist_txt = f"{data['distanceKm']:.3f} km"

    return temp_txt, hr_txt, dist_txt


if __name__ == "__main__":
    # debug=True só em desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)
