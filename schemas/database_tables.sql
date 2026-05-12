CREATE TABLE IF NOT EXISTS player_week (
    player_week_id INTEGER PRIMARY KEY,
    game_week_from INTEGER,
    game_week_to INTEGER
    season_year INTEGER,
    player_name TEXT,
    team TEXT, 
    pos TEXT,
    opp TEXT,
    fantasy_score REAL
);

CREATE TABLE IF NOT EXISTS passing (
    passing_id INTEGER PRIMARY KEY,
    player_week_id INTEGER,
    passing_yds INTEGER,
    passing_td INTEGER,
    passing_int INTEGER,
    FOREIGN KEY (player_week_id) REFERENCES player_week (player_week_id)
);

CREATE TABLE IF NOT EXISTS rushing (
    rushing_id INTEGER PRIMARY KEY,
    player_week_id INTEGER,
    rushing_yds INTEGER,
    rushing_td INTEGER,
    FOREIGN KEY (player_week_id) REFERENCES player_week (player_week_id)
);

CREATE TABLE IF NOT EXISTS receiving (
    receiving_id INTEGER PRIMARY KEY,
    player_week_id INTEGER,
    receiving_rec INTEGER,
    receiving_yds INTEGER,
    receiving_td INTEGER,
    FOREIGN KEY (player_week_id) REFERENCES player_week (player_week_id)
);

CREATE TABLE IF NOT EXISTS defense (
    defense_id INTEGER PRIMARY KEY,
    player_week_id INTEGER,
    defense_sck INTEGER,
    defense_int INTEGER,
    defense_ff INTEGER,
    defense_fr INTEGER,
    FOREIGN KEY (player_week_id) REFERENCES player_week(player_week_id)
);