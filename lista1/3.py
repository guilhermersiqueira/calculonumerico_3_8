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
