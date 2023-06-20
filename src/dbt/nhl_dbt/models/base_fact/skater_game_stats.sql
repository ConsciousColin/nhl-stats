{{ config(materialized='external', format='parquet')}}


with src_player_game_stats as (

    select * from {{ source('nhl_stats', 'player_game_stats') }}
    where player_position !='G'
)

select
        game_id,
        game_date,
        season,
        team_id,
        team_name,
        is_away,
        player_id,
        player_type,
        player_position,
        skaterStats_timeOnIce             as time_on_ice,
        skaterStats_assists               as assists,
        skaterStats_goals                 as goals,
        skaterStats_shots                 as shots,
        skaterStats_hits                  as hits,
        skaterStats_powerPlayGoals        as power_play_goals,
        skaterStats_powerPlayAssists      as power_play_assists,
        skaterStats_penaltyMinutes        as penalty_minutes,
        skaterStats_faceOffWins           as face_off_wins,
        skaterStats_faceoffTaken          as face_off_taken,
        skaterStats_takeaways             as takeaways,
        skaterStats_giveaways             as giveaways,
        skaterStats_shortHandedGoals      as short_handed_goals,
        skaterStats_shortHandedAssists    as short_handed_assists,
        skaterStats_blocked               as blocked,
        skaterStats_plusMinus             as plus_minus,
        skaterStats_evenTimeOnIce         as even_time_on_ice,
        skaterStats_powerPlayTimeOnIce    as power_play_time_on_ice,
        skaterStats_shortHandedTimeOnIce  as short_handed_time_on_ice,
        skaterStats_faceOffPct            as face_off_pct
        
from  src_player_game_stats