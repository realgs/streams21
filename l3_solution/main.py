import ctypes
from multiprocessing import Manager

from l3_solution.market_api import MarketApi
from l3_solution.visualizers.visualizer_runner import VisualizerRunner

init_json = """{"BTC": {"price": "0", "quantity": "0"}, "LTC": {"price": "0", "quantity": "0"}, "ETH": {"price": "0", "quantity": "0"}}"""


def init_shared_data():
    return Manager().Value(ctypes.c_char_p, init_json)


if __name__ == '__main__':
    shared_json = init_shared_data()
    MarketApi(shared_json)
    app_runner = VisualizerRunner()
    app_runner.execute(shared_json)
