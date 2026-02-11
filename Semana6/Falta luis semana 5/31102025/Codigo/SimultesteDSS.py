
import os
import random
import pandas as pd
from pathlib import Path
import py_dss_interface
from py_dss_toolkit import dss_tools


class SimulacaoDSS:
    def __init__(self, dss_name="ieee37.dss", xlsx_name="lines_bus1.xlsx"):
        self.script_path = Path(os.path.dirname(os.path.abspath(__file__)))

        self.dss_name = dss_name
        self.xlsx_path = self.script_path / xlsx_name

        self.export_dir = self.script_path / "Antes"
        self.export_dir.mkdir(exist_ok=True)

        self.export_dir_fault = self.script_path / "Depois"
        self.export_dir_fault.mkdir(exist_ok=True)

        self.dss = py_dss_interface.DSS()
        dss_tools.update_dss(self.dss)

    # -------------------------------------------------------
    def iniciar_arquivo_dss(self):
        dss_file = self.script_path / self.dss_name
        print(f"Compilando DSS: {dss_file}")

        if not dss_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {dss_file}")

        self.dss.text(f"compile [{dss_file}]")
        self.dss.text("set mode=snap")

    # -------------------------------------------------------
    def resolver_falta(self):
        self.dss.text("Reset Monitors")
        self.dss.text("CalcV")
        self.dss.text("Set mode=snap")
        self.dss.text("Solve")
        self.dss.text("Sample")

    # -------------------------------------------------------
    def organizar_arquivos(self, nome_falta, monitor_name):
        nome_csv = f"Mon_Falta_{nome_falta}"
        self.dss.text(f"Set casename={nome_csv}")
        self.dss.text(f"Export Monitor {monitor_name}")

        csv_path = self.script_path / f"{nome_csv}.CSV"

        if csv_path.exists():
            print(f"✅ Arquivo criado: {csv_path}")
        else:
            print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

    # -------------------------------------------------------
    # MONITORES ANTES DA FALTA
    # -------------------------------------------------------
    def configurar_monitores_antes_falta(self, linhas):
       for ln, _ in selection:
           elem = f"Line.{ln}" # monta o nome completo do elemento line
           self.dss.text(f"New Monitor.{ln}_power    element={elem} terminal=1 mode=1 ppolar=no") # monitor de potência (P/Q)
           self.dss.text(f"New Monitor.{ln}_voltage  element={elem} terminal=1 mode=0") # monitor de tensão
           self.dss.text(f"New Monitor.{ln}_losses   element={elem} terminal=1 mode=9") # monitor de perdas
           self.dss.text(f"New Monitor.{ln}_seqMag   element={elem} terminal=1 mode=48") # monitor de magnitudes de sequência
           self.dss.text(f"New EnergyMeter.{ln}_meter element={elem} terminal=1") # medidor de energia
           print(f"Monitors/Meter criados para {elem}")
    # -------------------------------------------------------
    def exportar_antes(self): 
        self.dss.text("reset monitors") 
        self.dss.text("reset meters") 
        self.dss.text(f'set datapath="{self.export_dir}"') 
        self.dss.text("solve") self.dss.text("sample") 
        self.dss.text("export monitors all") 
        self.dss.text("export meters /multiple")

    # -------------------------------------------------------
    # MONITORES DEPOIS DA FALTA
    # -------------------------------------------------------
    def configurar_monitores_depois_falta(self, linhas):
       # Depois da falha
for ln, b1 in selection: # percorre cada par (line, bus1) sorteado
    dss.text(f"New fault.{ln}_fault bus1={b1}.1 phases=1 r=5") # cria falta monofásica no nó 1 do bus1
    print(f"Fault em {b1}.1 (line {ln})")

for ln, _ in selection:
    dss.text(f"New Monitor.{ln}_power_fault    element={elem} terminal=1 mode=1 ppolar=no") # monitor de potência (P/Q)
    dss.text(f"New Monitor.{ln}_voltage_fault  element={elem} terminal=1 mode=0") # monitor de tensão
    dss.text(f"New Monitor.{ln}_losses_fault   element={elem} terminal=1 mode=9") # monitor de perdas
    dss.text(f"New Monitor.{ln}_seqMag_fault   element={elem} terminal=1 mode=48") # monitor de magnitudes de sequência
    dss.text(f"New EnergyMeter.{ln}_meter_fault element={elem} terminal=1") # medidor de energia
    print(f"Monitors/Meter criados para {elem}")

    # -------------------------------------------------------
    def exportar_depois(self): 
      self.dss.text("reset monitors") 
      self.dss.text("reset meters") 
      self.dss.text(f'set datapath="{self.export_dir_fault}"') 
      self.dss.text("solve") self.dss.text("sample") 
      self.dss.text("export monitors all") 
      self.dss.text("export meters /multiple"))

    # -------------------------------------------------------
    # FALTAS
    # -------------------------------------------------------

    def aplicar_falta_monofasica(self, barra, resistencia):
        for n in range(1, 4):
            nome_falta = f"FT_1F_{n}"
            monitor_name = f"Mon_{nome_falta}"

            print(f"\n➡️ Executando falta monofásica na fase {n}...")

            self.dss.text(f"New Fault.{nome_falta} bus1={barra}.{n} phases=1 r={resistencia}")
            self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

            self.resolver_falta()
            self.organizar_arquivos(nome_falta, monitor_name)

            self.dss.text(f"Edit Fault.{nome_falta} enabled=no")

    # -------------------------------------------------------
    def aplicar_falta_bifasica_com_terra(self, barra, resistencia):
        for n in range(1, 4):
            for m in range(n + 1, 4):

                nome_falta = f"FT_2F_T_{n}{m}"
                monitor_name = f"Mon_{nome_falta}"

                print(f"\n➡️ Executando falta bifásica COM terra entre fases {n}-{m}...")

                self.dss.text(f"New Fault.{nome_falta} bus1={barra}.{n}{m} phases=2 r={resistencia}")
                self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

                self.resolver_falta()
                self.organizar_arquivos(nome_falta, monitor_name)

                self.dss.text(f"Edit Fault.{nome_falta} enabled=no")

    # -------------------------------------------------------
    def aplicar_falta_bifasica_sem_terra(self, barra, resistencia):
        for n in range(1, 4):
            for m in range(n + 1, 4):

                nome_falta = f"FT_2F_{n}{m}"
                monitor_name = f"Mon_{nome_falta}"

                print(f"\n➡️ Executando falta bifásica SEM terra entre fases {n}-{m}...")

                self.dss.text(f"New Fault.{nome_falta} bus1={barra}.{n} bus2={barra}.{m} phases=2 r={resistencia}")
                self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

                self.resolver_falta()
                self.organizar_arquivos(nome_falta, monitor_name)

                self.dss.text(f"Edit Fault.{nome_falta} enabled=no")

    # -------------------------------------------------------
    def aplicar_falta_trifasica_sem_terra(self, barra, resistencia):

        nome_falta = "FT_3F_ST"
        monitor_name = f"Mon_{nome_falta}"

        print("\n➡️ Executando falta trifásica SEM terra...")

        self.dss.text(
            f"New Fault.{nome_falta} bus1={barra}.1 bus2={barra}.2 bus3={barra}.3 phases=3 r={resistencia}"
        )
        self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

        self.resolver_falta()
        self.organizar_arquivos(nome_falta, monitor_name)

        self.dss.text(f"Edit Fault.{nome_falta} enabled=no")

    # -------------------------------------------------------
    def aplicar_falta_trifasica_com_terra(self, barra, resistencia):

        nome_falta = "FT_3F_T"
        monitor_name = f"Mon_{nome_falta}"

        print("\n➡️ Executando falta trifásica COM terra...")

        self.dss.text(f"New Fault.{nome_falta} bus1={barra}.1.2.3 phases=3 r={resistencia}")
        self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

        self.resolver_falta()
        self.organizar_arquivos(nome_falta, monitor_name)

        self.dss.text(f"Edit Fault.{nome_falta} enabled=no")

    # -------------------------------------------------------
    def sorteio_linhas_aleatorias(self, X=5):
        if not self.xlsx_path.exists():
            raise FileNotFoundError(f"Excel não encontrado: {self.xlsx_path}")

        df = pd.read_excel(self.xlsx_path, dtype={"line": str, "bus1": str})
        df = df[["line", "bus1"]].dropna()

        return random.sample(list(df.itertuples(index=False, name=None)), k=min(X, len(df)))


# ======================================================================
# Função FORA da classe (igual à que você enviou)
# ======================================================================

def squash_folder(folder, out_mon="Monitors_ALL.csv", out_meter="EnergyMeters_ALL.csv", delete=True):
    p = Path(folder)

    if not p.exists():
        print(f"[squash_folder] Pasta não existe: {p}")
        return

    csvs = [f for f in p.glob("*.csv") if f.name not in (out_mon, out_meter)]

    meters = [f for f in csvs if "meter" in f.name.lower()]
    monitors = [f for f in csvs if f not in meters]

    if monitors:
        df_mon = pd.concat([pd.read_csv(f).assign(source=f.name) for f in monitors], ignore_index=True)
        df_mon.to_csv(p / out_mon, index=False)
        if delete:
            for f in monitors:
                f.unlink()

    if meters:
        df_met = pd.concat([pd.read_csv(f).assign(source=f.name) for f in meters], ignore_index=True)
        df_met.to_csv(p / out_meter, index=False)
        if delete:
            for f in meters:
                f.unlink()

# ======================================================================
#main da simulacao
#arquivo main da simulacao
import os
import pathlib
import random
import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools

from SimulacaoDSS import SimulacaoDSS, squash_folder


def main():
    sim = SimulacaoDSS(dss_name="ieee37.dss", xlsx_name="lines_bus1.xlsx")

    sim.iniciar_arquivo_dss()

    linhas = sim.sorteio_linhas_aleatorias(5)

    # ANTES DA FALTA
    sim.configurar_monitores_antes_falta(linhas)
    sim.exportar_antes()

    # DEPOIS DA FALTA
    sim.configurar_monitores_depois_falta(linhas)

    for ln, barra in linhas:
        sim.aplicar_falta_monofasica(barra, resistencia=0.001)
        sim.aplicar_falta_bifasica_com_terra(barra, resistencia=0.001)
        sim.aplicar_falta_bifasica_sem_terra(barra, resistencia=0.001)
        sim.aplicar_falta_trifasica_sem_terra(barra, resistencia=0.001)
        sim.aplicar_falta_trifasica_com_terra(barra, resistencia=0.001)

    sim.exportar_depois()

    squash_folder(sim.export_dir)
    squash_folder(sim.export_dir_fault)

    print("Simulação finalizada com sucesso!")


if __name__ == "__main__":
    main()


