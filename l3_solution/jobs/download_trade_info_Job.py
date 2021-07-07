from l3_solution.bitbay.bit_bay_service import BitBayService
from l3_solution.visualizers.bit_bay_trade_chart_visualizer import BitbayTradeChartVisualizer


class DownloadTradeInfoJob:
    bit_bay_service = BitBayService()
    visualizer = BitbayTradeChartVisualizer()

    def execute(self):
        try:
            trade_buy, trade_sell = self.download_trade()
            self.visualizer.visualize(trade_buy, trade_sell)
        except:
            print("Download or visualize trade Fail")

    def download_trade(self):
        trade_buy = {
            'BTC': self.bit_bay_service.get_crypto_trade_buy('USD', 'BTC'),
            'LTC': self.bit_bay_service.get_crypto_trade_buy('USD', 'LTC'),
            'DASH': self.bit_bay_service.get_crypto_trade_buy('USD', 'DASH'),
        }
        trade_sell = {
            'BTC': self.bit_bay_service.get_crypto_trade_sell('USD', 'BTC'),
            'LTC': self.bit_bay_service.get_crypto_trade_sell('USD', 'LTC'),
            'DASH': self.bit_bay_service.get_crypto_trade_sell('USD', 'DASH'),
        }
        return trade_buy, trade_sell
