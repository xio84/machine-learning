import pandas as pd
import math

pd.set_option('display.max_rows', 151)

threshold_dict = dict()

class Node:
    def __init__(self,
                _parent = None, # A Node
                _children = [], # list of NODES
                _infoGain = None, # double?
                _attribute = None, # string?
                _valuesTaken = {}): # rules chosen (decision made in each nodes of the parent)
        self.parent = _parent
        self.children = _children
        self.infoGain = _infoGain
        self.attribute = _attribute
        self.valuesTaken = _valuesTaken

    def addChild(self, _node = None):
        if(_node == None):
            _node = self.__init__()
        self.children.append(_node)
        return _node

    def isLeaf(self):
        return not self.children

    def _printTree(self, space):
        if(self.isLeaf()):
            return
        else:
            print(str(space*' ') + str(self.attribute))
            for child in self.children:
                #print(self.children)
                child._printTree(space+2)

class MyTree:
    """A custom decision tree.

    Parameters
    ----------
    root : lambda function (returns bool), optional (default=x: True)
        the rule to enter this node (example : rule = x: x.outlook == 'sunny').
    targetAttribute : string, optional (default=None)
        label of the node, applies only to leaf nodes.
    node : array, optional (default=[])
        children nodes of tree, applies only to non-leaf nodes.

    Attributes
    ----------
    root = 
    targetAttribute = attribute hasil prediksi
    """
    def __init__(self, 
                _root = Node(),
                _targetAttribute = None):
        self.root = _root
        self.targetAttribute = _targetAttribute
    
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
        valueSet = self.getValuesInAttribute(data, self.targetAttribute)
        valueMap = dict.fromkeys(valueSet, 0)
        instances = len(data)

        for value in data.loc[:,self.targetAttribute]:
            valueMap[value]+=1

        entropy = 0
        for value in valueSet:
            entropy += -valueMap[value]/instances * math.log(valueMap[value]/instances,2) 
        # print(data)
        # print("entropy : ", entropy)
        return entropy

    def filterDataFrame(self, data, attr, value):
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

    def informationGain(self, dataset, attr):
        """
        dataset = dataset yang sudah terfilter
        attr = atribut yang ingin dicari information gainnya
        """
        gain = self.entropyData(dataset)
        # print(gain)
        instances = len(dataset)
        for value in self.getValuesInAttribute(dataset, attr):
            # print(value)
            # print(self.filterDataFrame(dataset, attr, value))
            gain = gain -(self.getValueInstance(dataset,attr,value)/instances) * (self.entropyData(self.filterDataFrame(dataset, attr, value))) 
        
        # print("gain" , gain)
        return gain

    def partitionData(self, dataset, attr):

        return 0

    def splitInformation(self, dataset):
        """
        Alternative measures for selecting attributes
        """

        return 1

    def gainRatio(self, dataset, attr):
        """
        Alternative measures for selecting attributes 
        """

        return informationGain(dataset, attr)/splitInformation(dataset, attr)

    def getValueInstance(self, data, attr, targetValue):
        count = 0
        for value in data.loc[:,attr]:
            if(targetValue == value):
                count +=1
        return count


    def getValuesInAttribute(self, data, attr):
        return list(set(data.loc[:, attr]))

    def getAttributesInData(self, data):
        atrs = list(data.columns)
        del atrs[-1]
        return atrs
        
    def buildTreeInit(self, trainingSet = None):
        curr_node = self.root
        attr_set = self.getAttributesInData(trainingSet)
        self.buildTree(curr_node, trainingSet, attr_set)

    def buildTree(  self,
                    curr_node = None, # current root 
                    trainingSet = None, # dataset training
                    attr_set = None
                    ):

        
        # initial dataframe pruning from VALUES/decision taken by parents
        dataset = trainingSet
        # print(curr_node.valuesTaken.items())
        for attr,val in curr_node.valuesTaken.items():
            dataset = self.filterDataFrame(dataset, attr, val)
            if(attr in attr_set):
                attr_set.remove(attr)

        print(dataset)
        print("EntropyBigData: ", self.entropyData(dataset))
        if self.entropyData(dataset) == 0.0 :
            # leaf node!
            # print("LEAF!!!")
            curr_node.attribute = self.targetAttribute
            curr_node.valuesTaken[curr_node.attribute] = self.getValuesInAttribute(dataset, curr_node.attribute)[0]
            curr_node.children = []
            print("Attribute1: " + curr_node.attribute)
            # print("EntropyData: ", self.entropyData(dataset))
            return
        
        

        best_node = (None, -999) # best_node -> (attribute name, information gain value)
        # count Information Gain for every attributes:
        for attr in attr_set:
            candidateIG = self.informationGain(dataset, attr)
            if (candidateIG > best_node[1]):
                best_node = (attr, candidateIG)

        # best attribute = best_node
        curr_node.attribute = best_node[0]
        print("Attribute2: ", curr_node.attribute)
        vals_set = self.getValuesInAttribute(data, best_node[0])
        for value in vals_set:
            temp = dict(curr_node.valuesTaken)
            temp[best_node[0]] = value
            next_node = curr_node.addChild(_node = Node(_parent = curr_node,
                                    _children = [],
                                    _valuesTaken = temp
                                    ))
            # print(curr_node.attribute, " : ")
            # for x in curr_node.children:
            #     print("--", x.attribute)
            self.buildTree(next_node, dataset, set(attr_set))
        #print(curr_node.attribute, next_node.attribute)
        
        

    def printTree(self):
        # print self (root)
        self.root._printTree(space = 0)

def handleContinuousAttribute(data):
    target = data.columns[-1]
    t = MyTree(_targetAttribute=target)
    for attr in t.getAttributesInData(data):
        if (isinstance(data.iloc[0][attr], float)):
            threshold_dict[attr] = max(data[attr])
            best_threshold = threshold_dict[attr]
            best_information_gain = -1
            data = data.sort_values(by=[attr])
            target_value = data.iloc[0][target]
            data_temp = data.copy()
            for index, row in data.iterrows():
                if (row[target] == target_value):
                    pass
                else:
                    threshold_temp = (data.iloc[index-1][attr] + data.iloc[index][attr]) / 2
                    data_temp.loc[data_temp[attr] < threshold_temp, attr] = 0
                    data_temp.loc[data_temp[attr] >= threshold_temp, attr] = 1
                    information_gain_temp = t.informationGain(data_temp, attr)
                    if (information_gain_temp > best_information_gain):
                        best_information_gain = information_gain_temp
                        best_threshold = threshold_temp
            
            threshold_dict[attr] = best_threshold
            print("best_threshold: " + str(best_threshold))
            data.loc[data[attr] < best_threshold , attr] = 0
            data.loc[data[attr] >= best_threshold , attr] = 1

    return data

if __name__ == "__main__":
    # Dataset Iris
    data = pd.read_csv("iris.csv", header=None, names=['attr1', 'attr2', 'attr3', 'attr4', 'target'])
    data = handleContinuousAttribute(data)

    print(data)
    print(threshold_dict)
    # t = MyTree(_targetAttribute="target")
    # t.buildTreeInit(trainingSet=data)
    # t.printTree()

    # Dataset Tennis
    '''
    data = pd.read_csv("tennis.csv")
    t = MyTree(_targetAttribute = "play")
    # for attr in t.getAttributesInData(data):
    #     if (len(t.getValuesInAttribute(data, attr)) > 10):
    #         print("attr: " + attr + " is continuous")

    t.buildTreeInit(trainingSet = data)
    t.printTree()
    '''
