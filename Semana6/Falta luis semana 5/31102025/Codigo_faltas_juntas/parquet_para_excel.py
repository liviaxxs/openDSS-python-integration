import pandas as pd
import pathlib

base = pathlib.Path(".")

arquivos = [
    base / "Antes" / "Monitors_ALL.parquet",
    base / "Antes" / "EnergyMeters_ALL.parquet",
    base / "Depois" / "Monitors_FAULT_ALL.parquet",
    base / "Depois" / "EnergyMeters_FAULT_ALL.parquet",
]

for p in arquivos:
    if p.exists():
        df = pd.read_parquet(p)
        out = p.with_suffix(".xlsx")
        df.to_excel(out, index=False)
        print(f"Excel gerado: {out}")
    else:
        print(f"Arquivo não encontrado: {p}")
