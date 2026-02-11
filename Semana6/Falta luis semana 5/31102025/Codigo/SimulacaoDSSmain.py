import os
import pathlib
import random
import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools

from SimulacaoDSS import SimulacaoDSS, squash_folder
import sys

def main():
    print("\n=== MENU ===")
    print("1 - Executar IEEE37 com sorteio de linhas (antes/depois da falta)")
    print("2 - Executar IEEE34 aplicando faltas em uma barra fixa")
    escolha = input("\nEscolha (1 ou 2): ")

    # =================================================================
    # OPÇÃO 1 — IEEE37 (SORTEIO)
    # =================================================================
    if escolha == "1":
        sim = SimulacaoDSS(
            dss_name="ieee37.dss",
            xlsx_name="lines_bus1.xlsx"
        )

        print("\n➡️ Compilando sistema...")
        sim.iniciar_arquivo_dss()

        print("\n➡️ Sorteando linhas...")
        sim.sortear_linhas(quantidade=5)

        print("\n➡️ Criando monitores ANTES da falta...")
        sim.configurar_monitores_antes_falta()
        sim.exportar_antes()

        print("\n➡️ Aplicando faltas nas linhas sorteadas...")
        for ln, bus in sim.linhas_sorteadas:
            print(f"\n=== Faltas na linha {ln} / barra {bus} ===")
            sim.aplicar_falta_monofasica(bus, resistencia=5)
            sim.aplicar_falta_bifasica_com_terra(bus, resistencia=5)
            sim.aplicar_falta_bifasica_sem_terra(bus, resistencia=5)
            sim.aplicar_falta_trifasica_sem_terra(bus, resistencia=5)
            sim.aplicar_falta_trifasica_com_terra(bus, resistencia=5)

        print("\n➡️ Criando monitores DEPOIS da falta...")
        sim.configurar_monitores_depois_falta()
        sim.exportar_depois()

        print("\n➡️ Comprimindo pastas (squash)...")
        squash_folder(sim.export_dir)
        squash_folder(sim.export_dir_fault)

        print("\n🎉 Finalizado com sucesso! (OPÇÃO 1)")
        return

    # =================================================================
    # OPÇÃO 2 — IEEE34 (BARRA FIXA)
    # =================================================================
    elif escolha == "2":
        sim = SimulacaoDSS(dss_name="ieee37.dss")

        print("\n➡️ Compilando sistema...")
        sim.iniciar_arquivo_dss()

        barra = input("Informe a barra para aplicar as faltas: ")
        resistencia = float(input("Informe a resistência da falta: "))
        # ❗ NÃO EXPORTA DEPOIS  
        # porque CADA função de falta já exporta os monitores internamente

        print("\n➡️ Aplicando faltas monofásicas...")
        sim.aplicar_falta_monofasica(barra, resistencia)

        print("\n➡️ Aplicando faltas bifásicas + terra...")
        sim.aplicar_falta_bifasica_com_terra(barra, resistencia)

        print("\n➡️ Aplicando faltas bifásicas sem terra...")
        sim.aplicar_falta_bifasica_sem_terra(barra, resistencia)

        print("\n➡️ Aplicando falta trifásica sem terra...")
        sim.aplicar_falta_trifasica_sem_terra(barra, resistencia)

        print("\n➡️ Aplicando falta trifásica COM terra...")
        sim.aplicar_falta_trifasica_com_terra(barra, resistencia)

        print("\n🎉 Finalizado com sucesso! (OPÇÃO 2)")
        return

    else:
        print("Opção inválida.")
        sys.exit()

if __name__ == "__main__":
    main()

