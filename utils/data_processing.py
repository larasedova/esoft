import pandas as pd


def analyze_data(filepath):
    # Чтение файла
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Анализ данных
    result = {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'correlation': df.corr().to_dict()
    }

    return result


def clean_data(filepath):
    # Чтение файла
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Очистка данных
    cleaned_df = df.drop_duplicates()
    cleaned_df = cleaned_df.fillna(cleaned_df.mean())

    return cleaned_df