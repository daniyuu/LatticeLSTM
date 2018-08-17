from utils.data import Data

data = Data()
debug_file = "debug.txt"
gaz_file = "data/ctb.50d.vec"
data.build_alphabet(debug_file)
data.build_gaz_file(gaz_file)
data.build_gaz_alphabet(debug_file)
