import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import pearsonr
import json
import os

class ExploracaoTemporalSNE:
    """
    Sistema de Exploração Temporal do SNE
    - Zoom temporal magnético
    - Mapeamento de ciclos fractais
    - Detecção de ressonâncias históricas
    """
    
    def __init__(self):
        self.caminho_ciclos = "ciclos_fractais.json"
        self.ciclos_detectados = self.carregar_ciclos()
        self.ressonancias_temporais = []
        
    def carregar_ciclos(self):
        """
        Carrega ciclos fractais detectados anteriormente
        """
        if os.path.exists(self.caminho_ciclos):
            with open(self.caminho_ciclos, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'ciclos': [],
                'fractais': [],
                'ressonancias': []
            }
    
    def salvar_ciclos(self):
        """
        Salva ciclos detectados
        """
        with open(self.caminho_ciclos, 'w', encoding='utf-8') as f:
            json.dump(self.ciclos_detectados, f, indent=2, ensure_ascii=False)
    
    def detectar_ciclos_fractais(self, df, janela_min=10, janela_max=100):
        """
        Detecta ciclos fractais em diferentes escalas temporais
        """
        precos = df['close'].values
        timestamps = df.index.values
        
        ciclos_encontrados = []
        
        # Testa diferentes tamanhos de janela
        for janela in range(janela_min, min(janela_max, len(precos)//2)):
            # Divide os dados em segmentos
            segmentos = []
            for i in range(0, len(precos) - janela, janela//2):
                segmento = precos[i:i+janela]
                if len(segmento) == janela:
                    segmentos.append(segmento)
            
            # Compara segmentos adjacentes
            for i in range(len(segmentos) - 1):
                seg1 = segmentos[i]
                seg2 = segmentos[i+1]
                
                # Calcula correlação entre segmentos
                if len(seg1) == len(seg2):
                    correlacao, p_valor = pearsonr(seg1, seg2)
                    
                    if correlacao > 0.7 and p_valor < 0.05:  # Correlação significativa
                        ciclo = {
                            'tamanho': janela,
                            'correlacao': correlacao,
                            'p_valor': p_valor,
                            'inicio_seg1': i * janela//2,
                            'inicio_seg2': (i+1) * janela//2,
                            'timestamp_detectado': datetime.now().isoformat()
                        }
                        ciclos_encontrados.append(ciclo)
        
        # Salva ciclos encontrados
        self.ciclos_detectados['ciclos'].extend(ciclos_encontrados)
        self.salvar_ciclos()
        
        return ciclos_encontrados
    
    def zoom_temporal_magnetico(self, df, centro_timestamp, raio_horas=24):
        """
        Aplica zoom temporal magnético em uma região específica
        """
        # Converte timestamp para datetime se necessário
        if isinstance(centro_timestamp, str):
            centro_timestamp = pd.to_datetime(centro_timestamp)
        
        # Define janela de zoom
        inicio = centro_timestamp - timedelta(hours=raio_horas)
        fim = centro_timestamp + timedelta(hours=raio_horas)
        
        # Filtra dados na janela
        df_zoom = df[(df.index >= inicio) & (df.index <= fim)].copy()
        
        if df_zoom.empty:
            return None, "Nenhum dado encontrado na janela temporal"
        
        # Calcula intensidade magnética na região
        intensidade_magnetica = self.calcular_intensidade_magnetica(df_zoom)
        
        # Detecta ressonâncias na região
        ressonancias = self.detectar_ressonancias_regiao(df_zoom)
        
        resultado_zoom = {
            'centro': centro_timestamp.isoformat(),
            'raio_horas': raio_horas,
            'dados_filtrados': len(df_zoom),
            'intensidade_magnetica': intensidade_magnetica,
            'ressonancias_detectadas': len(ressonancias),
            'periodo_mais_ressonante': self.identificar_periodo_ressonante(df_zoom),
            'padroes_fractais': self.detectar_padroes_fractais(df_zoom)
        }
        
        return df_zoom, resultado_zoom
    
    def calcular_intensidade_magnetica(self, df):
        """
        Calcula a intensidade magnética de uma região temporal
        """
        if 'densidade' in df.columns:
            return df['densidade'].mean()
        
        # Calcula baseado em volatilidade e volume
        volatilidade = df['close'].pct_change().std()
        volume_medio = df['volume'].mean() if 'volume' in df.columns else 0
        
        # Normaliza valores
        intensidade = (volatilidade * 1000) + (volume_medio / 1000)
        return min(intensidade, 100)  # Limita a 100
    
    def detectar_ressonancias_regiao(self, df):
        """
        Detecta ressonâncias em uma região específica
        """
        ressonancias = []
        precos = df['close'].values
        
        # Procura por padrões repetitivos
        for i in range(len(precos) - 20):
            padrao = precos[i:i+10]
            
            # Procura por padrões similares
            for j in range(i+20, len(precos) - 10):
                padrao_comparacao = precos[j:j+10]
                
                # Calcula similaridade
                correlacao, _ = pearsonr(padrao, padrao_comparacao)
                
                if correlacao > 0.8:  # Alta similaridade
                    ressonancia = {
                        'padrao_inicio': i,
                        'repeticao_inicio': j,
                        'correlacao': correlacao,
                        'preco_medio': np.mean(padrao)
                    }
                    ressonancias.append(ressonancia)
        
        return ressonancias
    
    def identificar_periodo_ressonante(self, df):
        """
        Identifica o período mais ressonante em uma região
        """
        if len(df) < 50:
            return "Dados insuficientes para análise"
        
        # Calcula autocorrelação
        precos = df['close'].values
        autocorr = np.correlate(precos, precos, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Normaliza
        autocorr = autocorr / autocorr[0]
        
        # Encontra picos de autocorrelação
        picos, _ = signal.find_peaks(autocorr[:len(autocorr)//2], height=0.5)
        
        if len(picos) > 0:
            periodo_principal = picos[0]
            return f"Período ressonante: {periodo_principal} candles"
        else:
            return "Nenhum período ressonante detectado"
    
    def detectar_padroes_fractais(self, df):
        """
        Detecta padrões fractais em diferentes escalas
        """
        padroes = []
        precos = df['close'].values
        
        # Testa diferentes escalas
        escalas = [5, 10, 20, 50]
        
        for escala in escalas:
            if len(precos) >= escala * 3:
                # Divide em segmentos da escala
                segmentos = []
                for i in range(0, len(precos) - escala, escala//2):
                    segmento = precos[i:i+escala]
                    if len(segmento) == escala:
                        segmentos.append(segmento)
                
                # Verifica similaridade entre segmentos
                if len(segmentos) >= 2:
                    similaridades = []
                    for i in range(len(segmentos)):
                        for j in range(i+1, len(segmentos)):
                            corr, _ = pearsonr(segmentos[i], segmentos[j])
                            similaridades.append(corr)
                    
                    if similaridades:
                        media_similaridade = np.mean(similaridades)
                        if media_similaridade > 0.6:
                            padrao = {
                                'escala': escala,
                                'similaridade_media': media_similaridade,
                                'segmentos_analisados': len(segmentos)
                            }
                            padroes.append(padrao)
        
        return padroes
    
    def sobrepor_eventos_historicos(self, df, preco_atual, margem_preco=100):
        """
        Sobrepõe eventos históricos similares ao preço atual
        """
        eventos_similares = []
        
        # Procura por preços similares no histórico
        for i, (timestamp, row) in enumerate(df.iterrows()):
            preco_historico = row['close']
            
            if abs(preco_historico - preco_atual) <= margem_preco:
                # Verifica contexto similar
                contexto = self.analisar_contexto(df, i)
                
                evento = {
                    'timestamp': timestamp.isoformat(),
                    'preco': preco_historico,
                    'diferenca_preco': preco_historico - preco_atual,
                    'contexto': contexto,
                    'similaridade': self.calcular_similaridade_contexto(contexto)
                }
                eventos_similares.append(evento)
        
        # Ordena por similaridade
        eventos_similares.sort(key=lambda x: x['similaridade'], reverse=True)
        
        return eventos_similares[:10]  # Retorna os 10 mais similares
    
    def analisar_contexto(self, df, indice):
        """
        Analisa o contexto de um ponto específico no histórico
        """
        if indice < 20 or indice >= len(df) - 20:
            return {}
        
        # Janela de contexto
        inicio = max(0, indice - 20)
        fim = min(len(df), indice + 20)
        
        contexto_df = df.iloc[inicio:fim]
        
        contexto = {
            'tendencia_curta': self.calcular_tendencia(contexto_df.iloc[:10]),
            'tendencia_media': self.calcular_tendencia(contexto_df),
            'volatilidade': contexto_df['close'].pct_change().std(),
            'volume_medio': contexto_df['volume'].mean() if 'volume' in contexto_df.columns else 0,
            'range_preco': contexto_df['close'].max() - contexto_df['close'].min()
        }
        
        return contexto
    
    def calcular_tendencia(self, df):
        """
        Calcula a tendência de um DataFrame
        """
        if len(df) < 2:
            return 0
        
        precos = df['close'].values
        x = np.arange(len(precos))
        
        # Regressão linear
        coeficiente = np.polyfit(x, precos, 1)[0]
        
        if coeficiente > 0.01:
            return 'ascendente'
        elif coeficiente < -0.01:
            return 'descendente'
        else:
            return 'lateral'
    
    def calcular_similaridade_contexto(self, contexto):
        """
        Calcula similaridade entre contextos
        """
        # Implementação simplificada - pode ser expandida
        return 0.5  # Placeholder
    
    def gerar_relatorio_temporal(self, df):
        """
        Gera relatório completo de análise temporal
        """
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'total_dados': len(df),
            'periodo_analisado': {
                'inicio': df.index[0].isoformat(),
                'fim': df.index[-1].isoformat()
            },
            'ciclos_detectados': len(self.ciclos_detectados['ciclos']),
            'ressonancias_ativas': len(self.ressonancias_temporais),
            'intensidade_magnetica_geral': self.calcular_intensidade_magnetica(df),
            'padroes_fractais_ativos': len(self.detectar_padroes_fractais(df)),
            'recomendacoes_temporais': self.gerar_recomendacoes_temporais(df)
        }
        
        return relatorio
    
    def gerar_recomendacoes_temporais(self, df):
        """
        Gera recomendações baseadas na análise temporal
        """
        recomendacoes = []
        
        # Analisa ciclos ativos
        ciclos_ativos = self.detectar_ciclos_fractais(df)
        if ciclos_ativos:
            recomendacoes.append(f"Detectados {len(ciclos_ativos)} ciclos fractais ativos")
        
        # Analisa intensidade magnética
        intensidade = self.calcular_intensidade_magnetica(df)
        if intensidade > 70:
            recomendacoes.append("Alta intensidade magnética - período de alta atividade esperada")
        elif intensidade < 30:
            recomendacoes.append("Baixa intensidade magnética - período de consolidação")
        
        # Analisa padrões fractais
        padroes = self.detectar_padroes_fractais(df)
        if padroes:
            recomendacoes.append(f"Padrões fractais detectados em {len(padroes)} escalas")
        
        return recomendacoes
