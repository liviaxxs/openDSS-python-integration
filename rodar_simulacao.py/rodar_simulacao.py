import opendssdirect as dss
import pandas as pd

# ----------------------------------------------------
# 1. CARREGAR O CIRCUITO E RODAR A SIMULAÇÃO
# ----------------------------------------------------

# (O comando Compile já está OK, supondo que você corrigiu o nome do arquivo DSS)
dss.Text.Command("Compile circuito_principal.dss") 

dss.Text.Command("Solve")

# ----------------------------------------------------
# 2. ACESSAR E TRATAR OS RESULTADOS
# ----------------------------------------------------

print("--- TENSÕES NAS BARRAS (Exemplo) ---")

# a) Obter o nome de todas as barras
nomes_barras = dss.Circuit.AllBusNames()

# b) Obter o valor da tensão em p.u. (por unidade) para cada barra
# CORRIGIDO: O nome da função correta é AllBusMagPu
v_pu = dss.Circuit.AllBusMagPu() 

# c) Juntar os dados em uma tabela (DataFrame)
tabela_resultados = pd.DataFrame({
    'Barra': nomes_barras,
    'Tensao_PU': v_pu
})

# d) Mostrar e Salvar
print(tabela_resultados.head()) 

tabela_resultados.to_csv('resultados_finais.csv', index=False)

print("\nSimulação concluída e resultados salvos em 'resultados_finais.csv'.")

# ... (início do seu script)

dss.Text.Command("Compile circuito_principal.dss") 

# NOVO PASSO DE VERIFICAÇÃO:
# Verifica se o circuito foi carregado (o número de elementos deve ser > 0)
num_elements = dss.Circuit.NumElements()
if num_elements == 0:
    print("\nERRO CRÍTICO: O circuito não foi carregado! Verifique:\n1. O nome do arquivo DSS.\n2. Se há um comando 'Redirect' ou 'Compile' DENTRO do seu arquivo DSS que não encontra outros arquivos (Loads, Wires, etc.).")
    # Tenta obter a mensagem de erro do OpenDSS
    print(f"Mensagem de Erro do OpenDSS: {dss.Error.Description()}")
    exit() # Interrompe o script para não gerar o erro de DataFrame

    # ... (após o comando Compile)

dss.Text.Command("Compile circuito_principal.dss")

# NOVO BLOCO DE VERIFICAÇÃO:
num_elements = dss.Circuit.NumElements()
if num_elements == 0:
    print("\nERRO CRÍTICO: O OpenDSS NÃO CONSEGUIU CARREGAR O CIRCUITO!")
    print("Verifique se TODOS os arquivos (linhas, cargas, etc.) chamados no seu DSS estão na mesma pasta.")
    
    # Esta linha tenta obter a mensagem de erro detalhada do OpenDSS
    print(f"Mensagem de Erro do OpenDSS: {dss.Error.Description()}")
    exit() # Interrompe o script

dss.Text.Command("Solve")
# ... (continua a extrair os dados)

dss.Text.Command("Solve")

# ... (continua a extrair os dados)