{{ config(materialized='external', format='parquet')}}


with player_game_stats as (

    select * from {{ ref('skater_game_stats') }}

)

select  player_id, 
        season,
        avg(goals)      as avg_goals,
        avg(assists)    as avg_assists, 
        -- avg(skaterStats_timeOnIce)  as time_on_ice,
        avg(shots)      as avg_shots,

from player_game_stats

group by 1, 2