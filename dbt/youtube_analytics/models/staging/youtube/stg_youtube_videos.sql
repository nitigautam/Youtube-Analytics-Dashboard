{{ config(
    materialized='view'
) }}

SELECT

    -------------------------------------------------
    -- Primary Key
    -------------------------------------------------

    POST_ID AS video_id,

    -------------------------------------------------
    -- Video Information
    -------------------------------------------------

    UPLOAD_DATE AS upload_timestamp,

    VIDEO_DURATION_MIN AS video_duration_minutes,

    AVG_VIEW_DURATION_SEC AS avg_view_duration_seconds,

    AVG_VIEW_PERCENTAGE AS avg_view_percentage,

    -------------------------------------------------
    -- Growth Metrics
    -------------------------------------------------

    SUBSCRIBERS_GAINED AS subscribers_gained,

    -------------------------------------------------
    -- Discovery Metrics
    -------------------------------------------------

    TRIM(TRAFFIC_SOURCE) AS traffic_source,

    CTR_PERCENTAGE AS click_through_rate,

    -------------------------------------------------
    -- Performance Metrics
    -------------------------------------------------

    IMPRESSIONS,

    LIKES,

    COMMENTS,

    SHARES,

    TOTAL_WATCH_TIME_HOURS AS total_watch_time_hours,

    -------------------------------------------------
    -- Classification
    -------------------------------------------------

    TRIM(CONTENT_CATEGORY) AS content_category

FROM {{ source('youtube_raw','RAW_YOUTUBE_VIDEOS') }}