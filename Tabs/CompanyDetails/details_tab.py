import numpy as np
import uuid
import re

from Core.utilities import format_to_inr
from numpy import dtype, insert


def ticker_details_tab(st, ticker, ticker_info):
    st.title(ticker)
    industry_col, _, sector_col, _ = st.columns([1, 0.5, 1, 2])
    with industry_col:
        if "industry" in ticker_info.keys():
            st.caption(f"Industry: {ticker_info['industry']}")
    with sector_col:
        if "sector" in ticker_info.keys():
            st.caption(f"Sector: {ticker_info['sector']}")

    st.subheader(f"{ticker_info['longName']}")
    st.markdown("---")

    ticker_info_details = {}
    for key, value in ticker_info.items():
        if key in [
            "address1",
            "address2",
            "city",
            "zip",
            "country",
            "phone",
            "fax",
            "website",
            "longBusinessSummary",
        ]:
            pass
        else:
            ticker_info_details[key] = value

    selected_metrics = [
        {
            "Info": [
                "exchange",
                "symbol",
                "quoteType",
            ]
        },
        {
            f"Price - {ticker_info_details['currency']}": [
                "fiftyTwoWeekLow",
                "fiftyTwoWeekHigh",
                "previousClose",
                "marketCap",
            ]
        },
        {
            "Risk": [
                "auditRisk",
                "boardRisk",
                "compensationRisk",
                "shareHolderRightsRisk",
                "overallRisk",
            ]
        },
        {
            "Dividend": [
                "dividendRate",
                "dividendYield",
                "payoutRatio",
                "fiveYearAvgDividendYield",
            ]
        },
        {"PE": ["trailingPE", "forwardPE"]},
    ]

    for metric_index in range(len(selected_metrics)):
        key = uuid.uuid4()
        metric_json = selected_metrics[metric_index]
        metric_title = list(metric_json.keys())[0]
        row = metric_json[metric_title]

        st.subheader(metric_title)
        all_cols = st.columns(len(row))

        for col in all_cols:
            key_index = all_cols.index(col)
            label = re.findall(".[^A-Z]*", row[key_index])
            label = " ".join([x.capitalize() for x in label])

            if row[key_index] in ticker_info_details.keys():
                value = ticker_info_details[row[key_index]]

                if isinstance(value, int) or isinstance(value, float):
                    if label == "Market Cap":
                        value = format_to_inr(value)
                    else:
                        value = "{:,}".format(value)
                col.metric(label=label, value=value)

        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
    # st.write(ticker_info_details)
