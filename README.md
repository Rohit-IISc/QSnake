# QSnake
This project is developed for Quantum Games Hackathon 2022 by our team Schrodinger's Kittens.
Team members :
  1. Aniruddha Sharma
  2. Kass Yassin
  3. Rohit Saini
  4. Santanu Banerjee
  5. Yuri Han

Before running the main files please make sure you have all the required libraries in requirements.txt installed.

QSnake Rules:
Most of the rules are similar to that of classical snake game:

a. The player uses the arrow keys to move the "snake" around the board.

b. As the snake finds food, it eats the food, and thereby grows larger.

c. The game ends when the snake either moves off the screen or moves into itself.

d. The goal is to make the snake as large as possible before the game ends.

To increase the complexity of the game we modified the rules:

e. Instead of only 1 food as in classical game, we have added 2 poisons to the board.

f. There are 4 types of food which work as following when consumed iff there are no curses accumulated, otherwise curse count decreases by 1:
          i.    Mustard       : Increases the length of snake by 1 unit.
          ii.   White         : Increases the length of snake by 1 unit and updates the "stealth" count to 2.
          iii.  Green         : Increases the length of snake by 4 units.
          iv.   Dark Green    : Increases the length of snake by 15 units.
 g. There are 4 types of poisons which work as following when consumed iff there are no stealths accumulated, otherwise stealth count decreases by 1:
          i.    Pink          : Decreases the length of snake by 1 unit.
          ii.   Purple        : Decreases the length of snake by 1 unit and updates the "curse" count to 2.
          iii.  Orange        : Decreases the length of snake by 4 units.
          iv.   Red           : Instant Death/Game over.
h. Whenever an item is consumed, game environment resets itself with new positions of 1 food and 2 poisons.

Following is the interface:
  Top left corner shows Score, Stealth and Curses accumulated.
  There's one stealth food(white), one curse poison (purple) and one death poison (red) in the state below.
![image](https://user-images.githubusercontent.com/56411951/193431319-45024466-967c-41c6-89e8-5ded30641b1a.png)


Where's the Quantum Part?
  We have used a variation of QCA(Quantum Cellular Automaton) devised in analogy to conventional models of cellular automata introduced by John von Neumann, wherein
  each cell changes state as a function of time, according to a defined set of rules driven by the states of neighboring cells. 
  
  ![image](https://user-images.githubusercontent.com/56411951/193431523-575e6b6e-0523-4485-ab57-60f2c246406b.png)
