{{ config(
    materialized='view'
) }}

SELECT
    *,
    'existing' AS source_batch

FROM {{ ref('stg_youtube_videos') }}

UNION ALL

SELECT
    *,
    '2023' AS source_batch

FROM {{ ref('stg_youtube_videos_2023') }}