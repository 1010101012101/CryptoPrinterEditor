import Candle_Manager
import File_Loader

__loaded_indicators = []
__active_indicators = []

def load_indicators():
    indicators = File_Loader.get_objects('Indicators')
    for indi in indicators:
        __loaded_indicators.append(indi)

def set_indicator(name, key, value):
    indicator = __get_indicator_by_name(name)
    indicator.set_values(key,value)

def get_indicator_names():
    names = [x.name for x in __loaded_indicators]
    return names

def get_indicator_values(name):
    indicator = __get_indicator_by_name(name)
    return(indicator.get_values())

def get_indicatordata(name, length):
    candles = Candle_Manager.get_candles(length=length+50)
    indicator = __get_indicator_by_name(name)
    return __get_indicatorpoints(indicator, candles, length)
    
def get_activeindicatordata(length):
    candles = Candle_Manager.get_candles(length=length+50)
    allpoints = []
    for indicator in __active_indicators:
        allpoints.append(__get_indicatorpoints(indicator,candles,length))
    addedpoints = []
    addedpoints = [0 for x in range(length)]
    for points in allpoints:
        for i in range(len(points)):
            addedpoints[i] += points[i]
    return addedpoints
        

def __get_indicatorpoints(indicator, candles, length):
    points = []
    for i in range(length):
            newpoint = indicator.get_points(candles[i:i+50])
            if newpoint is not None:
                points.append(newpoint)
    return points

def add_to_active(name):
    indicator = __get_indicator_by_name(name)
    __active_indicators.append(indicator)

def remove_from_active(name):
    indicator = __get_indicator_by_name(name)
    __active_indicators.remove(indicator)


def __get_indicator_by_name(name):
    return(next((x for x in __loaded_indicators if x.name == name), None))