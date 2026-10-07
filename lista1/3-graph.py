import math
from decimal import Decimal, localcontext

N_MAX = 30
N_ESTAVEL = 60
PRECISAO = 150


def recorrencia(n_max):
    # I_0 = (e - 1) / e  e  I_{n+1} = 1 - (n + 1) I_n, em ponto flutuante.
    valores = [(math.e - 1) / math.e]
    for n in range(n_max):
        valores.append(1 - (n + 1) * valores[-1])
    return valores


def referencia(n_max):
    # Mesma recorrência com 150 dígitos. O erro inicial, de ordem 1e-150,
    # é multiplicado por n! e continua desprezível para n <= 60.
    with localcontext() as contexto:
        contexto.prec = PRECISAO
        valores = [(Decimal(1).exp() - 1) / Decimal(1).exp()]
        for n in range(n_max):
            valores.append(1 - (n + 1) * valores[-1])
        return valores


def recorrencia_inversa(n_max, n_inicio):
    # I_{n-1} = (1 - I_n) / n, partindo de I_{n_inicio} = 0 e andando para trás.
    valores = [0.0] * (n_inicio + 1)
    for n in range(n_inicio, 0, -1):
        valores[n - 1] = (1 - valores[n]) / n
    return valores[:n_max + 1]


def erro_absoluto(valor, exato):
    # from_float preserva exatamente o valor binário que o computador calculou.
    with localcontext() as contexto:
        contexto.prec = PRECISAO
        return float(abs(Decimal.from_float(valor) - exato))


progressiva = recorrencia(N_MAX)
exatos = referencia(N_ESTAVEL)

print('Recorrência progressiva (ponto flutuante)')
for n, i in enumerate(progressiva):
    erro = erro_absoluto(i, exatos[n])
    print(f'n = {n:>2}   I_n = {i:>14.6e}   Referência = {float(exatos[n]):.6e}   Erro absoluto = {erro:.3e}')

primeiro = next(n for n, i in enumerate(progressiva) if not 0 < i < 1 / (n + 1))
print(f'\nPrimeiro n com I_n fora do intervalo (0, 1/(n+1)]: n = {primeiro}')
erro_inicial = erro_absoluto(progressiva[0], exatos[0])
print(f'Erro inicial: {erro_inicial:.3e}   N! x erro inicial para N = {N_MAX}: {math.factorial(N_MAX) * erro_inicial:.3e}')

inversa = recorrencia_inversa(N_MAX, N_ESTAVEL)
print('\nRecorrência inversa (partindo de I_60 = 0)')
for n in [0, 5, 10, 20, 30]:
    erro = erro_absoluto(inversa[n], exatos[n])
    print(f'n = {n:>2}   I_n = {inversa[n]:.15f}   Erro absoluto = {erro:.3e}')

print('\nLimite exato I_n -> 0')
for n in [5, 10, 20, 30]:
    print(f'n = {n:>2}   Referência = {float(exatos[n]):.6e}   Cota 1/(n+1) = {1 / (n + 1):.6e}')

# Gráficos
from pathlib import Path
import matplotlib.pyplot as plt

PASTA = Path(__file__).resolve().parent
VERDE = '#007C78'
LARANJA = '#C15A36'
CINZA = '#71888D'
plt.rcParams.update({
    'font.size': 11, 'axes.titlesize': 13, 'axes.titleweight': 'bold',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.25, 'legend.frameon': False,
    'axes.axisbelow': True,
})

ns = list(range(N_MAX + 1))
ref = [float(exatos[n]) for n in ns]
erros = [erro_absoluto(i, exatos[n]) for n, i in enumerate(progressiva)]
u = 2.0 ** -54

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.7), layout='constrained')
ax1.plot(ns, progressiva, 'o-', color=LARANJA, markersize=4, label='Recorrência em ponto flutuante')
ax1.plot(ns, ref, color=VERDE, linewidth=2, label='Valor de referência')
ax1.axhline(0, color=CINZA, linestyle='--', label='Limite exato: 0')
ax1.set_yscale('symlog', linthresh=1e-1)
ax1.set(xlabel='n', ylabel='Iₙ (escala symlog)', title='Sucessão calculada e limite')
ax1.legend(loc='upper left', fontsize=9)
ax2.semilogy(ns, erros, 'o-', color=LARANJA, markersize=4, label='Erro absoluto')
ax2.semilogy(ns, [math.factorial(n) * u for n in ns], color=CINZA, linestyle='--',
             label=r'$n!\cdot 2^{-54}$')
ax2.set(xlabel='n', ylabel='Erro absoluto (escala log)', title='Amplificação do erro')
ax2.legend(loc='upper left')
fig.savefig(PASTA / 'ex3.png', dpi=180)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.7), layout='constrained')
ax1.semilogy(ns, [max(e, 1e-20) for e in erros], 'o-', color=LARANJA, markersize=4, label='Progressiva')
erros_inv = [max(erro_absoluto(inversa[n], exatos[n]), 1e-20) for n in ns]
ax1.semilogy(ns, erros_inv, 'o-', color=VERDE, markersize=4, label='Inversa (a partir de n = 60)')
ax1.set(xlabel='n', ylabel='Erro absoluto (escala log)', title='Comparação dos dois sentidos')
ax1.legend(loc='upper left')
ax2.plot(ns, inversa[:N_MAX + 1], color=VERDE, linewidth=2, label='Recorrência inversa')
ax2.plot(ns, [1 / (n + 1) for n in ns], color=CINZA, linestyle='--', label='Cota 1/(n + 1)')
ax2.axhline(0, color=LARANJA, linestyle=':', label='Limite: 0')
ax2.set(xlabel='n', ylabel='Iₙ', title='A sucessão tende a zero')
ax2.legend()
fig.savefig(PASTA / 'ex3-estabilidade.png', dpi=180)
print('\nGráficos salvos na pasta:', PASTA)
plt.show()
