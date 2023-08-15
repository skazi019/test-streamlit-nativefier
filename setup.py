import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "wrap_main.py",
        # "--onefile",
        "--additional-hooks-dir=./hooks",
        "--windowed",
        "--add-data=all_sector_ticker.csv:all_sector_ticker.csv",
        "-n StockMarket Dashboard v1.0",
        # "--python-option=v",
        # "--hidden-import=streamlit",
        "--paths=.:/Users/kaushal/.local/share/virtualenvs/StockMarketStreamlitApp-8-LmOD_b/lib/python3.10/site-packages",
        "--noconfirm",
        "--clean"
    ]
)
