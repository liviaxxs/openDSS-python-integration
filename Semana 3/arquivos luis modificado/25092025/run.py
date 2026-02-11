import os
import pathlib
import py_dss_interface

from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("ieee37.dss")

dss = py_dss_interface.DSS()

dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")

dss.text("New EnergyMeter.Met_Ini    element=Line.L35 terminal=1")
dss.text("New Monitor.Mon_Ini        element=Line.L35 terminal=1 mode=1")

dss.text("New EnergyMeter.Met_Ramal  element=Line.L9  terminal=1")
dss.text("New Monitor.Mon_Ramal      element=Line.L9  terminal=1 mode=1")

dss.text("reset meters")
dss.text("reset monitors")
# =========================================================
# 1. SIMULAÇÃO PRÉ-FALTA (Medição "Antes")
# =========================================================
print("Simulando condição PRÉ-FALTA...")

dss.text("solve")

dss.text("sample")
dss.text("save monitors")

meters_csv   = dss.text("export meters")
mon_ini_csv  = dss.text("export monitor Mon_Ini")
mon_ram_csv  = dss.text("export monitor Mon_Ramal")

print("here")
# =========================================================
# 2. INSERÇÃO DA FALTA MONOFÁSICA
# =========================================================
dss.text("Nova falta monofasica (Fase A) no barramento 701.1 com 5 ohm")
dss.text("New Fault.Falta bus1=701.1 phases=1 r=5")

print("Simulando condição PÓS-FALTA (com a falta inserida)...")
dss.text("solve")
dss.text("sample") # Captura os novos dados do monitor

# Exporta os dados dos monitores no estado pós-falta.
# Os arquivos terão o sufixo _POST: Mon_Ini_POST.csv, Mon_Ramal_POST.csv
dss.monitors_write_name("Mon_Ini")
mon_ini_post_csv = dss.text("export monitor Mon_Ini_POST") 
dss.monitors_write_name("Mon_Ramal")
mon_ramal_post_csv = dss.text("export monitor Mon_Ramal_POST") 

# Exporta o EnergyMeter (agora no estado pós-falta)
meters_post_csv = dss.text("export meters")

print("\nArquivos CSV gerados com sucesso:")
print(f"Pré-Falta (Monitores): {mon_ini_csv}, {mon_ram_csv}") 
print(f"Pós-Falta (Monitores): {mon_ini_post_csv}, {mon_ramal_post_csv}")
print(f"Medidores (Última Exportação - Pós-Falta): {meters_post_csv}")