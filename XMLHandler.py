'''
This class is used to handle the strategies.xml file, which contains the parameters that are generated by the
genetic algorithm. They are mainly linked to how agressive or conservative the pokerbot should play in different
circumstances or game stages.
'''

import xml.etree.ElementTree as xml
from copy import deepcopy
import re


class XMLHandler(object):
    def __init__(self, filename):
        self.XMLEntriesList = dict()
        self.filename = filename

    def readXML(self):
        self.tree = xml.parse(self.filename)
        self.root = self.tree.getroot()

        self.CurrentStrategy = self.root.find('CurrentStrategy')

        for self.XML_entry in self.root.findall('Strategy'):
            if self.XML_entry.get('name') == self.CurrentStrategy.text:
                for child in self.XML_entry:
                    self.XMLEntriesList[child.tag] = child

        self.XMLEntriesList2 = deepcopy(self.XMLEntriesList)

        for e in self.XMLEntriesList2:
            self.XMLEntriesList2[e].set('updated', 'False')

        self.modified = False
        self.Template = self.CurrentStrategy.text

    def modifyXML(self, elementName, change):
        self.XMLEntriesList2[elementName].text = str(round(float(self.XMLEntriesList2[elementName].text) + change, 2))
        self.XMLEntriesList2[elementName].set('updated', str(change))
        self.modified = True

    def saveXML(self):
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        m = r.match(self.CurrentStrategy.text)
        stringPart = m.group(1)
        numberPart = int(m.group(2))
        numberPart += 1
        self.newStrategyName = stringPart + str(numberPart)
        self.CurrentStrategy.text = self.newStrategyName
        newElement = xml.Element('Strategy')
        newElement.set('name', self.newStrategyName)
        self.root.append(newElement)
        for child in self.XML_entry:
            newElement.append(self.XMLEntriesList2[child.tag])

            self.tree.write(self.filename)
            self.XMLEntriesList = deepcopy(self.XMLEntriesList2)

        self.Template = self.CurrentStrategy.text


if __name__ == '__main__':
    XML = XMLHandler('strategies.xml')
    XML.readXML()
    # XML.modifyXML('RiverCallPower',-1)
    pass