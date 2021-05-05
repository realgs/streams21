import requests as r
from time import sleep
from matplotlib import pyplot as plt
from requests.exceptions import HTTPError
from datetime import datetime
from matplotlib.animation import FuncAnimation
from apikey import apikey
import numpy as np
from tabulate import tabulate
import os

y = [1,2,3,4,5]
plt.plot(y)
plt.show()