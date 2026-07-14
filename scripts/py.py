import pandas as pd
import matplotlib.pyplot as plt

# Exemplo de processamento
df = pd.read_csv('dados/denuncias-2026.csv')
print("Total de denúncias:", df['quantidade'].sum())

# Gráfico simples (pode salvar imagem para o dashboard)
df.groupby('ano')['quantidade'].sum().plot(kind='bar')
plt.title('Evolução de Denúncias de Ciberbullying')
plt.savefig('evolucao.png')
print("Gráfico salvo!")
