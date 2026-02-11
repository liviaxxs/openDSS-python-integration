 
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

        self.linhas_sorteadas = []   # lista de (line, bus1)

    # -------------------------------------------------------
    def iniciar_arquivo_dss(self):
        dss_file = self.script_path / self.dss_name
        print(f"Compilando DSS: {dss_file}")

        if not dss_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {dss_file}")

        self.dss.text(f"compile [{dss_file}]")
        self.dss.text("set mode=snap")

    # -------------------------------------------------------
    def sortear_linhas(self, quantidade=5):
        df = pd.read_excel(self.xlsx_path, dtype={"line": str, "bus1": str})
        df = df[["line", "bus1"]].dropna()

        pares = list(df.itertuples(index=False, name=None))

        quantidade = min(quantidade, len(pares))
        self.linhas_sorteadas = random.sample(pares, quantidade)

        print("\n📌 Linhas sorteadas:", [ln for ln, _ in self.linhas_sorteadas])

    # -------------------------------------------------------
    # MONITORES ANTES DA FALTA
    # -------------------------------------------------------
    def configurar_monitores_antes_falta(self):
        for ln, _ in self.linhas_sorteadas:
            elem = f"Line.{ln}"

            self.dss.text(f"New Monitor.{ln}_power    element={elem} terminal=1 mode=1 ppolar=no")
            self.dss.text(f"New Monitor.{ln}_voltage  element={elem} terminal=1 mode=0")
            self.dss.text(f"New Monitor.{ln}_losses   element={elem} terminal=1 mode=9")
            self.dss.text(f"New Monitor.{ln}_seqMag   element={elem} terminal=1 mode=48")
            self.dss.text(f"New EnergyMeter.{ln}_meter element={elem} terminal=1")
            print(f"Monitores criados para {ln}")

    def exportar_antes(self):
        self.dss.text("reset monitors")
        self.dss.text("reset meters")
        self.dss.text(f'set datapath="{self.export_dir}"')

        self.dss.text("solve")
        self.dss.text("sample")

        self.dss.text("export monitors all")
        self.dss.text("export meters /multiple")

    # -------------------------------------------------------
    # MONITORES DEPOIS DA FALTA
    # -------------------------------------------------------
    def configurar_monitores_depois_falta(self):
        for ln, _ in self.linhas_sorteadas:
            elem = f"Line.{ln}"

            self.dss.text(f"New Monitor.{ln}_power_fault    element={elem} terminal=1 mode=1 ppolar=no")
            self.dss.text(f"New Monitor.{ln}_voltage_fault  element={elem} terminal=1 mode=0")
            self.dss.text(f"New Monitor.{ln}_losses_fault   element={elem} terminal=1 mode=9")
            self.dss.text(f"New Monitor.{ln}_seqMag_fault   element={elem} terminal=1 mode=48")
            self.dss.text(f"New EnergyMeter.{ln}_meter_fault element={elem} terminal=1")

            print(f"Monitores DEPOIS criados para {ln}")

    def exportar_depois(self):
        self.dss.text("reset monitors")
        self.dss.text("reset meters")
        self.dss.text(f'set datapath=\"{self.export_dir_fault}\"')

        self.dss.text("solve")
        self.dss.text("sample")

        self.dss.text("export monitors all")
        self.dss.text("export meters /multiple")

    # -------------------------------------------------------
    # FALTAS (seguindo o padrão que você enviou)
    # -------------------------------------------------------

    def _exportar_monitor_e_verificar(self, nome_falta, monitor_name):
        """
        Helper interno: seta datapath para pasta 'Depois', seta casename
        e exporta o monitor; verifica se o CSV foi criado.
        """
        # garante que o datapath está na pasta de exports pós-falta
        self.dss.text(f'set datapath="{self.export_dir_fault}"')

        nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
        self.dss.text(f"Set casename={nome_arquivo_csv}")
        self.dss.text(f"Export Monitor {monitor_name}")

        # caminho esperado do CSV
        csv_path = os.path.join(self.script_path, f"{nome_arquivo_csv}.CSV")
        if os.path.exists(csv_path):
            print(f"✅ Arquivo criado: {csv_path}")
        else:
            print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

    def resolver_falta(self):
        self.dss.text("reset monitors")
        self.dss.text("calcv")
        self.dss.text("set mode=snap")
        self.dss.text("solve")
        print("Solução para a falta executada com sucesso.")
        self.dss.text("sample")

    # -------------------------------------------------------
    # ===================== FALTAS =====================

def aplicar_falta_monofasica(self, barra, resistencia):
    """Aplica as 3 faltas monofásicas (fase 1,2,3)."""
    for n in range(1, 4):
        nome_falta = f"FT_phase_{n}"
        monitor_name = f"Mon_{nome_falta}"

        print(f"\n➡️ Executando {nome_falta}...")

        # cria falta + monitor
        self.dss.text(f"New Fault.{nome_falta} bus1={barra}.{n} phases=1 r={resistencia}")
        self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

        # resolve/aplica a falta
        self.resolver_falta()

        # exporta monitor
        nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
        self.dss.text(f"Set casename={nome_arquivo_csv}")
        self.dss.text(f"Export Monitor {monitor_name}")

        csv_path = os.path.join(self.script_path, f"{nome_arquivo_csv}.CSV")
        if os.path.exists(csv_path):
            print(f"✅ Arquivo criado: {csv_path}")
        else:
            print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

        # desabilita falta
        self.dss.text(f"Edit Fault.{nome_falta} enabled=no")


def aplicar_falta_bifasica_com_terra(self, barra, resistencia):
    """Aplica faltas bifásicas + terra."""
    for n in range(1, 4):
        for m in range(n + 1, 4):
            nome_falta = f"FT_phase_{n}{m}_T"
            monitor_name = f"Mon_{nome_falta}"

            print(f"\n➡️ Executando {nome_falta} (bifásica + terra)...")

            self.dss.text(f"New Fault.{nome_falta} bus1={barra}.{n}{m} phases=2 r={resistencia}")
            self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

            self.resolver_falta()

            nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
            self.dss.text(f"Set casename={nome_arquivo_csv}")
            self.dss.text(f"Export Monitor {monitor_name}")

            csv_path = os.path.join(self.script_path, f"{nome_arquivo_csv}.CSV")
            if os.path.exists(csv_path):
                print(f"✅ Arquivo criado: {csv_path}")
            else:
                print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

            self.dss.text(f"Edit Fault.{nome_falta} enabled=no")


def aplicar_falta_bifasica_sem_terra(self, barra, resistencia):
    """Aplica faltas bifásicas sem terra (pares de fases)."""
    for n in range(1, 4):
        for m in range(n + 1, 4):
            nome_falta = f"FT_phase_{n}{m}"
            monitor_name = f"Mon_{nome_falta}"

            print(f"\n➡️ Executando {nome_falta} (bifásica sem terra)...")

            self.dss.text(
                f"New Fault.{nome_falta} bus1={barra}.{n} bus2={barra}.{m} phases=2 r={resistencia}"
            )
            self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

            self.resolver_falta()

            nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
            self.dss.text(f"Set casename={nome_arquivo_csv}")
            self.dss.text(f"Export Monitor {monitor_name}")

            csv_path = os.path.join(self.script_path, f"{nome_arquivo_csv}.CSV")
            if os.path.exists(csv_path):
                print(f"✅ Arquivo criado: {csv_path}")
            else:
                print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

            self.dss.text(f"Edit Fault.{nome_falta} enabled=no")


def aplicar_falta_trifasica_sem_terra(self, barra, resistencia):
    """Aplica falta trifásica sem terra (três fases)."""
    nome_falta = "FT_trifasica_sem_terra"
    monitor_name = f"Mon_{nome_falta}"

    print("\n➡️ Executando falta trifásica SEM terra...")

    self.dss.text(
        f"New Fault.{nome_falta} bus1={barra}.1 bus2={barra}.2 bus3={barra}.3 phases=3 r={resistencia}"
    )
    self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

    self.resolver_falta()

    nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
    self.dss.text(f"Set casename={nome_arquivo_csv}")
    self.dss.text(f"Export Monitor {monitor_name}")

    csv_path = os.path.join(self.script_path, f"{nome_arquivo_csv}.CSV")
    if os.path.exists(csv_path):
        print(f"✅ Arquivo criado: {csv_path}")
    else:
        print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

    self.dss.text(f"Edit Fault.{nome_falta} enabled=no")


def aplicar_falta_trifasica_com_terra(self, barra, resistencia):
    """Aplica falta trifásica com terra (todas as fases no mesmo bus)."""
    nome_falta = "FT_trifasica_com_terra"
    monitor_name = f"Mon_{nome_falta}"

    print("\n➡️ Executando falta trifásica COM terra...")

    self.dss.text(f"New Fault.{nome_falta} bus1={barra}.1.2.3 phases=3 r={resistencia}")
    self.dss.text(f"New Monitor.{monitor_name} element=Line.L2 terminal=1 mode=0")

    self.resolver_falta()

    nome_arquivo_csv = f"Mon_Falta_{nome_falta}"
    self.dss.text(f"Set casename={nome_arquivo_csv}")
    self.dss.text(f"Export Monitor {monitor_name}")

    csv_path = os.path.join(self.script_path, f"{nome_arquivo_csv}.CSV")
    if os.path.exists(csv_path):
        print(f"✅ Arquivo criado: {csv_path}")
    else:
        print(f"⚠️ Nenhum CSV encontrado para {monitor_name}")

    self.dss.text(f"Edit Fault.{nome_falta} enabled=no")


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