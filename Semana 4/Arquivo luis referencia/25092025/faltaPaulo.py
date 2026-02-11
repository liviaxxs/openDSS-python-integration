import os
import pathlib
import py_dss_interface
import pandas as pd

# 1. Configurações ESSENCIAIS (Mantidas)
# O usuário deve garantir que 'ieee34Mod1.dss' esteja no local correto.
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("ieee34Mod1.dss")

# Inicializa o OpenDSS, compila o circuito e define o DataPath
dss = py_dss_interface.DSS()
dss.text(f"compile [{dss_file}]")
# CORREÇÃO CRÍTICA: Adiciona aspas duplas ao caminho para evitar erros com espaços (Windows Path)
dss.text(f'set datapath="{script_path}"')

# ==========================================================
# ESPAÇO PARA CONFIGURAÇÃO DE MEDIÇÃO (CORRIGIDO)
# ==========================================================
# ADIÇÃO: EnergyMeter é necessário para definir a zona de medição do Fault (Erro 287261)
dss.text("New Energymeter.Substation_Meter element=Line.L2 terminal=1")

# Monitor de Tensão no barramento 802 (Modo=0: tensão p.u. e L-N)
dss.text("set mode=snap")
# Monitor 'Mon_Falta' definido no mesmo elemento do EnergyMeter
dss.text("New Monitor.Mon_Falta element=Line.L2 terminal=1 mode=0")
# ==========================================================


# Definições Comuns para Faltas
barra_falta = 802
resistencia_falta = 5 # Ohms

# ==========================================================
# 1. FALTAS MONOFÁSICAS (3 TIPOS) - L-G
# ==========================================================

# --- FT_A (Falta Fase A - Terra) ---
nome_falta_a = "FT_A"
dss.text(f"New fault.{nome_falta_a} bus1={barra_falta}.1 phases=1 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("calcv")
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_a} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_a}"
dss.text(f"set casename={nome_arquivo_csv}")
mon_falta_csv = dss.text(f"export monitor Mon_Falta")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"edit fault.{nome_falta_a} enabled=no")

# --- FT_B (Falta Fase B - Terra) ---
