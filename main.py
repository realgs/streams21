# 1. Dajemy możliwość naniesienia na wykres punktu odniesienia - ceny kupna zasobów.
# - Wykres jest odświeżany w czasie rzeczywistym i reprezentuje strumienie danych dotyczące
#   trzech zasobów giełdowych, jak w poprzedniej liście.
# - Podczas działania programu użytkownik ma mieć możliwość wielokrotnego wprowadzenia
#   informacji co, w jakiej ilości i za ile kupił. Może to robić w odstępach czasowych
#   i dla różnych zasobów, w nieokreślonej kolejności.
# - Na podstawie wprowadzonych przez użytkownika danych wyliczamy dotychczasową średnią zakupu
#   danego waloru i nanosimy poziomą, przerywaną linią na wykres wartości zasobu.
# - Zwrócić uwagę na zakresy wartości na osi y, wszystko ma się mieścić w zakresie wartości.

# 2. Dodajemy możliwość wprowadzenia sprzedaży zasobów analogicznie do kupna.
# - Po sprzedaży aktualizujemy obecną średnią cenę zakupu (nie uwzględniającą już tych jednostek,
#   które zostały sprzedane. Zasada FIFO - first in first out)
#   przykład: jeśli kupiliśmy 10 jednostek po 4000$, następnie 20 jednostek po 6000$, a na końcu
#   20 jednostek po 10000$, a następnie sprzedaliśmy 10 jednostek za 50000$ to nasz zysk wynosi
#   460000$ a obecna średnia cena zakupu to 8000$.
# - Przy sprzedaży obliczamy osiągnięty zysk/stratę i nanosimy informację o zysku/stracie
#   w okolicy wykresu danego zasobu.

# 3. Program ma umożliwiać zapis (i odczyt) wprowadzonych danych w formacie .json
#    tak, by po ponownym uruchomieniu można było wprowadzić nazwę pliku przechowującego dane
#    i nie gromadzić danych od nowa.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image
import requests
import time


