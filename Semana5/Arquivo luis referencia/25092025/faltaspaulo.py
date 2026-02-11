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
nome_falta_b = "FT_B"
dss.text(f"New fault.{nome_falta_b} bus1={barra_falta}.2 phases=1 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_b} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_b}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_b}")

# --- FT_C (Falta Fase C - Terra) ---
nome_falta_c = "FT_C"
dss.text(f"New fault.{nome_falta_c} bus1={barra_falta}.3 phases=1 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_c} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_c}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_c}")

# ==========================================================
# 2. FALTAS BIFÁSICAS COM TERRA (3 TIPOS) - L-L-G
# ==========================================================

# --- FFT_AB (Falta Fase A-B - Terra) ---
nome_falta_fft_ab = "FFT_AB"
dss.text(f"New fault.{nome_falta_fft_ab} bus1={barra_falta}.1.2 phases=2 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_fft_ab} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_fft_ab}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_fft_ab}")

# --- FFT_BC (Falta Fase B-C - Terra) ---
nome_falta_fft_bc = "FFT_BC"
dss.text(f"New fault.{nome_falta_fft_bc} bus1={barra_falta}.2.3 phases=2 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_fft_bc} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_fft_bc}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_fft_bc}")

# --- FFT_AC (Falta Fase A-C - Terra) ---
nome_falta_fft_ac = "FFT_AC"
dss.text(f"New fault.{nome_falta_fft_ac} bus1={barra_falta}.1.3 phases=2 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_fft_ac} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_fft_ac}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_fft_ac}")

# ==========================================================
# 3. FALTAS BIFÁSICAS ISOLADAS (3 TIPOS) - L-L
# ==========================================================

# --- FF_AB (Falta Fase A-B Isolada) ---
nome_falta_ff_ab = "FF_AB"
dss.text(f"New fault.{nome_falta_ff_ab} bus1={barra_falta}.1 bus2={barra_falta}.2 phases=1 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_ff_ab} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_ff_ab}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_ff_ab}")

# --- FF_BC (Falta Fase B-C Isolada) ---
nome_falta_ff_bc = "FF_BC"
dss.text(f"New fault.{nome_falta_ff_bc} bus1={barra_falta}.2 bus2={barra_falta}.3 phases=1 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_ff_bc} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_ff_bc}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_ff_bc}")

# --- FF_AC (Falta Fase A-C Isolada) ---
nome_falta_ff_ac = "FF_AC"
dss.text(f"New fault.{nome_falta_ff_ac} bus1={barra_falta}.1 bus2={barra_falta}.3 phases=1 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_ff_ac} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_ff_ac}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_ff_ac}")

# ==========================================================
# 4. FALTAS TRIFÁSICAS (2 TIPOS)
# ==========================================================

# --- FFFT_ABC (Falta Trifásica com Terra) - L-L-L-G ---
nome_falta_abc_t = "FFFT_ABC"
dss.text(f"New fault.{nome_falta_abc_t} bus1={barra_falta}.1.2.3 phases=3 r={resistencia_falta}")
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_abc_t} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_abc_t}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_abc_t}")


# --- FFF_ABC (Falta Trifásica Isolada) - L-L-L ---
nome_falta_abc = "FFF_ABC"
# FFF (Isolada): curto-circuitando as fases a um BUS FICTÍCIO (DUMMY_BUS)
dss.text(f"New fault.{nome_falta_abc} bus1={barra_falta}.1.2.3 bus2=DUMMY_BUS.1.2.3 phases=3 r={resistencia_falta}") 
# --- Comandos SOLVE e EXPORT inseridos ---
dss.text("reset monitors")

# 5. Resolve circuito
dss.text("set mode=snap")
dss.text("solve")
print(f"Solução para {nome_falta_abc} executada com sucesso.")

# ⚡ ADICIONAR ESSA LINHA AQUI ⚡
dss.text("sample") # captura a amostra nos monitores

# 6. Exporta monitor (com nome único)
nome_arquivo_csv = f"Mon_Falta_{nome_falta_abc}"
mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 7. Lê resultado
csv_path = os.path.join(script_path, f"{nome_arquivo_csv}.CSV")
if not os.path.exists(csv_path):
    # alguns casos o OpenDSS salva com outro nome (fallback para o nome de arquivo único)
    csv_path = os.path.join(script_path, f"ieee34mod1_Mon_{nome_arquivo_csv.lower()}_1.csv")

dss.text(f"Remove fault.{nome_falta_abc}")



