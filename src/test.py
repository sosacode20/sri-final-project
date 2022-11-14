from irs.parsers import cran_parser

file = open('/home/ironbeardx/MyStuff/School/SRI-Final_Proyect/sri-final-project/src/Datasets/cran/cran.all.1400','r')
parser = cran_parser()
doc = parser.parse(file)

doc