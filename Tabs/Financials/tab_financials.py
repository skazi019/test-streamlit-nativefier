import datetime
from time import strftime, strptime
from state import State
from Core.utilities import format_to_inr
from Core.fetch_ticker_data import (
    fetch_yahoo_fin_info,
    fetch_yahoo_fin_income_statement,
    fetch_yahoo_fin_balance_sheet,
)
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    DataReturnMode,
    ColumnsAutoSizeMode,
)

def get_aggrid(data):
    data.reset_index(inplace=True)
    data.columns = [col.strftime("%d %B %Y") if col != "index" else col for col in data.columns]
    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_selection(use_checkbox=True, selection_mode="multiple")
    gd.configure_default_column(
        enablePivot=True, enableValue=True, enableRowGroup=True
    )

    gridOptions = gd.build()
    return AgGrid(
        data,
        height=550,
        theme="alpine",
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        header_checkbox_selection_filtered_only=True,
        use_checkbox=True,
    )

def tab_financials(st):
    ticker_income_stmt, ticker_q_income_stmt = fetch_yahoo_fin_income_statement(
        State.get(st, "ticker")
    )
    st.subheader("Income Statement")
    for col in ticker_income_stmt:
        ticker_income_stmt[col] = ticker_income_stmt[col].apply(format_to_inr)


    get_aggrid(ticker_income_stmt)
    # st.data_editor(ticker_income_stmt, use_container_width=True)

    st.subheader("Quaterly Income Statement")
    for col in ticker_q_income_stmt:
        ticker_q_income_stmt[col] = ticker_q_income_stmt[col].apply(format_to_inr)

    get_aggrid(ticker_q_income_stmt)
    # st.data_editor(ticker_q_income_stmt, use_container_width=True)

    ticker_balance_sheet, ticker_q_balance_sheet = fetch_yahoo_fin_balance_sheet(
        State.get(st, "ticker")
    )

    st.subheader("Balance Sheet")
    for col in ticker_balance_sheet:
        ticker_balance_sheet[col] = ticker_balance_sheet[col].apply(format_to_inr)

    get_aggrid(ticker_balance_sheet)
    # st.data_editor(ticker_balance_sheet, use_container_width=True)

    st.subheader("Quaterly Balance Sheet")
    for col in ticker_q_balance_sheet:
        ticker_q_balance_sheet[col] = ticker_q_balance_sheet[col].apply(format_to_inr)

    get_aggrid(ticker_q_balance_sheet)
    # st.data_editor(ticker_q_balance_sheet, use_container_width=True)
