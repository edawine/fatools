
import pandas

#
#
# Multiplicity of Infection (MoI) calculation
# ===========================================
#
# histogram of sample with MoI:
#       MoI     Freq(sample)
#       1       10
#       2       15
#       3       8
#
# histogram of marker with MoI:
#       No of marker with allele > 1   Freq (sample)
#       1                               30
#       2                               5
#
#

def summarize_moi(analytical_sets):

    moi_sets = {}

    for analytical_set in analytical_sets:
        moi_sets[analytical_set.label] = calculate_moi(analytical_set.allele_df)

    # because of the non-normality of the dataset, we will just have to use
    # rank-based (parametric/catagorical) statistical test

    return moi_sets


class MoISummary(object):

    def __init__(self):
        pass


def calculate_moi(allele_df):
    # given allele_df, return (moi_table)

    moi = MoISummary()

    am = allele_df.allele_multiplicity
    sm = allele_df.sample_multiplicity

    am_filter = am.applymap(lambda x: 1 if x > 1 else 0)
    am_filter_dist = am_filter.sum(1)

    moi.sample_dist = pandas.concat([sm, am_filter_dist], axis=1)
    moi.sample_dist.columns = ('MOI', 'MLOCI')
    moi.group = sm.groupby(sm)
    moi.histogram = moi.group.count()
    moi.alleles = am_filter_dist.groupby(am_filter_dist).count()
    moi.mean = sm.mean()
    moi.std = sm.std()

    return moi

