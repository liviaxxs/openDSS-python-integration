#Semana_3
import os
import pathlib
import py_dss_interface
import pandas as pd

from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("ieee37.dss")

dss = py_dss_interface.DSS()

dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")

dss.text("New Monitor.Mon_Ini element=Line.L1 terminal=1 mode=0")

dss.text("reset monitors")

dss.text("solve")

dss.text("sample")
dss.text("save monitors")

mon_ini_csv  = dss.text("export monitor Mon_Ini")
print(f"Dados iniciais exportados para: {mon_ini_csv}")

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

df_falta = pd.read_csv(mon_falta_csv)

# remove espaços das colunas
df_falta.columns = df_falta.columns.str.strip()

print(df_falta[['V1','I1','IAngle1']].head())

