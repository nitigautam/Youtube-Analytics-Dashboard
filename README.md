# Youtube-Analytics-Platform
End-to-end YouTube analytics platform using Snowflake, dbt, Streamlit in Snowflake, Cortex and Snowflake Cortex Analyst.

## Overview

The YouTube Analytics Dashboard is an end-to-end data engineering project built on the Snowflake Data Cloud. It demonstrates how raw analytical data can be transformed into meaningful business insights using modern ELT practices and interactive dashboards.

The project uses dbt to build a scalable transformation pipeline, Snowflake as the cloud data warehouse, and Snowflake Native Streamlit to create an interactive dashboard for analyzing YouTube channel performance.

The objective is to simulate how organizations collect, transform, and analyze large volumes of analytical data to support data-driven decision making.


## Problem Statement

YouTube creators and marketing teams often rely on multiple reports to monitor channel performance. Raw analytics data contains thousands of records that are difficult to analyze directly.

This project centralizes the data into Snowflake, transforms it into business-ready datasets using dbt, and presents key performance metrics through an interactive dashboard.


## Solution

The solution follows a modern ELT architecture.

- Load raw YouTube analytics data into Snowflake.
- Transform and clean the data using dbt.
- Build analytics-ready data models.
- Visualize insights using Snowflake Native Streamlit.
- Enables AI-powered conversational analytics using Snowflake Cortex Analyst
- Maintain the project using Git and GitHub.



## Architecture

```
Dataset
   │
   ▼
Snowflake
   │
   ▼
dbt Transformation Layer
(Staging → Intermediate → Mart)
   │
   ▼
Business Ready Tables
   │
   ▼
Snowflake Native Streamlit Dashboard 
Snowflake Cortex Analyst AI
```



## Technologies Used

- Snowflake Data Cloud
- dbt Core
- SQL
- Snowflake Native Streamlit
- Snowflake Cortex Analyst
- YAML Semantic Model
- Git & GitHub


## Features

The dashboard provides insights into:

- Overall channel performance
- Video performance analysis
- Audience engagement
- Watch time trends
- Revenue analysis
- Subscriber growth
- Traffic source analysis
- Geographic distribution
- Device usage analytics
- Interactive filtering and KPI tracking


## Data Pipeline

The project follows a layered transformation approach.

### Raw Layer

Stores the original dataset without modification.

### Staging Layer

- Data cleaning
- Data type conversion
- Standardized column names
- Basic transformations

### Intermediate Layer

- Business calculations
- Aggregations
- Derived metrics
- Data enrichment

### Mart Layer

Creates analytics-ready tables optimized for dashboard reporting.



### Dashboard

The dashboard enables users to explore YouTube analytics through interactive visualizations and business KPIs.

Some of the key metrics include:

- Total Views
- Watch Time
- Subscribers Gained
- Revenue
- Click Through Rate (CTR)
- Average View Duration
- Engagement Rate
- Likes
- Comments
- Shares

### Snowflake Cortex Analyst

To extend traditional dashboarding capabilities, the project integrates **Snowflake Cortex Analyst**.

A semantic model was created using YAML that enables business users to query data using natural language instead of writing SQL.

The semantic model is built on the Mart layer and exposes business-friendly metrics and dimensions to Cortex Analyst.

### Semantic Model

The semantic model contains:

- Business Dimensions
- Facts
- Metrics
- Descriptions
- Verified Queries

This enables Cortex Analyst to understand business terminology and automatically generate SQL queries.



### Example Questions

Users can ask questions such as:

- Which month had the highest engagement rate?
- What is the total watch time this year?
- Which year generated the highest impressions?
- What is the average CTR?
- Compare yearly subscriber growth.
- Which upload month generated the highest revenue?
- Show monthly watch time trends.
- Which videos generated the highest engagement?

## Key Features

- End-to-End ELT Pipeline
- Cloud Data Warehouse
- dbt Data Modeling
- SQL-based Transformations
- Interactive Business Dashboard
- AI-powered Natural Language Analytics
- Semantic Modeling using YAML
- Modern Data Engineering Workflow
- Version Control using Git and GitHub


## Future Improvements

Potential enhancements include:

- Automated data ingestion using Snowpipe
- CI/CD integration with GitHub Actions
- Data quality testing using dbt tests
- Data Quality Monitoring

## Learning Outcomes

This project demonstrates practical knowledge of:

- Cloud Data Warehousing
- Data Modeling with dbt
- ELT Pipeline Development
- SQL-based Data Transformation
- Interactive Dashboard Development
- Version Control using Git
- End-to-End Data Engineering Workflows





