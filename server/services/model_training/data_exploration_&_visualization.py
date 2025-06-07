import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from sklearn.ensemble import RandomForestClassifier
import matplotlib as mpl

COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

def configure_plotting():
    plt.style.use('seaborn-v0_8-whitegrid')
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['figure.titlesize'] = 16
    mpl.rcParams['axes.labelsize'] = 14
    mpl.rcParams['axes.titlesize'] = 15
    mpl.rcParams['xtick.labelsize'] = 12
    mpl.rcParams['ytick.labelsize'] = 12

def save_or_show_figure(fig, filename=None):
    plt.tight_layout()
    if filename:
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def print_section_header(title):
    print(f"\n{'='*80}\n{title}\n{'='*80}")

def load_data():
    authors_files = {
        'Charles Dickens': 'data/Charles_Dickens.csv',
        'H. G. Wells': 'data/H.G.Wells.csv',
        'Jane Austen': 'data/Jane_Austen.csv',
        'Mark Twain': 'data/Mark_Twain.csv'
    }

    dfs = []
    for author, filepath in authors_files.items():
        df = pd.read_csv(filepath)
        df['author'] = author
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def explore_data(data):
    X = data.drop('author', axis=1)
    y = data['author']

    print(f"several examples in the database: {data.shape[0]}")
    print(f"several features: {X.shape[1]}")
    print("\n distribution of examples by author:")
    print(y.value_counts())

    missing = data.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        print("\n missing values:")
        print(missing)
    else:
        print("\n There are no missing values ​​in the data.. ")

    print("\n Example data:")
    print(data.head())
    print("\n descriptive statistics:")
    print(X.describe().T)

# גרף התפלגות מחברים
def plot_author_distribution(data):
    author_counts = data['author'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 8))
    author_counts.plot.pie(
        autopct='%1.1f%%',
        startangle=90,
        colors=COLOR_PALETTE,
        ax=ax,
        textprops={'fontsize': 12},
        explode=[0.05] * len(author_counts),
        shadow=True,
        wedgeprops={'edgecolor': 'w', 'linewidth': 1}
    )
    ax.set_ylabel('')
    ax.set_title('distribution of examples by author', pad=20)
    save_or_show_figure(fig)

#  ניתוח שונות ותיבות
def analyze_top_variance_features(data):
    X = data.drop('author', axis=1)
    variances = X.var().sort_values(ascending=False)
    top_features = variances.head(5).index.tolist()
    print(f"\n5 the characteristics with the highest variance:")
    for i, feature in enumerate(top_features, 1):
        print(f"{i}. {feature} (שונות: {X[feature].var():.4f})")
    return top_features

def plot_boxplots(data, features):
    fig, axes = plt.subplots(3, 2, figsize=(14, 18))
    axes = axes.flatten()
    for i, feature in enumerate(features):
        if i < 6:
            ax = axes[i]
            sns.boxplot(x='author', y=feature, data=data, ax=ax, palette=COLOR_PALETTE)
            ax.set_title(f'split {feature} According to the author')
            ax.set_xlabel('')
            ax.tick_params(axis='x', rotation=45)
    for j in range(i+1, 6):
        fig.delaxes(axes[j])
    save_or_show_figure(fig)
# הצגת היסטוגרמות של מספר מאפיינים
def plot_histograms(data, features):
    fig, axes = plt.subplots(3, 2, figsize=(14, 18))
    axes = axes.flatten()
    for i, feature in enumerate(features):
        if i < 6:
            ax = axes[i]
            for idx, author in enumerate(data['author'].unique()):
                sns.histplot(
                    data[data['author'] == author][feature],
                    ax=ax, kde=True,
                    alpha=0.5, label=author,
                    color=COLOR_PALETTE[idx]
                )
            ax.set_title(f'split {feature}')
            ax.legend()
            ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    for j in range(i+1, 6):
        fig.delaxes(axes[j])
    save_or_show_figure(fig)

# שלב 5: קורלציה
def correlation_analysis(X):
    corr = X.corr()
    plt.figure(figsize=(16, 14))
    mask = np.triu(corr)
    sns.heatmap(corr, mask=mask, cmap='coolwarm', vmin=-1, vmax=1, center=0,
                annot=False, square=True, linewidths=0)
    plt.title('Correlation matrix between features', pad=20)
    plt.tight_layout()
    plt.show()

    high_corr = corr.unstack().sort_values(ascending=False)
    high_corr = high_corr[(high_corr < 1.0) & (high_corr >= 0.7)]

    if not high_corr.empty:
        print("\n high correlations between characteristics (above 0.7): ")
        for idx, value in high_corr.items():
            print(f"{idx[0]} ~ {idx[1]}: {value:.4f}")
    else:
        print("\n there are no high correlations above 0.7 between the characteristics..")

# שלב 6: חשיבות מאפיינים
def feature_importance_analysis(X, y):
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n The 15 most important characteristics according to Random Forest:")
    print(importances.head(15))

    plt.figure(figsize=(12, 10))
    sns.barplot(x='importance', y='feature',
                data=importances.head(15),
                palette=sns.color_palette("Blues_d", n_colors=15))
    plt.title('the 15 most important characteristics', pad=20)
    plt.tight_layout()
    plt.show()

# שלב 7: סיכום
def print_summary():
    print_section_header("סיכום ומסקנות")
    print("""
סיכום הממצאים מניתוח הנתונים:

1. מבנה הנתונים:
   - הדאטאסט מכיל נתונים עבור 4 מחברים שונים
   - לכל מחבר יש מספר דוגמאות טקסט שונות
   - המאפיינים מבוססים על מדדים לשוניים וסגנוניים

2. איכות הנתונים:
   - לא נמצאו ערכים חסרים בנתונים
   - התפלגות הדוגמאות בין המחברים מאוזנת יחסית

3. מאפיינים חשובים:
   - זוהו מאפיינים עם שונות גבוהה המבדילים בין המחברים השונים
   - המאפיינים החשובים ביותר לסיווג הם: [יש להשלים על סמך התוצאות]

4. קורלציות:
   - ישנן מספר קורלציות חזקות בין מאפיינים, מה שמצביע על יתירות מסוימת
   - יתכן שניתן לשקול הפחתת מימדים או בחירת מאפיינים לשיפור המודל

המלצות להמשך:
1. לשקול נירמול הנתונים לפני אימון המודל הסופי
2. לבחון מודלים שונים מעבר ל-Random Forest
3. לנסות שיטות לבחירת מאפיינים או הפחתת מימדים
""")

def main():
    configure_plotting()
    print_section_header("טעינת קבצי הנתונים")
    data = load_data()
    print_section_header("מידע בסיסי על הנתונים")
    explore_data(data)
    print_section_header("ויזואליזציה של התפלגות המחברים")
    plot_author_distribution(data)
    print_section_header("ניתוח מאפיינים מרכזיים")
    top_features = analyze_top_variance_features(data)
    plot_boxplots(data, top_features)
    plot_histograms(data, top_features)
    print_section_header("ניתוח קורלציות בין מאפיינים")
    correlation_analysis(data.drop('author', axis=1))
    print_section_header("הערכת חשיבות מאפיינים")
    feature_importance_analysis(data.drop('author', axis=1), data['author'])
    print_summary()

# להרצה:
if __name__ == "__main__":
    main()