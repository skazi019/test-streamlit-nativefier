import datetime
from state import State
from Core.fetch_ticker_data import fetch_yahoo_option_chain


def tab_options(st):
    current_date = str(datetime.datetime.now().date())
    status, ticker_option_chain = fetch_yahoo_option_chain(State.get(st, "ticker"))
    if not status:
        st.error(f"No options found for date: {current_date}")
        st.stop()
    st.write("Calls")
    st.write(ticker_option_chain.calls)
    st.write("Puts")
    st.write(ticker_option_chain.put)
