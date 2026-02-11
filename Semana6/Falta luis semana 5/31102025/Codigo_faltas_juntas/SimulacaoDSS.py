import os
import pathlib
import random
import re
import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools
import pyarrow

class SimulacaoDSS:
    def __init__(self):
        # caminhos fixos
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.xlsx_path = pathlib.Path(self.script_path, "lines_bus1.xlsx")

        # pastas de exportação
        self.export_dir = pathlib.Path(self.script_path, "Antes")
        self.export_dir.mkdir(parents=True, exist_ok=True)

        self.export_dir_fault = pathlib.Path(self.script_path, "Depois")
        self.export_dir_fault.mkdir(parents=True, exist_ok=True)

        # instancia DSS uma vez
        self.dss = py_dss_interface.DSS()
        dss_tools.update_dss(self.dss)

    # compila o arquivo dss
    def iniciar_arquivo_dss(self, arquivo_dss):
        dss_file = pathlib.Path(self.script_path, arquivo_dss)
        self.dss.text("clear")
        self.dss.text(f"compile [{dss_file}]")
        self.dss.text("set mode=snap")

    # monitors e meters antes da falta
    def configurar_monitores_antes_falta(self, linhas_selecionadas):
        for ln, _ in linhas_selecionadas:
            elem = f"Line.{ln}"
            self.dss.text(f"New Monitor.{ln}_power element={elem} terminal=1 mode=1 ppolar=no")
            self.dss.text(f"New Monitor.{ln}_voltage element={elem} terminal=1 mode=0")
            self.dss.text(f"New Monitor.{ln}_losses element={elem} terminal=1 mode=9")
            self.dss.text(f"New Monitor.{ln}_seqMag element={elem} terminal=1 mode=48")
            self.dss.text(f"New EnergyMeter.{ln}_meter element={elem} terminal=1")
            print(f"Monitors/Meter (Antes) criados para {elem}")

    # monitors e meters depois da falta
    def configurar_monitores_depois_falta(self, linhas_selecionadas):
        for ln, _ in linhas_selecionadas:
            elem = f"Line.{ln}"
            self.dss.text(f"New Monitor.{ln}_power_fault    element={elem} terminal=1 mode=1 ppolar=no")
            self.dss.text(f"New Monitor.{ln}_voltage_fault  element={elem} terminal=1 mode=0")
            self.dss.text(f"New Monitor.{ln}_losses_fault   element={elem} terminal=1 mode=9")
            self.dss.text(f"New Monitor.{ln}_seqMag_fault   element={elem} terminal=1 mode=48")
            self.dss.text(f"New EnergyMeter.{ln}_meter_fault element={elem} terminal=1")
            print(f"Monitors/Meter (Depois) criados para {elem}")

    # exporta a simulação sem falta para a pasta Antes
    def simular_sem_falta(self):
        self.dss.text("reset monitors")
        self.dss.text("reset meters")
        self.dss.text(f'set datapath="{self.export_dir}"')
        self.dss.text('set casename="ANTES"') # prefixo nos arquivos
        self.dss.text("set mode=snap")
        self.dss.text("solve")
        self.dss.text("sample")

        # comandos do run.py
        self.dss.text("export monitors all")
        self.dss.text("export meters /multiple")

        print(f"Arquivos de antes da falta exportados em: {self.export_dir}")

    # aplica todas as faltas
    def aplicar_faltas(self, barra_falta, resistencia_falta, fases=None):
        # garante que a barra é string ("701", "744", ...)
        barra_falta = str(barra_falta)

        # falta monofásica
        if fases is None or fases == 1:
            for n in range(1, 4):
                nome_falta = f"FT_1F_fase{n}"
                self.dss.text(f"New Fault.{nome_falta} bus1={barra_falta}.{n} phases=1 r={resistencia_falta}")
                print(f"Falta monofásica: {nome_falta} em {barra_falta}.{n}")
                self.resolver_falta(nome_falta)

        # falta bifásica com terra
        if fases is None or fases == 2:
            for n in range(1, 4):
                for m in range(n + 1, 4):
                    nome_falta = f"FT_2F_T_{n}{m}"
                    self.dss.text(
                        f"New Fault.{nome_falta} bus1={barra_falta}.{n}{m} phases=2 r={resistencia_falta}"
                    )
                    print(f"Falta bifásica + terra: {nome_falta} em {barra_falta}.{n}{m}")
                    self.resolver_falta(nome_falta)

        # falta bifásica sem terra
        if fases is None or fases == 2:
            for n in range(1, 4):
                for m in range(n + 1, 4):
                    nome_falta = f"FT_2F_{n}{m}"
                    self.dss.text(
                        f"New Fault.{nome_falta} bus1={barra_falta}.{n} bus2={barra_falta}.{m} phases=2 r={resistencia_falta}"
                    )
                    print(f"Falta bifásica sem terra: {nome_falta} entre {barra_falta}.{n} e {barra_falta}.{m}")
                    self.resolver_falta(nome_falta)

        # falta trifásica
        if fases is None or fases == 3:
            nome_falta_trifasica = "FT_3F_123"
            self.dss.text(
                f"New Fault.{nome_falta_trifasica} bus1={barra_falta}.1.2.3 phases=3 r={resistencia_falta}"
            )
            print(f"Falta trifásica: {nome_falta_trifasica} em {barra_falta}.1.2.3")
            self.resolver_falta(nome_falta_trifasica)

    # resolve um caso de falta e exporta para a pasta Depois
    def resolver_falta(self, nome_falta):
        self.dss.text("reset monitors")
        self.dss.text("reset meters")
        self.dss.text(f'set datapath="{self.export_dir_fault}"')
        # prefixo dos arquivos vai ser o nome da falta
        self.dss.text(f'set casename="{nome_falta}"')
        self.dss.text("set mode=snap")
        self.dss.text("solve")
        self.dss.text("sample")

        # aproveitado do run.py
        self.dss.text("export monitors all")
        self.dss.text("export meters /multiple")

        print(f"Resultado exportado para falta {nome_falta} em: {self.export_dir_fault}")

        # desabilita essa falta para não acumular com as próximas
        self.dss.text(f"edit fault.{nome_falta} enabled=no")

    # sorteio das linhas
    def sorteio_linhas_aleatorias(self, X=5):
        df = pd.read_excel(self.xlsx_path, dtype={"line": str, "bus1": str})
        df = df[["line", "bus1"]].dropna()
        line_bus1 = list(df.itertuples(index=False, name=None))
        X = min(X, len(line_bus1))
        selection = random.sample(line_bus1, k=X)
        sorted_lines = [ln for ln, _ in selection]
        print("Lines sorteadas:", sorted_lines)
        return selection  # (line, bus1)

    # une todos os csv de uma pasta em dois arquivos: um para monitors e um para meters
    def squash_folder(self, folder, out_mon, out_meter, delete=True):
        p = pathlib.Path(folder)
        csvs = list(p.glob("*.csv"))

        meters = [f for f in csvs if re.search(r"(meter|energymeter)", f.name, re.IGNORECASE)]
        monitors = [f for f in csvs if f not in meters]

        def merge_and_save(files, out_name):
            dfs = []
            for f in files:
                df = pd.read_csv(f, sep=None, engine="python")
                df["source_file"] = f.name
                dfs.append(df)

            if dfs:
                out_path = p / out_name
                pd.concat(dfs, ignore_index=True).to_parquet(
                    out_path, engine="pyarrow", index=False
                )
                if delete:
                    for f in files:
                        f.unlink()

        merge_and_save(monitors, out_mon)
        merge_and_save(meters, out_meter)

    def unificar_resultados(self, delete=True):
        self.squash_folder(
            self.export_dir,
            out_mon="Monitors_ALL.parquet",
            out_meter="EnergyMeters_ALL.parquet",
            delete=delete,
        )

        self.squash_folder(
            self.export_dir_fault,
            out_mon="Monitors_FAULT_ALL.parquet",
            out_meter="EnergyMeters_FAULT_ALL.parquet",
            delete=delete,
        )

        self.rotular_energymeters_antes()
        self.rotular_energymeters_depois()

    def rotular_energymeters_antes(self):
        path = self.export_dir / "EnergyMeters_ALL.parquet"
        if not path.exists():
            return

        df = pd.read_parquet(path)
        df["fault"] = "SEM_FALTA"
        df = df[["fault"] + [c for c in df.columns if c != "fault"]]
        df.to_parquet(path, engine="pyarrow", index=False)

    def rotular_energymeters_depois(self):
        path = self.export_dir_fault / "EnergyMeters_FAULT_ALL.parquet"
        if not path.exists():
            return

        df = pd.read_parquet(path)

        faults = [
            "FT_MONOFASICA_1", "FT_MONOFASICA_2", "FT_MONOFASICA_3",
            "FT_BIFASICA_T_12", "FT_BIFASICA_T_13", "FT_BIFASICA_T_23",
            "FT_TRIFASICA_123"
        ]

        def label_group(g):
            g = g.copy()
            g["fault"] = faults[:len(g)]
            return g

        df = df.groupby("source_file", group_keys=False).apply(label_group)
        df = df[["fault"] + [c for c in df.columns if c != "fault"]]
        df.to_parquet(path, engine="pyarrow", index=False)