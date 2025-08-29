from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import threading
import time
import requests
import pytz

# Importa módulos SNE
from visualizacao_avancada import VisualizacaoSNE
from linguagem_proprietaria import LinguagemSNE
from exploracao_temporal import ExploracaoTemporalSNE

app = Flask(__name__)
app.config["SECRET_KEY"] = "sne_secret_key_2024"
socketio = SocketIO(app, cors_allowed_origins="*")

# Instâncias dos módulos SNE
visualizacao = VisualizacaoSNE()
linguagem = LinguagemSNE()
exploracao = ExploracaoTemporalSNE()

# Configurações
symbol = "BTCUSDT"
interval = "1m"
limit = 100
br_tz = pytz.timezone("America/Sao_Paulo")

# Estado global da aplicação
estado_app = {
    "dados_atuais": None,
    "ultima_atualizacao": None,
    "interpretacoes_ativas": [],
    "zonas_magneticas": [],
    "ressonancias_detectadas": []
}

def buscar_dados_binance():
    try:
        print(f"[BINANCE] Buscando dados para {symbol}...")
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"[BINANCE] Erro na API: {response.status_code}")
            return None
            
        data = response.json()
        
        if not data or len(data) == 0:
            print("[BINANCE] Dados vazios da API")
            return None
        
        print(f"[BINANCE] Recebidos {len(data)} registros")
        
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "trades", "tbb", "tbq", "ignore"
        ])
        
        df["time"] = pd.to_datetime(df["open_time"], unit="ms").dt.tz_localize("UTC").dt.tz_convert(br_tz)
        df = df[["time", "open", "high", "low", "close", "volume", "trades"]].astype({
            "open": float, "high": float, "low": float, "close": float,
            "volume": float, "trades": int
        })
        df.set_index("time", inplace=True)
        
        # Calcula indicadores
        df["EMA8"] = df["close"].ewm(span=8).mean()
        df["EMA21"] = df["close"].ewm(span=21).mean()
        df["SMA200"] = df["close"].rolling(window=20).mean()
        df["densidade"] = 1 / (abs(df["EMA8"] - df["EMA21"]) + abs(df["EMA21"] - df["SMA200"]) + 1e-6)
        
        print(f"[BINANCE] Dados processados: {len(df)} registros, Preço atual: {df["close"].iloc[-1]:.2f}")
        return df
        
    except Exception as e:
        print(f"[BINANCE] Erro ao buscar dados: {e}")
        return None

def analisar_dados_sne(df):
    if df is None or df.empty:
        return {}
    
    analise = {
        "timestamp": datetime.now().isoformat(),
        "preco_atual": float(df["close"].iloc[-1]),
        "energia_magnetica": float(df["densidade"].iloc[-1]) if "densidade" in df.columns else 0,
        "zonas_magneticas": [],
        "ressonancias": [],
        "fluxos_gravitacionais": [],
        "interpretacoes": []
    }
    
    # Detecta zonas magnéticas
    if "densidade" in df.columns:
        zonas_altas = df[df["densidade"] > df["densidade"].quantile(0.9)]
        for _, row in zonas_altas.iterrows():
            zona = {
                "preco": float(row["close"]),
                "forca": float(row["densidade"]),
                "timestamp": row.name.isoformat()
            }
            analise["zonas_magneticas"].append(zona)
    
    # Detecta ressonâncias
    eventos_similares = exploracao.sobrepor_eventos_historicos(df, float(df["close"].iloc[-1]))
    analise["ressonancias"] = eventos_similares[:5]
    
    # Analisa fluxos gravitacionais
    tendencia = "ascendente" if df["EMA8"].iloc[-1] > df["EMA21"].iloc[-1] else "descendente"
    intensidade = abs(df["EMA8"].iloc[-1] - df["EMA21"].iloc[-1]) / df["close"].iloc[-1]
    
    fluxo = {
        "direcao": tendencia,
        "intensidade": float(intensidade),
        "timestamp": datetime.now().isoformat()
    }
    analise["fluxos_gravitacionais"].append(fluxo)
    
    return analise

def atualizar_dados_background():
    print("[SNE] Iniciando thread de atualização de dados...")
    while True:
        try:
            print("[SNE] Buscando dados da Binance...")
            df = buscar_dados_binance()
            if df is not None and not df.empty:
                estado_app["dados_atuais"] = df
                estado_app["ultima_atualizacao"] = datetime.now().isoformat()
                
                print(f"[SNE] Dados carregados: {len(df)} registros")
                
                # Executa análise SNE
                analise = analisar_dados_sne(df)
                
                # Emite dados via WebSocket
                dados = df.reset_index().to_dict("records")
                # Converte timestamps para string
                for registro in dados:
                    if "time" in registro:
                        registro["time"] = registro["time"].isoformat()
                
                socketio.emit("dados_atualizados", {
                    "dados": dados,
                    "analise": analise,
                    "timestamp": datetime.now().isoformat()
                })
                
                print(f"[SNE] Dados atualizados: {len(df)} registros, Preço: {df["close"].iloc[-1]:.2f}")
            else:
                print("[SNE] Nenhum dado recebido da Binance")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"[SNE] Erro na atualização: {e}")
            time.sleep(30)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dados")
def api_dados():
    print(f"[API] Solicitação de dados - Estado: {estado_app["dados_atuais"] is not None}")
    
    if estado_app["dados_atuais"] is not None and not estado_app["dados_atuais"].empty:
        dados = estado_app["dados_atuais"].reset_index().to_dict("records")
        # Converte timestamps para string
        for registro in dados:
            if "time" in registro:
                registro["time"] = registro["time"].isoformat()
        
        print(f"[API] Retornando {len(dados)} registros")
        return jsonify({
            "dados": dados,
            "ultima_atualizacao": estado_app["ultima_atualizacao"],
            "status": "sucesso"
        })
    else:
        print("[API] Dados não disponíveis")
        return jsonify({
            "status": "erro",
            "mensagem": "Dados não disponíveis"
        })

@app.route("/api/analise")
def api_analise():
    if estado_app["dados_atuais"] is not None:
        analise = analisar_dados_sne(estado_app["dados_atuais"])
        return jsonify(analise)
    else:
        return jsonify({
            "status": "erro",
            "mensagem": "Análise não disponível"
        })

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")
    emit("status", {"message": "Conectado ao SNE"})

@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")

@socketio.on("solicitar_dados")
def handle_solicitar_dados():
    print("[WebSocket] Cliente solicitou dados")
    
    if estado_app["dados_atuais"] is not None and not estado_app["dados_atuais"].empty:
        analise = analisar_dados_sne(estado_app["dados_atuais"])
        dados = estado_app["dados_atuais"].reset_index().to_dict("records")
        
        # Converte timestamps para string
        for registro in dados:
            if "time" in registro:
                registro["time"] = registro["time"].isoformat()
        
        print(f"[WebSocket] Enviando {len(dados)} registros")
        emit("dados_atualizados", {
            "dados": dados,
            "analise": analise,
            "timestamp": datetime.now().isoformat()
        })
    else:
        print("[WebSocket] Dados não disponíveis")
        emit("status", {"message": "Dados não disponíveis"})

if __name__ == "__main__":
    # Inicia thread de atualização
    thread_atualizacao = threading.Thread(target=atualizar_dados_background, daemon=True)
    thread_atualizacao.start()
    
    # Inicia servidor
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
