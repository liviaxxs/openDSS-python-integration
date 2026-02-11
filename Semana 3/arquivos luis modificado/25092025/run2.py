import os
import pathlib
import py_dss_interface
import pandas as pd # Importar pandas para ler o arquivo CSV depois

# 1. Configurações de Arquivo
script_path = os.path.dirname(os.path.abspath(__file__))
# Assumindo que seu arquivo ieee37.dss está na mesma pasta
dss_file = pathlib.Path(script_path).joinpath("ieee37.dss")

# 2. Inicializa o OpenDSS
dss = py_dss_interface.DSS()

# 3. Compila o Circuito
dss.text(f"compile [{dss_file}]")
print(f"Circuito {dss_file.name} compilado com sucesso.")

# 4. Define o Monitor em uma Linha/Barramento de Interesse
# Vamos usar a Linha L1, Terminal 1 (o barramento)
# Mode=0: Salva Tensão (V) e Corrente (I) complexa (Magnitude e Ângulo).
dss.text("New Monitor.Mon_Regime element=Line.L1 terminal=1 mode=0") 
print("Monitor 'Mon_Regime' instalado na Linha L1 para medir T/C em regime.")

# 5. Executa a Solução de Fluxo de Potência (Snapshot)
# Isto é o regime normal, sem falta
dss.text("solve")
print("Solução em regime (sem falta) executada.")

# 6. Captura a Amostra no Monitor e Exporta
# O comando "sample" registra os valores no monitor.
dss.text("sample")
# O comando "export monitor" salva o resultado em um arquivo CSV.
mon_regime_csv = dss.text("export monitor Mon_Regime") 
print(f"Dados do regime normal exportados para: {mon_regime_csv}")

# 7. (Opcional, mas útil) Lê e mostra o resultado
df_regime = pd.read_csv(mon_regime_csv)
print("\n--- Amostra dos Dados de Regime Normal (Sem Falta) ---")
print(df_regime.head()) 
print(f"Linhas no CSV: {len(df_regime)}")
# Note que só há uma linha, pois foi um único 'solve' seguido de 'sample'.