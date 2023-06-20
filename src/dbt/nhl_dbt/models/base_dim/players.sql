{{ config(materialized='external', format='parquet')}}

with src as (
    select * from {{ source('nhl_stats', 'nhl_players') }}
)

select * from src