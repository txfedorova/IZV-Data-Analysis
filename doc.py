from matplotlib import pyplot as plt
import pandas as pd
import os
import seaborn as sns

DO_PLOT = True
FIG_DIR = 'fig'

SEVERE_INJURIES = 'Severe Injuries'
LIGHT_INJURIES = 'Light Injuries'


def preprocess_data(data):
    """Preprocess the data by renaming columns and filtering."""

    # drop if no info about intoxication is present
    data = data.drop(data[(data['p11'] == 0)].index)

    # drop if both alcohol and drugs are present
    data = data.drop(data[(data['p11'] == 5)].index)

    data = data[['p1', 'p11', 'p13a', 'p13b', 'p13c', 'p45a']]

    data = data.rename({
        'p13a': 'Death',
        'p13b': SEVERE_INJURIES,
        'p13c': LIGHT_INJURIES,
        'p11': 'Intoxication Type',
        'p1': 'Accidents',
        'p12': 'Cause',
        'p45a': 'Auto Brand'
    }, axis='columns')

    return data


def categorize_data(data: pd.DataFrame) -> pd.DataFrame:
    """Categorize by intoxication type."""
    intoxication_mapping = {
        4: "drugs",
        1: "drunk",
        2: "sober",
        3: "drunk",
        6: "drunk",
        7: "drunk",
        8: "drunk",
        9: "drunk"
    }
    data['Intoxication Type'] = data['Intoxication Type'].map(intoxication_mapping)

    return data


def group_data(df: pd.DataFrame, columns_to_group_by, labels):
    return df.groupby(columns_to_group_by)[labels].mean()


def injury_by_intoxication(data: pd.DataFrame):
    # Rearranging the DataFrame for the required plot format
    df_prop_t = data[[SEVERE_INJURIES, LIGHT_INJURIES]].T
    df_prop_t.columns = ['Drugs', 'Drunk', 'Sober']
    df_prop_t = df_prop_t.reset_index()

    # Plotting
    plt.figure(figsize=(12, 8))
    sns.barplot(x='index', y='value', hue='variable', data=pd.melt(df_prop_t, id_vars='index'), palette=['#c3553a', '#a5c1ca', '#3f7f93'])
    plt.title('Mean Value of Injury Types by Intoxication Type', fontsize=16)
    plt.xlabel('Injury Type', fontsize=14)
    plt.ylabel('Mean Value', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(title='Intoxication Type', bbox_to_anchor=(0.1, 0.8), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig(os.path.join(FIG_DIR, f'mean_values_by_intoxication_types.png'))
    if DO_PLOT:
        plt.show()


def injuries_heatmap(data: pd.DataFrame):
    df_prop_t = data[[SEVERE_INJURIES, LIGHT_INJURIES]].T

    plt.figure(figsize=(12, 7))
    sns.set(style="whitegrid")

    print('Probability of being drunk or on drugs by injury type:')
    for i in range(len(df_prop_t)):
        print(f'{df_prop_t.index[i]}: {df_prop_t.iloc[i, 0]:.2%} drunk, {df_prop_t.iloc[i, 1]:.2%} drugs')

    # Create a custom colormap
    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    ax = sns.heatmap(df_prop_t, annot=True, cmap=cmap, fmt=".2%", linewidths=.5, cbar_kws={'shrink': .5})
    plt.title('Probability of Intoxication Type for Each Injury Type', fontsize=18, fontweight='bold', pad=15)
    plt.ylabel('Injury Type', fontsize=14, labelpad=10)
    plt.xlabel('Intoxication Type', fontsize=14, labelpad=10)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(rotation=0, fontsize=12)

    for t in ax.texts:
        t.set_text(t.get_text())
    sns.despine(offset=10, trim=True)  # removes the top and right spines from plot

    plt.tight_layout()

    plt.savefig(os.path.join(FIG_DIR, f'2_prob_intox_type_for_each_injury_type.png'))
    if DO_PLOT:
        plt.show()


def create_auto_data(data: pd.DataFrame) -> pd.DataFrame:
    auto_brand_mapping = {
        2: 'Audi',
        4: 'BMW',
        48: 'Volvo',
        44: 'Toyota',
        39: 'Skoda'
    }
    data['Auto Brand'] = data['Auto Brand'].map(auto_brand_mapping)
    return data


def show_auto_data(data: pd.DataFrame):
    new_data = create_auto_data(data.copy()).dropna(subset=['Auto Brand'])

    # Calculating probabilities
    prob_df = new_data.groupby('Auto Brand')['Intoxication Type'].value_counts(normalize=True).unstack().fillna(0)[['drunk', 'drugs']]
    print(
        f'Probability of being drunk or on drugs by auto brand:\n{prob_df}\n',
        prob_df.to_csv()
    )

    # Plotting
    plt.figure(figsize=(12, 7))
    sns.set(style="whitegrid")
    ax = sns.barplot(data=prob_df.T, palette="coolwarm", errorbar=None)
    plt.title('Probability of Being Drunk or on Drugs by Auto Brand', fontsize=18, fontweight='bold', pad=15)
    plt.xlabel('Intoxication Type', fontsize=14, labelpad=10)
    plt.ylabel('Probability', fontsize=14, labelpad=10)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    # plt.legend(title='Auto Brand', bbox_to_anchor=(1.05, 1), loc='upper left')
    sns.despine(offset=10, trim=True)
    plt.tight_layout()

    plt.savefig(os.path.join(FIG_DIR, f'3_prob_drunk_by_auto_brand.png'))
    if DO_PLOT:
        plt.show()


if __name__ == "__main__":
    f = "accidents.pkl.gz"
    if not os.path.exists(f):
        print(f'{f} does not exist')
        exit(-1)

    df = pd.read_pickle(f)
    os.makedirs(FIG_DIR, exist_ok=True)

    DF = categorize_data(preprocess_data(df.copy()))
    grouped_data = group_data(DF, ['Intoxication Type'], [SEVERE_INJURIES, LIGHT_INJURIES])

    injury_by_intoxication(grouped_data)
    injuries_heatmap(grouped_data)
    show_auto_data(DF.copy())
