
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

def normality_check (data):
    """
    Checks if normality is satisfied
    Parameters
    ----------
    data

    Returns
    -------

    """
    test_stat, pvalue = shapiro(data.dropna())
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

    if pvalue < 0.05:
        normality = False
        print('Normality is NOT satisfied')
    else:
        normality = True
        print('Normality is satisfied')
    return normality


def homogeneity_check(control_data, test_data):
    """

    Parameters
    ----------
    control_data
    test_data

    Returns
    -------

    """
    test_stat, pvalue = levene(control_data.dropna(),
                               test_data.dropna())
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

    if pvalue < 0.05:
        homogeneity = False
        print('Homogeneity is NOT satisfied')
    else:
        homogeneity = True
        print('Homogeneity is satisfied')
    return homogeneity


def ab_testing_for_means(control_data, test_data):
    cont_norm = normality_check(control_data)
    test_norm = normality_check(test_data)
    homogeneity = homogeneity_check(control_data, test_data)

    if (cont_norm is True) and (test_norm is True) and (homogeneity is True):
        test_stat, pvalue = ttest_ind(control_data, test_data,
                                      equal_var=True)
        test_name = 'Two Sample T-test'
    elif (cont_norm is False) or (test_norm is False) or (homogeneity is False):
        test_stat, pvalue = mannwhitneyu(control_data,
                                         test_data)
        test_name = 'Man-Whitneyyu'
    elif (cont_norm is True) or (test_norm is True) or (homogeneity is False):
        test_stat, pvalue = ttest_ind(control_data, test_data,
                                      equal_var=False)
        test_name = 'Welch test'

    if pvalue < 0.05:
        print('Test name = %s is applied H0 is REJECTED, there is a significant difference between the means '
                  'Test Stat = %.4f, p-value = %.4f' % (test_name, test_stat, pvalue))
    else:
        print('Test name = %s is applied H0 is NOT REJECTED there is no significant difference between the means '
              'Test Stat = %.4f, p-value = %.4f' % (test_name, test_stat, pvalue))

def ab_testing_for_ratios(success_data, observation_data):
    test_stat, pvalue = proportions_ztest(count=success_data,
                                          nobs=observation_data)

    if pvalue < 0.05:
        print('H0 is REJECTED, there is a significant difference between the ratios '
              'Test Stat = %.4f, p-value = %.4f' % (test_name, test_stat, pvalue))
    else:
        print('H0 is NOT REJECTED there is no significant difference between the ratios '
                'Test Stat = %.4f, p-value = %.4f' % (test_name, test_stat, pvalue))


if __name__ == "__main__":
    control_group = pd.read_excel("AB Testing/ab_testing.xlsx", sheet_name = "Control Group")
    test_group = pd.read_excel("AB Testing/ab_testing.xlsx", sheet_name = "Test Group")

    ###########AB TESTING (Two Sample Mean)###############
    # Defining hypothesis test
    # H0: M1 = M2 There is no significant difference between control group and test group
    # H1: M1 != M2 There is a significant difference

    ab_testing_for_means(control_group["Purchase"], test_group["Purchase"])




