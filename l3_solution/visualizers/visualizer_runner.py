from l3_solution.bitbay.bit_bay_service import BitBayService
from l3_solution.visualizers.bit_bay_trade_chart_visualizer import BitbayTradeChartVisualizer
import traceback


class VisualizerRunner:
    bit_bay_service = BitBayService()
    visualizer = BitbayTradeChartVisualizer()

    def execute(self, shared_json):
        try:
            self.visualizer.visualize(self.bit_bay_service, shared_json)
        except:
            print("Download or visualize trade Fail")
            traceback.print_exc()
            self.visualizer.config = {"range": 20}
            self.execute(shared_json)
