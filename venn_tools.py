from __future__ import division
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from matplotlib_venn_wordcloud import venn2_wordcloud, venn3_wordcloud


def draw_word_venn(datasets, dataset_name1, dataset_name2):
    fig, ax = plt.subplots(1, 1, figsize=(30, 30))
    set1 = set(get_names_from_files(datasets[dataset_name1]))
    set2 = set(get_names_from_files(datasets[dataset_name2]))
    v = venn2_wordcloud([set1, set2], (dataset_name1, dataset_name2), ax=ax, set_colors=['blue', 'yellow'])
    for text in v.set_labels:
        text.set_fontsize(30)
    for text in v.subset_labels:
        text.set_fontsize(18)
    plt.show()


def draw_venn(datasets, dataset_name1, dataset_name2):
    fig, ax = plt.subplots(1, 1, figsize=(30, 30))
    set1 = set(get_names_from_files(datasets[dataset_name1]))
    set2 = set(get_names_from_files(datasets[dataset_name2]))
    v = venn2([set1, set2], (dataset_name1, dataset_name2), ax=ax, set_colors=['blue', 'yellow'])
    for text in v.set_labels:
        text.set_fontsize(30)
    for text in v.subset_labels:
        text.set_fontsize(18)
    plt.show()


def draw_word_venn_3(datasets, dataset_name1, dataset_name2, dataset_name3):
    fig, ax = plt.subplots(1, 1, figsize=(30, 30))
    set1 = set(get_names_from_files(datasets[dataset_name1]))
    set2 = set(get_names_from_files(datasets[dataset_name2]))
    set3 = set(get_names_from_files(datasets[dataset_name3]))
    v = venn3_wordcloud([set1, set2, set3], (dataset_name1, dataset_name2, dataset_name3), ax=ax,
                        set_colors=['blue', 'yellow', 'green'])
    for text in v.set_labels:
        text.set_fontsize(30)
    for text in v.subset_labels:
        text.set_fontsize(18)
    plt.show()

