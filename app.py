# Import das bibliotecas
import pandas as pd
import yfinance as yf  # Yahoo Finance
import matplotlib.pyplot as plt
import numpy as np

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
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(window=22).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window=22).mean()

dados_ativo = dados_ativo.dropna()

# Calcular o RSI
dados_ativo['RSI'] = 100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos'])

# Sinais de compra e venda
dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
dados_ativo.loc[dados_ativo['RSI'] > 30, 'compra'] = 'nao'

# Armazenar as datas de compra
datas_compra = []
datas_venda = []

for i in range(len(dados_ativo)):

  if "sim" in dados_ativo['compra'].iloc[i]:

    datas_compra.append(dados_ativo.iloc[i+1].name) # +1 porque compra no preço de abertura do dia

    for j in range(1, 11):

        if dados_ativo['RSI'].iloc[i + j] > 40: # Vendo se nos proximos 10 dias o RSI passa de 40

            datas_venda.append(dados_ativo.iloc[i + j + 1].name) # Vende no dia seguinte que bater 40
            break

        elif j == 10:
                datas_venda.append(dados_ativo.iloc[i + j + 1].name)

        datas_venda


# Observando pontos de compra ao longo do tempo

plt.figure(figsize= (12, 5))
plt.scatter(dados_ativo.loc[datas_compra].index, dados_ativo.loc[datas_compra]['Adj Close'], marker = '^', c = 'g')
plt.plot(dados_ativo['Adj Close'], alpha = 0.7)

# Calculando lucros
lucros = dados_ativo.loc[datas_venda]['Open'].values/dados_ativo.loc[datas_compra]['Open'].values - 1

if len(lucros) > 0:
    operacao_vencedoras = len(lucros[lucros > 0]) / len(lucros)
else:
    operacao_vencedoras = 0.0  # Não há lucro, então todas as operações são perdedoras

operacao_vencedoras

media_ganhos = np.mean(lucros[lucros > 0])

media_ganhos * 100

media_perdas = abs(np.mean(lucros[lucros < 0]))

media_perdas

expectativas_matematica_modelo = (operacao_vencedoras * media_ganhos) - ((1 - operacao_vencedoras) * media_perdas)

expectativas_matematica_modelo * 100

performace_acumulada = (np.cumprod((1 + lucros)) - 1) * 100

performace_acumulada

retorno_buy_and_hold = dados_ativo['Adj Close'].iloc[-1]/dados_ativo['Adj Close'].iloc[0] - 1

retorno_buy_and_hold * 100

plt.figure(figsize = (12, 5))
print(datas_compra, performace_acumulada)
plt.plot(datas_compra, performace_acumulada)

dados_ativo #Exibe os dados em formato Excel
        
# Exibir pontos de compra ao longo do tempo no gráfico
plt.scatter(datas_compra, dados_ativo.loc[datas_compra]['Adj Close'], marker='^', c='g')

# Exibir o gráfico
plt.show()
