# 7 Cudów Świata | 7 Wonders
autor: kacper Solecki
A simple terminal-controlled implementation of & Wonders (https://boardgamegeek.com/boardgame/68448/7-wonders) board game.

## Aby uruchomić grę:

1) Sklonuj repozytorium
2) W katalogu game/ uruchom komend
  python main.py [--verbose VERBOSE] [--num_games NUM_GAMES] [--p P] [--m M] [players ...]
  
  gdzie VERBOSE $\in$ {0, 1} to opcja wypisywania wszystkich ruchów,
  
  NUM_GAMES to liczba gier do rozegrania,
  
  P to limit czsowy w sekundach na przygotowanie się agentów przed grą,
  
  M to limit czsowy agentów na wykonanie ruchu,
  
  players to (przynajmniej 3, co najwyżej 7) liczby oznaczające numery agentów, którzy mają brać udział w rozgrywce:
  
  | Gracz ludzki | Agent prawie losowy  | Agent Monte Carlo | Agent oceniający ruchy | Agent OPPS | Agent testowy |
  | --------     | --------             | --------          | -------                | ------     | ------        |
  | 0            | 1                    | 2                 | 3                      | 4          | 5             |

## To play the game:

1) Clone repository
2) In game/ catalog run
  python main.py [--verbose VERBOSE] [--num_games NUM_GAMES] [--p P] [--m M] [players ...]
  
  where VERBOSE $\in$ {0, 1} is option to display all moves,
  
  NUM_GAMES is the number of games to be played,
  
  P is time limit in seconds for agents to prepare before game,
  
  M is time limit in seconds for agents to choose move,
  
  players are (at least 3, at most 7) numbers describing which agents should play:
  
  | Human | Almost Random Agent  | Monte Carlo Agent | Move Evaluating Agent | OPPS Agent | Test Agent |
  | --------     | --------             | --------          | -------                | ------     | ------        |
  | 0            | 1                    | 2                 | 3                      | 4          | 5             |
