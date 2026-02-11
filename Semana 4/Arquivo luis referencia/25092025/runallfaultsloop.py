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



dss.text("New Energymeter.Substation element=Line.L6 terminal=1")

# Mapeamento e Definições (necessário para este bloco funcionar):



fase_map = {
  'A': '1',

  'B': '2',

  'C': '3'

 

}

fases_letras = ['A', 'B', 'C']

barra_falta = 812

resistencia_falta = 5



# ==========================================================

# 0. CONFIGURAÇÃO E CRIAÇÃO DO MONITOR (APENAS UMA VEZ)

# ==========================================================

dss.text("set mode=snap")

# Monitora a Corrente (I) da Linha 2 (ajuste para o nome da sua linha)

dss.text("New Monitor.Mon_Falta element=Line.L2 terminal=1 mode=0")

print("Monitor 'Mon_Falta' criado com sucesso.")



for fase in fases_letras:



 fase_numero = fase_map[fase]

 nome_falta = f"FT_{fase}" # FT_A, FT_B, FT_C



# 1. PREPARAÇÃO: Zera o monitor para capturar APENAS esta falta

 dss.text("Reset Monitors")

 # 2. CRIA E SOLUCIONA A FALTA

 dss.text(f"New fault.{nome_falta} bus1=802.{fase_numero} phases=1 r=5")



 print(f"Falta monofásica na fase {fase} adicionada no barramento 802 com R=5Ω")


# set mode=snap é redundante, pois o Monitor já está em mode=0

dss.text("solve")


 # sample é desnecessário em mode=0 (snapshot), pois ele coleta automaticamente



 # 3. EXPORTAÇÃO: O NOME DO ARQUIVO CSV AGORA É ÚNICO (ex: Mon_Falta_FT_A.CSV)

nome_arquivo_csv = f"Mon_Falta_{nome_falta}"

 # Não precisa de 'set datapath' se você quer salvar na pasta do script

mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_csv}")

# 4. LIMPEZA

dss.text(f"Remove fault.{nome_falta}")


 # Feedback no terminal

print(f"-> Falta {fase}-T (monofásica) simulada. Dados exportados para: {mon_falta_csv}")





# Mapeamento e Lista (necessário para este bloco funcionar):

# fase_map = {'A': '1', 'B': '2', 'C': '3'}

# fases_letras = ['A', 'B', 'C']

barra_falta = 802

resistencia_falta = 5



print("\n--- 2. INICIANDO FALTAS BIFÁSICAS (3 C/ TERRA e 3 ISOLADAS) ---")



for i in range(len(fases_letras)):

 for j in range(i + 1, len(fases_letras)):
  
  fase1_letra = fases_letras[i]

  fase2_letra = fases_letras[j]

  fase1_numero = fase_map[fase1_letra]

  fase2_numero = fase_map[fase2_letra]

  nome_base = f"{fase1_letra}{fase2_letra}" # Ex: AB


 # ==========================================================

 # 1. SIMULAÇÃO BIFÁSICA COM TERRA (X-Y-T) - 3 TIPOS

 # ==========================================================

  dss.text("Reset Monitors") # Zera o monitor SÓ para esta nova falta


  nome_falta_terra = f"FFT_{nome_base}"

  dss_cmd_terra = f"New fault.{nome_falta_terra} bus1={barra_falta}.{fase1_numero}.{fase2_numero} phases=2 r={resistencia_falta}"


  dss.text(dss_cmd_terra)

  dss.text("solve")

 # Exporta com nome único: Mon_Falta_FFT_AB.CSV, Mon_Falta_FFT_BC.CSV, etc.

  nome_arquivo_terra = f"Mon_Falta_{nome_falta_terra}"

  mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_terra}")


 # Limpa o circuito (REMOVE SÓ ESTA FALTA)

 dss.text(f"Remove fault.{nome_falta_terra}")

 print(f"-> Falta {nome_base}-T (c/ Terra) simulada. Arquivo: {mon_falta_csv}")

 # ==========================================================

 # 2. SIMULAÇÃO BIFÁSICA ISOLADA (X-Y) - 3 TIPOS

 # ==========================================================

 dss.text("Reset Monitors") # Zera o monitor SÓ para esta segunda falta



 nome_falta_isolada = f"FF_{nome_base}"

 dss_cmd_isolada = f"New fault.{nome_falta_isolada} bus1={barra_falta}.{fase1_numero} bus2={barra_falta}.{fase2_numero} phases=2 r={resistencia_falta}"



 dss.text(dss_cmd_isolada)

 dss.text("solve")

# Exporta com nome único: Mon_Falta_FF_AB.CSV, Mon_Falta_FF_BC.CSV, etc.

 nome_arquivo_isolada = f"Mon_Falta_{nome_falta_isolada}"

 mon_falta_csv = dss.text(f"export monitor Mon_Falta {nome_arquivo_isolada}")


# Limpa o circuito (REMOVE SÓ ESTA FALTA)

dss.text(f"Remove fault.{nome_falta_isolada}")

print(f"-> Falta {nome_base} (Isolada) simulada. Arquivo: {mon_falta_csv}")

# 3a. FALTA TRIFÁSICA C/ TERRA (A-B-C-T) - 10º Tipo

nome_falta_abc_t = "FFFT_ABC"

dss.text("Reset Monitors")

dss.text(f"New fault.{nome_falta_abc_t} bus1={barra_falta}.1.2.3 phases=3 r={resistencia_falta}")

dss.text("solve")

nome_arquivo_abc_t = f"Mon_Falta_{nome_falta_abc_t}"

dss.text(f"export monitor Mon_Falta {nome_arquivo_abc_t}")

dss.text(f"Remove fault.{nome_falta_abc_t}")

print(f"-> Falta A-B-C-T (c/ Terra) simulada. Arquivo: {nome_arquivo_abc_t}.CSV")

# 3b. FALTA TRIFÁSICA ISOLADA (A-B-C) - 11º Tipo

nome_falta_abc = "FFF_ABC"

dss.text("Reset Monitors")

# CORREÇÃO: Usando bus1, bus2 e bus3 para garantir que não toque o terra

dss.text (f"New fault.{nome_falta_abc} bus1={barra_falta}.1.2.3 bus2={barra_falta}.1.2.3 phases=3 r={resistencia_falta}")

dss.text("solve")

nome_arquivo_abc = f"Mon_Falta_{nome_falta_abc}"

dss.text(f"export monitor Mon_Falta {nome_arquivo_abc}")

dss.text(f"Remove fault.{nome_falta_abc}")

print(f"-> Falta A-B-C (Isolada) simulada. Arquivo: {nome_arquivo_abc}.CSV")



print("\n\n*** SIMULAÇÃO CONCLUÍDA: 11 arquivos CSV gerados. ***")



