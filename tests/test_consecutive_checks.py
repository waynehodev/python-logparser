from log_analyzer import consecutive_error_check
from datetime import datetime

def test_many_errors_in_5sec(): # Feed a valid list with one designed error. Expect the output to report a dictionary with single data recorded 
    timestamps = [
            datetime(2025, 5, 5, 3, 4, 5), 
            datetime(2025, 5, 5, 3, 4, 6), 
            datetime(2025, 5, 5, 3, 4, 7), 
            datetime(2025, 5, 5, 3, 4, 8),
            datetime(2025, 5, 5, 3, 4, 9),
            datetime(2025, 5, 5, 3, 4, 10),
            datetime(2025, 5, 5, 3, 4, 11)]
    results = consecutive_error_check(timestamps)
    assert results == {"consecutive_error_count": [7], "consecutive_error_time": [datetime(2025,5,5,3,4,5)]}

def test_multiple_error_sets(): # Feed a valid list with multiple designed errors. Expect the output to contain a dictionary with multiple data recorded 
    timestamps = [
            datetime(2025, 5, 5, 3, 4, 5), 
            datetime(2025, 5, 5, 3, 4, 6), 
            datetime(2025, 5, 5, 13, 4, 7), 
            datetime(2025, 5, 5, 13, 4, 8), 
            datetime(2025, 5, 5, 13, 4, 9), 
            datetime(2025, 5, 5, 13, 4, 10), 
            datetime(2025, 5, 5, 13, 4, 11), 
            datetime(2025, 5, 5, 13, 4, 12), 
            datetime(2025, 5, 5, 14, 4, 13), 
            datetime(2025, 5, 5, 15, 4, 13), 
            datetime(2025, 5, 5, 15, 5, 14), 
            datetime(2025, 5, 5, 16, 5, 14), 
            datetime(2025, 5, 5, 16, 5, 15), 
            datetime(2025, 5, 5, 16, 5, 19), 
            datetime(2025, 5, 5, 16, 5, 24), 
            datetime(2025, 5, 5, 16, 5, 26), 
            datetime(2025, 5, 5, 16, 5, 29),
            datetime(2025, 5, 5, 17, 5, 29),
            datetime(2025, 5, 5, 17, 6, 29)]
    results = consecutive_error_check(timestamps)
    # print(results)
    assert results == {"consecutive_error_count": [6, 6], "consecutive_error_time": [datetime(2025, 5, 5, 13, 4, 7), datetime(2025, 5, 5, 16, 5, 14)]}

def test_not_enough_errors_in_5sec(): # Feed a valid list with no errors in timing. Expect the output to be an empty disctionary. 
    timestamps = [
            datetime(2025, 5, 5, 3, 4, 5), 
            datetime(2025, 5, 5, 3, 4, 6), 
            datetime(2025, 5, 5, 3, 4, 7), 
            datetime(2025, 5, 5, 3, 4, 8), 
            datetime(2025, 5, 5, 3, 4, 16)]
    results = consecutive_error_check(timestamps)
    assert results == {"consecutive_error_count": [], "consecutive_error_time": []}

def test_empty_list(): # Feed an empty list input into the function. Expect the output to be an empty dictionary.
    results = consecutive_error_check([])
    assert results == {"consecutive_error_count": [], "consecutive_error_time": []}

