import os
import pathlib
import py_dss_interface

from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("ieee37.dss")

dss = py_dss_interface.DSS()

dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")

dss.text("New EnergyMeter.Met_Ini    element=Line.L35 terminal=1")
dss.text("New Monitor.Mon_Ini        element=Line.L35 terminal=1 mode=1")

dss.text("New EnergyMeter.Met_Ramal  element=Line.L9  terminal=1")
dss.text("New Monitor.Mon_Ramal      element=Line.L9  terminal=1 mode=1")

dss.text("reset meters")
dss.text("reset monitors")

dss.text("solve")

dss.text("sample")
dss.text("save monitors")

meters_csv   = dss.text("export meters")
mon_ini_csv  = dss.text("export monitor Mon_Ini")
mon_ram_csv  = dss.text("export monitor Mon_Ramal")

print("here")