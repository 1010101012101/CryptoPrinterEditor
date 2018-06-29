import Candle_Manager
import File_Loader

__loaded_indicators = []
__active_indicators = []

def load_indicators():
    indicators = File_Loader.get_objects('Indicators')
    for indi in indicators:
        __loaded_indicators.append(indi)

def set_indicator(name, **kwargs):
    indicator = next((x for x in __loaded_indicators if x.name == name), None)
    indicator.set_values(**kwargs)

def get_indicatordata(name, length):
    candles = Candle_Manager.get_candles(length=500)
    indicator = next((x for x in __loaded_indicators if x.name == name), None)
    points = []
    for i in range(length):
        points.append(indicator.get_points(candles[i:i+50]))
    return points