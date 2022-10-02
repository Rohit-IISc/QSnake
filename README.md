# QSnake
This project is developed for Quantum Games Hackathon 2022 by our team Schrodinger's Kittens.

Team members :
  1. Aniruddha Sharma
  2. Kass Yassin
  3. Rohit Saini
  4. Santanu Banerjee
  5. Yuri Han

**Files:**

    1. QSnake.mp4        : Video presentation of ~5min explaining the concept and implementation.
    2. requirements.txt  : All the required libraries to be installed before running the following.
    3. SnakeQCAModule.py : Module containing QCA implementation using qiskit.
    4. QSnake.py         : Main file containg the game code.
    5. License           : MIT License as part of requirements.
    

**QSnake Rules**:

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
  
  ![1_KndgQpIlxcxxuIb9takepw](https://user-images.githubusercontent.com/56411951/193433968-a18c0ad2-cefb-4f3c-85f3-67543ce4441c.gif)

Quantum Implementation (this code can be found in SnakeQCAModule.py):

    Step 1: Initialized a 10 qubit circuit comprising of random X gate (to have initial state of 1 in some qubits) followed by H gate for superposition and CNOT gates for entanglement and interaction.
    Step 2: Unitary operator with random values of Theta, Phi and Lambda was defined to act upon the initial circuit.
  
  ![image](https://user-images.githubusercontent.com/56411951/193432248-f30d5d0b-e0ff-4d3c-86e5-0241330be36c.png)

  
    Step 3: At each time-step/iteration this unitary is multiplied to the previous state to get the next state, such that at step t: state = U(U(U(..t times(S)..))) where S was the initial state. After a certain number of iterations this step was slowing the process so we limited it to 15 time steps, post which a new initial state is initialised and Step 1-3 are repeated.
    Step 4: At each time-step the elements of final state-vector representation obtained were normalised using L2 distance.
    Step 5: These 1024 elements gave n unique amplitudes corresponding to each state.
    Step 6: As we only required 8 outcomes, we encoded these n unique amplitudes by sorting and indexing these amplitudes and then restricting the index between 0 & 7 and storing their respective frequencies out of 1024.
    Step 7: These indexes were then labelled alterating between poison and food, and then were encoded back using a 2 qubit system and RY gates as follows:
  
  ![image](https://user-images.githubusercontent.com/56411951/193432260-43ee345f-dc57-413a-923a-38bbf6afa56c.png)
  ![image](https://user-images.githubusercontent.com/56411951/193432270-1235293c-885f-4dd1-9e3e-9fe5a98347ab.png)
  
    Step 8: These states were then collapsed using measurement to get 2 poison and 1 food item.
    Step 9: Random cell coordinates were chosen to place these items on the grid, excluding the cells having snake or already chosen for another item.
    Step 10: Chosen items along with their X,Y coordinates were passed on to game module for game play.
  
Explanation to points 5,6:

  _**Consider these 1024 states to be houses, each house having a bulb/light of a different intensity. When we measure these intensities we find there are only n unique intensities spread across all these houses. We start counting the houses associated to each intensity and get the frequency distribution and then the corresponding probabilities. These probabilities were used as the probabilities of occurrance of each type of poison/food while all being in super-position until collapsed/measured.**_
  

Way Forward:

    1. Better UI-UX and a web app for the next version.
    2. Currently we used random.random module for choosing the cells to place the items, we intend to use Quantum variant of the same.
    3. We plan on using Quantum enhanced Reinforcement Learning to create an auto-pilot mode where the snake is left to play on it's on and learns to survive in the environment.
    4. Next we plan to optimise the auto-pilot mode for Hamiltonian cycle.
