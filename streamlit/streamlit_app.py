import calendar
import streamlit as st
import altair as alt
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="YouTube Analytics Executive Dashboard", layout="wide")

session = get_active_session()


@st.cache_data(ttl=300)
def load_data():
    return session.sql("""
        SELECT *
        FROM RAW_DB.YOUTUBE.MART_EXECUTIVE_OVERVIEW
        ORDER BY UPLOAD_YEAR, UPLOAD_MONTH
    """).to_pandas()


df = load_data()

st.title("YouTube Analytics Executive Dashboard")

st.sidebar.header("Filters")

years = sorted(df["UPLOAD_YEAR"].unique())
year = st.sidebar.selectbox("Year", years)

filtered = df[df["UPLOAD_YEAR"] == year]

months = sorted(filtered["UPLOAD_MONTH"].unique())
selected = st.sidebar.multiselect(
    "Month",
    months,
    default=months,
    format_func=lambda m: calendar.month_name[m],
)
filtered = filtered[filtered["UPLOAD_MONTH"].isin(selected)]

filtered = filtered.sort_values(["UPLOAD_YEAR", "UPLOAD_MONTH"]).reset_index(drop=True)
filtered["MONTH_NAME"] = filtered["UPLOAD_MONTH"].apply(lambda m: calendar.month_abbr[m])
month_name_order = filtered["MONTH_NAME"].tolist()

fmti = lambda x: f"{int(x):,}"

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.metric("Total Videos", fmti(filtered["TOTAL_VIDEOS"].sum()))
c2.metric("Total Impressions", fmti(filtered["TOTAL_IMPRESSIONS"].sum()))
c3.metric("Total Likes", fmti(filtered["TOTAL_LIKES"].sum()))
c4.metric("Total Watch Time (Hours)", f"{filtered['TOTAL_WATCH_TIME_HOURS'].sum():,.2f}")
c5.metric("Subscribers Gained", fmti(filtered["TOTAL_SUBSCRIBERS_GAINED"].sum()))
c6.metric("Average Engagement Rate", f"{filtered['AVG_ENGAGEMENT_RATE'].mean():.2f}%")

st.divider()

st.subheader("Monthly Impressions")
impressions_chart = (
    alt.Chart(filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X("MONTH_NAME:N", title="Month", sort=month_name_order),
        y=alt.Y("TOTAL_IMPRESSIONS:Q", title="Total Impressions"),
        tooltip=["MONTH_NAME", "TOTAL_IMPRESSIONS"],
    )
    .properties(height=380)
)
st.altair_chart(impressions_chart, use_container_width=True)

st.divider()

st.subheader("Monthly Watch Time")
watch_time_chart = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X("MONTH_NAME:N", title="Month", sort=month_name_order),
        y=alt.Y("TOTAL_WATCH_TIME_HOURS:Q", title="Watch Time (Hours)"),
        tooltip=["MONTH_NAME", "TOTAL_WATCH_TIME_HOURS"],
    )
    .properties(height=380)
)
st.altair_chart(watch_time_chart, use_container_width=True)

st.divider()

st.subheader("Average Engagement Rate")
engagement_chart = (
    alt.Chart(filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X("MONTH_NAME:N", title="Month", sort=month_name_order),
        y=alt.Y("AVG_ENGAGEMENT_RATE:Q", title="Engagement Rate (%)"),
        tooltip=["MONTH_NAME", "AVG_ENGAGEMENT_RATE"],
    )
    .properties(height=380)
)
st.altair_chart(engagement_chart, use_container_width=True)

st.divider()

st.subheader("CTR vs Engagement")
st.caption(
    "Each month has its own color and marker shape. The faint dotted line traces "
    "the chronological path from month to month, and labels are nudged up/down "
    "so nearby points stay readable."
)

ctr_df = filtered.copy()
ctr_df["MONTH_LABEL"] = ctr_df["MONTH_NAME"] + " " + ctr_df["UPLOAD_YEAR"].astype(str)

engagement_range = max(
    ctr_df["AVG_ENGAGEMENT_RATE"].max() - ctr_df["AVG_ENGAGEMENT_RATE"].min(), 1
)
label_offset = engagement_range * 0.06
ctr_df["LABEL_Y"] = ctr_df["AVG_ENGAGEMENT_RATE"] + [
    (label_offset if i % 2 == 0 else -label_offset) for i in range(len(ctr_df))
]

SHAPE_CYCLE = [
    "circle", "square", "triangle-up", "diamond", "triangle-down",
    "cross", "triangle-right", "triangle-left", "square", "circle",
    "diamond", "triangle-up",
]
month_label_order = ctr_df["MONTH_LABEL"].tolist()
shape_range = [SHAPE_CYCLE[i % len(SHAPE_CYCLE)] for i in range(len(month_label_order))]

base = alt.Chart(ctr_df)

trend_line = base.mark_line(
    strokeDash=[3, 3], opacity=0.35, color="gray"
).encode(
    x=alt.X("AVG_CTR:Q", title="Average CTR (%)"),
    y=alt.Y("AVG_ENGAGEMENT_RATE:Q", title="Average Engagement Rate (%)"),
    order="UPLOAD_MONTH:O",
)

points = base.mark_point(filled=True, size=220, opacity=0.9, strokeWidth=1).encode(
    x=alt.X("AVG_CTR:Q", title="Average CTR (%)"),
    y=alt.Y("AVG_ENGAGEMENT_RATE:Q", title="Average Engagement Rate (%)"),
    color=alt.Color(
        "MONTH_LABEL:N",
        title="Month",
        scale=alt.Scale(domain=month_label_order, scheme="tableau20"),
    ),
    shape=alt.Shape(
        "MONTH_LABEL:N",
        title="Month",
        scale=alt.Scale(domain=month_label_order, range=shape_range),
    ),
    tooltip=[
        alt.Tooltip("MONTH_LABEL:N", title="Month"),
        alt.Tooltip("AVG_CTR:Q", title="Avg CTR (%)", format=".2f"),
        alt.Tooltip("AVG_ENGAGEMENT_RATE:Q", title="Avg Engagement (%)", format=".2f"),
        alt.Tooltip("TOTAL_IMPRESSIONS:Q", title="Total Impressions", format=","),
    ],
)

labels = base.mark_text(fontSize=11, fontWeight="bold").encode(
    x=alt.X("AVG_CTR:Q"),
    y=alt.Y("LABEL_Y:Q"),
    text="MONTH_LABEL:N",
)

ctr_chart = (trend_line + points + labels).properties(height=460).interactive()
st.altair_chart(ctr_chart, use_container_width=True)

with st.expander("Alternative view: CTR & Engagement trend over time"):
    st.caption(
        "If overlap is still hard to read at a glance, this dual-axis line view "
        "plots CTR and Engagement Rate independently across the same timeline."
    )
    ctr_line = alt.Chart(ctr_df).mark_line(point=True, color="#1f77b4").encode(
        x=alt.X("MONTH_LABEL:N", title="Month", sort=month_label_order),
        y=alt.Y("AVG_CTR:Q", title="Average CTR (%)", axis=alt.Axis(titleColor="#1f77b4")),
        tooltip=[alt.Tooltip("AVG_CTR:Q", format=".2f")],
    )
    engagement_line = alt.Chart(ctr_df).mark_line(point=True, color="#9467bd").encode(
        x=alt.X("MONTH_LABEL:N", title="Month", sort=month_label_order),
        y=alt.Y(
            "AVG_ENGAGEMENT_RATE:Q",
            title="Average Engagement Rate (%)",
            axis=alt.Axis(titleColor="#9467bd"),
        ),
        tooltip=[alt.Tooltip("AVG_ENGAGEMENT_RATE:Q", format=".2f")],
    )
    dual_axis_chart = alt.layer(ctr_line, engagement_line).resolve_scale(
        y="independent"
    ).properties(height=380)
    st.altair_chart(dual_axis_chart, use_container_width=True)

st.divider()

st.subheader("Monthly Summary")
summary_df = filtered.drop(columns=["MONTH_NAME"])
st.dataframe(summary_df, use_container_width=True, hide_index=True)
