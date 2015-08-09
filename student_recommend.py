import numpy as np
from hmmlearn.hmm import MultinomialHMM
import matplotlib.pyplot as plt
import copy
# import generate_exercise as gen_ex


class HMMparam:
    def __init__(self):
        self.Trans = np.array([[0.8, 0.2, 0, 0],
                              [0.1, 0.8, 0.1, 0],
                              [0, 0.1, 0.8, 0.1],
                              [0, 0, 0.2, 0.8]])

        self.Emiss_sub = 0.25 * np.ones([4, 4])

        self.Emiss_obj_1 = np.array([[0.5, 0.7, 0.8, 0.9],
                                     [0.3, 0.65, 0.7, 0.85],
                                     [0.2, 0.5, 0.6, 0.8],
                                     [0.1, 0.3, 0.5, 0.6]])
        self.Emiss_obj_2 = 1 - self.Emiss_obj_1
        self.Emiss = np.zeros([2, 4, 4])
        self.Emiss[0, :, :] = self.Emiss_obj_1.T * self.Emiss_sub
        self.Emiss[1, :, :] = self.Emiss_obj_2.T * self.Emiss_sub
        self.Emiss = self.Emiss.reshape((8, 4))

        self.Startprob = np.array([0.167, 0.333,
                                   0.333, 0.167])

        self.T1 = 0.3
        self.T2 = 0.3
        self.TPass = 0.6
        self.past_num = 3


class User:
    def __init__(self, param=HMMparam()):
        # Init HMM model
        self.Startprob = param.Startprob
        self.HMM_model = MultinomialHMM(n_components=4,
                                        startprob=self.Startprob,
                                        tramsmat=param.Trans,
                                        algorithm="map")
        self.HMM_model._set_emissionprob(param.Emiss.T)

        # State parameters
        self.seq = []
        self.post_level = []  # record level after recommended
        self.know_cover = []  # record covered knowledges

        self.current_state = None
        self.last_problem_id = None
        self.new_observe = None
        self.knowledge = None
        self.counter = 0  # question counter

        # exercise difficulty simulation
        self.Diff_level = np.array([[0.2, 0.8], [0.5, 0.5],
                                    [0.6, 0.4], [0.8, 0.2]])

    def sel_first_question(self):
        """ Select the first question"""
        self.post_level.append(self.Startprob)
        self.current_state = np.argmax(self.Startprob)
        self.last_problem_id = [self.current_state, 0]

        self.new_observe = self.random_observation(self.Diff_level,
                                                   np.argmax(self.Startprob))
        self.seq.append(self.new_observe)
        self.last_problem_id = \
                        self.data_base.search_problem(self.current_state,
                                                      self.last_problem_id,
                                                      answer=1 -
                                                      int(self.new_observe/4))
        self.knowledge = np.double(self.data_base.get_know_mask())
        self.know_cover.append(np.sum(self.knowledge)/self.knowledge.size)

    def get_next_question(self):
        """ Calculate next question to recommend """
        if (self.counter >= 60):
            return None

        logprob, posterior = self.HMM_model.score_samples(self.seq)
        # estimating current state
        last_post = posterior[posterior.shape[0]-1]
        # appending current posterior estimation
        self.post_level.append(last_post)
        # hidden state based level change
        self.current_state = self.level_change(last_post, self.current_state,
                                               self.T1, self.T2, self.Tpass)
        # rule based level change
        # current_state = current_state + rule_based_level_change(seq,past_num)

        if self.current_state != -1 and self.last_problem_id[1] != -1:
            # boven: replace with real performance
            new_observe = self.random_observation(self.Diff_level,
                                                  self.current_state)
            # randomly generate answer for next question
            self.seq.append(new_observe)
            self.last_problem_id = self.data_base.search_problem(
                                                        self.current_state,
                                                        self.last_problem_id,
                                                        answer=1 -
                                                        int(new_observe/5))
            self.knowledge = np.double(self.data_base.get_know_mask())
            self.know_cover.append(np.sum(self.knowledge)/self.knowledge.size)
        else:
            return None  # all the knowledge are covered

    def random_observation(self, Diff_level, level):
        """ randomly generate observation by using beta distribution modeling
            student correctness
            Diff_level : beta distribution parameter for different level 4 by
            2 matrix
            level: current level
            return : observation

            """
        if np.random.beta(Diff_level[level, 0],
                          Diff_level[level, 1]) >= 0.5:
            return level
        else:
            return level + 4

    def level_change(state_estimate, current_state, T1, T2, Tpass):
        """ probability based to decide when to increase/decrease student level
            state_estimate : hmm state estimation for current time
            current_state : t-1 state (deterministic)
            T1 : increase level threshold
            T2 : decrease level threshold
            Tpass: pass threshold
            """
        if current_state != 0:
            if current_state != 3:
                if np.sum(state_estimate[0: current_state + 1]) /\
                        (current_state + 1) >= T1:
                    return current_state - 1
                elif np.sum(state_estimate[current_state:4]) /\
                        (4-current_state) >= T2:
                    return current_state + 1
                else:
                    return current_state

            elif state_estimate[3] <= T1:
                return 2

            else:
                return 3

        elif state_estimate[0] >= Tpass:
            return - 1

        elif np.sum(state_estimate[1:4])/3 >= T2:
            return 1

        else:
            return 0

    def rule_based_level_change(seq, past_num=3):
        """  rule based to decide when to increase/ decrease student level
        return_num = -1: increase
            return_num = 0: hold
            return_num = 1: decrease
            """
        new_seq = copy.copy(seq)
        # get past values
        A = new_seq.pop()
        return_num = 0

        for i in range(past_num-1):
            try:
                if A == new_seq.pop():
                    if A >= 4 and A != 7:
                        return_num = 1
                    elif A >= 4 and A == 7:
                        return_num = 0
                    else:
                        return_num = -1
                else:
                    return 0

            except IndexError:
                return_num = 0
                break

        return return_num

    def plot_seq(seq, post_level, know_cover):
        """Plotting posterior probability and sequence """
        array_seq = np.array(seq)
        # array_post_level = np.array(post_level)
        know_seq = np.array(know_cover)
        plt.subplot(3, 1, 1)
        # plotting exercise sequence
        for i in range(len(seq)):
            if array_seq[i] >= 4:
                plt.plot(i, array_seq[i] - 4, 'rs')
            else:
                plt.plot(i, array_seq[i], 'gd')

        plt.ylim(0, 3)

        plt.subplot(3, 1, 2)
        # lg1= plt.plot(array_post_level[:,0],'r-',label ='A')
        # lg2=plt.plot(array_post_level[:,1],'g-',label ='B')
        # lg3=plt.plot(array_post_level[:,2],'b-',label ='C')
        # lg4=plt.plot(array_post_level[:,3],'k-',label ='D')

        plt.legend()
        plt.ylim(0, 1)
        plt.subplot(3, 1, 3)
        plt.plot(know_seq)
        plt.show()


if __name__ == '__main__':
    param = HMMparam()
    user = User()
    user.sel_first_question()

    for i in range(60):
        user.get_next_question()

    user.plot_seq(user.seq, user.post_level, user.know_cover)
