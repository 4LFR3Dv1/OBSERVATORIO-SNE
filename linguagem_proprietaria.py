import json
import os
from datetime import datetime
import pandas as pd

class LinguagemSNE:
    """
    Linguagem Proprietária do SNE
    - Vocabulário gráfico único
    - Interpretações automáticas
    - Registro de leituras visuais
    """
    
    def __init__(self):
        self.vocabulario = {
            # Campos Magnéticos
            'campo_magnetico_ativo': {
                'descricao': 'Zona onde forças magnéticas estão concentradas',
                'indicadores': ['alta_densidade', 'volume_elevado', 'rupturas_frequentes'],
                'cor': '#00ffff',
                'simbolo': '⚡'
            },
            'ponto_ressonancia': {
                'descricao': 'Local onde padrões históricos se repetem',
                'indicadores': ['similaridade_temporal', 'preco_proximo', 'volume_similar'],
                'cor': '#ff00ff',
                'simbolo': '🔄'
            },
            'fluxo_gravitacional': {
                'descricao': 'Direção predominante da atração de preços',
                'indicadores': ['tendencia_clara', 'momentum_sustentado', 'suporte_resistencia'],
                'cor': '#ffff00',
                'simbolo': '🌊'
            },
            'compressao_magnetica': {
                'descricao': 'Acúmulo de energia antes de uma explosão',
                'indicadores': ['volatilidade_baixa', 'volume_crescente', 'range_estreito'],
                'cor': '#ff8800',
                'simbolo': '💥'
            },
            'eco_temporal': {
                'descricao': 'Repetição de padrões em diferentes escalas temporais',
                'indicadores': ['fractal_detectado', 'ciclo_similar', 'proporcao_constante'],
                'cor': '#8800ff',
                'simbolo': '🎵'
            }
        }
        
        self.caminho_codice = "codice_interpretacoes.json"
        self.interpretacoes = self.carregar_interpretacoes()
    
    def carregar_interpretacoes(self):
        """
        Carrega interpretações salvas ou cria novo arquivo
        """
        if os.path.exists(self.caminho_codice):
            with open(self.caminho_codice, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'interpretacoes': [],
                'vocabulario_usado': {},
                'padroes_detectados': []
            }
    
    def salvar_interpretacao(self, interpretacao):
        """
        Salva uma nova interpretação no códice
        """
        self.interpretacoes['interpretacoes'].append(interpretacao)
        
        # Atualiza estatísticas de vocabulário
        for termo in interpretacao.get('termos_usados', []):
            if termo in self.interpretacoes['vocabulario_usado']:
                self.interpretacoes['vocabulario_usado'][termo] += 1
            else:
                self.interpretacoes['vocabulario_usado'][termo] = 1
        
        with open(self.caminho_codice, 'w', encoding='utf-8') as f:
            json.dump(self.interpretacoes, f, indent=2, ensure_ascii=False)
    
    def interpretar_campo_magnetico(self, df, zona_preco, forca):
        """
        Interpreta um campo magnético detectado
        """
        interpretacao = {
            'timestamp': datetime.now().isoformat(),
            'tipo': 'campo_magnetico_ativo',
            'localizacao': {
                'preco_centro': zona_preco,
                'range': [zona_preco - 50, zona_preco + 50]
            },
            'intensidade': forca,
            'descricao': f"Campo magnético ativo detectado na zona {zona_preco:.0f} USDT",
            'analise': self.analisar_intensidade_campo(forca),
            'termos_usados': ['campo_magnetico_ativo'],
            'recomendacoes': self.gerar_recomendacoes_campo(forca)
        }
        
        self.salvar_interpretacao(interpretacao)
        return interpretacao
    
    def interpretar_ressonancia_temporal(self, preco_atual, eventos_similares):
        """
        Interpreta uma ressonância temporal detectada
        """
        if not eventos_similares:
            return None
        
        interpretacao = {
            'timestamp': datetime.now().isoformat(),
            'tipo': 'ponto_ressonancia',
            'localizacao': {
                'preco_atual': preco_atual,
                'eventos_similares': len(eventos_similares)
            },
            'intensidade': len(eventos_similares),
            'descricao': f"Ressonância temporal detectada em {preco_atual:.2f} USDT",
            'analise': self.analisar_ressonancia(eventos_similares),
            'termos_usados': ['ponto_ressonancia', 'eco_temporal'],
            'recomendacoes': self.gerar_recomendacoes_ressonancia(eventos_similares)
        }
        
        self.salvar_interpretacao(interpretacao)
        return interpretacao
    
    def interpretar_fluxo_gravitacional(self, df, direcao, intensidade):
        """
        Interpreta um fluxo gravitacional detectado
        """
        interpretacao = {
            'timestamp': datetime.now().isoformat(),
            'tipo': 'fluxo_gravitacional',
            'caracteristicas': {
                'direcao': direcao,
                'intensidade': intensidade,
                'duracao': len(df)
            },
            'descricao': f"Fluxo gravitacional {direcao} detectado",
            'analise': self.analisar_fluxo(direcao, intensidade),
            'termos_usados': ['fluxo_gravitacional'],
            'recomendacoes': self.gerar_recomendacoes_fluxo(direcao, intensidade)
        }
        
        self.salvar_interpretacao(interpretacao)
        return interpretacao
    
    def analisar_intensidade_campo(self, forca):
        """
        Analisa a intensidade de um campo magnético
        """
        if forca > 80:
            return "Campo magnético extremamente intenso - alta probabilidade de ruptura"
        elif forca > 50:
            return "Campo magnético forte - movimento significativo esperado"
        elif forca > 20:
            return "Campo magnético moderado - atenção redobrada"
        else:
            return "Campo magnético suave - monitoramento passivo"
    
    def analisar_ressonancia(self, eventos_similares):
        """
        Analisa uma ressonância temporal
        """
        if len(eventos_similares) > 5:
            return "Ressonância múltipla detectada - padrão histórico muito forte"
        elif len(eventos_similares) > 2:
            return "Ressonância significativa - repetição de padrão confirmada"
        else:
            return "Ressonância leve - possível repetição de padrão"
    
    def analisar_fluxo(self, direcao, intensidade):
        """
        Analisa um fluxo gravitacional
        """
        if intensidade > 0.8:
            return f"Fluxo gravitacional {direcao} muito forte - movimento direcional claro"
        elif intensidade > 0.5:
            return f"Fluxo gravitacional {direcao} moderado - tendência estabelecida"
        else:
            return f"Fluxo gravitacional {direcao} suave - direção incerta"
    
    def gerar_recomendacoes_campo(self, forca):
        """
        Gera recomendações baseadas na intensidade do campo
        """
        if forca > 80:
            return ["Aguardar ruptura iminente", "Preparar posição", "Monitorar volume"]
        elif forca > 50:
            return ["Atenção redobrada", "Verificar ressonâncias", "Aguardar confirmação"]
        else:
            return ["Monitoramento passivo", "Aguardar fortalecimento"]
    
    def gerar_recomendacoes_ressonancia(self, eventos_similares):
        """
        Gera recomendações baseadas na ressonância
        """
        if len(eventos_similares) > 5:
            return ["Alta probabilidade de repetição", "Posicionar estrategicamente", "Usar stop tight"]
        elif len(eventos_similares) > 2:
            return ["Considerar entrada", "Verificar contexto atual", "Monitorar confirmação"]
        else:
            return ["Aguardar mais sinais", "Manter observação"]
    
    def gerar_recomendacoes_fluxo(self, direcao, intensidade):
        """
        Gera recomendações baseadas no fluxo gravitacional
        """
        if intensidade > 0.8:
            return [f"Seguir fluxo {direcao}", "Posicionar na direção", "Usar momentum"]
        elif intensidade > 0.5:
            return [f"Considerar fluxo {direcao}", "Aguardar confirmação", "Monitorar força"]
        else:
            return ["Aguardar direção clara", "Manter neutralidade"]
    
    def gerar_relatorio_linguagem(self):
        """
        Gera um relatório da linguagem utilizada
        """
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'total_interpretacoes': len(self.interpretacoes['interpretacoes']),
            'vocabulario_mais_usado': sorted(
                self.interpretacoes['vocabulario_usado'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            'padroes_detectados': self.interpretacoes['padroes_detectados'],
            'resumo': self.gerar_resumo_linguagem()
        }
        
        return relatorio
    
    def gerar_resumo_linguagem(self):
        """
        Gera um resumo da linguagem utilizada
        """
        total_interpretacoes = len(self.interpretacoes['interpretacoes'])
        if total_interpretacoes == 0:
            return "Nenhuma interpretação registrada ainda"
        
        tipos_mais_comuns = {}
        for interpretacao in self.interpretacoes['interpretacoes']:
            tipo = interpretacao.get('tipo', 'desconhecido')
            tipos_mais_comuns[tipo] = tipos_mais_comuns.get(tipo, 0) + 1
        
        tipo_principal = max(tipos_mais_comuns.items(), key=lambda x: x[1])
        
        return f"Total de {total_interpretacoes} interpretações. Padrão principal: {tipo_principal[0]} ({tipo_principal[1]} ocorrências)"
    
    def traduzir_para_linguagem_sne(self, evento_tradicional):
        """
        Traduz eventos tradicionais para a linguagem SNE
        """
        traducoes = {
            'support': 'campo_magnetico_ativo',
            'resistance': 'campo_magnetico_ativo',
            'breakout': 'ruptura_magnetica',
            'breakdown': 'ruptura_magnetica',
            'trend': 'fluxo_gravitacional',
            'pattern': 'eco_temporal',
            'volume_spike': 'compressao_magnetica',
            'consolidation': 'compressao_magnetica'
        }
        
        return traducoes.get(evento_tradicional, 'evento_desconhecido')
