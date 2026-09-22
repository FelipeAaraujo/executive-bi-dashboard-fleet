# Executive BI Dashboard & Automation

**Python (pipeline) + SQL + Power BI — de 3 fontes de dado separadas a um painel único, atualizado automaticamente**

## Contexto
A diretoria da RotaViva recebia relatório mensal montado manualmente em Excel, juntando dados de
frota (Projeto 1), rentabilidade por rota (Projeto 2) e previsão de demanda (Projeto 5) em
planilhas separadas — processo lento e sujeito a erro humano.

## Problema de negócio
Consolidar as três fontes num único pipeline automatizado (extract → transform → load) e entregar
um painel executivo de uma tela só, sem depender de trabalho manual mensal.

## O que foi consolidado
- Dados de frota e manutenção (Projeto 1: 21.719 viagens, 60 veículos).
- Dados de rentabilidade por rota (Projeto 2: 20.173 viagens, 25 rotas).
- Previsão de demanda por região (Projeto 5).

## Pipeline (`consolidate.py`)
Script Python único que lê as 3 fontes, aplica as transformações (padronização, cálculo de custo
total e margem, agregação mensal) e grava um modelo dimensional simplificado (fato de viagens +
KPIs mensais), pronto para o Power BI consumir.

## Resultado (medido na execução real do pipeline)
- **Pipeline executado ponta a ponta em 0,74 segundos**, consolidando as 3 fontes automaticamente
  — elimina o trabalho manual de juntar planilhas mês a mês.
- KPIs executivos consolidados e recalculados automaticamente a cada rodada: faturamento mensal
  (R$ 6,0M–6,6M), margem consolidada estável em **~80%**, disponibilidade média da frota de
  **94,0%**, custo de manutenção total de **R$ 679.218,55** no período.
- O painel evidencia que os mesmos veículos problemáticos identificados no Projeto 1 (custo de
  manutenção) também aparecem entre os de rota menos rentável do Projeto 2 — uma correlação que só
  fica visível quando os dados são vistos juntos, não em relatórios separados.

## Recomendação
Tratar os veículos que aparecem simultaneamente nos alertas de manutenção e de baixa rentabilidade
como prioridade única e transversal, em vez de decisões isoladas por área.

## Ferramentas
Python (pipeline de consolidação), SQL, Power BI (camada de apresentação).

## Competências demonstradas
Automação de pipeline (ETL simplificado), modelagem dimensional, integração de múltiplas fontes,
storytelling executivo orientado a dado real e mensurável.

