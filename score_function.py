import numpy as np
import scipy as sp

from scipy.stats import norm
import matplotlib.pyplot as plt
import pdb
def init_stat (ans_vector):
    """ input: numpy vector
        output:
        mean
        mean_square
        variance
        n_num
        """
    
    return np.mean(ans_vector), np.mean(np.multiply(ans_vector,ans_vector)), np.var(ans_vector), ans_vector.size



def update_stat(old_mean,old_mean_square,n_num, ans_vector):

    """ Input:
        old_mean(scaler) : 1/n * sum(x)
        old_mean_square(scaler): 1/n* sum(x^2)
        n_num(scaler) : n
        ans_vector(numpy vector): vector of new person's answer(i.e. time for questions for one particular person)
        
        equation in (https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance)
        
        Output:
        new_mean
        new_mean_square
        new_variance
        
        """
    
    n_new = ans_vector.size
    n_all = n_new + n_num
    new_mean = (old_mean*n_num+ np.mean(ans_vector)* n_new)/(n_num+n_new )
    
    new_mean_square = (old_mean_square* n_num + np.sum(np.multiply(ans_vector,ans_vector))) /n_all
    new_variance= (new_mean_square*n_all - new_mean*new_mean*n_all)/(n_all-1)

    return new_mean, new_mean_square,new_variance,n_all


def cal_score( mean,variance,ans_vector):

    """mean: scaler
        variance: scaler
        ans_vector: numpy vector"""
    tune_param = 10

    return norm.cdf(np.mean(ans_vector),mean,variance/tune_param)


def none_linear_score_mapping(score):
    return []


if __name__ == '__main__':
    # test code
#    # draw initial samples
#    rand_vector = np.random.normal(200,50,10000)
#    
##    plt.plot(rand_vector,'rs')
##    plt.show()
#    # compute statistics
#    mean_, mean_square_,var_,n_ = init_stat(rand_vector)
#    # draw new_samples
#    new_person = 100
#    
#    score = np.zeros(new_person)
#    true_score = np.zeros(new_person)
#    updated_mean = np.zeros(new_person+1)
#    updated_mean[0] = mean_
#    for i in range(new_person):
#        #pdb.set_trace()
#        # draw person's mean variance
#        p_mean = np.random.normal(200,100,1)
#        p_var = np.random.normal(10,1,1)
#        new_rand_vec = np.random.normal(p_mean,p_var,10)
#
#        # compute score
#        score[i] = cal_score(mean_,var_,new_rand_vec)
#        true_score[i] = np.mean(new_rand_vec)
#        # update stat
#        mean_, mean_square_,var_,n_ = update_stat(mean_,mean_square_,n_, new_rand_vec)
#        updated_mean[i+1] = mean_
#    axis_list = []
#
#    for i in range(new_person):
#        axis =plt.plot(score[i],true_score[i],'rs')
##        axis_list.append(axis)
##    plt.legend(axis_list,['0','1','2','3','4'])
#    plt.show()
#    pdb.set_trace()

    """ system flow  """
    
    # 1) intialize statistics
    rand_vector = np.random.normal(200,50,10000)
    
    mean_, mean_square_,var_,n_ = init_stat(rand_vector)

    # note: mean_, mean_square_,var_,n_ should be stored at local file

    # 2) new person comes in:
    new_rand_vec = np.random.normal(200,10,10)
    # 2.1) calculate score
    # for time score#
    score = 1- cal_score(mean_,var_,new_rand_vec)
    # for accuracy score
    score = cal_score(mean_,var_,new_rand_vec)
    # 2.2)update stat
    mean_, mean_square_,var_,n_ = update_stat(mean_,mean_square_,n_, new_rand_vec)














