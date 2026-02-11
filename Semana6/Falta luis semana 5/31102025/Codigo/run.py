import os
import pathlib
import random
import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools

# IDEIA INICIAL: SALVAR APENAS VALORES QUE IMPORTAM
# MANTER SIMULAÇÃO E CRIAR FUNÇÃO SEPARADA QUE EXTRAIA AS INFORMAÇÕES DE TODOS OS CSVs GERADOS

script_path = os.path.dirname(os.path.abspath(__file__))# caminho do script atual
dss_file   = pathlib.Path(script_path, "ieee37.dss")
xlsx_path  = pathlib.Path(script_path, "lines_bus1.xlsx") # Excel com colunas: line, bus1
export_dir = pathlib.Path(script_path, "Antes")
export_dir.mkdir(parents=True, exist_ok=True)
export_dir_fault = pathlib.Path(script_path, "Depois")
export_dir_fault.mkdir(parents=True, exist_ok=True)

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)
dss.text(f"compile [{dss_file}]")

df = pd.read_excel(xlsx_path, dtype={"line": str, "bus1": str}) # lê o Excel garantindo que line e bus1 sejam strings
df = df[["line", "bus1"]].dropna() # mantém apenas as colunas necessárias e remove linhas nulas

line_bus1 = list(df.itertuples(index=False, name=None)) # vira lista de pares (line, bus1)

X = 5 # número de lines
X = min(X, len(line_bus1)) # total disponível de lines no Excel

selection = random.sample(line_bus1, k=X) # sorteia X pares (line, bus1) sem repetição
sorted_lines = [ln for ln, _ in selection] # extrai os nomes das lines sorteadas
print("Lines sorteadas: ", sorted_lines)
# Antes da falha
for ln, _ in selection:
    elem = f"Line.{ln}" # monta o nome completo do elemento line
    dss.text(f"New Monitor.{ln}_power    element={elem} terminal=1 mode=1 ppolar=no") # monitor de potência (P/Q)
    dss.text(f"New Monitor.{ln}_voltage  element={elem} terminal=1 mode=0") # monitor de tensão
    dss.text(f"New Monitor.{ln}_losses   element={elem} terminal=1 mode=9") # monitor de perdas
    dss.text(f"New Monitor.{ln}_seqMag   element={elem} terminal=1 mode=48") # monitor de magnitudes de sequência
    dss.text(f"New EnergyMeter.{ln}_meter element={elem} terminal=1") # medidor de energia
    print(f"Monitors/Meter criados para {elem}")

dss.text("reset monitors")
dss.text("reset meters")
dss.text(f'set datapath="{export_dir}"')  
dss.text("solve")
dss.text("sample")
dss.text("save monitors")
dss.text("export monitors all")
dss.text("export meters /multiple")

# Depois da falha
for ln, b1 in selection: # percorre cada par (line, bus1) sorteado
    dss.text(f"New fault.{ln}_fault bus1={b1}.1 phases=1 r=5") # cria falta monofásica no nó 1 do bus1
    print(f"Fault em {b1}.1 (line {ln})")

for ln, _ in selection:
    dss.text(f"New Monitor.{ln}_power_fault    element={elem} terminal=1 mode=1 ppolar=no") # monitor de potência (P/Q)
    dss.text(f"New Monitor.{ln}_voltage_fault  element={elem} terminal=1 mode=0") # monitor de tensão
    dss.text(f"New Monitor.{ln}_losses_fault   element={elem} terminal=1 mode=9") # monitor de perdas
    dss.text(f"New Monitor.{ln}_seqMag_fault   element={elem} terminal=1 mode=48") # monitor de magnitudes de sequência
    dss.text(f"New EnergyMeter.{ln}_meter_fault element={elem} terminal=1") # medidor de energia
    print(f"Monitors/Meter criados para {elem}")


dss.text("reset monitors")
dss.text("reset meters")
dss.text(f'set datapath="{export_dir_fault}"')  
dss.text("solve")
dss.text("sample")
dss.text("save monitors")
dss.text("export monitors all")
dss.text("export meters /multiple")