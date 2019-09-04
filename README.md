# xword_solver
Solves a crossword puzzle. Well, kinda, for now.

## TODO: Various optimizations to improve accuracy / success
### High priority 
Pretty critical missing pieces of the current solution
   - [ ] optimized solving algorithm

### Low Priority:
Look [here](https://www.nytimes.com/guides/crosswords/how-to-solve-a-crossword-puzzle) 
for more details on what some of these refer to
   - [ ] data loading that doesn't break randomly
   - [ ] fill in the blank clues
   - [ ] abbreviations
   - [ ] match tense
   - [ ] part of speech
   - [ ] foreign languages
   - [ ] cross-referenced clues
   - [ ] partner clues
   - [ ] clues with ?
   - [ ] slang
   - [ ] "quotes" and [brackets]
   - [ ] Capitalized hints
   - [ ] Rebuses


## Creating the databse:
1. install neo4j and such
1. Use load_json.py with datasets from data_collection/xwordinfo/*.json


*Note: Got words from Princeton's WordNet. Properly cite them if/when I ever finish this project*
*Also cite [xwordinfo](https://www.xwordinfo.com/)*





