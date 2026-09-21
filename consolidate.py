import pandas as pd, time

t0 = time.time()

# --- Extract: reuse data already generated for projects 1, 2, 5 ---
viagens1 = pd.read_csv("/mnt/user-data/outputs/projeto1-fleet-logistics-analytics/viagens.csv")
manut1 = pd.read_csv("/mnt/user-data/outputs/projeto1-fleet-logistics-analytics/manutencoes.csv")
veic1 = pd.read_csv("/mnt/user-data/outputs/projeto1-fleet-logistics-analytics/veiculos.csv")

viagens2 = pd.read_csv("/mnt/user-data/outputs/projeto2-route-profitability-sql/viagens.csv")
rotas2 = pd.read_csv("/mnt/user-data/outputs/projeto2-route-profitability-sql/rotas.csv")

demanda5 = pd.read_csv("/mnt/user-data/outputs/projeto5-demand-forecasting/demanda_mensal_regiao.csv")

# --- Transform: build a simple star schema ---
# dim_veiculo
dim_veiculo = veic1.copy()

# fact_viagem (from project 1: has fuel/toll/loading, availability)
fact_viagem = viagens1[["id_viagem","id_veiculo","regiao","data_viagem","km_rodado",
                         "custo_combustivel","custo_pedagio","faturamento_viagem"]].copy()
fact_viagem["custo_total"] = fact_viagem["custo_combustivel"] + fact_viagem["custo_pedagio"]
fact_viagem["margem"] = fact_viagem["faturamento_viagem"] - fact_viagem["custo_total"]

# fact_manutencao
fact_manutencao = manut1.copy()

# executive KPI aggregation
kpi_mensal = fact_viagem.copy()
kpi_mensal["mes"] = pd.to_datetime(kpi_mensal["data_viagem"]).dt.to_period("M").astype(str)
kpi_mensal = kpi_mensal.groupby("mes").agg(
    faturamento=("faturamento_viagem","sum"),
    custo=("custo_total","sum"),
    margem=("margem","sum"),
    viagens=("id_viagem","count"),
    km_total=("km_rodado","sum"),
).reset_index()
kpi_mensal["margem_pct"] = kpi_mensal["margem"]/kpi_mensal["faturamento"]*100

manut_total = fact_manutencao["custo_manutencao"].sum()
faturamento_total = kpi_mensal["faturamento"].sum()
margem_total = kpi_mensal["margem"].sum() - manut_total
disponibilidade_media = viagens1["disponibilidade_mes_veiculo"].mean()

fact_viagem.to_csv("/home/claude/project6/fact_viagem.csv", index=False)
kpi_mensal.to_csv("/home/claude/project6/kpi_mensal_executivo.csv", index=False)

elapsed = time.time() - t0
print(f"Pipeline executado em {elapsed:.2f} segundos (extract -> transform -> load de 3 fontes)")
print(f"Faturamento total (12m, Projeto 1): R$ {faturamento_total:,.2f}")
print(f"Margem total apos manutencao: R$ {margem_total:,.2f}")
print(f"Disponibilidade media da frota: {disponibilidade_media*100:.1f}%")
print(f"Custo de manutencao total: R$ {manut_total:,.2f}")
print(kpi_mensal.to_string(index=False))
