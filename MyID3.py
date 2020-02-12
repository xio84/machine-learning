import pandas as pd
import math

class MyTree:
    """A custom decision tree.

    Parameters
    ----------
    rule : lambda function (returns bool), optional (default=x: True)
        the rule to enter this node (example : rule = x: x.outlook == 'sunny').
    label : string, optional (default=None)
        label of the node, applies only to leaf nodes.
    node : array, optional (default=[])
        children nodes of tree, applies only to non-leaf nodes.

    Attributes
    ----------
    rule : lamda -> bool
    label : string
    prune : array
    """
    def __init__(self, rule = lambda x: True, label = None, node = []):
        super().__init__()
        self.rule = rule
        self.label = label
        self.node = node

    def addNode(tree):
        self.node.append(tree)

class MyID3Estimator:
    """ A custom ID3Estimator
    Attributes
    ----------
    tree : MyTree
    the decision tree

    labelAttr : string
    class attribute
    """
    def __init__(self):
        super().__init__()
        self.tree = MyTree()
        self.attr = []
        self.labelAttr = None

    def fit(self, data):
        """Creates decision tree based on training dataset

        Attributes
        ----------
        data: dataframe
        training dataset
        """
        

    def estimate(self, x):
        """ Estimate label of instance x based on decision tree
        
        Parameters
        ----------
        x = collections.namedtuple
        the instance to be tested
        https://pymotw.com/2/collections/namedtuple.html

        Returns
        ----------
        label = string, None
        """
        root = self.tree
        while (label == None):
            nodes = root.node
            if (nodes == []):
                break
            for node in nodes:
                if node.rule(x):
                    root = node
                    break
            label = root.label
        return label
        
    def entropyData(self, data):
        """
        data = dataframes yang sudah difilter sesuai kebutuhan
        """
        dataAtr = data.loc[:, self.labelAttr]
        labelSet = set(dataAtr)
        labelMap = dict.fromkeys(labelSet, 0)
        instances = len(dataAtr)

        for label in dataAtr:
            labelMap[label]++

        entropy = 0
        for label in labelSet:
            entropy += -(labelMap[label]/instances) * math.log(labelMap[label]/instances) 

        return entropy    

    def filterDataFrame(self, data, attr, value, root):
        """ Filter data based on attr and value parameters

        Parameters
        ----------
        data = dataframe yang ingin difilter
        attr = Atribut filter
        value = value dari attribute filter yang ingin
                diaplikasikan ke dataframe

        Returns
        ----------
        filteredData = data yang sudah difilter
        """

        # Inisialisasi dataframe temporer 'filteredData' dengan dataframe 'data'
        filteredData = data

        # Filter data dengan melakukan drop row
        # Hanya row dengan nilai 'value' pada atribut 'attr' saja yang tetap ada di dataframe
        filteredData = filteredData[filteredData[attr] == value]

        return filteredData

    def informationGain(self, dataset, attr, root):
        if root == none:
            return entropyData(dataset) - filterDataFrame(dataset, attr) - filterDataFrame(dataset, attr)
