import data_load, hw4, importlib
import numpy as np

if __name__ == "__main__":
    texts, count = data_load.loadDir("data", False, False)

    importlib.reload(hw4)
    Pjoint = hw4.joint_distribution_of_word_counts(texts, "mr", "company")
    print("문제1. Joint distribution:")
    print(Pjoint)
    print("---------------------------------------------")

    P0 = hw4.marginal_distribution_of_word_counts(Pjoint, 0)
    P1 = hw4.marginal_distribution_of_word_counts(Pjoint, 1)
    print("문제2. Marginal distribution:")
    print("P0:", P0)
    print("P1:", P1)
    print("---------------------------------------------")

    Pcond = hw4.conditional_distribution_of_word_counts(Pjoint, P0)
    print("문제3. Conditional distribution:")
    print(Pcond)
    print("---------------------------------------------")

    Pathe = hw4.joint_distribution_of_word_counts(texts, "a", "the")
    Pthe = hw4.marginal_distribution_of_word_counts(Pathe, 1)

    mu_the = hw4.mean_from_distribution(Pthe)
    print("문제4-1. Mean from distribution:")
    print(mu_the)

    var_the = hw4.variance_from_distribution(Pthe)
    print("문제4-2. Variance from distribution:")
    print(var_the)

    covar_a_the = hw4.covariance_from_distribution(Pathe)
    print("문제4-3. Covariance from distribution:")
    print(covar_a_the)
    print("---------------------------------------------")

    def f(x0, x1):
        return np.log(x0 + 1) + np.log(x1 + 1)

    expected = hw4.expectation_of_a_function(Pathe, f)
    print("문제5. Expectation of a function:")
    print(expected)
