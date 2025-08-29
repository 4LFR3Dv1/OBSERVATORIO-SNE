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
app.config['SECRET_KEY'] = 'sne_secret_key_2024'
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
    'dados_atuais': None,
    'ultima_atualizacao': None,
    'interpretacoes_ativas': [],
    'zonas_magneticas': [],
    'ressonancias_detectadas': []
}

def buscar_dados_binance():
    """
    Busca dados da Binance
    """
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"Erro na API Binance: {response.status_code}")
            return None
            
        data = response.json()
        
        if not data or len(data) == 0:
            print("Dados vazios da API Binance")
            return None
        
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
        
        print(f"Dados carregados: {len(df)} registros, Preço atual: {df['close'].iloc[-1]:.2f}")
        return df
        
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None

def analisar_dados_sne(df):
    """
    Executa análise completa do SNE
    """
    if df is None or df.empty:
        return {}
    
    analise = {
        'timestamp': datetime.now().isoformat(),
        'preco_atual': float(df['close'].iloc[-1]),
        'energia_magnetica': float(df['densidade'].iloc[-1]) if 'densidade' in df.columns else 0,
        'zonas_magneticas': [],
        'ressonancias': [],
        'fluxos_gravitacionais': [],
        'interpretacoes': []
    }
    
    # Detecta zonas magnéticas
    if 'densidade' in df.columns:
        zonas_altas = df[df['densidade'] > df['densidade'].quantile(0.9)]
        for _, row in zonas_altas.iterrows():
            zona = {
                'preco': float(row['close']),
                'forca': float(row['densidade']),
                'timestamp': row.name.isoformat()
            }
            analise['zonas_magneticas'].append(zona)
    
    # Detecta ressonâncias
    eventos_similares = exploracao.sobrepor_eventos_historicos(df, float(df['close'].iloc[-1]))
    analise['ressonancias'] = eventos_similares[:5]  # Top 5
    
    # Analisa fluxos gravitacionais
    tendencia = 'ascendente' if df['EMA8'].iloc[-1] > df['EMA21'].iloc[-1] else 'descendente'
    intensidade = abs(df['EMA8'].iloc[-1] - df['EMA21'].iloc[-1]) / df['close'].iloc[-1]
    
    fluxo = {
        'direcao': tendencia,
        'intensidade': float(intensidade),
        'timestamp': datetime.now().isoformat()
    }
    analise['fluxos_gravitacionais'].append(fluxo)
    
    # Gera interpretações
    if analise['zonas_magneticas']:
        for zona in analise['zonas_magneticas']:
            interpretacao = linguagem.interpretar_campo_magnetico(df, zona['preco'], zona['forca'])
            analise['interpretacoes'].append(interpretacao)
    
    if analise['ressonancias']:
        interpretacao = linguagem.interpretar_ressonancia_temporal(
            analise['preco_atual'], analise['ressonancias']
        )
        if interpretacao:
            analise['interpretacoes'].append(interpretacao)
    
    return analise

def atualizar_dados_background():
    """
    Thread para atualização contínua dos dados
    """
    while True:
        try:
            df = buscar_dados_binance()
            if df is not None:
                estado_app['dados_atuais'] = df
                estado_app['ultima_atualizacao'] = datetime.now().isoformat()
                
                # Executa análise SNE
                analise = analisar_dados_sne(df)
                
                # Emite dados via WebSocket
                socketio.emit('dados_atualizados', {
                    'dados': df.to_dict('records'),
                    'analise': analise,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Atualiza estado
                estado_app['interpretacoes_ativas'] = analise.get('interpretacoes', [])
                estado_app['zonas_magneticas'] = analise.get('zonas_magneticas', [])
                estado_app['ressonancias_detectadas'] = analise.get('ressonancias', [])
                
                print(f"[SNE] Dados atualizados: {len(df)} registros, Preço: {df['close'].iloc[-1]:.2f}")
            
            time.sleep(10)  # Atualiza a cada 10 segundos para ser mais responsivo
            
        except Exception as e:
            print(f"Erro na atualização: {e}")
            time.sleep(30)  # Espera mais tempo em caso de erro
            
        except Exception as e:
            print(f"Erro na atualização: {e}")
            time.sleep(60)  # Espera mais tempo em caso de erro

# Rotas da aplicação
@app.route('/')
def index():
    """
    Página principal
    """
    return render_template('index.html')

@app.route('/api/dados')
def api_dados():
    """
    API para obter dados atuais
    """
    if estado_app['dados_atuais'] is not None:
        return jsonify({
            'dados': estado_app['dados_atuais'].to_dict('records'),
            'ultima_atualizacao': estado_app['ultima_atualizacao'],
            'status': 'sucesso'
        })
    else:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Dados não disponíveis'
        })

@app.route('/api/analise')
def api_analise():
    """
    API para obter análise SNE
    """
    if estado_app['dados_atuais'] is not None:
        analise = analisar_dados_sne(estado_app['dados_atuais'])
        return jsonify(analise)
    else:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Análise não disponível'
        })

@app.route('/api/interpretacoes')
def api_interpretacoes():
    """
    API para obter interpretações da linguagem SNE
    """
    return jsonify({
        'interpretacoes_ativas': estado_app['interpretacoes_ativas'],
        'vocabulario': linguagem.vocabulario,
        'relatorio': linguagem.gerar_relatorio_linguagem()
    })

@app.route('/api/exploracao/<timestamp>')
def api_exploracao(timestamp):
    """
    API para exploração temporal
    """
    if estado_app['dados_atuais'] is not None:
        try:
            df_zoom, resultado = exploracao.zoom_temporal_magnetico(
                estado_app['dados_atuais'], timestamp
            )
            return jsonify({
                'zoom_data': df_zoom.to_dict('records') if df_zoom is not None else [],
                'resultado': resultado
            })
        except Exception as e:
            return jsonify({
                'status': 'erro',
                'mensagem': str(e)
            })
    else:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Dados não disponíveis'
        })

@app.route('/api/visualizacao')
def api_visualizacao():
    """
    API para gerar visualização
    """
    if estado_app['dados_atuais'] is not None:
        try:
            # Gera visualização
            df = estado_app['dados_atuais']
            
            # Limpa camadas anteriores
            visualizacao.limpar_camadas()
            
            # Cria zonas magnéticas
            for zona in estado_app['zonas_magneticas']:
                visualizacao.criar_zona_magnetica(
                    zona['preco'] - 25, zona['preco'] + 25,
                    zona['forca'], pd.to_datetime(zona['timestamp'])
                )
            
            # Cria ressonâncias
            for ressonancia in estado_app['ressonancias_detectadas'][:3]:
                visualizacao.criar_ressonancia_temporal(
                    ressonancia['preco'],
                    pd.to_datetime(ressonancia['timestamp']),
                    [ressonancia]
                )
            
            # Cria HUD
            visualizacao.criar_hud_evoluido(
                df,
                estado_app['zonas_magneticas'],
                estado_app['ressonancias_detectadas']
            )
            
            # Exporta visualização
            nome_arquivo = f"visualizacao_sne_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            visualizacao.exportar_visualizacao(nome_arquivo)
            
            return send_file(nome_arquivo, mimetype='image/png')
            
        except Exception as e:
            return jsonify({
                'status': 'erro',
                'mensagem': str(e)
            })
    else:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Dados não disponíveis'
        })

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """
    Cliente conectado
    """
    print('Cliente conectado')
    emit('status', {'message': 'Conectado ao SNE'})

@socketio.on('disconnect')
def handle_disconnect():
    """
    Cliente desconectado
    """
    print('Cliente desconectado')

@socketio.on('solicitar_dados')
def handle_solicitar_dados():
    """
    Cliente solicita dados
    """
    if estado_app['dados_atuais'] is not None:
        analise = analisar_dados_sne(estado_app['dados_atuais'])
        emit('dados_atualizados', {
            'dados': estado_app['dados_atuais'].to_dict('records'),
            'analise': analise,
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    # Inicia thread de atualização
    thread_atualizacao = threading.Thread(target=atualizar_dados_background, daemon=True)
    thread_atualizacao.start()
    
    # Inicia servidor
    port = int(os.environ.get('PORT', 8080))  # Mudando para porta 8080
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
