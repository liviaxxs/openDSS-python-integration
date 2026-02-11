import os
import pathlib
import random
import re
import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools
from pathlib import Path

# Função criada que recebe o local onde os CSVs serão salvos (folder), os nomes de cada tipo de CSV e se vai ou não apagar os arquivos originais
def squash_folder(folder, out_mon, out_meter, delete=True):
    p = Path(folder) # recebe o path da pasta folder
    # considera .csv e .CSV e ignora os arquivos finais
    csvs = [f for f in p.glob("*.[cC][sS][vV]") if f.name not in {out_mon, out_meter}]
    # meters por regex, monitores = o restante
    meters = [f for f in csvs if re.search(r"(meter|energymeter)", f.name, re.IGNORECASE)]
    monitors = [f for f in csvs if f not in meters]

    if monitors:
        pd.concat([pd.read_csv(f, sep=None, engine="python").assign(source=f.name) for f in monitors], ignore_index=True).to_csv(p / out_mon, index=False)
        print(f"Arquivos dos Monitors unificados")
        if delete:
            for f in monitors:
                try: f.unlink()
                except: pass

    if meters:
        pd.concat([pd.read_csv(f, sep=None, engine="python").assign(source=f.name) for f in meters], ignore_index=True).to_csv(p / out_meter, index=False)
        print(f"Arquivos dos Meters unificados")
        if delete:
            for f in meters:
                try: f.unlink()
                except: pass

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file   = pathlib.Path(script_path, "ieee37.dss")
xlsx_path  = pathlib.Path(script_path, "lines_bus1.xlsx")  # Excel: ['line','bus1']
export_dir = pathlib.Path(script_path, "Antes");   export_dir.mkdir(parents=True, exist_ok=True)
export_dir_fault = pathlib.Path(script_path, "Depois"); export_dir_fault.mkdir(parents=True, exist_ok=True)

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)
dss.text(f"compile [{dss_file}]")

df = pd.read_excel(xlsx_path, dtype={"line": str, "bus1": str}).loc[:, ["line", "bus1"]].dropna()
line_bus1 = list(df.itertuples(index=False, name=None))  # [(line, bus1), ...]

X = 5
X = min(X, len(line_bus1))
selection = random.sample(line_bus1, k=X)
sorted_lines = [ln for ln, _ in selection]
print("Lines sorteadas:", sorted_lines)

# ANTES DA FALHA
for ln, _ in selection:
    elem = f"Line.{ln}"
    dss.text(f"New Monitor.{ln}_power    element={elem} terminal=1 mode=1 ppolar=no")
    dss.text(f"New Monitor.{ln}_voltage  element={elem} terminal=1 mode=0")
    dss.text(f"New Monitor.{ln}_losses   element={elem} terminal=1 mode=9")
    dss.text(f"New Monitor.{ln}_seqMag   element={elem} terminal=1 mode=48")
    dss.text(f"New EnergyMeter.{ln}_meter element={elem} terminal=1")
    print(f"Monitors/Meter criados para {elem}")

dss.text("reset monitors")
dss.text("reset meters")
dss.text(f'set datapath="{export_dir}"')
dss.text("solve")
dss.text("sample")
#dss.text("save monitors")
dss.text("export monitors all")
dss.text("export meters /multiple")

squash_folder(export_dir, "Monitors_ALL.csv", "EnergyMeters_ALL.csv")

dss.text("clear") # limpa circuito atual
dss.text(f"compile [{dss_file}]") # recompila

# DEPOIS DA FALHA
for ln, b1 in selection:
    dss.text(f"New fault.{ln}_fault bus1={b1}.1 phases=1 r=5")
    print(f"Fault em {b1}.1 (line {ln})")

for ln, _ in selection:
    elem = f"Line.{ln}"
    dss.text(f"New Monitor.{ln}_power_fault    element={elem} terminal=1 mode=1 ppolar=no")
    dss.text(f"New Monitor.{ln}_voltage_fault  element={elem} terminal=1 mode=0")
    dss.text(f"New Monitor.{ln}_losses_fault   element={elem} terminal=1 mode=9")
    dss.text(f"New Monitor.{ln}_seqMag_fault   element={elem} terminal=1 mode=48")
    dss.text(f"New EnergyMeter.{ln}_meter_fault element={elem} terminal=1")
    print(f"Monitors/Meter (com FAULT) criados para {elem}")

dss.text("reset monitors")
dss.text("reset meters")
dss.text(f'set datapath="{export_dir_fault}"')
dss.text("solve")
dss.text("sample")
#dss.text("save monitors")
dss.text("export monitors all")
dss.text("export meters /multiple")

squash_folder(export_dir_fault, "Monitors_FAULT_ALL.csv", "EnergyMeters_FAULT_ALL.csv")