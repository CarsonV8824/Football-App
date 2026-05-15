# NFL Fantasy Football App

A Python web scraper that collects NFL fantasy football data and stores it in a SQLite database for analysis.

## Overview

This app scrapes player statistics from [Fantasy Data](https://fantasydata.com/nfl/fantasy-football-leaders?scope=game) and organizes it into a relational database. Data includes passing, rushing, receiving, and defense statistics for players across multiple seasons and weeks.

## Database

**Location:** `fantasy.db`

**Data Source:** [FantasyData.com](https://fantasydata.com/nfl/fantasy-football-leaders?scope=game)

### Tables

**player_week** - Main player statistics table
- `player_week_id` - Unique identifier (Primary Key)
- `rank` - Player ranking for that week
- `game_week_from` - Starting week
- `game_week_to` - Ending week
- `season_year` - Year of the season
- `player_name` - Player name
- `team` - Team abbreviation
- `pos` - Position (QB, RB, WR, etc.)
- `opp` - Opponent team
- `fantasy_score` - Total fantasy points (PPR scoring)

**passing** - Passing statistics (Foreign Key: player_week_id)
- `passing_yds` - Passing yards
- `passing_td` - Passing touchdowns
- `passing_int` - Interceptions

**rushing** - Rushing statistics (Foreign Key: player_week_id)
- `rushing_yds` - Rushing yards
- `rushing_td` - Rushing touchdowns

**receiving** - Receiving statistics (Foreign Key: player_week_id)
- `receiving_rec` - Receptions
- `receiving_yds` - Receiving yards
- `receiving_td` - Receiving touchdowns

**defense** - Defense statistics (Foreign Key: player_week_id)
- `defense_sck` - Sacks
- `defense_int` - Interceptions
- `defense_ff` - Forced fumbles
- `defense_fr` - Fumble recoveries

## Setup

1. Create a virtual environment with a working local Python install:
```bash
python -m venv .venv
```

2. Activate it:
```bash
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

If you are on Windows without an Intel XPU setup, keep the default CPU PyTorch build. Do not install the `xpu` wheel unless you specifically need Intel GPU acceleration and have the required runtime libraries installed.

4. Create the database:
```python
from database import Database
Database.create_tables()
```

5. Run the scraper:
```bash
python scrape.py
```

## Files

- `database.py` - Database connection and insert logic
- `scrape.py` - Web scraper for FantasyData
- `fantasy schemas/database_tables.sql` - SQL schema definitions

- defense_sck

- defense_int

- defense_ff

- defense_fr

## model element

**Users Input:**

- Passing stats

- Rushing stats

- Receiving stats

- Defensive stats

- Position

- Team

- opp team

- amount of years of player

**Output:**

- Predicted Fantasy Points

- Predicted Fantasy Points Per Game

- Predicted Rank (you calculate this by sorting predictions)
