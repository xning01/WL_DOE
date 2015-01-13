from time import time
import scipy as sp
import numpy as np
import sklearn as skl
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.svm import LinearSVC

def pre_outlier_removal(feature_matrix,label_vector,parameter):
    """ Ning's work: outlier removal
        ------
        
        """"
    return raw_feature, raw_label

def train_knn(train_feature,train_label,parameter):
    """ Tong's work :
        train_knn : KNN classifier """
    return model
    
def test_knn(test_feature,model):
    """ Tong's work :
        test_knn : KNN classifier """
    return label
    
def train_svm(train_feature,train_label,parameter):
    """ Tong's work :
        train_knn : KNN classifier """
    return model
   
def test_svm(test_feature,model):
    """ Tong's work :
        test_svm : svm classifier """
    return label

    
def train_NB(train_feature,train_label,parameter):
    """ Song's work :
        train_NB : naive bayssian classifier """
    return model

def test_NB(test_feature,model):
    """ Song's work :
        test_NB : naive bayssian classifier """
    return label

def train_struct(train_feature,train_label,parameter):
    """ Song's work :
        train_struct : structure classifier """
    return model

def train_struct(test_feature,model):
    """ Song's work :
        train_struct : structure classifier  """
    return label




class Student_classification:
    """student classification:
        Initialization input : training set
        
        Attributes
        ---------
        raw_feature : without preprocessing raw feature
        raw_label : without outlier removal label
        
        Functions:
        ---------
        pre_mutual : mutual information based feature selection
        pre_struct : structure learning based feature selection
        pre_mrmr   : minimum redundancy maximum relevance feature selection

        """
    def __init__(self, train_raw_feature,train_label,valid_raw_feature,valid_label):
        """ class initialization: for now assume complete data and given student label
            """
        # feature matrix dimension 0: datasample dimension 1: features
        self.raw_train_feature = train_raw_feature
        self.train_label = train_label
        self.raw_test_feature = valid_raw_feature
        self.valid_label = valid_label
    
    def pre_mutual(self,parameter = 0.5):
        
        # calculating adjusted mutual information between feature and label
        for i in range(self.raw_train_feature.shape[1]):
            score[i] = np.absolute(adjusted_mutual_info_score(self.raw_train_feature,self.train_label))
        # sorting  features
        sort_score = np.argsort(-score)
        # selecting top features number
        select_feature_len = int(sort_score.size*parameter)
        # selecting top features
        select_feature = sort_score[0:select_feature]
        # returning selected training features
        self.train_feature = self.raw_train_feature[select_feature,:]
        # returning selected testing features
        self.test_feature = self.raw_test_feature[select_feature,:]



    
    def pre_L1(self,parameter=0.1):
        """Parameter is the C factor of svm """
        
        # concatenating feature matrix
        feature = np.concatenate(self.raw_train_feature,self.raw_test_feature,axis = 0)
        # concatenation label vector
        label = np.concatenate(self.train_label,self.valid_label,axis = 0)
        # L1 based feature selection
        new_feature = LinearSVC(C=parameter, penalty="l1", dual=False).fit_transform(feature, label)
        # reallocating into training set and testing set
        self.train_feature = new_feature[0:self.raw_train_feature.shape[0],:]
        self.test_feature = new_feature[self.raw_train_feature.shape[0]+1:end,:]
    
    
        
    def pre_mrmr(self,parameter):
        """ Song's work:
            example code:
            self.train_feature,self.train_label = process_method(self.raw_feature,self.raw_label,parameter)
            self.valid_feature,self.valid_label = process_method(self.raw_feature,self.raw_label,parameter)
            
            """
    def get_train(self):
        return self.train_feature,self.train_label

    def get_valid(self):
        return self.valid_feature,self.valid_label





if __name__ == '__main__':
## sample code(flow chart):
# outlier removal -> preprocess -> train -> validation
    # outlier removal
    feature_matrix,label_vector = pre_outlier_removal(feature,label,parameter1)
    
    # preprocessing(i.e. feature extraction)
    model_A = Student_classification(feature_matrix,label_vector)
    
    # select feature: take mutual information feature extraction as example
    model_A.pre_mutual(parameter2,train ='true')
    
    # return train feature
    train_feature, train_label = model_A.get_train()
    # return validation feature
    valid_feature, valid_label = model_A.get_valid()
    
    # training model
    model = train_knn(train_feature,train_label,parameter3)
    # validating model
    label_predict = test_knn(valid_feature,model)



