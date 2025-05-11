import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, f_oneway, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scikit_posthocs import posthoc_dunn

# CSV 파일 불러오기
data = pd.read_csv('상권_결측치 처리 (1).csv')

# 정규성 검정 함수
def check_normality(data, group_column, value_column):
    groups = data[group_column].unique()
    for group in groups:
        stat, p = shapiro(data[value_column][data[group_column] == group])
        if p < 0.05:
            return False
    return True

# 분산의 동질성 검정 함수
def check_homogeneity(data, group_column, value_column):
    groups = [data[value_column][data[group_column] == group] for group in data[group_column].unique()]
    stat, p = levene(*groups)
    return p >= 0.05

# 일원분산분석 (ANOVA) 함수
def perform_anova(data, group_column, value_column):
    groups = [data[value_column][data[group_column] == group] for group in data[group_column].unique()]
    stat, p = f_oneway(*groups)
    return p

# Kruskal-Wallis 검정 함수
def perform_kruskal(data, group_column, value_column):
    groups = [data[value_column][data[group_column] == group] for group in data[group_column].unique()]
    stat, p = kruskal(*groups)
    return p

# Tukey's HSD 함수
def perform_tukey_hsd(data, group_column, value_column):
    tukey = pairwise_tukeyhsd(endog=data[value_column], groups=data[group_column], alpha=0.05)
    return tukey

# Dunn's test 함수
def perform_dunn_test(data, group_column, value_column):
    return posthoc_dunn(data, val_col=value_column, group_col=group_column, p_adjust='bonferroni')

# 변수 목록
group_column = 'type'
variables = [
    'size', 'user'
]
# 'size', 'user', 'Population_woman', 'Population_man', 'under10', '10', '20', '30', '40', 
#'50', '60', '70', '80', '90', 'transit_count', 'library', 'gallery', 'perform', 
 #   'local', 'total', 'Store_count'
results = {}

for var in variables:
    normality = check_normality(data, group_column, var)
    homogeneity = check_homogeneity(data, group_column, var)
    
    if normality and homogeneity:
        p_value = perform_anova(data, group_column, var)
        if p_value < 0.05:
            tukey_result = perform_tukey_hsd(data, group_column, var)
            results[var] = {
                'test': 'ANOVA',
                'anova_p_value': p_value,
                'significant': True,
                'post_hoc': tukey_result.summary()
            }
        else:
            results[var] = {
                'test': 'ANOVA',
                'anova_p_value': p_value,
                'significant': False,
                'post_hoc': 'No significant difference'
            }
    else:
        p_value = perform_kruskal(data, group_column, var)
        if p_value < 0.05:
            dunn_result = perform_dunn_test(data, group_column, var)
            results[var] = {
                'test': 'Kruskal-Wallis',
                'kruskal_p_value': p_value,
                'significant': True,
                'post_hoc': dunn_result
            }
        else:
            results[var] = {
                'test': 'Kruskal-Wallis',
                'kruskal_p_value': p_value,
                'significant': False,
                'post_hoc': 'No significant difference'
            }

# 결과 출력 및 시각화
for var, result in results.items():
    print(f"Variable: {var}")
    print(f"Test: {result['test']}")
    if result['test'] == 'ANOVA':
        print(f"ANOVA p-value: {result['anova_p_value']:.4e}")
    else:
        print(f"Kruskal-Wallis p-value: {result['kruskal_p_value']:.4e}")
    print(f"Significant: {result['significant']}")
    print("Post-hoc:")
    if isinstance(result['post_hoc'], str):
        print(result['post_hoc'])
    else:
        print(result['post_hoc'])
    print("\n")
