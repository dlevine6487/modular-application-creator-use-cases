# Simple Procedural Test for EM400 Economizer Logic

# Mock PLC Class to simulate the TIA Portal environment
class MockPLC:
    def __init__(self):
        self.tags = {
            "AHU1_DMP_PosCmd": 0.0,
            "AHU1_DMP_PosFdbk": 0.0,
            "AHU1_RAT_Temp": 70.0,
            "AHU1_OAT_Temp": 50.0,
            "AHU1_DAT_Temp": 65.0,
            "SA_Temp_SP": 68.0,
            "Min_Fresh_Air_Pos": 20.0,
            "RA_RH": 50.0,
            "OA_RH": 80.0,
        }
        self.test_results = []

    def get_tag(self, tag_name):
        return self.tags.get(tag_name)

    def set_tag(self, tag_name, value):
        self.tags[tag_name] = value
        print(f"  PLC_WRITE: {tag_name} = {value:.2f}")

    def run_assertion(self, description, expected, actual, comparison="equal"):
        is_correct = False
        if comparison == "equal":
            is_correct = (expected == actual)
        elif comparison == "greater":
            is_correct = (actual > expected)

        if is_correct:
            result = "PASS"
        else:
            result = "FAIL"

        self.test_results.append(f"{result}: {description} | Expected: {expected}, Actual: {actual}")
        print(f"  {result}: {description}")


# The SCL logic we are testing, translated to Python
def economizer_logic(plc):
    oa_temp = plc.get_tag("AHU1_OAT_Temp")
    ra_temp = plc.get_tag("AHU1_RAT_Temp")
    sa_temp_sp = plc.get_tag("SA_Temp_SP")
    min_fresh_air = plc.get_tag("Min_Fresh_Air_Pos")

    # Simplified Enthalpy for testing
    oa_enthalpy = oa_temp + plc.get_tag("OA_RH")
    ra_enthalpy = ra_temp + plc.get_tag("RA_RH")

    print("  Running economizer logic...")
    if (oa_enthalpy < ra_enthalpy) and (oa_temp < sa_temp_sp) and (oa_temp > 35.0):
        print("  -> Condition: Economizer ACTIVE")
        error = plc.get_tag("AHU1_DAT_Temp") - sa_temp_sp
        new_pos = plc.get_tag("AHU1_DMP_PosCmd") + (error * 5.0)
        new_pos = max(min_fresh_air, min(100.0, new_pos))
        plc.set_tag("AHU1_DMP_PosCmd", new_pos)
    else:
        print("  -> Condition: Economizer INACTIVE")
        plc.set_tag("AHU1_DMP_PosCmd", min_fresh_air)


def run_tests():
    plc = MockPLC()
    print("\n" + "="*40)
    print("Executing Test Suite for EM400")
    print("="*40)

    # Test Case 1: Economizer mode should activate
    print("\n[ Test Case 1: Favorable economizer conditions ]")
    plc.set_tag("AHU1_OAT_Temp", 55.0)
    plc.set_tag("OA_RH", 40.0)
    plc.set_tag("AHU1_RAT_Temp", 72.0)
    plc.set_tag("RA_RH", 50.0)
    plc.set_tag("SA_Temp_SP", 68.0)
    plc.set_tag("AHU1_DAT_Temp", 69.0) # Slightly warm
    plc.set_tag("Min_Fresh_Air_Pos", 20.0)
    plc.set_tag("AHU1_DMP_PosCmd", 20.0)
    economizer_logic(plc)
    plc.run_assertion(
        "Damper should modulate open for free cooling",
        expected=20.0,
        actual=plc.get_tag("AHU1_DMP_PosCmd"),
        comparison="greater"
    )

    # Test Case 2: Economizer mode should not activate (too warm)
    print("\n[ Test Case 2: Outside air is too warm ]")
    plc.set_tag("AHU1_OAT_Temp", 75.0)
    plc.set_tag("SA_Temp_SP", 68.0)
    plc.set_tag("Min_Fresh_Air_Pos", 25.0)
    economizer_logic(plc)
    plc.run_assertion(
        "Damper should be at minimum position",
        expected=25.0,
        actual=plc.get_tag("AHU1_DMP_PosCmd"),
        comparison="equal"
    )

    # Test Case 3: Economizer mode should not activate (high enthalpy)
    print("\n[ Test Case 3: Outside air has high enthalpy ]")
    plc.set_tag("AHU1_OAT_Temp", 60.0)
    plc.set_tag("OA_RH", 95.0)
    plc.set_tag("AHU1_RAT_Temp", 72.0)
    plc.set_tag("RA_RH", 40.0)
    plc.set_tag("Min_Fresh_Air_Pos", 20.0)
    economizer_logic(plc)
    plc.run_assertion(
        "Damper should be at minimum position",
        expected=20.0,
        actual=plc.get_tag("AHU1_DMP_PosCmd"),
        comparison="equal"
    )

    print("\n" + "="*40)
    print("Test Summary:")
    for result in plc.test_results:
        print(f" - {result}")
    print("="*40)

# Execute the test runner function
run_tests()
