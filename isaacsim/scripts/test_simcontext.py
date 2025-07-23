from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": True})  # set to False if you want GUI

from omni.isaac.core import SimulationContext
print("SUCCESS: omni.isaac.core imported!")

simulation_app.close()
