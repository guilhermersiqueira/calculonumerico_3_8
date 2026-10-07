# Cálculo Numérico — Lista 1

Resoluções dos exercícios 3 e 8, com os códigos em Python, os resultados e os gráficos.

- **[Exercício 3](ex3.md):** sucessão I₀ = (e − 1)/e, Iₙ₊₁ = 1 − (n + 1)Iₙ, propagação de erros e comparação com a recorrência inversa.
- **[Exercício 8](ex8.md):** volume de um gás de CO₂ pela equação de estado, com bissecção, falsa-posição e Newton-Raphson.

## Arquivos

| Arquivo | Descrição |
|---|---|
| [3.py](3.py) | Cálculo da sucessão em ponto flutuante, com referência de 150 dígitos e recorrência inversa. |
| [3-graph.py](3-graph.py) | Mesmos cálculos do exercício 3, com geração dos gráficos. |
| [ex3.md](ex3.md) | Resolução e discussão dos resultados do exercício 3. |
| [ex3.png](ex3.png) | Sucessão calculada, limite e amplificação do erro. |
| [ex3-estabilidade.png](ex3-estabilidade.png) | Comparação entre a recorrência progressiva e a inversa. |
| [8.py](8.py) | Cálculo do volume por bissecção, falsa-posição e Newton-Raphson. |
| [8-graph.py](8-graph.py) | Mesmos cálculos do exercício 8, com geração dos gráficos. |
| [ex8.md](ex8.md) | Resolução e análise da convergência do exercício 8. |
| [ex8.png](ex8.png) | Função da equação de estado e convergência dos três métodos. |
| [ex8-newton.png](ex8-newton.png) | Newton com diferentes chutes iniciais. |

## Como executar

Os códigos usam Python 3. Para instalar as bibliotecas necessárias:

```bash
python -m pip install numpy matplotlib
```

Abra o terminal nesta pasta. Para executar apenas os cálculos:

```bash
python 3.py
python 8.py
```

Para executar os cálculos e gerar os gráficos:

```bash
python 3-graph.py
python 8-graph.py
```

Cada arquivo funciona separadamente. Os gráficos são salvos na mesma pasta dos códigos e já estão incluídos aqui para consulta. O `3.py` e o `8.py` usam apenas bibliotecas que vêm com o Python; as versões com gráficos precisam do Matplotlib, e o `8-graph.py` também usa NumPy.

No exercício 3, a referência é calculada com 150 dígitos e a sucessão é mostrada até n = 30. No exercício 8, os três métodos usam a mesma tolerância de 10⁻¹² para a diferença entre iterações.

As explicações, as tabelas de resultados e as referências estão em [ex3.md](ex3.md) e [ex8.md](ex8.md).
