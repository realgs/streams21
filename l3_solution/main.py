from matplotlib import pyplot as plt

from l3_solution.jobs.download_trade_info_Job import DownloadTradeInfoJob

if __name__ == '__main__':
    download_trade_info_Job = DownloadTradeInfoJob()

    download_trade_info_Job.execute()
