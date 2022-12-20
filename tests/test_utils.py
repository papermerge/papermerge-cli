from papermerge_cli.utils import sanitize_host


def test_sanitize_host_1():
    actual_output = sanitize_host("http://localhost:8000/")
    expected_output = "http://localhost:8000"

    assert actual_output == expected_output


def test_sanitize_host_2():
    actual_output = sanitize_host("http://localhost:8000")
    # exactly same as input
    expected_output = "http://localhost:8000"

    assert actual_output == expected_output


def test_sanitize_host_3():
    actual_output = sanitize_host("http://localhost:8000/  ")
    expected_output = "http://localhost:8000"

    assert actual_output == expected_output


def test_sanitize_host_4():
    actual_output = sanitize_host("http://localhost:8000//////  ")
    expected_output = "http://localhost:8000"

    assert actual_output == expected_output
