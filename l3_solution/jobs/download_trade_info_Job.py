from l3_solution.bitbay.bit_bay_service import BitBayService
from l3_solution.visualizers.bit_bay_trade_chart_visualizer import BitbayTradeChartVisualizer


class DownloadTradeInfoJob:
    bit_bay_service = BitBayService()
    visualizer = BitbayTradeChartVisualizer()

    def execute(self):
        try:
            trade_buy, trade_sell = self.download_trade()
            volume = self.download_volume()
            self.visualizer.visualize(trade_buy, trade_sell, volume)
        except:
            print("Download or visualize trade Fail")

    def download_trade(self):
        trade_buy = {
            'BTC': self.bit_bay_service.get_crypto_trade_buy('EUR', 'BTC'),
            'LTC': self.bit_bay_service.get_crypto_trade_buy('EUR', 'LTC'),
            'DASH': self.bit_bay_service.get_crypto_trade_buy('EUR', 'DASH'),
        }
        trade_sell = {
            'BTC': self.bit_bay_service.get_crypto_trade_sell('EUR', 'BTC'),
            'LTC': self.bit_bay_service.get_crypto_trade_sell('EUR', 'LTC'),
            'DASH': self.bit_bay_service.get_crypto_trade_sell('EUR', 'DASH'),
        }
        return trade_buy, trade_sell

    def download_volume(self):
        return {
            'BTC': self.bit_bay_service.get_crypto_volume('EUR', 'BTC'),
            'LTC': self.bit_bay_service.get_crypto_volume('EUR', 'LTC'),
            'DASH': self.bit_bay_service.get_crypto_volume('EUR', 'DASH'),
        }
