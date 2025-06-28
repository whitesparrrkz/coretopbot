# Coretop Discord Bot

This is a bot made with py-cord for my Friends and I to use as a leaderboard for **Geometry Dash** levels we have completed with some other fun commands.

Pretty much, the main idea of the bot is that you are able to upload a level, give it a position on the leaderboard, and then assign victors to those levels. 
This would show off the hardest levels we have completed, who has beaten the most levels, stuff like that!  
  
And, some other cool things, like a level guessing game *(Similiar to Sparky, but it randomly downloads frames from a completion video, and turns it into a gif).*

## Main (Useful) Commands
### Level
All of these commands have something to do with levels  
(BTW position means where a level is ranked on the leaderboard.)  
- Get Level by Position (Type in a levels position to get info about the level, and the videos thumbnail)  
![](https://i.imgur.com/YD20mQK.png)
- List Levels (lists out levels in order from hardest to easiest, 10 at a time)  
![](https://i.imgur.com/08x9SKB.png)
- Add Level (it brings up a modal, where you type out the level info and then sends to the db)
![](https://i.imgur.com/WRduvmj.png)
- Delete Level (simple delete command, deletes a level given its position)  
![](https://i.imgur.com/Adupw2U.png)
---
### Victor
All of these commands have something to do with victors/players  
- Add Victor by Level Position (Adds a victor to a certain level)  
![](https://i.imgur.com/19xFw8t.png)
- Get Victor (Gets information about a certain player)   
![](https://i.imgur.com/x68o7oH.png)
---
### Silly
The commands in here are meant for fun stuff and games, and currently contains the **level guessing game**.  
  
The guessing game randomly takes a random level off of the list and takes random frame(s) from a video of the level.
Then, under a time limit, people can try to guess the name of the level for points!!!!  
*This one is honestly my favorite command and it took quite a bit of time to make.*
- Play Guesser (Starts a game of guesser)  
<img src="https://i.imgur.com/WDaPaKD.gif" height="600">
sorry for the poor quality

## Other

Thanks to my friends for helping me out with ideas and stuff, and especially Benn (the Best!!) *(he wrote like 2 lines of code)*
  
The requirements for this project are in are in **requirements.txt**.  
Its also needed to install **gifski** and add a path variable to the directory containing the binary (this is for the guessing game).  

thanks
