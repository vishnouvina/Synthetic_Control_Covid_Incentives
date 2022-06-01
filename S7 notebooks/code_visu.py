import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm, Normalize
import seaborn as sns


def importation(filename):
    return pd.read_csv(filename, sep=",")


# Importations
df_prm_corr = importation("df_prm_corr.csv")
df_prm_scaled = importation("df_prm_scaled.csv")
V40 = importation("V40.csv")
V40_18 = importation("V40_18.csv")
V40_65 = importation("V40_65.csv")
df_delta_f = importation("df_delta_f.csv")
df_delta_f_18 = importation("df_delta_f_18.csv")
df_delta_f_65 = importation("df_delta_f_65.csv")
df_fit = importation("df_fit.csv")
df_fit_18 = importation("df_fit_18.csv")
df_fit_65 = importation("df_fit_65.csv")


df_character = df_prm_scaled.rename(
    columns={'Population density (number of people/square mile)': 'Population density'})
df_character = df_character.rename(
    columns={'Median income (in US dollars)': 'Median income'})
df_character = df_character.rename(
    columns={'Governor: democrat (1) / republican (0)': "Governor's political party"})
df_character = df_character.rename(
    columns={'%' + ' non couverts par une assurance maladie': "Health insurance %"})
df_character = df_character.rename(
    columns={'Access to Care  (score between 0 and 1)': 'Access to care'})
del df_character["État"]
character = df_character.columns
states = []
for i in range(1, 19):
    states.append(df_delta_f["t_fit"][i])
groups = []
for i in range(0, 18):
    groups.append(V40["0"][i])
group_states = []
for i in range(0, 18):
    group_states.append(states[i]+' : Group '+groups[i])

# Cleaning df_prm_corr
del df_prm_corr["Unnamed: 0"]
df_prm_corr = df_prm_corr.rename(columns={'Population density (number of people/square mile)': 'Population density'},
                                 index={'Population density (number of people/square mile)': 'Population density'})
df_prm_corr = df_prm_corr.rename(columns={'Median income (in US dollars)': 'Median income'},
                                 index={'Median income (in US dollars)': 'Median income'})
df_prm_corr = df_prm_corr.rename(columns={'Governor: democrat (1) / republican (0)': "Governor's political party"},
                                 index={'Governor: democrat (1) / republican (0)': "Governor's political party"})
df_prm_corr = df_prm_corr.rename(columns={'%' + ' non couverts par une assurance maladie': "Health insurance %"},
                                 index={'%' + ' non couverts par une assurance maladie': "Health insurance %"})
df_prm_corr = df_prm_corr.rename(columns={'Access to Care  (score between 0 and 1)': 'Access to care'},
                                 index={'Access to Care  (score between 0 and 1)': 'Access to care'})

# Cleaning df_prm_scaled
list_state = df_prm_scaled["État"].tolist()
del df_prm_scaled["État"]

df_prm_scaled = df_prm_scaled.rename(
    columns={'Population density (number of people/square mile)': 'Population density'})
df_prm_scaled = df_prm_scaled.rename(
    columns={'Median income (in US dollars)': 'Median income'})
df_prm_scaled = df_prm_scaled.rename(
    columns={'Governor: democrat (1) / republican (0)': "Governor's political party"})
df_prm_scaled = df_prm_scaled.rename(
    columns={'%' + ' non couverts par une assurance maladie': "Health insurance %"})
df_prm_scaled = df_prm_scaled.rename(
    columns={'Access to Care  (score between 0 and 1)': 'Access to care'})
df_prm_scaled["Asian"][10] = 3
df_prm_scaled["Hawaiian"][10] = 3.1


# Calcul nombre d'états par groupe
l_group = []
l_tar_con = []


def app(name, liste, n):
    for i in range(0, n):
        liste.append(name)


app("Group A", l_group, 19)
app("Group B", l_group, 20)
app("Groupe C", l_group, 11)
app("Potential Target States", l_tar_con, 11)
app("Control States", l_tar_con, 8)
app("Potential Target States", l_tar_con, 6)
app("Control States", l_tar_con, 14)
app("Potential Target States", l_tar_con, 1)
app("Control States", l_tar_con, 10)
dic_grp_states = {"Groups": l_group, "Target/Control": l_tar_con}
df_grp_states = pd.DataFrame(dic_grp_states)


# Cleaning df_delta_f
def clean_delta_f(data_delta_f):

    data_delta_f = data_delta_f.drop([0], axis=0)
    del data_delta_f["t_fit"]

# for column in df_delta_f.columns:
#     for i in range(1, 19):
#         if df_delta_f[column][i] > 0:
#             df_delta_f[column][i] = 7.4
    return data_delta_f


df_delta_f = clean_delta_f(df_delta_f)
df_delta_f_18 = clean_delta_f(df_delta_f_18)
df_delta_f_65 = clean_delta_f(df_delta_f_65)

# Cleaning V_matrix


def clean_V_n(data_V_n):
    del data_V_n["Unnamed: 0"]
    del data_V_n["0"]
    for column in data_V_n.columns:
        for i in range(0, 18):
            data_V_n[column][i] = round(data_V_n[column][i], 2)
    return data_V_n


V40 = clean_V_n(V40)

# Cleaning df_fit


def clean_fit(data_fit):
    del data_fit["Unnamed: 0"]
    return data_fit


df_fit = clean_fit(df_fit)


# Concaténation des df_delta_f_n
data_concat = {'global: t_0': [], 'global: t_0+30': [], 'global: t_0+40': [], 'global: t_0+90': [], '18-65: t_0': [],
               '18-65: t_0+30': [], '18-65: t_0+40': [], '18-65: t_0+90': [], '65+: t_0': [], '65+: t_0+30': [], '65+: t_0+40': [], '65+: t_0+90': []}
for i in range(1, 19):
    data_concat['global: t_0'].append(
        df_delta_f["------------ 40 ------------"][i])
    data_concat['global: t_0+30'].append(
        df_delta_f["------------ 40 ------------.1"][i])
    data_concat['global: t_0+40'].append(
        df_delta_f["------------ 40 ------------.2"][i])
    data_concat['global: t_0+90'].append(
        df_delta_f["------------ 40 ------------.3"][i])
    data_concat['18-65: t_0'].append(
        df_delta_f_18["------------ 40 ------------"][i])
    data_concat['18-65: t_0+30'].append(
        df_delta_f_18["------------ 40 ------------.1"][i])
    data_concat['18-65: t_0+40'].append(
        df_delta_f_18["------------ 40 ------------.2"][i])
    data_concat['18-65: t_0+90'].append(
        df_delta_f_18["------------ 40 ------------.3"][i])
    data_concat['65+: t_0'].append(
        df_delta_f_65["------------ 40 ------------"][i])
    data_concat['65+: t_0+30'].append(
        df_delta_f_65["------------ 40 ------------.1"][i])
    data_concat['65+: t_0+40'].append(
        df_delta_f_65["------------ 40 ------------.2"][i])
    data_concat['65+: t_0+90'].append(
        df_delta_f_65["------------ 40 ------------.3"][i])
df_delta_f_concat = pd.DataFrame.from_dict(data_concat)


# # Plotting df_delta_f_concat
# color_map = plt.cm.get_cmap('RdYlGn')
# color_map = color_map.reversed()
# ax = sns.heatmap(
#     df_delta_f_concat, cmap=color_map, vmin=-5, vmax=5, center=0, annot=True, yticklabels=group_states)
# ax.axvline(4, 0, 2, linewidth=20, c='w')
# ax.axvline(8, 0, 2, linewidth=20, c='w')
# plt.xticks(rotation=30, ha="right")
# plt.show()


# # Plotting df_fit
# color_map = plt.cm.get_cmap('plasma')
# color_map = color_map.reversed()
# list_t_fit = ["t_fit=30", "t_fit=40", "t_fit=50", "t_fit=60"]
# ax = sns.heatmap(
#     df_fit, cmap=color_map, xticklabels=list_t_fit, yticklabels=states)
# plt.xticks(rotation=30, ha="right")
# plt.show()


# Plotting V_n dataframe

# colormap = plt.cm.get_cmap('BuPu')
# ax = sns.heatmap(
#     V40, cmap=colormap, annot=True, xticklabels=character, yticklabels=group_states)
# for i in range(1, 19):
#     ax.axhline(i, 0, 1, linewidth=0.5, c='black')
# plt.xticks(rotation=30, ha="right")
# plt.show()

# # # Plotting df_delta_f

# t_fit_l = ["t_fit=30", "t_fit=40", "t_fit=50", "t_fit=60"]
# t_0_l = ["t_0", "t_0+30", "t_0+40", "t_0+90"]
# t_fit_t_0 = []
# for fit in t_fit_l:
#     for t_0 in t_0_l:
#         t_fit_t_0.append(fit+', '+t_0)
# color_map = plt.cm.get_cmap('RdYlGn')
# color_map = color_map.reversed()
# ax = sns.heatmap(
#     df_delta_f, cmap=color_map, vmin=-5, vmax=5, center=0, annot=True, xticklabels=t_fit_t_0, yticklabels=group_states)
# ax.axvline(4, 0, 2, linewidth=20, c='w')
# ax.axvline(8, 0, 2, linewidth=20, c='w')
# ax.axvline(12, 0, 2, linewidth=20, c='w')
# plt.xticks(rotation=30, ha="right")
# plt.show()


# Plotting répartition des groupes

# sns.catplot(x="Groups", hue="Target/Control", kind="count",
#             palette="pastel", edgecolor=".6",
#             data=df_grp_states)
# plt.show()


# Plotting df_prm_scaled

# ax = sns.heatmap(
#     df_prm_scaled, cmap='PuBuGn', xticklabels=df_prm_scaled.columns, yticklabels=list_state)
# plt.xticks(rotation=30, ha="right")
# plt.show()


# Potting df_prm_corr

# ax = sns.heatmap(df_prm_corr, cmap='YlGnBu', annot=True,
#                  xticklabels=df_prm_corr.columns, yticklabels=df_prm_corr.columns)
# plt.xticks(rotation=30, ha="right")
# plt.yticks(rotation=0, ha="right")
# plt.show()
