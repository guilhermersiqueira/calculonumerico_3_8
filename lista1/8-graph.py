import math
from decimal import Decimal, localcontext

A = 0.401            # Pa m^3
B = 42.7e-6          # m^3
N = 1000
T = 300.0            # K
P = 3.5e7            # Pa
K = 1.3806503e-23    # J/K
TOL = 1e-12
MAX_ITER = 10000

NB = N * B           # volume mínimo possível: V > N b


def f(v):
    return (P + A * (N / v) ** 2) * (v - NB) - K * N * T


def df(v):
    return (P + A * (N / v) ** 2) - 2 * A * N ** 2 * (v - NB) / v ** 3


def bissecao(a, b):
    if f(a) * f(b) > 0:
        raise ValueError('A função precisa trocar de sinal em [a, b].')
    valores = []
    for k in range(MAX_ITER):
        m = (a + b) / 2
        valores.append(m)
        if (b - a) / 2 <= TOL or f(m) == 0:
            return valores
        if f(a) * f(m) < 0:
            b = m
        else:
            a = m
    raise ArithmeticError('A bissecção não convergiu no limite de iterações.')


def falsa_posicao(a, b):
    if f(a) * f(b) > 0:
        raise ValueError('A função precisa trocar de sinal em [a, b].')
    valores = []
    for k in range(MAX_ITER):
        fa, fb = f(a), f(b)
        c = (a * fb - b * fa) / (fb - fa)
        valores.append(c)
        if len(valores) > 1 and abs(valores[-1] - valores[-2]) <= TOL:
            return valores
        fc = f(c)
        if fc == 0:
            return valores
        if fa * fc < 0:
            b = c
        else:
            a = c
    raise ArithmeticError('A falsa-posição não convergiu no limite de iterações.')


def newton(x0):
    valores = [x0]
    x = x0
    for k in range(MAX_ITER):
        novo = x - f(x) / df(x)
        valores.append(novo)
        if abs(novo - x) <= TOL:
            return valores
        x = novo
    raise ArithmeticError('Newton não convergiu no limite de iterações.')


A0, B0 = NB, 0.5     # intervalo inicial: f(NB) < 0 e f(0,5) > 0
X0 = 0.05            # chute inicial de Newton

print(f'N b = {NB:.10f} m^3')
print(f'Gás ideal: V = N k T / p = {N * K * T / P:.6e} m^3')
print(f'f({A0:.4f}) = {f(A0):.3e}   f({B0}) = {f(B0):.3e}')

historicos = {}
for nome, funcao in [('Bissecção', lambda: bissecao(A0, B0)),
                     ('Falsa-posição', lambda: falsa_posicao(A0, B0)),
                     ('Newton-Raphson', lambda: newton(X0))]:
    valores = funcao()
    historicos[nome] = valores
    v = valores[-1]
    print(f'\n{nome}')
    for k, x in enumerate(valores[:6]):
        print(f'Iteração: {k}   V = {x:.12f}   f(V) = {f(x):.3e}')
    # Em Newton, a lista também guarda o chute inicial.
    iteracoes = len(valores) - 1 if nome == 'Newton-Raphson' else len(valores)
    print(f'V = {v:.12f} m^3   f(V) = {f(v):.3e}   Iterações: {iteracoes}')

print('\nOutros chutes iniciais e intervalos')
for x0 in [0.0428, 0.05, 0.06, 0.1, 0.2, 0.5, 1.0]:
    print(f'Newton   x0 = {x0:<6g}   Iterações: {len(newton(x0)) - 1:2d}')
for b in [0.05, 0.5, 1.0]:
    print(f'[N b, {b:<4g}]   Bissecção: {len(bissecao(A0, b)):2d}   Falsa-posição: {len(falsa_posicao(A0, b)):2d}')

print('\nVerificação com 60 dígitos (V = N b + w)')
with localcontext() as contexto:
    contexto.prec = 60
    a, b, n = Decimal(str(A)), Decimal(str(B)), Decimal(N)
    t, p, k = Decimal(str(T)), Decimal(str(P)), Decimal(str(K))
    nb = n * b
    w = k * n * t / p
    for _ in range(5):
        # w = k N T / (p + a N^2 / (N b + w)^2)
        w = k * n * t / (p + a * n * n / (nb + w) ** 2)
    print(f'V - N b = {w:.6E} m^3')
    print(f'V = {nb + w:.30f} m^3')

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

import numpy as np
from matplotlib.ticker import MaxNLocator

v_ref = NB  # a raiz fica a ~1,6e-26 de N b, abaixo da resolução do float
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.7), layout='constrained')
v = np.linspace(NB, 0.5, 400)
ax1.plot(v, [f(x) for x in v], color=VERDE, linewidth=2, label='f(V)')
ax1.axhline(0, color=CINZA, linewidth=1)
ax1.scatter([NB], [0], color=LARANJA, zorder=3, label='Raiz: V ≈ N b')
ax1.set(xlabel='V (m³)', ylabel='f(V) (J)', title='Função da equação de estado')
ax1.legend(loc='upper left')
for nome, cor in [('Bissecção', VERDE), ('Falsa-posição', LARANJA), ('Newton-Raphson', CINZA)]:
    valores = historicos[nome]
    erros = [max(abs(x - v_ref), 1e-18) for x in valores]
    ax2.semilogy(range(len(valores)), erros, 'o-', color=cor, markersize=4, label=nome)
ax2.axhline(TOL, color='#18363E', linestyle=':', label='Tolerância 10⁻¹²')
ax2.set(xlabel='Iteração k', ylabel='|Vₖ − N b| (escala log)', title='Convergência dos métodos')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.legend(fontsize=9)
fig.savefig(PASTA / 'ex8.png', dpi=180)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.7), layout='constrained')
for x0, cor in [(0.05, VERDE), (0.1, LARANJA)]:
    valores = newton(x0)
    ax1.plot(range(len(valores)), valores, 'o-', color=cor, markersize=4, label=f'V₀ = {x0:g} m³')
ax1.axhline(NB, color=CINZA, linestyle='--', label='N b')
ax1.axhline(0, color='#18363E', linewidth=1)
ax1.set(xlabel='Iteração k', ylabel='Vₖ (m³)', title='Newton com dois chutes iniciais')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.legend()
chutes = [0.0428, 0.05, 0.06, 0.1, 0.2, 0.5, 1.0]
ax2.bar(range(len(chutes)), [len(newton(x0)) - 1 for x0 in chutes], color=VERDE)
ax2.set_xticks(range(len(chutes)), [f'{x0:g}' for x0 in chutes])
ax2.set(xlabel='Chute inicial V₀ (m³)', ylabel='Iterações até a tolerância', title='Newton: sensibilidade ao chute')
fig.savefig(PASTA / 'ex8-newton.png', dpi=180)
print('\nGráficos salvos na pasta:', PASTA)
plt.show()
