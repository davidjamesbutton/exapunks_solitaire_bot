A spike to solve the ПАСЬЯНС (Solitare) mini-game in Exapunks


Inspiration:

https://www.youtube.com/watch?v=bkp6n52KBZ0
https://www.youtube.com/watch?v=ZFTDrvYOFHg
https://github.com/aaronrudkin/exapunks_solitaire_bot (greedy, 'best first' search)

About ПАСЬЯНС:

- Russian Solitare variant
- 9 stacks and 1 spare spaces
- 36 cards total:
    * 6-10 red x2 (10)
    * 6-10 black x2 (10)
    * Club black (4)
    * Space black (4)
    * Heart red (4)
    * Diamond red (4)
- Start with 4 cards on each stack and spare empty
- Valid move 1: card with lower value and opposite color is put below (e.g. 9R below 10B)
- Valid move 2: can place onto spare cell if empty
- Valid move 3: same suit place onto another card of same suit (e.g. HR onto HR)
- Strategies:
    * Try to empty a stack so you can place a 10 and descend
    * Try to empty a stack so you can place a suit and stack
- Stacks are locked when 4 of same suit or 10-6 are stacked
