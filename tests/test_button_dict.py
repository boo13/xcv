import pytest
from xcv.controller_button_press import press_button


def test_press_button_input_incorrect():
    # GIVEN: An incorrect value
    # WHEN: entered into button_press
    # THEN: do not create a new key for it in button_dict
    bad_values = ["j", 1, 0.25, " a", "+", "", " ", "rr", "exit"]
    for val in bad_values:
        bd = press_button(val)
        assert val not in bd


def test_press_button_input_lowercase():
    # GIVEN: A correct value, which happens to be lowercase
    # WHEN: entered into button_press
    # THEN: change the correct value in button_dict
    ok_values = ["a", "b", "x", "y", "rb", "lb", "rpb", "lpb"]
    not_so_ok_values = ["st", "se", "xb"]
    expected_vals = ["A", "B", "X", "Y", "RB", "LB", "RPB", "LPB", "START", "SELECT", "XBOX"]
    
    for val in ok_values:
        bd = press_button(val)
        with pytest.raises(KeyError):
            x = bd[val.lower()]
        assert bd[val.upper()]

def test_press_button_input_multiple_values():
    # press_button("b", "Y", "X", "Start", "select", "xb")
    assert True

def test_press_button_input_list():
    # press_button(["b", "Y", "X", "Start", "select", "xb"])
    assert True

def test_press_button_input_keyword_args():
    press_button(A=123, j=12, b=1, x=0)
    assert True
