import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_marketing_data(num_rows: int = 100) -> pd.DataFrame:
    """
    『ECサイト売上サンプルデータ』を生成する。
    意図的に欠損値や異常値を混ぜ、データクレンジングの練習用に用いる。
    """
    np.random.seed(42)
    
    # 基本データの定義
    categories = ['電化製品', '服', '雑貨', 'おもちゃ', '書籍']
    regions = ['東京', '大阪', '名古屋', '福岡', '札幌']
    
    data = {
        '日付': [(datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_rows)],
        'カテゴリ': [np.random.choice(categories) for _ in range(num_rows)],
        '地域': [np.random.choice(regions) for _ in range(num_rows)],
        '売上': np.random.randint(1000, 50000, num_rows),
        '利益率': np.random.uniform(0.05, 0.4, num_rows).round(4),
        '顧客満足度': np.random.randint(1, 6, num_rows)
    }
    
    df = pd.DataFrame(data)
    
    # --- 意図的に欠損値や異常値を混ぜる ---
    # 1. 欠損値を数か所入れる
    for _ in range(5):
        df.loc[np.random.randint(0, num_rows), '売上'] = np.nan
    
    # 2. 異常値（外れ値）を入れる
    df.loc[0, '売上'] = 500000
    
    return df

if __name__ == "__main__":
    # フォルダがなければ作成する
    os.makedirs('../data', exist_ok=True)
    
    df_sample: pd.DataFrame = generate_marketing_data(200)
    # 保存先を ../data/ フォルダに変更
    df_sample.to_csv('../data/sample_data.csv', index=False)
    print("✅ ../data/sample_data.csv has been generated successfully!")