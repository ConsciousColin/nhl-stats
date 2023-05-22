
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with player_game_stats as (

    select * from {{ source('nhl_stats', 'nhl_player_game_stats') }}

)

select  player_id, 
        season,
        avg(skaterStats_goals)      as goals, 
        avg(skaterStats_assists)    as assists, 
        -- avg(skaterStats_timeOnIce)  as time_on_ice,
        avg(skaterStats_shots)      as shots,

from player_game_stats

where player_position !='G'

group by 1, 2