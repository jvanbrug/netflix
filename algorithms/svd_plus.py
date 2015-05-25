__author__ = 'quinnosha'
import numpy as np

from algorithms.svd import SVD
from utils.c_interface import c_run_svd_plus_epoch
from utils.constants import SVD_FEATURE_VALUE_INITIAL
from utils.constants import MOVIE_INDEX, USER_INDEX, K_NEIGHBORS

class SVD_Plus(SVD):

    def __init__(self, num_features=3, feature_initial=SVD_FEATURE_VALUE_INITIAL,
            offset_learn_rate=0.007, feature_learn_rate=0.007, feedback_learn_rate=0.001,
            offset_k_factor=0.005, feature_k_factor=0.015, feedback_k_factor=0.015):
        self.num_features = num_features
        self.feature_initial = feature_initial
        self.offset_learn_rate = offset_learn_rate
        self.feature_learn_rate = feature_learn_rate
        self.feedback_learn_rate = feedback_learn_rate
        self.offset_k_factor = offset_k_factor
        self.feature_k_factor = feature_k_factor
        self.feedback_k_factor = feedback_k_factor
        self.users = np.array([])
        self.movies = np.array([])
        self.implicit_preference = np.array([])
        self.explicit_feedback = np.array([])
        self.implicit_feedback = np.array([])
        self.train_points = np.array([])
        self.stats = None
        self.max_user = 0
        self.max_movie = 0
        self.debug = False
        self.run_c = False


    def set_train_points(self, train_points):
        self.train_points = train_points


    def calculate_prediction(self, user, movie):
        return self.stats.get_baseline(user=user, movie=movie) + np.dot(
            self.users[user, :], self.movies[movie, :])

    def update_epoch_in_c(self, feature):
        c_run_svd_plus_epoch(train_points=self.train_points, users=self.users, user_offsets=self.stats.user_offsets,
                             user_rating_count=self.stats.user_rating_count, movies=self.movies,
                             movie_averages=self.stats.movie_averages, movie_rating_count=self.stats.movie_rating_count,
                             similarity_matrix_rated=self.stats.similarity_matrix_rated,
                             num_neighbors=K_NEIGHBORS, nearest_neighbors_matrix=self.stats.similarity_matrix_sorted,
                             implicit_preference=self.implicit_preference, explicit_feedback=self.explicit_feedback,
                             implicit_feedback=self.implicit_feedback, num_features=self.num_features,
                             offset_learn_rate=self.offset_learn_rate, feature_learn_rate=self.feature_learn_rate,
                             feedback_learn_rate=self.feedback_learn_rate, offset_k_factor=self.offset_k_factor,
                             feature_k_factor=self.feature_k_factor, feedback_k_factor=self.feedback_k_factor)