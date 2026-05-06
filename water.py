"""
Python model 'water.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="water level",
    units="Liters",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_water_level": 1},
    other_deps={
        "_integ_water_level": {
            "initial": {},
            "step": {"faucet_flow_rate": 1, "drain_rate": 1},
        }
    },
)
def water_level():
    return _integ_water_level()


_integ_water_level = Integ(
    lambda: faucet_flow_rate() - drain_rate(), lambda: 0, "_integ_water_level"
)


@component.add(
    name="faucet flow rate",
    units="Liters/Minute",
    comp_type="Constant",
    comp_subtype="Normal",
)
def faucet_flow_rate():
    return 0.1


@component.add(
    name="drain rate",
    units="Liters/Minute",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"drain_coefficient": 1, "water_level": 1},
)
def drain_rate():
    return drain_coefficient() * water_level()


@component.add(
    name="drain coefficient",
    units="1/Minute",
    comp_type="Constant",
    comp_subtype="Normal",
)
def drain_coefficient():
    return 0.5
