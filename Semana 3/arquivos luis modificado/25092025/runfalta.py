import os
import pathlib
import py_dss_interface
import pandas as pd

# 1. Configurações de Arquivo
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("ieee37.dss")

# 2. Inicializa uma NOVA instância do OpenDSS
# Isso garante que a simulação comece "limpa", sem os dados do Monitor do arquivo anterior.
dss = py_dss_interface.DSS()
print("Nova instância do OpenDSS inicializada.")

# 3. Compila o Circuito (obrigatório em cada script)
dss.text(f"compile [{dss_file}]")
print(f"Circuito {dss_file.name} compilado com sucesso.")

# 4. Adiciona o Elemento Falta (Fault)
# Falta Monofásica (Fase 1-Terra) com baixa resistência.
dss.text("New Fault.Falta bus1=701.1 phases=1 r = 5")
print("Elemento 'Fault.Falta' adicionado no Barramento 701, Fase 1.")

# 5. Define o Monitor para a Falta
# Usando o modo 0 (Tensão e Corrente) na Linha L1.
dss.text("New Monitor.Mon_Falta element=Line.L1 terminal=1 mode=0")
dss.text("reset monitors") # Limpa qualquer lixo de memória anterior

# 6. Executa a Solução de Fluxo de Potência (Snapshot)
# O "solve" calcula o estado do sistema com a falta ativa.
dss.text("solve")
print("Solução de Fluxo de Potência com a Falta executada.")

# 7. Captura a Amostra e Exporta
dss.text("sample")
mon_falta_csv = dss.text("export monitor Mon_Falta") 
print(f"Dados com a Falta exportados para: {mon_falta_csv}")

# 8. (Opcional) Lê o resultado
df_falta = pd.read_csv(mon_falta_csv)
print("\n--- Amostra dos Dados com a Falta ---")
print(df_falta[[' V1_pu', ' I1', ' I1_ang']].head())