from SimulacaoDSS import SimulacaoDSS
import pandas as pd
import pathlib

def main():
    sim = SimulacaoDSS()
    arquivo_dss = "ieee37.dss"

    # sorteia linhas
    num_linhas = 5
    linhas_sorteadas = sim.sorteio_linhas_aleatorias(X=num_linhas)

    # antes das faltas
    sim.iniciar_arquivo_dss(arquivo_dss)
    sim.configurar_monitores_antes_falta(linhas_sorteadas)
    sim.simular_sem_falta()   # exporta para "Antes"

    # depois da falta
    sim.iniciar_arquivo_dss(arquivo_dss)
    sim.configurar_monitores_depois_falta(linhas_sorteadas)

    barra_falta = linhas_sorteadas[0][1]  # bus1 da primeira linha sorteada
    resistencia_falta = 5
    fases = None  # None = aplica todos os tipos

    sim.aplicar_faltas(barra_falta, resistencia_falta, fases=fases)

    print("\nSimulação finalizada e arquivos individuais gerados.")

    # unificar os csv
    sim.unificar_resultados(delete=True)

    print("\nUnificação concluída!")

    # ===== VERIFICAÇÃO DO PARQUET =====
    path = pathlib.Path("Antes/Monitors_ALL.parquet")

    if path.exists():
        df = pd.read_parquet(path)

        print("\n=== INFO DO PARQUET ===")
        print(df.info())

        print("\n=== PRIMEIRAS LINHAS ===")
        print(df.head())

        print("\n=== COLUNAS ===")
        print(df.columns.tolist())
    else:
        print("Arquivo Parquet não encontrado!")

if __name__ == "__main__":
    main()
