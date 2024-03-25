# Import das bibliotecas
import pandas as pd
import yfinance as yf  # Yahoo Finance
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

# Definição do ativo
ativo = "BTC-USD"  # Yahoo finance Bitcoin (BTC-USD)

# Puxar os dados do Yahoo Finance
dados_ativo = yf.download(ativo, '2011-12-11')

# Plotar o gráfico de preços de fechamento ajustado
dados_ativo['Adj Close'].plot()

# Calcular os retornos
dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change().dropna()

# Separar os retornos positivos dos negativos
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x > 0 else 0)

# Calcular a média de retornos positivos e negativos dos últimos 7 dias
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(window=7).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window=7).mean()

dados_ativo = dados_ativo.dropna()

# Calcular o RSI
dados_ativo['RSI'] = 100 - 100 / (1 + dados_ativo['media_retornos_negativos'] / dados_ativo['media_retornos_negativos'])

# Sinais de compra e venda
dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
dados_ativo.loc[dados_ativo['RSI'] > 30, 'compra'] = 'nao'

# Armazenar as datas de compra
datas_compra = []

for i in range(len(dados_ativo)):
    if dados_ativo['compra'].iloc[i] == 'sim':
        datas_compra.append(dados_ativo.index[i])

# Exibir pontos de compra ao longo do tempo no gráfico
plt.scatter(datas_compra, dados_ativo.loc[datas_compra]['Adj Close'], marker='^', c='g')

# Exibir o gráfico
plt.show()
