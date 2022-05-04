from aggregater.main import output_results, single_test_metadata, get_file_name


def test_output():
    assert output_results('test_file', 0.2, ['\u2705 GetTransaction PASS 0.2'], 1, 0, 0) == \
        "On Test File: test_file => 1 test(s) run in 2000ms; 1 passed; 0 failed; 0 skipped\n" \
        "\t\u2705 GetTransaction PASS 0.2"


def test_pass_metadata():
    assert single_test_metadata('--- PASS: TestReadLastOperation (0.35s)')[
        0] == '\u2705 TestReadLastOperation PASS 0.35s'


def test_fail_metadata():
    assert single_test_metadata('--- FAIL: TestReadLastOperation (0.10s)')[
        0] == '\u274C TestReadLastOperation FAIL 0.10s'


def test_skipped_metadata():
    assert single_test_metadata(
        '--- SKIP: TestAllDepsBuilt (0.20s)')[0] == '\u2757 TestAllDepsBuilt SKIP 0.20s'
    assert single_test_metadata(
        '--- SKIP: TestAllDepsBuilt (0.20s)')[0] != '\u2757 TestAllDepsBuilt PASS 0.20s'


def test_get_filename():
    assert get_file_name(
        '--> START //src/core:graph_test') == '//src/core:graph_test'
    assert get_file_name(
        '--> OHH //src/core:graph_test') == 'Test file does not adhere to the format'
