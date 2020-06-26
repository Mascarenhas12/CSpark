# CSpark

Project's motivation:
  Chess position evaluations are based the best possible moves that engines can foresee 
  which leads innacurate evaluations for humans playing, especially when it is a timed match.
  This engine evaluation is more and more accurate as the player's skill increases and becomes a master, 
  however it's radically innacurate when it comes to the "average Joe".
  Furthermore, to the intermmediate player there might be confusion when they see the evaluation when there
  is no "apparent" mistake (i.e equal material and pieces) in the engine line's provided until a unreasonable
  ammount of moves for their rating.


Project methodology:
1st -> Defining objective:
(from a certain player's perspective)
    From a given chess position, owner's elo rating, elo differential, time remaining and time differential be able to provide a more accurate and representative estimation of the position's evaluation based on Stockfish 11, with said evaluation henceforth named CSE.

2nd -> Create neural network structure and code

3rd -> Create a small dataset for testing purposes

4th -> Create a big data set of different positions from chess game databases:
    Create scripts that extract positions from games

5th -> Survey players of different levels on positions (of a new big dataset) and collect owner's elo rating

6th -> Train CSpark on new training set with collected data

7th -> Create new dataset for CSpark to evaluate and collect its CSE

8th -> Review with peers and adapt CSpark to more accurately evaluate positions
