from lxml import etree as ET
import Indicator_Manager
import InstanceHolder

def save_data(path, symbol, timeframe):
    indicatordata = Indicator_Manager.get_activeindicators()
    root = ET.Element("printerTemplate")
    ET.SubElement(root, "version").text = InstanceHolder.version
    ET.SubElement(root, "tradingSymbol").text = str(symbol)
    ET.SubElement(root, "tradingInterval").text = str(timeframe)
    indicators = ET.SubElement(root, "indicators")
    for indicator in indicatordata:
        name = indicator.name
        values = indicator.get_values()
        sub = ET.SubElement(indicators, name)
        for key in values:
            ET.SubElement(sub, key).text = str(values[key])
    tree = ET.ElementTree(root)
    tree.write(path, pretty_print=True)