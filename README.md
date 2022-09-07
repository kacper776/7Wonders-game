# 7 Cudów Świata
autor: kacper Solecki

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
