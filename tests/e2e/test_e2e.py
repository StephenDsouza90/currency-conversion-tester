from main import main


def test_main_workflow_true():
    """
    Test the main workflow for a successful currency conversion.
    This test checks if the currency rate is above the threshold.
    """

    result = main("GB", threshold=1)
    assert result is True


def test_main_workflow_false():
    """
    Test the main workflow for a failed currency conversion.
    This test checks if the currency rate is below the threshold.
    """
    result = main("TR", threshold=1)
    assert result is False
