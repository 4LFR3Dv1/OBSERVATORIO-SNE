import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle, Polygon
import matplotlib.animation as animation
from datetime import datetime, timedelta
import colorsys

class VisualizacaoSNE:
    """
    Sistema de Visualização Avançada do SNE
    - Camadas magnéticas, ressonâncias temporais e gravidade
    - Linguagem visual proprietária
    - Interface minimalista e artística
    """
    
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#0a0a0a')
        
        # Paleta de cores SNE
        self.cores = {
            'magnético': '#00ffff',  # Ciano para campos magnéticos
            'ressonância': '#ff00ff',  # Magenta para ressonâncias
            'gravidade': '#ffff00',  # Amarelo para gravidade
            'ruptura': '#ff4444',  # Vermelho para rupturas
            'fluxo': '#00ff00',  # Verde para fluxos
            'neutro': '#888888'  # Cinza para elementos neutros
        }
        
        # Camadas de visualização
        self.camadas = {
            'magnéticas': [],
            'ressonâncias': [],
            'gravidade': [],
            'fluxos': []
        }
    
    def criar_zona_magnetica(self, preco_min, preco_max, forca, timestamp):
        """
        Cria uma zona magnética com intensidade visual proporcional à força
        """
        alpha = min(0.8, float(forca) / 100)  # Transparência baseada na força
        zona = Rectangle(
            (timestamp, float(preco_min)), 
            timedelta(minutes=30), 
            float(preco_max) - float(preco_min),
            facecolor=self.cores['magnético'],
            alpha=alpha,
            edgecolor=self.cores['magnético'],
            linewidth=2,
            linestyle='--'
        )
        self.ax.add_patch(zona)
        self.camadas['magnéticas'].append(zona)
        
        # Adiciona label com força
        self.ax.text(
            timestamp, float(preco_max) + 50,
            f'⚡ {float(forca):.1f}',
            color=self.cores['magnético'],
            fontsize=10,
            ha='center'
        )
    
    def criar_ressonancia_temporal(self, preco, timestamp, eventos_similares):
        """
        Cria arcos/círculos indicando ressonâncias temporais
        """
        for evento in eventos_similares:
            # Linha de conexão temporal
            linha = plt.Line2D(
                [timestamp, evento['timestamp']],
                [preco, evento['preco']],
                color=self.cores['ressonância'],
                alpha=0.6,
                linewidth=1,
                linestyle=':'
            )
            self.ax.add_line(linha)
            
            # Círculo de ressonância
            circulo = Circle(
                (timestamp, preco),
                radius=20,
                facecolor=self.cores['ressonância'],
                alpha=0.3,
                edgecolor=self.cores['ressonância'],
                linewidth=2
            )
            self.ax.add_patch(circulo)
            self.camadas['ressonâncias'].append(circulo)
    
    def criar_campo_gravitacional(self, df, centro_preco, raio_influencia):
        """
        Cria "curvatura" visual mostrando atração gravitacional
        """
        precos = df['close'].values.astype(float)
        timestamps = df.index.values
        
        # Calcula força gravitacional em cada ponto
        forcas = []
        for i, preco in enumerate(precos):
            distancia = abs(float(preco) - float(centro_preco))
            if distancia <= raio_influencia:
                forca = 1 - (distancia / raio_influencia)
                forcas.append(forca)
            else:
                forcas.append(0)
        
        # Cria linhas de campo gravitacional
        pontos = np.column_stack([timestamps, precos])
        segmentos = np.concatenate([pontos[:-1], pontos[1:]], axis=1)
        
        cores_segmentos = []
        for forca in forcas[:-1]:
            cor = colorsys.hsv_to_rgb(0.17, 1, float(forca))  # Amarelo com intensidade variável
            cores_segmentos.append(cor)
        
        lc = LineCollection(
            segmentos.reshape(-1, 2, 2),
            colors=cores_segmentos,
            linewidths=2,
            alpha=0.7
        )
        self.ax.add_collection(lc)
        self.camadas['gravidade'].append(lc)
    
    def criar_fluxo_dinamico(self, df, direcao='ascendente'):
        """
        Cria linhas de fluxo dinâmico como campos magnéticos
        """
        precos = df['close'].values.astype(float)
        timestamps = df.index.values
        
        # Calcula gradiente de preços
        gradientes = np.gradient(precos)
        
        # Cria linhas de fluxo
        for i in range(0, len(precos)-1, 5):  # A cada 5 pontos
            if abs(gradientes[i]) > 0.1:  # Só mostra fluxos significativos
                # Linha de fluxo
                linha = plt.Line2D(
                    [timestamps[i], timestamps[i+1]],
                    [float(precos[i]), float(precos[i+1])],
                    color=self.cores['fluxo'],
                    alpha=0.5,
                    linewidth=1,
                    linestyle='-'
                )
                self.ax.add_line(linha)
                
                # Seta indicando direção
                if gradientes[i] > 0:
                    self.ax.arrow(
                        timestamps[i], float(precos[i]),
                        timestamps[i+1] - timestamps[i],
                        float(precos[i+1]) - float(precos[i]),
                        head_width=10,
                        head_length=10,
                        fc=self.cores['fluxo'],
                        ec=self.cores['fluxo'],
                        alpha=0.7
                    )
                
                self.camadas['fluxos'].append(linha)
    
    def criar_hud_evoluido(self, df, zonas_ativas, ressonancias_ativas):
        """
        HUD evoluído com fluxos dinâmicos e informações contextuais
        """
        # Área do HUD
        hud_area = Rectangle(
            (0.02, 0.02), 0.3, 0.25,
            facecolor='black',
            alpha=0.8,
            edgecolor=self.cores['neutro'],
            linewidth=1,
            transform=self.ax.transAxes
        )
        self.ax.add_patch(hud_area)
        
        # Informações dinâmicas
        preco_atual = df['close'].iloc[-1]
        energia_magnetica = df['densidade'].iloc[-1] if 'densidade' in df.columns else 0
        
        info_texto = f"""
        🔮 SNE - Observatório de Forças
        
        💰 Preço: {preco_atual:.2f} USDT
        ⚡ Energia Magnética: {energia_magnetica:.4f}
        🎯 Zonas Ativas: {len(zonas_ativas)}
        🔄 Ressonâncias: {len(ressonancias_ativas)}
        
        📊 Campos Ativos:
        • Magnético: {'Ativo' if zonas_ativas else 'Quieto'}
        • Gravitacional: {'Ativo' if energia_magnetica > 0.5 else 'Suave'}
        • Temporal: {'Ressonante' if ressonancias_ativas else 'Linear'}
        """
        
        self.ax.text(
            0.05, 0.20, info_texto,
            transform=self.ax.transAxes,
            color='white',
            fontsize=9,
            fontfamily='monospace',
            verticalalignment='top'
        )
    
    def limpar_camadas(self):
        """
        Remove todas as camadas visuais para nova renderização
        """
        for camada in self.camadas.values():
            for elemento in camada:
                if hasattr(elemento, 'remove'):
                    elemento.remove()
                else:
                    self.ax.collections.remove(elemento)
        
        # Limpa as listas
        for key in self.camadas:
            self.camadas[key] = []
    
    def exportar_visualizacao(self, nome_arquivo):
        """
        Exporta a visualização como imagem
        """
        self.fig.savefig(
            nome_arquivo,
            dpi=300,
            bbox_inches='tight',
            facecolor='#0a0a0a',
            edgecolor='none'
        )
        print(f"🎨 Visualização exportada: {nome_arquivo}")
    
    def mostrar_visualizacao(self):
        """
        Exibe a visualização interativa
        """
        plt.tight_layout()
        plt.show()
