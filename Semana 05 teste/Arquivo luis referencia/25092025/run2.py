import os
import pathlib
import py_dss_interface
import pandas as pd

# ==========================================================
# 1. CONFIGURAÇÕES INICIAIS
# ==========================================================
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("ieee34Mod1.dss")

dss = py_dss_interface.DSS()
print("Nova instância do OpenDSS inicializada.")

# 2. Compila e configura o circuito
dss.text(f"compile [{dss_file}]")
dss.text("set mode=snap")

# Parâmetros fixos
barra_falta = 802
resistencia_falta = 5

# Necessário para evitar avisos de "meter zone" e habilitar relatórios
dss.text("New EnergyMeter.Substation Line.L1 1") 

# Cria o Monitor (ÚNICA VEZ)
# ppolar=yes garante que as correntes e tensões de fase serão gravadas
dss.text("New Monitor.Mon_Falta element=Line.L2 terminal=1 mode=0 ppolar=yes")
print(f"Circuito {dss_file.name} compilado e Monitor configurado.")

print("\n*** INICIANDO SIMULAÇÃO MANUAL DE 11 TIPOS DE FALTA ***")

# Função auxiliar para simular, exportar e remover (evita repetição de código)
def simular_e_exportar(nome_falta, dss_comando):
    dss.text("Reset Monitors") 
    dss.text(dss_comando)
    dss.text("solve")
    
    nome_arquivo_csv = f"Mon_Falta_{nome_falta}.CSV"
    # Exporta com nome único para não sobrescrever
    dss.text(f"Export Mon_Falta {nome_arquivo_csv}") 
    dss.text(f"Remove fault.{nome_falta}")
    print(f"-> Falta {nome_falta} simulada. Arquivo: {nome_arquivo_csv} gerado.")

# ==========================================================
# 1. FALTAS MONOFÁSICAS C/ TERRA (3 TIPOS)
# ==========================================================

# 1. Falta A-T
nome_falta = "FT_A"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.1 phases=1 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# 2. Falta B-T
nome_falta = "FT_B"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.2 phases=1 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# 3. Falta C-T
nome_falta = "FT_C"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.3 phases=1 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# ==========================================================
# 2. FALTAS BIFÁSICAS C/ TERRA (3 TIPOS)
# ==========================================================

# 4. Falta A-B-T
nome_falta = "FFT_AB"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.1.2 phases=2 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# 5. Falta B-C-T
nome_falta = "FFT_BC"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.2.3 phases=2 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# 6. Falta C-A-T
nome_falta = "FFT_CA"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.3.1 phases=2 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# ==========================================================
# 3. FALTAS BIFÁSICAS ISOLADAS (3 TIPOS)
# ==========================================================

# 7. Falta A-B (Isolada)
nome_falta = "FF_AB"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.1 bus2={barra_falta}.2 phases=2 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# 8. Falta B-C (Isolada)
nome_falta = "FF_BC"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.2 bus2={barra_falta}.3 phases=2 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# 9. Falta C-A (Isolada)
nome_falta = "FF_CA"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.3 bus2={barra_falta}.1 phases=2 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

# ==========================================================
# 4. FALTAS TRIFÁSICAS (2 TIPOS)
# ==========================================================

# 10. Falta A-B-C-T (Trifásica c/ Terra)
nome_falta = "FFFT_ABC"
dss_cmd = f"New fault.{nome_falta} bus1={barra_falta}.1.2.3 phases=3 r={resistencia_falta}"
simular_e_exportar(nome_falta, dss_cmd)

#