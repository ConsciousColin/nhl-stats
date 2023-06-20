{{ config(materialized='external', format='parquet')}}

with src as (
    select * from {{ source('nhl_stats', 'game_boxscores') }}
)

select 
        game_id,
        game_date::date as game_date,
        season,
        case when away_team_goals > home_team_goals
                then away_team_id
                else home_team_id
                end as winning_team_id,
        case when away_team_goals > home_team_goals
                then home_team_id
                else away_team_id
                end as losing_team_id        

from src
