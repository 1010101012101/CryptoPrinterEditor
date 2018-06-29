from Indicators._RSI_Indicator import RSI
import Candle_Manager
import File_Loader

__loaded_indicators = []
__active_indicators = []

def load_indicators():
    indicators = File_Loader.get_objects('Indicators')
    for indi in indicators:
        __loaded_indicators.append(indi)

def get_indicatordata(name, length):
    candles = Candle_Manager.get_candles(length=500)
    indicator = next((x for x in __loaded_indicators if x.name == name), None)
    points = []
    for i in range(length):
        points.append(indicator.get_points())
    return points