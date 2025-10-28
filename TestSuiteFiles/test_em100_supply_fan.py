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

class TestSupplyFan(unittest.TestCase):
    def setUp(self):
        """Set up a new mock PLC for each test."""
        self.plc = MockPLC()
        # Set default values for the UDT
        self.plc.set_tag("FB100_EM_SupplyFan.Enable", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Run_Fdbk_DI", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Airflow_Status_DI", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.VFD_Fault_DI", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Start_Cmd_DO", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Fan_Failure_Alm", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.VFD_Fault_Alm", False)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Is_Running", False)

        # Mock the TON_TIME timer for the fault delay
        self.mock_timer = Mock()
        self.mock_timer.Q = False

    def run_fan_logic(self):
        """Simulates one scan of the FB100_EM_SupplyFan logic."""
        enable = self.plc.get_tag("FB100_EM_SupplyFan.Enable")
        run_feedback = self.plc.get_tag("FB100_EM_SupplyFan.UDT.Run_Fdbk_DI")
        vfd_fault_di = self.plc.get_tag("FB100_EM_SupplyFan.UDT.VFD_Fault_DI")

        # By default, alarms are not latched in this simulation
        fan_failure_alm = False
        vfd_fault_alm = False
        start_cmd = False
        is_running = False

        if enable:
            # VFD Fault is a hardwired safety, it has the highest priority
            if vfd_fault_di:
                vfd_fault_alm = True
                start_cmd = False
            else:
                # If no VFD fault, try to start the fan
                start_cmd = True

                # Check for fan failure (feedback doesn't match command after delay)
                timer_in = start_cmd and not run_feedback
                if timer_in and self.mock_timer.Q:
                    fan_failure_alm = True
                    start_cmd = False # Latch off on failure

            is_running = start_cmd and run_feedback

        # Update all outputs
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Start_Cmd_DO", start_cmd)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Is_Running", is_running)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Fan_Failure_Alm", fan_failure_alm)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.VFD_Fault_Alm", vfd_fault_alm)

    def test_normal_start_sequence(self):
        """TC1: Test normal fan start and run sequence."""
        self.plc.set_tag("FB100_EM_SupplyFan.Enable", True)
        self.run_fan_logic()
        self.assertTrue(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Start_Cmd_DO"))

        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Run_Fdbk_DI", True)
        self.run_fan_logic()
        self.assertTrue(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Is_Running"))
        self.assertFalse(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Fan_Failure_Alm"))

    def test_fan_failure_with_delay(self):
        """TC2: Test fan failure alarm after a delay if feedback is missing."""
        self.plc.set_tag("FB100_EM_SupplyFan.Enable", True)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Run_Fdbk_DI", False)

        # 1. First scan, timer is running but not complete
        self.mock_timer.Q = False
        self.run_fan_logic()
        self.assertTrue(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Start_Cmd_DO"))
        self.assertFalse(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Fan_Failure_Alm"))

        # 2. Second scan, timer has completed
        self.mock_timer.Q = True
        self.run_fan_logic()
        self.assertTrue(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Fan_Failure_Alm"))
        self.assertFalse(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Start_Cmd_DO"))

    def test_vfd_fault_trip(self):
        """TC3: Test that a VFD fault immediately stops the fan."""
        self.plc.set_tag("FB100_EM_SupplyFan.Enable", True)
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.Run_Fdbk_DI", True)
        self.run_fan_logic()
        self.assertTrue(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Is_Running"))

        # Simulate VFD Fault
        self.plc.set_tag("FB100_EM_SupplyFan.UDT.VFD_Fault_DI", True)
        self.run_fan_logic()

        self.assertFalse(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Start_Cmd_DO"))
        self.assertFalse(self.plc.get_tag("FB100_EM_SupplyFan.UDT.Is_Running"))
        self.assertTrue(self.plc.get_tag("FB100_EM_SupplyFan.UDT.VFD_Fault_Alm"))

if __name__ == '__main__':
    unittest.main()
