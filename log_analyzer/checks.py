from datetime import timedelta

def consecutive_error_check(errordatetime): # Checks if multiple errors has been detected within a 5 seconds from each other more than 5 times
    errorcounter = 0
    consecutive_errors_count = []
    consecutive_errors_time = []

    for i in range(len(errordatetime)):

        if i == 0:
            continue
        elif (errorcounter == 0) and (errordatetime[i] - errordatetime[i-1] <= timedelta(seconds=5)):
            errorstarttime = i - 1
            errorcounter += 1
        elif (errorcounter != 0) and (errordatetime[i] - errordatetime[i-1] <= timedelta(seconds=5)):
            errorcounter += 1
        else:
            if errorcounter >= 4:
                consecutive_errors_count.append(errorcounter + 1)
                consecutive_errors_time.append(errordatetime[errorstarttime])
            errorcounter = 0
    
    if errorcounter >= 4:
        consecutive_errors_count.append(errorcounter + 1)
        consecutive_errors_time.append(errordatetime[-1])

    
    return {
        "consecutive_error_count": consecutive_errors_count,
        "consecutive_error_time": consecutive_errors_time
    }

