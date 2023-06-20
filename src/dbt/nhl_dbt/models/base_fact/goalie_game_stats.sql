{{ config(materialized='external', format='parquet')}}


with src_player_game_stats as (

    select * from {{ source('nhl_stats', 'player_game_stats') }}
    where player_position =='G'
)

select
        game_id,
        game_date,
        season,
        team_id,
        team_name,
        is_away,
        player_id,
        goalieStats_timeOnIce                     as time_on_ice,
        goalieStats_assists                       as assists,
        goalieStats_goals                         as goals,
        goalieStats_pim                           as pim,
        goalieStats_shots                         as shots,
        goalieStats_saves                         as saves,
        goalieStats_powerPlaySaves                as power_play_saves,
        goalieStats_shortHandedSaves              as short_handed_saves,
        goalieStats_evenSaves                     as even_saves,
        goalieStats_shortHandedShotsAgainst       as short_handed_shots_against,
        goalieStats_evenShotsAgainst              as even_shots_against,
        goalieStats_powerPlayShotsAgainst         as power_play_shots_against,
        goalieStats_decision                      as decision,
        goalieStats_savePercentage                as save_percentage,
        goalieStats_powerPlaySavePercentage       as power_play_save_percentage,
        goalieStats_shortHandedSavePercentage     as short_handed_save_percentage,
        goalieStats_evenStrengthSavePercentage    as even_strength_save_percentage
        
from  src_player_game_stats