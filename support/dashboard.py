"""Streamlit dashboard for SafeX bot analytics."""

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from support.analytics import get_summary, load_analytics, top_queries
except ImportError:
    from analytics import get_summary, load_analytics, top_queries


def _show_metrics(summary: dict[str, int]) -> None:
    """Display the main dashboard metrics."""
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Chats", summary["Total Chats"])
    col2.metric("Successful Chats", summary["Successful Chats"])
    col3.metric("Escalated Chats", summary["Escalated Chats"])


def _show_top_queries_chart(queries_df: pd.DataFrame) -> None:
    """Display the top queries bar chart."""
    if queries_df.empty:
        st.write("No query data available.")
        return

    chart = px.bar(queries_df, x="Message", y="Count", title="Top Queries")
    st.plotly_chart(chart, use_container_width=True)


def _show_status_chart(summary: dict[str, int]) -> None:
    """Display the chat status pie chart."""
    status_df = pd.DataFrame(
        {
            "Status": ["Successful", "Escalated"],
            "Count": [summary["Successful Chats"], summary["Escalated Chats"]],
        }
    )
    chart = px.pie(status_df, names="Status", values="Count", title="Successful vs Escalated")
    st.plotly_chart(chart, use_container_width=True)


st.set_page_config(page_title="SafeX WhatsApp Bot Analytics", layout="wide")
st.title("SafeX WhatsApp Bot Analytics")

analytics_df = load_analytics()

if analytics_df.empty:
    st.info("No analytics available.")
else:
    summary_data = get_summary()
    _show_metrics(summary_data)
    st.subheader("Top Queries")
    _show_top_queries_chart(top_queries())
    st.subheader("Chat Status")
    _show_status_chart(summary_data)