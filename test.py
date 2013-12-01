import math
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET

import xml.etree.ElementTree as ET
tree = ET.parse('test.xml')
root = tree.getroot()

print root[0][5][0].text


