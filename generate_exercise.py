import numpy as np
from hmmlearn.hmm import MultinomialHMM,GMMHMM
import scipy.io as scipy_io
from sklearn.metrics.cluster import adjusted_mutual_info_score
import matplotlib.pyplot as plt
import copy

# generate DB
def generate_exercise(N=1000,K=30,beta=2):
    """ N :  numbers of questions
        K  : knowledge point number
        return : binary matrix N by K
        """
    matrix = np.zeros([N,K])
    for i in range(N):
        peu_K = int(np.random.exponential(beta))
        while peu_K >= K or peu_K == 0:
            peu_K = int(np.random.exponential(beta))
        matrix[i,np.unique(np.random.random_integers(0,K-1,peu_K))]=1
    return matrix

# per-person ... simulate per-person behavior
class question_search():
    def __init__(self,N_seq,K,beta_seq):
        """  quest_A/B/C/D : simulated dataset
             Kmask : keep record whether one knowledge point has been covered
             qmask_A/B/C/D : keep record whether one problem has been answered
            """
        self.quest_A = generate_exercise(N_seq[0],K,beta_seq[0])
        self.quest_B = generate_exercise(N_seq[1],K,beta_seq[1])
        self.quest_C = generate_exercise(N_seq[2],K,beta_seq[2])
        self.quest_D = generate_exercise(N_seq[3],K,beta_seq[3])
        self.Kmask = np.zeros(K)
        self.qmask_A = np.zeros(N_seq[0])
        self.qmask_B = np.zeros(N_seq[1])
        self.qmask_C = np.zeros(N_seq[2])
        self.qmask_D = np.zeros(N_seq[3])
    

    # given difficulty + performance =>  knowledge point update 
    # provide problems for recommendation
    def search_problem(self,diff_label= 0,last_problem_id =[0,0],answer = 0):
        """ diff_label : search difficulty
            last_problem_id : last problem id = [A,B] (A :difficulty, B : id)
            answer : correct or wrong 0/1 """
        # if last problem is correctly answered update knowledge mask
        if answer ==1:
            know_point = self._update_mask(last_problem_id,answer)
                         
        if diff_label ==0:
            data_matrix = self.quest_A
            mask_vector = self.qmask_A
        elif diff_label ==1:
            data_matrix = self.quest_B
            mask_vector = self.qmask_B
        elif diff_label ==2:
            data_matrix = self.quest_C
            mask_vector = self.qmask_C
        else:
            data_matrix = self.quest_D
            mask_vector = self.qmask_D
        
        # get knowledge point
        know_point = self._get_know_point(last_problem_id)
        
         # if last problem is correctly answered search for question
        if answer == 1:
            compare = 0
            quest_id = -1
            for i in range(data_matrix.shape[0]):
                if mask_vector[i] == 0:
                    temp_val = np.sum(np.abs(np.multiply((data_matrix[i,:] - know_point),(1-know_point))))
                    # updating compare value and keep record of id
                    if temp_val > compare:
                        quest_id = i
                        compare = temp_val
            return [diff_label,quest_id]
        else:
            compare = 0
            quest_id = -1
            for i in range(data_matrix.shape[0]):
                if mask_vector[i] == 0:
                    temp_val = np.sum(np.abs(np.multiply((data_matrix[i,:] - know_point),(know_point))))
                    # updating compare value and keep record of id
                    if temp_val > compare:
                        quest_id = i
                        compare = temp_val
            return [diff_label,quest_id]
        
                
                
                
    def _update_mask(self,last_problem_id ,answer):
        """ updating mask matrix
            last_problem_id : last problem id = [A,B] (A :difficulty, B : id)
            return knowledg point of current problem
            """
        A = last_problem_id[0]
        B = last_problem_id[1]
        # if correctly answered update both question mask and knowledge mask
        # otherwise only update question mask
        if answer == 1:
            
            if A == 0:
                know_point = self.quest_A[B,:]
                self.Kmask[np.where(know_point ==1)] = 1
                self.qmask_A[B] = 1
            elif A == 1:
                know_point = self.quest_B[B,:]
                self.Kmask[np.where(know_point ==1)] = 1
                self.qmask_B[B] = 1
            elif A == 2:
                know_point = self.quest_C[B,:]
                self.Kmask[np.where(know_point ==1)] = 1
                self.qmask_C[B] = 1
            else :
                know_point = self.quest_D[B,:]
                self.Kmask[np.where(know_point ==1)] = 1
                self.qmask_D[B] = 1
        else:
            if A == 0:
                self.qmask_A[B] = 1
            elif A == 1:
                self.qmask_B[B] = 1
            elif A == 2:
                self.qmask_C[B] = 1
            else :
                self.qmask_D[B] = 1


    def _get_know_point(self,last_problem_id):
        """get knowledge point of last problem """
        A = last_problem_id[0]
        B = last_problem_id[1]
        if A == 0:
            know_point = self.quest_A[B,:]
        elif A == 1:
            know_point = self.quest_B[B,:]
        elif A == 2:
            know_point = self.quest_C[B,:]
        else:
            know_point = self.quest_D[B,:]
        return know_point
    
    
    def get_know_mask(self):
        """get knowledge mask """
        return self.Kmask




if __name__ == '__main__':

    database = question_search(N_seq = np.array([1000,1000,1000,1000]),K = 30,beta_seq= [4,3,2.5,2])
    database.search_problem(2,[1,0],0)



