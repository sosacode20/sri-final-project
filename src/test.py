from irs.parsers import cran_parser
from irs.irs import IRS
from irs.document import document

file = open('/home/ironbeardx/MyStuff/School/SRI-Final_Proyect/sri-final-project/src/Datasets/cran/cran.all.1400','r')
parser = cran_parser()
doc = parser.parse(file)[0]

irs = IRS()
document = document(doc[2], doc[0], doc[1], "english", irs)

document