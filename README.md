# googlefeud-mc
A multiple choice version of the game Google Feud

Disclaimer: I do not own Google Feud, nor Family Feud.

How to use:
1. To add questions, add a text file in the questions folder. The filename doesn't matter.
1. The first line of the question files should be the prompt, followed by the top 15 Google results in order from the most searched to the least.
1. Run main.py

Description:
A multiple choice version of the game Google Feud.
The main reason for this is that the online Google Feud game
uses an open ended response, but I wanted it to be a multiple choice
grid when I used it as a church youth ministry game.
Furthermore, I wanted to make sure nothing too spicy came up in 
either the questions or the answers, which is the main reason why I went 
for manually creating the questions and answers over trying to make an 
automated system to get the top Google results. That and also I wanted to 
make sure it can still work if my internet connection dropped.
Also, note that I was still very inexperienced when I made this, so a lot of sizing 
used hard-coded numbers instead of scaling to screen. 
I kept these values towards the top of guistudd.py (XMARGIN, YMARGIN, CELL_WIDTH).

Requirements:
All requirements should be included in most Python distributions.
Notably I used Tkinter for the GUI, 
random to shuffle the tiles, and 
functools' partial to help with making the callbacks for buttons.