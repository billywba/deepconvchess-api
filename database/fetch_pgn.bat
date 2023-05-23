@echo off

set chess_username=%1
if [%chess_username%]==[] (
    echo Username must be provided as argument
    exit /b 0
)

set year=%2
if [%year%]==[] (
    echo Year must be provided as argument
    exit /b 0
)

echo Fetching chess.com games for: %chess_username%

FOR /L %%i in (1, 1, 12) DO (
    curl -o %CD%/pgn/chesscom_%chess_username%_%year%%%i.pgn --create-dirs https://api.chess.com/pub/player/%chess_username%/games/%year%/%%i/pgn 
)
