{{ config(
    materialized='view'
) }}

SELECT

    -- Primary Key
    video_id,

    -- Date
    upload_timestamp,
    YEAR(upload_timestamp)        AS upload_year,
    MONTH(upload_timestamp)       AS upload_month,
    QUARTER(upload_timestamp)     AS upload_quarter,
    DAYNAME(upload_timestamp)     AS upload_day_of_week,

    -- Video Metrics
    video_duration_minutes,
    avg_view_duration_seconds,
    avg_view_percentage,

    -- Raw Metrics
    impressions,
    likes,
    comments,
    shares,
    click_through_rate,
    subscribers_gained,
    total_watch_time_hours,

    traffic_source,
    content_category,

    ----------------------------------------------------
    -- Business Metrics
    ----------------------------------------------------

    (likes + comments + shares) AS engagement,

    ROUND(
        ((likes + comments + shares) * 100.0)
        / NULLIF(impressions,0),
        2
    ) AS engagement_rate,

    ROUND(
        (likes * 100.0)
        / NULLIF(impressions,0),
        2
    ) AS like_rate,

    ROUND(
        (comments * 100.0)
        / NULLIF(impressions,0),
        2
    ) AS comment_rate,

    ROUND(
        (shares * 100.0)
        / NULLIF(impressions,0),
        2
    ) AS share_rate,

    ROUND(
        (subscribers_gained * 100.0)
        / NULLIF(impressions,0),
        2
    ) AS subscriber_conversion_rate,

    ROUND(
        total_watch_time_hours
        / NULLIF(impressions,0),
        4
    ) AS watch_time_per_impression

FROM {{ ref('stg_youtube_videos') }}