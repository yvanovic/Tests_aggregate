"""" A python script to combine file tests results in two one single output """
import glob
import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(filename='./log_folder/test_results.log', filemode='w', level=logging.INFO,
                    format='%(message)s')


def get_file_name(test_str):
    """ retrieve file test name """
    try:
        name = re.search(r'(--> START)\s(.*)', test_str)
        return name.group(2)
    except AttributeError:
        return 'Test file does not adhere to the format'


def single_test_metadata(test_str):
    """ aggregate each test metadata """
    test_data = re.search(
        r'(---)\s(PASS|FAIL|SKIP)(:)\s(.*)\s\((.*)s\)', test_str)
    if 'PASS' in test_data.group(2):
        single_test_result = ['\u2705 ' + test_data.group(4) + ' ' + test_data.group(2) + ' '
                              + test_data.group(5) + 's', float(test_data.group(5))]
    elif 'FAIL' in test_data.group(2):
        single_test_result = ['\u274C ' + test_data.group(4) + ' ' + test_data.group(2) + ' '
                              + test_data.group(5) + 's', float(test_data.group(5))]
    elif 'SKIP' in test_data.group(2):
        single_test_result = ['\u2757 ' + test_data.group(4) + ' ' + test_data.group(2) + ' '
                              + test_data.group(5) + 's', float(test_data.group(5))]
    else:
        single_test_result = 'No test found in the file'
    return single_test_result


def output_results(title, to_time, my_lst, passed, failed, skipped):
    """ output formatted test results for each file"""
    num_test = passed + failed + skipped
    output = f'On Test File: {title} => {num_test} test(s) run in {to_time * 10e3:.0f}ms;' \
             f' {passed} passed; {failed} failed; {skipped} skipped'
    for _, item in enumerate(my_lst, 1):
        output += '\n\t' + ''.join(item)
    return output


def test_aggregator(filename):
    """ output test results for each file """
    time.sleep(1)
    with open(filename, 'r') as file:
        # initialise a list that will contains the metadata for each single test
        lst = []
        # initialise the total number of test by status
        total_tests_runtime = 0.0
        # initialise the total number of test by status
        pass_tests, fail_tests, skip_tests = 0, 0, 0

        # get all the line in the file
        tests_metadata = file.readlines()
        if tests_metadata:
            # when test file is not empty
            # retrieve test status, test name and time it runs
            test_name = get_file_name(tests_metadata[0])
            for line in tests_metadata:
                if "PASS:" in line:
                    # aggregate metadata for passed tests
                    pass_tests += 1
                    test_output = single_test_metadata(line)
                    lst.append(test_output[0])
                    total_tests_runtime += test_output[1]
                if "FAIL:" in line:
                    # aggregate metadata for failed tests
                    fail_tests += 1
                    test_output = single_test_metadata(line)
                    lst.append(test_output[0] +
                               ' => Check source file for failure')
                    total_tests_runtime += test_output[1]
                if "SKIP:" in line:
                    # aggregate metadata for skipped tests
                    skip_tests += 1
                    test_output = single_test_metadata(line)
                    lst.append(test_output[0])
                    total_tests_runtime += test_output[1]
                else:
                    try:
                        b = re.search(r'T\d{-5}', line)
                        lst[-1] += f' => Link Defect number is {b.group()}'
                    except AttributeError as e:
                        pass
                    except IndexError as e:
                        pass

            # output to the terminal
            all_test_results = output_results(test_name, total_tests_runtime, lst, pass_tests,
                                              fail_tests, skip_tests)

            # output to the terminal
            print(all_test_results)

            # output to a log file that can be used
            logging.info(all_test_results)


def main():
    start_time = time.perf_counter()
    with ThreadPoolExecutor() as executor:
        test_files = glob.glob('test_results_folder/*.txt')
        executor.map(test_aggregator, test_files)
    end_time = time.perf_counter()
    print(f'time took to process is {end_time - start_time:.4f} secs \n')


if __name__ == '__main__':
    main()
