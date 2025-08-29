#!/usr/bin/env python3
"""
Script de Teste para SNE v2.0
Testa todos os módulos principais da nova versão
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_visualizacao_avancada():
    """Testa o módulo de visualização avançada"""
    print("🧪 Testando Visualização Avançada...")
    
    try:
        from visualizacao_avancada import VisualizacaoSNE
        
        # Cria dados de teste
        dates = pd.date_range(start='2024-01-01', periods=100, freq='1min')
        prices = np.random.randn(100).cumsum() + 45000
        
        df = pd.DataFrame({
            'close': prices,
            'open': prices - np.random.randn(100) * 10,
            'high': prices + np.abs(np.random.randn(100) * 20),
            'low': prices - np.abs(np.random.randn(100) * 20),
            'volume': np.random.randint(100, 1000, 100),
            'densidade': np.random.uniform(0.1, 1.0, 100)
        }, index=dates)
        
        # Testa visualização
        viz = VisualizacaoSNE()
        
        # Testa criação de zona magnética
        viz.criar_zona_magnetica(44900, 45100, 75.5, dates[50])
        print("  ✅ Zona magnética criada")
        
        # Testa criação de ressonância
        eventos_similares = [{'timestamp': dates[20], 'preco': 44950}]
        viz.criar_ressonancia_temporal(45000, dates[50], eventos_similares)
        print("  ✅ Ressonância temporal criada")
        
        # Testa criação de fluxo dinâmico
        viz.criar_fluxo_dinamico(df)
        print("  ✅ Fluxo dinâmico criado")
        
        # Testa HUD evoluído
        zonas_ativas = [{'preco': 45000, 'forca': 75.5}]
        ressonancias = [{'preco': 44950, 'timestamp': dates[20]}]
        viz.criar_hud_evoluido(df, zonas_ativas, ressonancias)
        print("  ✅ HUD evoluído criado")
        
        # Testa limpeza de camadas
        viz.limpar_camadas()
        print("  ✅ Camadas limpas")
        
        print("  🎉 Visualização Avançada: OK")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na Visualização Avançada: {e}")
        return False

def test_linguagem_proprietaria():
    """Testa o módulo de linguagem proprietária"""
    print("🧪 Testando Linguagem Proprietária...")
    
    try:
        from linguagem_proprietaria import LinguagemSNE
        
        # Cria dados de teste
        dates = pd.date_range(start='2024-01-01', periods=50, freq='1min')
        prices = np.random.randn(50).cumsum() + 45000
        
        df = pd.DataFrame({
            'close': prices,
            'open': prices - np.random.randn(50) * 10,
            'high': prices + np.abs(np.random.randn(50) * 20),
            'low': prices - np.abs(np.random.randn(50) * 20),
            'volume': np.random.randint(100, 1000, 50),
            'densidade': np.random.uniform(0.1, 1.0, 50)
        }, index=dates)
        
        # Testa linguagem
        lang = LinguagemSNE()
        
        # Testa interpretação de campo magnético
        interpretacao = lang.interpretar_campo_magnetico(df, 45000, 75.5)
        print("  ✅ Interpretação de campo magnético criada")
        
        # Testa interpretação de ressonância
        eventos_similares = [{'timestamp': dates[20], 'preco': 44950}]
        interpretacao = lang.interpretar_ressonancia_temporal(45000, eventos_similares)
        print("  ✅ Interpretação de ressonância criada")
        
        # Testa interpretação de fluxo gravitacional
        interpretacao = lang.interpretar_fluxo_gravitacional(df, 'ascendente', 0.75)
        print("  ✅ Interpretação de fluxo gravitacional criada")
        
        # Testa relatório de linguagem
        relatorio = lang.gerar_relatorio_linguagem()
        print("  ✅ Relatório de linguagem gerado")
        
        # Testa tradução
        traduzido = lang.traduzir_para_linguagem_sne('support')
        print(f"  ✅ Tradução: support -> {traduzido}")
        
        print("  🎉 Linguagem Proprietária: OK")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na Linguagem Proprietária: {e}")
        return False

def test_exploracao_temporal():
    """Testa o módulo de exploração temporal"""
    print("🧪 Testando Exploração Temporal...")
    
    try:
        from exploracao_temporal import ExploracaoTemporalSNE
        
        # Cria dados de teste
        dates = pd.date_range(start='2024-01-01', periods=200, freq='1min')
        prices = np.random.randn(200).cumsum() + 45000
        
        df = pd.DataFrame({
            'close': prices,
            'open': prices - np.random.randn(200) * 10,
            'high': prices + np.abs(np.random.randn(200) * 20),
            'low': prices - np.abs(np.random.randn(200) * 20),
            'volume': np.random.randint(100, 1000, 200),
            'densidade': np.random.uniform(0.1, 1.0, 200)
        }, index=dates)
        
        # Testa exploração
        exp = ExploracaoTemporalSNE()
        
        # Testa detecção de ciclos fractais
        ciclos = exp.detectar_ciclos_fractais(df)
        print(f"  ✅ {len(ciclos)} ciclos fractais detectados")
        
        # Testa zoom temporal magnético
        df_zoom, resultado = exp.zoom_temporal_magnetico(df, dates[100])
        print("  ✅ Zoom temporal magnético executado")
        
        # Testa cálculo de intensidade magnética
        intensidade = exp.calcular_intensidade_magnetica(df)
        print(f"  ✅ Intensidade magnética: {intensidade:.2f}")
        
        # Testa detecção de ressonâncias
        ressonancias = exp.detectar_ressonancias_regiao(df)
        print(f"  ✅ {len(ressonancias)} ressonâncias detectadas")
        
        # Testa identificação de período ressonante
        periodo = exp.identificar_periodo_ressonante(df)
        print(f"  ✅ Período ressonante: {periodo}")
        
        # Testa detecção de padrões fractais
        padroes = exp.detectar_padroes_fractais(df)
        print(f"  ✅ {len(padroes)} padrões fractais detectados")
        
        # Testa sobreposição de eventos históricos
        eventos = exp.sobrepor_eventos_historicos(df, 45000)
        print(f"  ✅ {len(eventos)} eventos históricos encontrados")
        
        # Testa relatório temporal
        relatorio = exp.gerar_relatorio_temporal(df)
        print("  ✅ Relatório temporal gerado")
        
        print("  🎉 Exploração Temporal: OK")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na Exploração Temporal: {e}")
        return False

def test_app_web():
    """Testa a aplicação web"""
    print("🧪 Testando Aplicação Web...")
    
    try:
        # Testa se os módulos podem ser importados
        from app_web import app, socketio, estado_app
        
        print("  ✅ Aplicação Flask criada")
        print("  ✅ SocketIO configurado")
        print("  ✅ Estado da aplicação inicializado")
        
        # Testa se as rotas estão definidas
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/api/dados', '/api/analise', '/api/interpretacoes', '/api/visualizacao']
        
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ Rota {route} encontrada")
            else:
                print(f"  ⚠️ Rota {route} não encontrada")
        
        print("  🎉 Aplicação Web: OK")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na Aplicação Web: {e}")
        return False

def test_dependencias():
    """Testa se todas as dependências estão instaladas"""
    print("🧪 Testando Dependências...")
    
    dependencias = [
        'flask',
        'flask_socketio',
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'requests',
        'pytz'
    ]
    
    todas_ok = True
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"  ✅ {dep} instalado")
        except ImportError:
            print(f"  ❌ {dep} não encontrado")
            todas_ok = False
    
    if todas_ok:
        print("  🎉 Todas as dependências: OK")
    else:
        print("  ⚠️ Algumas dependências estão faltando")
    
    return todas_ok

def main():
    """Executa todos os testes"""
    print("🔮 SNE v2.0 - Teste de Funcionalidade")
    print("=" * 50)
    
    resultados = []
    
    # Testa dependências primeiro
    resultados.append(test_dependencias())
    
    # Testa módulos principais
    resultados.append(test_visualizacao_avancada())
    resultados.append(test_linguagem_proprietaria())
    resultados.append(test_exploracao_temporal())
    resultados.append(test_app_web())
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    total_tests = len(resultados)
    testes_ok = sum(resultados)
    
    print(f"Total de testes: {total_tests}")
    print(f"Testes aprovados: {testes_ok}")
    print(f"Testes reprovados: {total_tests - testes_ok}")
    
    if testes_ok == total_tests:
        print("🎉 TODOS OS TESTES APROVADOS!")
        print("🚀 SNE v2.0 está pronto para uso!")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
    
    print("\n📝 Próximos passos:")
    print("1. Execute: python app_web.py")
    print("2. Acesse: http://localhost:5000")
    print("3. Para deploy no Render, conecte o repositório")

if __name__ == "__main__":
    main()
