Smart Data Explorer

概要:
アップロードしたCSVデータを即座に可視化・分析するためのWebアプリケーションです。
サンプルデータは data/ にあります。
データの再生成は scripts/ 下のスクリプトで可能です。

なぜこれを作ったか：
実務のブランクを鑑み、近年主流の言語であるPythonを学習するために作成しています。

こだわった点:
・保守性の向上: 型ヒントが必要か不要かを考慮し、チーム開発を想定した可視性の高いコードを記述しました。
・ユーザー体験: Streamlitを採用し、HTML/CSS不要で直感的なデータ操作を実現。Plotlyによるインタラクティブなグラフ表示を実装しています。

使用技術:
Python 3.14.3 / numpy / pandas / streamlit / plotly

実行用コマンド:
pip install -r requirements.txt
streamlit run app.py