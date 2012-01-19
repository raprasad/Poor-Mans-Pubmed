from xml.parsers import expat

class Element(object):
    ''' A parsed XML element '''

    def __init__(self, name, attributes):
        # Record tagname and attributes dictionary
        self.name = name
        self.attributes = attributes
        
        # Initialize the element's cdata and children to empty
        self.cdata = ''
        self.children = []

    def addChild(self, element):
        self.children.append(element)

    def getAttribute(self, key):
        return self.attributes.get(key)

    def getData(self):
        return self.cdata

    def getElements(self, name=''):
        if name is None:
            return None
            
        if name:
            return [c for c in self.children if c.name == name]
        else:
            return list(self.children)

class Xml2Obj(object):
    ''' XML to Object converter '''
    def __init__(self):
        self.root = None
        self.nodeStack = []
        
    def StartElement(self, name, attributes):
        'Expat start element event handler'
        # Instantiate an Element object
        element = Element(name.encode(), attributes)
        # Push element onto the stack and make it a child of parent
        if self.nodeStack:
            parent = self.nodeStack[-1]
            parent.addChild(element)
        else:
            self.root = element
        self.nodeStack.append(element)
    
    def EndElement(self, name):
        'Expat end element event handler'
        self.nodeStack.pop()
    
    def CharacterData(self, data):
        'Expat character data event handler'
        if data.strip():
            data = data.encode("utf-8")
            element = self.nodeStack[-1]
            element.cdata += data
    
    def Parse(self, xmlstr):
        # Create an Expat parser
        Parser = expat.ParserCreate()
        # Set the Expat event handlers to our methods
        Parser.StartElementHandler = self.StartElement
        Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData
        # Parse the XML File
        ParserStatus = Parser.Parse(xmlstr, True)
        return self.root

if __name__ == '__main__':
    parser = Xml2Obj()
    root_element = parser.Parse(open('samples/article_001.xml').read())
    root_element.getElements('PubmedArticle')s    

