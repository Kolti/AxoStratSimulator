import datetime as dt

def GetPeriods(endDate: dt.datetime, overallTimePeriod:int, periodLength:int):
    if periodLength > overallTimePeriod:
        raise Exception()
    curPer = periodLength
    result = []
    while curPer <= overallTimePeriod:
        result.append((curPer, curPer - periodLength))
        curPer += 1
    return __GetPeriods(endDate, result)
    

def __GetPeriods(endDate:dt.datetime, dayShiftIntervals:list[tuple]):
    result = []
    oneDay=dt.timedelta(days=1)
    for interval in dayShiftIntervals:
        result.append((endDate-interval[0]*oneDay,endDate-interval[1]*oneDay))
    return result