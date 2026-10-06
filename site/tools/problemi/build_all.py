import sys; sys.path.insert(0, '.')
from common import page
import p_booking, p_prezzi, p_sostituibili, p_agenzie, p_valore, p_apertura
for m in (p_booking, p_prezzi, p_sostituibili, p_agenzie, p_valore, p_apertura):
    print(page(m.P))
