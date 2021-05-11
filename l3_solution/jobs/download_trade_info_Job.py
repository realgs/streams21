from l3_solution.bitbay.bit_bay_service import BitBayService
from l3_solution.visualizers.bit_bay_trade_chart_visualizer import BitbayTradeChartVisualizer
import traceback


class DownloadTradeInfoJob:
    bit_bay_service = BitBayService()
    visualizer = BitbayTradeChartVisualizer()

    def execute(self):
        try:
            self.bit_bay_service.update_crypto_trades()
            self.visualizer.visualize(self.bit_bay_service)
        except:
            print("Download or visualize trade Fail")
            traceback.print_exc()
            self.visualizer.config = {"range_elements": None, "range_rsi": None}
            self.execute()
