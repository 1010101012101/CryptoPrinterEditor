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
    candles = Candle_Manager.get_candles(length=500)
    indicator = __get_indicator_by_name(name)
    points = []
    for i in range(length):
            points.append(indicator.get_points(candles[i:i+50]))
    return points

def __get_indicator_by_name(name):
    return(next((x for x in __loaded_indicators if x.name == name), None))