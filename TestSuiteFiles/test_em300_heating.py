import unittest
from unittest.mock import Mock

# Mock PLC class to simulate the TIA Portal environment
class MockPLC:
    def __init__(self):
        self.tags = {}

    def set_tag(self, tag_name, value):
        self.tags[tag_name] = value

    def get_tag(self, tag_name):
        return self.tags.get(tag_name, None)

# Global constants
PLC_INSTANCE_NAME = "AHU_Controller_Sim"

class TestHeatingModule(unittest.TestCase):
    def setUp(self):
        """Set up a new mock PLC for each test."""
        self.plc = MockPLC()
        # Set default values for the UDT and inputs
        self.plc.set_tag("FB300_EM_Heating.Enable", False)
        self.plc.set_tag("FB300_EM_Heating.Valve_Demand_In", 0.0)
        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Freeze_Stat_DI", False)
        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Valve_Cmd_AO", 0.0)
        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Valve_Fdbk_AI", 0.0)
        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Freeze_Alm", False)
        self.plc.set_tag("FB300_EM_Heating.UDT.Valve_Failure_Alm", False)

        # Mock the TON_TIME timer for the fault delay
        self.mock_timer = Mock()
        self.mock_timer.Q = False

    def run_heating_logic(self):
        """Simulates one scan of the FB300_EM_Heating logic."""
        enable = self.plc.get_tag("FB300_EM_Heating.Enable")
        demand = self.plc.get_tag("FB300_EM_Heating.Valve_Demand_In")
        freeze_stat = self.plc.get_tag("FB300_EM_Heating.UDT.HW_Freeze_Stat_DI")
        cmd = self.plc.get_tag("FB300_EM_Heating.UDT.HW_Valve_Cmd_AO")
        fdbk = self.plc.get_tag("FB300_EM_Heating.UDT.HW_Valve_Fdbk_AI")

        valve_cmd = 0.0
        freeze_alm = False
        valve_failure_alm = False

        if enable and not freeze_stat:
            valve_cmd = demand

            # Simulate the timer-based failure logic
            timer_in = abs(cmd - fdbk) > 5.0
            if timer_in and self.mock_timer.Q:
                valve_failure_alm = True

        if freeze_stat:
            freeze_alm = True
            valve_cmd = 0.0 # Safety override

        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Valve_Cmd_AO", valve_cmd)
        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Freeze_Alm", freeze_alm)
        self.plc.set_tag("FB300_EM_Heating.UDT.Valve_Failure_Alm", valve_failure_alm)

    def test_valve_passthrough(self):
        """TC1: Test that the valve command follows the demand input."""
        self.plc.set_tag("FB300_EM_Heating.Enable", True)
        self.plc.set_tag("FB300_EM_Heating.Valve_Demand_In", 50.0)
        self.run_heating_logic()
        self.assertEqual(self.plc.get_tag("FB300_EM_Heating.UDT.HW_Valve_Cmd_AO"), 50.0)

    def test_freeze_safety_trip(self):
        """TC2: Test that the freeze stat safety overrides the demand."""
        self.plc.set_tag("FB300_EM_Heating.Enable", True)
        self.plc.set_tag("FB300_EM_Heating.Valve_Demand_In", 80.0)
        self.run_heating_logic()
        self.assertEqual(self.plc.get_tag("FB300_EM_Heating.UDT.HW_Valve_Cmd_AO"), 80.0)

        # Simulate freeze fault
        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Freeze_Stat_DI", True)
        self.run_heating_logic()

        self.assertTrue(self.plc.get_tag("FB300_EM_Heating.UDT.HW_Freeze_Alm"))
        self.assertEqual(self.plc.get_tag("FB300_EM_Heating.UDT.HW_Valve_Cmd_AO"), 0.0)

    def test_valve_failure_alarm(self):
        """TC3: Test that the failure alarm triggers after a delay."""
        self.plc.set_tag("FB300_EM_Heating.Enable", True)
        self.plc.set_tag("FB300_EM_Heating.Valve_Demand_In", 50.0)
        self.run_heating_logic() # Run once to set the command

        self.plc.set_tag("FB300_EM_Heating.UDT.HW_Valve_Fdbk_AI", 10.0) # Mismatched feedback

        # 1. First scan, timer is running but not complete
        self.mock_timer.Q = False
        self.run_heating_logic()
        self.assertFalse(self.plc.get_tag("FB300_EM_Heating.UDT.Valve_Failure_Alm"))

        # 2. Second scan, timer has completed
        self.mock_timer.Q = True
        self.run_heating_logic()
        self.assertTrue(self.plc.get_tag("FB300_EM_Heating.UDT.Valve_Failure_Alm"))

if __name__ == '__main__':
    unittest.main()
