{{ config(
    materialized='table'
) }}

SELECT

    upload_year,
    upload_month,

    COUNT(video_id) AS total_videos,

    SUM(impressions) AS total_impressions,

    SUM(likes) AS total_likes,

    SUM(comments) AS total_comments,

    SUM(shares) AS total_shares,

    SUM(subscribers_gained) AS total_subscribers_gained,

    SUM(total_watch_time_hours) AS total_watch_time_hours,

    ROUND(AVG(click_through_rate),2) AS avg_ctr,

    ROUND(AVG(avg_view_duration_seconds),2) AS avg_view_duration_seconds,

    ROUND(AVG(avg_view_percentage),2) AS avg_view_percentage,

    ROUND(AVG(engagement_rate),2) AS avg_engagement_rate,

    ROUND(AVG(subscriber_conversion_rate),2) AS avg_subscriber_conversion_rate

FROM {{ ref('int_video_metrics') }}

GROUP BY
    upload_year,
    upload_month

ORDER BY
    upload_year,
    upload_month