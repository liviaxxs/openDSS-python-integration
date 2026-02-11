import os
import pathlib
import py_dss_interface
import pandas as pd

# 1. Configurações
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("ieee34Mod1.dss")

dss = py_dss_interface.DSS()
print("Nova instância do OpenDSS inicializada.")

# 2. Compila o circuito
dss.text(f"compile [{dss_file}]")
print(f"Circuito {dss_file.name} compilado com sucesso.")

# 3. Falta monofásica (fase A, barramento 4)
dss.text("New fault.Falta_A bus1=802.1 phases=1 r=5")
print("Falta monofásica adicionada no barramento 802 com R=5Ω")

# Monitor de Tensão no barramento 802 (Modo=0: tensão p.u. e L-N)
dss.text("New Monitor.Mon_Falta element=Line.L2 terminal=1 mode=0")
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print("Solução executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample")  # captura a amostra nos monitores

# 6. Exporta monitor (com caminho protegido entre aspas)
dss.text(f'set datapath="{script_path}"')
mon_falta_csv = dss.text("export monitor Mon_Falta")
print(f"Monitor exportado para: {mon_falta_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, "Mon_Falta.csv")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome
    alt_csv = os.path.join(script_path, "IEEE4NODE_Mon_Mon_Falta_1.csv")
    if os.path.exists(alt_csv):
        csv_path = alt_csv

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print("\n--- Amostra dos Dados ---")
    print(df.head())
else:
    print("⚠️ O arquivo CSV do monitor não foi criado ou está vazio.")

