# Detecção de anomalias em séries temporais com Prophet e SARIMAX

Detecção automática de picos e quedas fora do normal no volume horário de transações de um app de pagamentos, sem disparar alarme nos picos que já são esperados.

> ⚠️ A série é **sintética**, gerada em [`src/gerar_serie.py`](src/gerar_serie.py), com anomalias injetadas no último mês. Nenhum dado real é usado.

## Problema

O volume de transações tem padrão: dois picos por dia, queda de madrugada e no fim de semana, e uma leve tendência de alta. Um limite fixo não respeita esse padrão. Ou ele dispara nos picos normais, ou fica alto demais e deixa passar o que é anormal em horários calmos.

**Ideia central:** aprender o comportamento normal e alertar quando o valor observado sai do intervalo previsto *para aquele momento*.

## Abordagem

1. **EDA** das sazonalidades diária e semanal
2. **Baseline**: limite fixo de média + 3 desvios padrão
3. **Prophet** com sazonalidade diária e semanal e intervalo de 99%
4. **SARIMAX** com termos de Fourier para as duas sazonalidades e raiz quadrada para estabilizar a variância
5. **Avaliação** contra as anomalias injetadas: precision, recall e F1

Treino nos primeiros 90 dias e detecção nos 30 dias seguintes.

## Resultados (30 dias de teste, 17 horas anômalas)

| Método | Alertas | Precision | Recall | F1 |
|---|---|---|---|---|
| Limite fixo | 5 | 0,80 | 0,24 | 0,36 |
| Prophet | 26 | 0,58 | 0,88 | 0,70 |
| **SARIMAX + Fourier** | **23** | **0,70** | **0,94** | **0,80** |

## Aprendizados

- O limite fixo tem precision alta, mas perde **3 de cada 4 anomalias**, incluindo a queda de volume no horário comercial.
- Modelos que aprendem a sazonalidade pegam quase todas as anomalias.
- No SARIMAX, **estabilizar a variância** com raiz quadrada fez toda a diferença: sem ela, o recall ficava abaixo de 30%.
- O Prophet é mais prático para várias sazonalidades e feriados. O SARIMAX dá mais controle estatístico.

## Limitações e próximos passos

- Com dados sintéticos existe gabarito para medir precision e recall. Em dados reais, quase nunca há esse gabarito pronto.
- A largura do intervalo é uma decisão de negócio: mais largo gera menos alarme falso e mais anomalias perdidas.
- Próximos passos: reajustar o modelo em janela móvel, tratar feriados e agrupar alertas consecutivos em um único evento.

## Como rodar

```bash
pip install -r requirements.txt
jupyter notebook deteccao_anomalias.ipynb
```

---
Feito por [Andressa Prudente](https://github.com/dessadev)
