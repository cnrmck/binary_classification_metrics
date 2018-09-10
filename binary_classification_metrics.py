import doctest
import copy

"""
the functions on this page were sourced from
https://en.wikipedia.org/wiki/Template:DiagnosticTesting_Diagram
and other relevant wikipedia pages

"""

#---------------------------------------------------------------

# Helper functions

def compare(fn, list1, list2, padding=8):
    """
    a utility function intended to be used as a wrapper that simply prints
    the two lists before calling the relevant function

    the padding and copy stuff is for text alignment in ipython
    copy.copy ensures the ipython namespace isn't trampled by fix_list_lengths()

    if not using ipython, don't worry about this, it will work fine without
    """
    print(" "*padding, list1)
    print(" "*padding, list2)

    list1 = copy.copy(list1)
    list2 = copy.copy(list2)

    return fn(list1, list2)

def fix_list_lengths(list1, list2, alert_if_same = False):
    """
    This function makes len(list1) == len(list2) -> True
    by adding 0s to the end of the shorter list
    (0s indicate nothing was detected)

    the list to be modified is copied before modification
    to preserve the integrity of the source data

    >>> fix_list_lengths([0,0,0,0,0], [0])
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])

    >>> fix_list_lengths([0], [0,0,0,0,0])
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])

    >>> fix_list_lengths([1], [1,1,1,1,1])
    ([1, 0, 0, 0, 0], [1, 1, 1, 1, 1])

    >>> fix_list_lengths([0, 1], [0,0,0,0,1])
    ([0, 1, 0, 0, 0], [0, 0, 0, 0, 1])

    >>> fix_list_lengths([1], [0], alert_if_same = True)
    The lists are already the same length
    ([1], [0])
    """
    if len(list1) < len(list2):
        list1 = copy.copy(list1)
        for _ in range(len(list2)-len(list1)):
            list1.append(0)

    elif len(list1) > len(list2):
        list2 = copy.copy(list2)
        for _ in range(len(list1)-len(list2)):
            list2.append(0)

    elif alert_if_same == True:
        print("The lists are already the same length")

    return list1, list2

#---------------------------------------------------------------

def safe_print(name, fn, *args, extra = "", zerodevmsg = ""):
    """
    This function tries to print a number, if that fails it doesn't stop the program
    """
    try:
        print("{} ({:.2f}) {}".format(name, fn(*args), extra))
    except ZeroDivisionError as e:
        if zerodevmsg is not "":
            print("{} cannot be printed: {}".format(name, zerodevmsg))
        else:
            print("{} cannot be printed: {}".format(name, e))
    except ValueError as e:
        print("{} cannot be printed: {}".format(name, e))

#---------------------------------------------------------------

# Core binary classification functions

def true_positives(ground_truth, predicted):
    """
    This function returns the true positives as a list
    (also called the 'power')
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a==1 and m==1 else 0 for a, m in zip(ground_truth, predicted)]

tps = true_positives


def false_negatives(ground_truth, predicted):
    """
    This function returns the false negatives as a list
    (also called a 'Type 2 error')
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a==1 and m == 0 else 0 for a, m in zip(ground_truth, predicted)]

fns = false_negatives


def false_positives(ground_truth, predicted):
    """
    This function returns the false positives as a list
    (also called a 'Type 1 error')
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a == 0 and m == 1 else 0 for a, m in zip(ground_truth, predicted)]

fps = false_positives


def true_negatives(ground_truth, predicted):
    """
    This function returns the true negatives as a list
    (also called "yeah, that was definitely nothing")
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a==0 and m == 0 else 0 for a, m in zip(ground_truth, predicted)]

tns = true_negatives

# the following are the same as the above, but return an integer (not a list)

def true_positive(ground_truth, predicted):
    """
    This function measures the true positives as a value
    (also called the 'power')
    """
    return sum(true_positives(ground_truth, predicted))

tp = true_positive


def true_negative(ground_truth, predicted):
    """
    This function measures the true negatives as a value
    (also called "yeah, that was definitely nothing")
    """
    return sum(true_negatives(ground_truth, predicted))

tn = true_negative


def false_positive(ground_truth, predicted):
    """
    This function measures the false positives as a value
    (also called a 'Type 1 error')
    """
    return sum(false_positives(ground_truth, predicted))

fp = false_positive


def false_negative(ground_truth, predicted):
    """
    This function measures the false negatives as a value
    (also called a 'Type 2 error')
    """
    return sum(false_negatives(ground_truth, predicted))

fn = false_negative

# ---------------------------------------------------------------

# Measurement functions
# These are general functions that tell us about our data and results

def prevalence(ground_truth):
    """
    This function tells us what percentage of the dataset has a True (i.e. 1) state
    """
    return sum(ground_truth) / len(ground_truth)

def accuracy(ground_truth, predicted):
    """
    This function measures the accuracy rate
    """
    n_of_correct_classifications = (true_positive(ground_truth, predicted) +
    true_negative(ground_truth, predicted))

    return n_of_correct_classifications / len(ground_truth)

def error(ground_truth, predicted):
    """
    This function measures the error rate
    """
    n_of_incorrect_classifications = (false_positive(ground_truth, predicted) +
    false_negative(ground_truth, predicted))

    return n_of_incorrect_classifications / len(ground_truth)

# These functions give us rates of performance (ratios rather than values)
# This allows us to compare against other data sets of different sizes

def true_positive_rate(ground_truth, predicted):
    """
    This function measures the true positive rate
    (also called "recall", "sensitivity", or "probability of detection")
    """
    return true_positive(ground_truth, predicted) / sum(ground_truth)

tpr = true_positive_rate


def true_negative_rate(ground_truth, predicted):
    """
    This function measures the true negative rate
    (also called "specificity" or "ability to not see things that aren't there")

    note that the values of 'ground_truth' are inverted to compare against all negatives
    could also write as: (len(ground_truth) - sum(ground_truth))
    """
    return true_negative(ground_truth, predicted) / sum([1 if a==0 else 0 for a in ground_truth])

tnr = true_negative_rate


def false_negative_rate(ground_truth, predicted):
    """
    This function measures the false negative rate
    (also called "miss rate")
    """
    return false_negative(ground_truth, predicted) / sum(ground_truth)

fnr = false_negative_rate


def false_positive_rate(ground_truth, predicted):
    """
    This function measures the false positive rate
    (also called "fall-out" or "rate of false alarm")

    note that the values of ground_truth are inverted to compare against all negatives
    could also write as: (len(ground_truth) - sum(ground_truth))
    """
    return false_positive(ground_truth, predicted) / sum([1 if a==0 else 0 for a in ground_truth])

fpr = false_positive_rate

# These allow us to measure the predictor's tendancy toward accuracy (or not)
# In all four cases, 1 is perfect

def positive_predictive_value(ground_truth, predicted):
    """
    This function measures the positive predictive value
    (also called "precision" or "thanks for removing the cyst and not my brain")

    1 is perfect and means the system only detected what it should have.
    More than 1 means it detected more than it should have. < 1 is the inverse.

    note that this number can be greater than 1, thus the word 'value'
    """
    return (true_positive(ground_truth, predicted) /
    (true_positive(ground_truth, predicted) + false_positive(ground_truth, predicted) ))

ppv = positive_predictive_value


def negative_predictive_value(ground_truth, predicted):
    """
    This function measures the negative predictive value
    (also called "that's not our son. Our son doesn't have fangs and a tail")

    1 is perfect and means the system only excluded what it should have.
    More than 1 means it excluded more than it should have. <1 is the inverse.

    note that this number can be greater than 1, thus the word 'value'
    """
    return (true_negative(ground_truth, predicted) /
    (true_negative(ground_truth, predicted) + false_negative(ground_truth, predicted) ))

npv = negative_predictive_value


def false_discovery_rate(ground_truth, predicted):
    """
    This function measures the false disecovery rate
    (also called "whoops, sorry for the radiation and chemotherapy")
    """
    return (false_positive(ground_truth, predicted) /
    (true_positive(ground_truth, predicted) + false_positive(ground_truth, predicted) ))

fdr = false_discovery_rate


def false_omission_rate(ground_truth, predicted):
    """
    This function measures the false omission rate
    (also called "I'm sure that fluffy bump we hit wasn't a bunny")
    """
    return (false_negative(ground_truth, predicted) /
    (true_negative(ground_truth, predicted) + false_negative(ground_truth, predicted) ))

FOR = false_omission_rate
foR = false_omission_rate

# These functions measure the bais of the predictor

def positive_likelihood_ratio(ground_truth, predicted):
    """
    This function measures the positive likelihood ratio
    (also called " likelihood ratio for positive results")

    sensitivity / (1 - specificity)

    The bigger this number the better.
    """
    return (true_positive_rate(ground_truth, predicted) /
    (1 - true_negative_rate(ground_truth, predicted) ))

plr = positive_likelihood_ratio


def negative_likelihood_ratio(ground_truth, predicted):
    """
    This function measures the negative likelihood ratio
    (also called " likelihood ratio for negative results")

    (1 - sensitivity) / specificity

    The smaller this number the better.
    """
    return ((1 - true_positive_rate(ground_truth, predicted)) /
    true_negative_rate(ground_truth, predicted) )

nlr = negative_likelihood_ratio


def diagnostic_odds_ratio(ground_truth, predicted):
    """
    This function measures the diagnostic odds ratio
    (also called "detection_tendancy")

    Greater than 1 means the test is discriminating correctly.
    """
    return (positive_likelihood_ratio(ground_truth, predicted) /
    negative_likelihood_ratio(ground_truth, predicted) )

dor = diagnostic_odds_ratio

# These functions I made up

def positive_unlikelihood_ratio(ground_truth, predicted):
    """
    This function measures the positive unlikelihood ratio
    (also called "")
    """
    return (false_positive_rate(ground_truth, predicted) /
    true_positive_rate(ground_truth, predicted) )

def negative_unlikelihood_ratio(ground_truth, predicted):
    """
    This function measures the negative unlikelihood ratio
    (also called "")
    """
    return (false_negative_rate(ground_truth, predicted) /
    true_negative_rate(ground_truth, predicted) )

def undiagnostic_odds_ratio(ground_truth, predicted):
    """
    This function measures the undiagnostic odds ratio
    (also called "")
    """
    return (negative_likelihood_ratio(ground_truth, predicted) /
    positive_likelihood_ratio(ground_truth, predicted) )

def diagnostic_disodds_ratio(ground_truth, predicted):
    """
    This function measures the undiagnostic odds ratio
    (also called "")
    """
    return (positive_unlikelihood_ratio(ground_truth, predicted) /
    negative_unlikelihood_ratio(ground_truth, predicted) )

def undiagnostic_disodds_ratio(ground_truth, predicted):
    """
    This function measures the undiagnostic disodds ratio
    (also called "")
    """
    return (negative_unlikelihood_ratio(ground_truth, predicted) /
    positive_unlikelihood_ratio(ground_truth, predicted) )

# These are F score functions

def f1_score(ground_truth, predicted):
    """
    This function measures the f1 score
    (also called "balanced f score")
    """
    return (2 / ((1/true_positive_rate(ground_truth, predicted)) +
    (1/positive_predictive_value(ground_truth, predicted))) )

def f_score(ground_truth, predicted, beta=.5):
    """
    This function returns the f beta score
    (also called "unbalanced effing score")

    https://en.wikipedia.org/wiki/F1_score
    beta measures how much the true_positive_rate is weighted by
    increasing and decreasing the influence of false negatives

    high beta means true_positive_rate is more important to you than the
    false_negative_rate

    denominator broken up into 3 parts for ease of reading
    """
    numer    = (1+beta**2) * true_positive_rate(ground_truth, predicted)

    denom1 = ((1+beta**2) * true_positive_rate(ground_truth, predicted))
    denom2 = ((beta**2)*false_negative_rate(ground_truth, predicted))
    denom3 = false_positive_rate(ground_truth, predicted)
    denoms = [denom1, denom2, denom3]
    return numer / sum([denom for denom in denoms if denom is not None])

# ---------------------------------------------------------------

def run(ground_truth, prediction):
    """
    This function prints a selection of the most common binary classification
    measurements

    safe_print is a function that prevents against ZeroDivisionErrors
    """

    print("Grond Truth: ")
    safe_print("prevalence", prevalence, ground_truth)
    print(ground_truth)

    print("Prediction: ")
    safe_print("prevalence", prevalence, prediction)
    print(prediction)

    print("")
    print("-"*30, "\n")

    safe_print("true positive rate", tpr, ground_truth, prediction)
    safe_print("false positive rate", fpr, ground_truth, prediction)

    safe_print("\npositive predictive value", ppv, ground_truth, prediction)

    print("")
    print("-"*30, "\n")

    safe_print("true negative rate", tnr, ground_truth, prediction)
    safe_print("false negative rate", fnr, ground_truth, prediction)

    safe_print("\nnegative predictive value", npv, ground_truth, prediction)

    print("")
    print("-"*30, "\n")

    safe_print("positive likelihood ratio", plr, ground_truth, prediction, extra="(bigger is better)")
    safe_print("negative likelihood ratio", nlr, ground_truth, prediction, extra="(smaller is better)")

    safe_print("\ndiagnostic odds ratio", dor, ground_truth, prediction, zerodevmsg="if accuracy is not perfect this is undefined")

    safe_print("\naccuracy", accuracy, ground_truth, prediction)

    safe_print("\nf1 score", f1_score, ground_truth, prediction)

    print("")
    print("="*30, "\n")


# ---------------------------------------------------------------

def main():
    """
    This function contains a handful of example detection lists that can
    be used to explore how the various metrics work
    """

    # the ground truth of the data set
    ground_truth = [1,1,0,1,1,0,1,1,1,1,1,0,0]

    # perfect prediction
    prediction0 = copy.copy(ground_truth)

    # prefect true positive, high false positive
    prediction1 = [1,1,0,1,1,0,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1]

    # perfect false negative (0), 0 true negative
    # note how trivial it is to achieve this perfect false negative score
    prediction2 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    # perfect false positive (0) / true negative
    # note how trivial it is to achieve this perfect false positive score
    prediction3 = [0]

    prediction4 = [1,0,1,0,1,0,1,0,1,0,1,0,1]
    prediction5 = [0,1,0,1,0,1,0,1,0,1,0,1,0]

    # a prediction just two off from perfect (in both directions)
    prediction6 = [1,1,0,1,1,0,1,1,1,0,1,0,1]


    predictions = []
    predictions.append(prediction0)
    predictions.append(prediction1)
    predictions.append(prediction2)
    predictions.append(prediction3)
    predictions.append(prediction4)
    predictions.append(prediction5)
    predictions.append(prediction6)

    for i, prediction in enumerate(predictions):
        print("Result {}".format(i))
        run(ground_truth, prediction)



if __name__ == "__main__":
    doctest.testmod()
    main()
