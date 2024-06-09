# Chess Engine
This chess engine is fully based on python with no module but random. It uses a weird notation created fully by me. I hope to get it better.
## How it works
Basically, it just lists every possible move in a specific board and then evaluates every board with preset weights. For now:
```
PIECE_EVAL_MULTIPLIER = 1
CHECK_EVAL_MULTIPLIER = 0.5
PROTECTED_TILE_EVAL_MULTIPLIER = 0.05
ENEMY_PROTECTED_TILE_EVAL_MULTIPLIER = -0.05
HANGING_PIECE_EVAL_MULTIPLIER = -0.75
ENEMY_HANGING_PIECE_EVAL_MULTIPLIER = 0.25
```
It is not actually done yet. However it is already able to play chess (it doesn't play well obviously).

Its current elo based on a chess.com account I have created for it is **350**. I hope to get it to 500 soon by improving the evaluation function and adding more parameters.