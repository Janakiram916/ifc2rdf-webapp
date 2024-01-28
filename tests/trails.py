import ifcopenshell
from icecream import ic

ifc_model = ifcopenshell.open("resources/TUD_NÜR_EI_Building.ifc")
ic(ifc_model.get_types())