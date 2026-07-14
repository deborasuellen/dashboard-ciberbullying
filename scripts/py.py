from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ===================== CONFIG =====================
DATA_DIR = Path("dados")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

APP_TITLE = "Análise de Ciberbullying no Brasil (2020-2026)"

# ===================== FUNÇÕES =====================
def load_data():
    """Carrega todos os arquivos CSV da pasta dados"""
    denuncias = pd.read_csv(DATA_DIR / "denuncias-2026.csv")
    plataformas = pd.read_csv(DATA_DIR / "plataformas.csv")
    regioes = pd.read_csv(DATA_DIR / "regioes.csv")
    vitimas = pd.read_csv(DATA_DIR / "vitimas-faixa-etaria.csv")
    
    print(f"✅ Dados carregados:")
    print(f"   • Denúncias: {len(denuncias)} registros")
    print(f"   • Plataformas: {len(plataformas)} registros")
    print(f"   • Regiões: {len(regioes)} registros")
    
    return denuncias, plataformas, regioes, vitimas


def analyze_general(denuncias, plataformas):
    """Análise geral e estatísticas"""
    total = denuncias['denuncias'].sum()
    print(f"\n📊 Total de denúncias (2020-2026): {total:,.0f}")
    
    # Evolução anual
    evolucao = denuncias.groupby('ano')['denuncias'].sum().reset_index()
    print("\nEvolução anual:")
    print(evolucao)
    
    # Plataforma mais crítica
    plataforma_top = plataformas.loc[plataformas['porcentagem'].idxmax()]
    print(f"\n🚨 Plataforma mais usada: {plataforma_top['plataforma']} ({plataforma_top['porcentagem']}% )")
    
    return evolucao


def generate_charts(denuncias, plataformas, regioes, vitimas):
    """Gera gráficos e salva em output/"""
    sns.set_style("darkgrid")
    
    # 1. Evolução Temporal
    plt.figure(figsize=(10, 6))
    plt.plot(denuncias['ano'], denuncias['denuncias'], marker='o', linewidth=3, color='#f87171')
    plt.title('Evolução de Denúncias de Ciberbullying (2020-2026)', fontsize=14)
    plt.xlabel('Ano')
    plt.ylabel('Número de Denúncias')
    plt.grid(True)
    plt.savefig(OUTPUT_DIR / 'evolucao_temporal.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Distribuição por Plataforma
    fig = px.pie(plataformas, names='plataforma', values='denuncias', 
                 title='Distribuição de Denúncias por Plataforma',
                 color_discrete_sequence=px.colors.sequential.Reds)
    fig.write_image(OUTPUT_DIR / 'distribuicao_plataformas.png')
    fig.write_html(OUTPUT_DIR / 'distribuicao_plataformas.html')
    
    # 3. Mapa de Regiões (barras)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=regioes, x='denuncias', y='regiao', palette='Reds')
    plt.title('Denúncias de Ciberbullying por Região')
    plt.savefig(OUTPUT_DIR / 'denuncias_por_regiao.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📈 Gráficos salvos na pasta '{OUTPUT_DIR}'")


def main():
    print(f"🚀 {APP_TITLE}\n")
    
    denuncias, plataformas, regioes, vitimas = load_data()
    evolucao = analyze_general(denuncias, plataformas)
    generate_charts(denuncias, plataformas, regioes, vitimas)
    
    # Exportar dados consolidados
    consolidated = denuncias.merge(plataformas, left_on='plataforma_principal', right_on='plataforma', how='left')
    consolidated.to_csv(OUTPUT_DIR / 'dados_consolidados.csv', index=False, encoding='utf-8-sig')
    
    print("\n✅ Análise concluída com sucesso!")
    print(f"📁 Arquivos gerados em: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
