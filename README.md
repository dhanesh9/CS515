Name - Dhanesh Akolu

login - dakolu@stevens.edu

URL: https://github.com/dhanesh9/CS515


Description of the game-

Welcome to a thrilling adventure game! In this game, your mission is to find the hidden treasure in a room. However, there's a twist: you need to have a gun to take down the guard who's protecting the treasure, and a key to unlock the treasure chest. Don't forget to enter "get treasure" to add both the key and treasure to your inventory and win the game.

But be careful, there's a deadly shaft in the map. If you fall into it without a rope, you lose the game. So, be sure to stay alert and make wise choices. Are you ready for the challenge? Let's begin the game and see if you can succeed in this exciting quest!



1)an estimate of how many hours you spent on the project- 
- 8-10 hours

2)a description of how you tested your code

-I created different maps and kept testing all the maps including the one on Canvas. Finally, when I thought about my final map I implemented the win/lose conditions for the map
and checked all the edge cases. I executed my code using both command prompt and visual studio. I made sure everything works perfectly with the items, inventory and current room.


3)an example of a difficult issue or bug and how you resolved

- I wasn't able to run the code without passing the json file path but I had to read a lot to find out about 'argparse'. I fixed it using argparse

4)a list of the three extensions you’ve chosen to implement, with appropriate detail on them for the CAs to evaluate them (i.e., what are the new verbs/features, how do you exercise them, where are they in the map)

- I implemented drop(), help() and winning losing condition.
  i)Drop()- with the drop function we can drop the items from the inventory one by one. Once you drop the item in a specific room, that particular item gets appended in the current room's
          item list.
  ii)help() - this function shows all the commands that you can perform while playing the game.
  iii)Winning losing condition- Basically, when you reach the treasure room you need to have the key in your inventory to open the treasure chest and a gun to kill the guard who is 
	protecting the treasure. You can even kill the guard first and then go get the key from storage room, then traverse back to the treasure room and win the game. Remember that you need
	to use say 'get treasure' so that treasure and key are both in your inventory to win the game.
	For losing condition, I have implemented a shaft room, if you fall in the shaft room without picking up the rope which is in the armory room, you will lose. But if you have the rope 
	and you fall in the shaft you can survive and then use the exits in the shaft to traverse.


