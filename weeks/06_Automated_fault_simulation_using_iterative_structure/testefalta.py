import os
import pathlib
import py_dss_interface
import pandas as pd

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("ieee37.dss")

# Inicializa o OpenDSS e compila o circuito
dss = py_dss_interface.DSS()
dss.text(f"compile [{dss_file}]")
dss.text("New Energymeter.Substation_Meter element=Line.L2 terminal=1")
dss.text("Set mode=snap")

barra_falta = 802
resistencia_falta = 5

# ======== Faltas monofásicas ========
for n in range(1, 4):
    nome_falta = f"FT_phase_{n}"
    monitor_name = f"Mon_{nome_falta}"

    print(f"\n➡️ Executando {nome_falta}...")

    dss.text(f"New Fault.{nome_falta} bus1={barra_falta}.{n} phases=1 r={resistencia_falta}")
    dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

    dss.text("Reset Monitors")
    dss.text("CalcV")
    dss.text("Set mode=snap")
    dss.text("Solve")
    dss.text("Sample")

    nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
    dss.text(f"Set casename={nome_arquivo_csv}")
    dss.text(f"Export Monitor {monitor_name}")

    csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
    if os.path.exists(csv_path):
        print(f"✅ Arquivo criado: {csv_path}")
    else:
        print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

    dss.text(f"Edit Fault.{nome_falta} enabled=no")

# ======== Faltas bifásicas com terra ========
for n in range(1, 4):
    for m in range(n + 1, 4):
        nome_falta_bifasica_terra = f"FT_phase_{n}{m}_T"
        monitor_name_bifasico_terra = f"Mon_{nome_falta_bifasica_terra}"

        print(f"\n➡️ Executando {nome_falta_bifasica_terra} (bifásica + terra)...")

        dss.text(f"New Fault.{nome_falta_bifasica_terra} bus1={barra_falta}.{n}{m} phases=2 r={resistencia_falta}")
        dss.text(f"New Monitor.{monitor_name_bifasico_terra} element=Line.L2 terminal=1 mode=0")

        dss.text("Reset Monitors")
        dss.text("CalcV")
        dss.text("Set mode=snap")
        dss.text("Solve")
        dss.text("Sample")

        nome_arquivo_csv_bifasico = f"Mon_Falta_{nome_falta_bifasica_terra}"
        dss.text(f"Set casename={nome_arquivo_csv_bifasico}")
        dss.text(f"Export Monitor {monitor_name_bifasico_terra}")

        csv_path_bifasico = os.path.join(script_path, f"{nome_arquivo_csv_bifasico}.CSV")
        if os.path.exists(csv_path_bifasico):
            print(f"✅ Arquivo criado: {csv_path_bifasico}")
        else:
            print(f"⚠️ Nenhum CSV encontrado para {monitor_name_bifasico_terra}")

        dss.text(f"Edit Fault.{nome_falta_bifasica_terra} enabled=no")

# ======== Faltas bifásicas sem terra ========
for n in range(1, 4):
    for m in range(n + 1, 4):
        nome_falta_bifasica = f"FT_phase_{n}{m}"
        monitor_name_bifasico = f"Mon_{nome_falta_bifasica}"

        print(f"\n➡️ Executando {nome_falta_bifasica} (bifásica sem terra)...")

        dss.text(f"New Fault.{nome_falta_bifasica} bus1={barra_falta}.{n} bus2={barra_falta}.{m} phases=2 r={resistencia_falta}")
        dss.text(f"New Monitor.{monitor_name_bifasico} element=Line.L2 terminal=1 mode=0")

        dss.text("Reset Monitors")
        dss.text("CalcV")
        dss.text("Set mode=snap")
        dss.text("Solve")
        dss.text("Sample")

        nome_arquivo_csv_bifasico = f"Mon_Falta_{nome_falta_bifasica}"
        dss.text(f"Set casename={nome_arquivo_csv_bifasico}")
        dss.text(f"Export Monitor {monitor_name_bifasico}")

        csv_path_bifasico = os.path.join(script_path, f"{nome_arquivo_csv_bifasico}.CSV")
        if os.path.exists(csv_path_bifasico):
            print(f"✅ Arquivo criado: {csv_path_bifasico}")
        else:
            print(f"⚠️ Nenhum CSV encontrado para {monitor_name_bifasico}")

        dss.text(f"Edit Fault.{nome_falta_bifasica} enabled=no")
# --- FALTAS TRIFÁSICAS ---

# Sem terra
nome_falta = "FT_trifasica_sem_terra"
monitor_name = f"Mon_{nome_falta}"

dss.text(f"New fault.{nome_falta} bus1={barra_falta}.1 bus2={barra_falta}.2 bus1={barra_falta}.3 phases=3 r={resistencia_falta}")
dss.text(f"New monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

dss.text("reset monitors")
dss.text("calcv")
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta} executada com sucesso.")
dss.text("sample")

nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
dss.text(f"set casename={nome_arquivo_csv}")
dss.text(f"export monitor {monitor_name}")

csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    csv_path = os.path.join(script_path, f"ieee34mod1_{monitor_name.lower()}_1.csv")

dss.text(f"edit fault.{nome_falta} enabled=no")


# Com terra
nome_falta = "FT_trifasica_com_terra"
monitor_name = f"Mon_{nome_falta}"

dss.text(f"New fault.{nome_falta} bus1={barra_falta}.1.2.3 phases=3 r={resistencia_falta}")
dss.text(f"New monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

dss.text("reset monitors")
dss.text("calcv")
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta} executada com sucesso.")
dss.text("sample")

nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
dss.text(f"set casename={nome_arquivo_csv}")
dss.text(f"export monitor {monitor_name}")

csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    csv_path = os.path.join(script_path, f"ieee34mod1_{monitor_name.lower()}_1.csv")

dss.text(f"edit fault.{nome_falta} enabled=no")


