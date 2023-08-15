from state import State
from Core.fetch_ticker_data import fetch_yahoo_fin_news


def tab_news(st):
    ticker_news = fetch_yahoo_fin_news(State.get(st, "ticker"))
    # st.write(ticker_news)
    for news in ticker_news:
        st.markdown(
            f"""
            ### {news['title']}

            {news['publisher']}


            [Open article]({news['link']})

            ---

            """
        )
