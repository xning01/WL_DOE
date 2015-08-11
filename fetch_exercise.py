import numpy as np
import EtlAdd_api
# from hmmlearn.hmm import MultinomialHMM,GMMHMM
# import scipy.io as scipy_io
# from sklearn.metrics.cluster import adjusted_mutual_info_score
# import matplotlib.pyplot as plt
# import copy


# def generate_exercise(N=1000, K=30, beta=2):
""" N :  numbers of questions
    K  : knowledge point number
    return : binary matrix N by K
"""
"""
    matrix = np.zeros([N, K])
    for i in range(N):
        peu_K = int(np.random.exponential(beta))
        while peu_K >= K or peu_K == 0:
            peu_K = int(np.random.exponential(beta))
        matrix[i, np.unique(np.random.random_integers(0, K-1, peu_K))] = 1
    return matrix
"""


class question_search():
    def __init__(self, conf="./config.ini"):
        """  quest_A/B/C/D : simulated dataset
             Kmask : keep record whether one knowledge point has been covered
             qmask_A/B/C/D : keep record whether one problem has been answered
        """
        # self.qID = []  # list of questions by id
        self.knowID = []  # dict searching index of a knowledge point
        self.quest_diff_id = {}  # dict recording id of questions by difficulty

        self.quest_A = None
        self.quest_B = None
        self.quest_C = None
        self.quest_D = None
        self.qmask_A = None
        self.qmask_B = None
        self.qmask_C = None
        self.qmask_D = None
        self.Kmask = None

        self.fetch_exercise(conf)

    def fetch_exercise(self, conf):
        db = EtlAdd_api.etl_add_api(conf)

        self.quest_diff_id[1] = db.get_ques_by_level(1)
        self.quest_diff_id[2] = db.get_ques_by_level(2)
        self.quest_diff_id[3] = db.get_ques_by_level(3)
        self.quest_diff_id[4] = db.get_ques_by_level(4)

        knowIDset = set()
        qIDset = set()

        # get number of exercise, knowledge
        for level in range(1, 5):
            for qID in self.quest_diff_id[level]:
                qIDset.add(qID)
                orig_know_cover = db.get_subject_by_ques(qID)

                for kID in orig_know_cover:
                    knowIDset.add(kID)

        # self.qID = list(qIDset)
        # self.qID.sort()
        self.knowID = list(knowIDset)
        self.knowID.sort()

        # construct full matrix (questionID v.s. knowlegepoint)
        self.quest_A = self._gen_qMask_mat(db, self.quest_diff_id[1],
                                           self.knowID)
        self.quest_B = self._gen_qMask_mat(db, self.quest_diff_id[2],
                                           self.knowID)
        self.quest_C = self._gen_qMask_mat(db, self.quest_diff_id[3],
                                           self.knowID)
        self.quest_D = self._gen_qMask_mat(db, self.quest_diff_id[4],
                                           self.knowID)

        self.qmask_A = np.zeros(len(self.quest_diff_id[1]))
        self.qmask_B = np.zeros(len(self.quest_diff_id[2]))
        self.qmask_C = np.zeros(len(self.quest_diff_id[3]))
        self.qmask_D = np.zeros(len(self.quest_diff_id[4]))

        self.Kmask = np.zeros(len(self.knowID))
        db.disconnect()

        print "Exercise Input Complete"

    def _gen_qMask_mat(self, db, quest_byDiff, knowList):
        qNo = len(quest_byDiff)
        kNo = len(knowList)
        quest = np.zeros([qNo, kNo])

        for qIDidx in range(qNo):
            qID = quest_byDiff[qIDidx]
            for knowID in db.get_subject_by_ques(qID):
                knowIDidx = knowList.index(knowID)
                quest[qIDidx][knowIDidx] = 1
        return quest

    # given difficulty + performance =>  knowledge point update
    # provide problems for recommendation
    def search_problem(self, diff_label=0,
                       last_problem_id=[0, 0],
                       ans_correct=0):
        """ diff_label : search difficulty
            last_problem_id : last problem id = [A,B] (A :difficulty, B : id)
            answer : correct or wrong 0/1 """
        # if last problem is correctly answered update knowledge mask
        if ans_correct == 1:
            know_point = self._update_mask(last_problem_id, ans_correct)

        if diff_label == 0:
            data_matrix = self.quest_A
            mask_vector = self.qmask_A
        elif diff_label == 1:
            data_matrix = self.quest_B
            mask_vector = self.qmask_B
        elif diff_label == 2:
            data_matrix = self.quest_C
            mask_vector = self.qmask_C
        else:
            data_matrix = self.quest_D
            mask_vector = self.qmask_D

        # get knowledge point
        know_point = self._get_know_point(last_problem_id)

        # if last problem is correctly answered search for question
        if ans_correct == 1:
            compare = 0
            quest_id = -1
            for i in range(data_matrix.shape[0]):
                if mask_vector[i] == 0:
                    temp_val = np.multiply(data_matrix[i, :] - know_point,
                                           1-know_point)
                    temp_val = np.sum(np.abs(temp_val))
                    # updating compare value and keep record of id
                    if temp_val > compare:
                        quest_id = i
                        compare = temp_val
            return [diff_label, quest_id]
        else:
            compare = 0
            quest_id = -1
            for i in range(data_matrix.shape[0]):
                if mask_vector[i] == 0:
                    temp_val = np.multiply(data_matrix[i, :] - know_point,
                                           know_point)
                    temp_val = np.sum(np.abs(temp_val))
                    # updating compare value and keep record of id
                    if temp_val > compare:
                        quest_id = i
                        compare = temp_val
            return [diff_label, quest_id]

    def get_true_questID(self, diff, diff_qID):
        return self.quest_diff_id[diff][diff_qID]

    def _update_mask(self, last_problem_id, ans_correct):
        """ updating mask matrix
            last_problem_id : last problem id = [A,B] (A :difficulty, B : id)
            return knowledg point of current problem
            """
        Q_diff = last_problem_id[0]
        Q_id = last_problem_id[1]
        # if correctly answered update both question mask and knowledge mask
        # otherwise only update question mask
        if Q_diff == 0:
            if ans_correct == 1:
                know_point = self.quest_A[Q_id, :]
                self.Kmask[np.where(know_point == 1)] = 1
            self.qmask_A[Q_id] = 1

        elif Q_diff == 1:
            if ans_correct == 1:
                know_point = self.quest_B[Q_id, :]
                self.Kmask[np.where(know_point == 1)] = 1
            self.qmask_B[Q_id] = 1

        elif Q_diff == 2:
            if ans_correct == 1:
                know_point = self.quest_C[Q_id, :]
                self.Kmask[np.where(know_point == 1)] = 1
            self.qmask_C[Q_id] = 1
        else:
            if ans_correct == 1:
                know_point = self.quest_D[Q_id, :]
                self.Kmask[np.where(know_point == 1)] = 1
            self.qmask_D[Q_id] = 1

    def _get_know_point(self, last_problem_id):
        """get knowledge point of last problem """
        Q_diff = last_problem_id[0]
        Q_id = last_problem_id[1]
        if Q_diff == 0:
            know_point = self.quest_A[Q_id, :]
        elif Q_diff == 1:
            know_point = self.quest_B[Q_id, :]
        elif Q_diff == 2:
            know_point = self.quest_C[Q_id, :]
        else:
            know_point = self.quest_D[Q_id, :]
        return know_point

    def get_know_mask(self):
        """get knowledge mask """
        return self.Kmask
