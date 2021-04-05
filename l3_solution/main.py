import time

import schedule

from l3_solution.jobs.download_trade_info_Job import DownloadTradeInfoJob

if __name__ == '__main__':
    download_trade_info_Job = DownloadTradeInfoJob()
    schedule.every(5).seconds.do(download_trade_info_Job.execute)

    while 1:
        schedule.run_pending()
        time.sleep(1)
