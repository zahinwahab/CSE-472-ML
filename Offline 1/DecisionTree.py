import pandas as pd 
import sklearn
import math
    
data = pd.read_csv("Tennis.csv")
#print(data.head())
df = pd.DataFrame (data, columns = ['Day','Outlook','Temperature','Humidity','Wind','Play'])
def calculate_entropy_step2(q):
    B1 = 0
    if q == 0:
        B1=0
    else:
        B1 = -q*math.log(q,2) 
    #print(B1)
    #print(1-q)
    B2=0
    if (1-q)==0:
        B2=0
    else:
        B2 = -(1-q)*math.log(1-q,2)
    B = B1+B2
    return B
def calculate_entropy(attribute_name,column_value,examples):
    total_p = 0
    total_n = 0
    for iter in examples[examples[attribute_name]==column_value]['Play'].values:
        if iter == 'Yes':
            total_p = total_p+1
        elif iter == 'No':
            total_n = total_n+1
    total = total_p+total_n
    q = total_p/total
    
    B = calculate_entropy_step2(q)
    return total_p,total_n,B


    

def calculate_information_gain(attribute_name,examples):
    print(attribute_name)
    unique_values = examples[attribute_name].unique()
    #print(unique_values)
    sum=0
    total_samples=len(examples)
    total_samples_positive= len(examples[examples['Play']=='Yes'])
    ParentEntropy = calculate_entropy_step2(total_samples_positive/total_samples)
    #print(ParentEntropy)
    for val in unique_values:

        pk,nk,B = calculate_entropy(attribute_name,val,examples)
        sum = sum + ((pk+nk)*B)/total_samples
    Entropy = ParentEntropy - sum
    #print(Entropy)
    return Entropy
def PluralityVal(examples):
    L = len(examples)
    #print(L)
    positive_samples = examples[examples['Play']=='Yes']
    negative_samples = examples[examples['Play']=='No']
    if len(positive_samples) > len(negative_samples):
        return 'Yes'
    else:
        return 'No'
def check_if_same_classification(examples):
    L = len(examples)
    #print(L)
    positive_samples = examples[examples['Play']=='Yes']
    negative_samples = examples[examples['Play']=='No']
    if len(positive_samples) == L:
        return 'Yes'
    elif len(negative_samples) == L:
        return 'No'
    else: 
        return 'False'
def DecisionTree(examples,attributes,parent_examples):
    #print(len(examples))
   # print(PluralityVal(examples))
    if examples.empty: 
        return PluralityVal(parent_examples)
    elif check_if_same_classification(examples) != 'False':
        return check_if_same_classification(examples)
    elif attributes is None:
        return PluralityVal(examples)
    else:
        max = -math.inf
        max_attr = ''
        for attr in attributes:

            Entropy = calculate_information_gain(attr,examples)
            if Entropy > max:
                max = Entropy
                max_attr = attr
            
        print("Attribute to be taken"+max_attr)
        tree = {}
       
        
        tree[max_attr] = list(examples[max_attr].unique())
        #print(tree)
        for vk in df[max_attr].unique():
            #print(vk)
            exs = examples.loc[examples[max_attr] == vk]
            #print(exs)
            #print(attributes)
            
            if max_attr in attributes:
                attributes.remove(max_attr)

            subtree = DecisionTree(exs,attributes,examples)
            tree[vk] = subtree
    
    return tree

initial_attributes = ['Outlook','Temperature','Humidity','Wind']
tree= DecisionTree(df,initial_attributes,df)
print(tree)