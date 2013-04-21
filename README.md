Moonlander Project using Fuzzy Logic
==================
Artificial Intelligence 
-----------------------
* CS470/570 
* Spring 2013
* Project #3b
* Due: Wednesday, April 19th

Project: Create a Fuzzy Logic controller to safely land the moonlander from Project 3a.

The moonlander is controlled by setting the 'burn' and 'thrust'. Burn controls vertical movement and thrust controls the horizontal movement. Both values are set in the control() function within the lander class. Your goal is to fill in the conrol() function with an Fuzzy Control system that safely lands the moonlander - as often as possible.

Requirements:
-------------
At a minimum the cotrol system should have fuzzy inputs for height, position (left, right), and velocity (horizontal and vertical). You may also want to include inputs for acceleration, fuel remaining, and windspeed, but it is not necessary.

Each of these inputs must be fuzzified. For example, the height of the moonlander must be mapped into fuzzy sets such as, high, medium, low. The exact number of fuzzy sets, their shapes, and boundries, is all up to you. You will probably need to modify them in some way (by-hand, local search, etc.) to improve landing performance.

Your fuzzy controller should (usually) result in multiple command 'recommendations' that need to be combined/defuzzified. For example, a typical fuzzy control, under some conditions, might recommend: high burn: 0.7 AND low burn: 0.3.

Your system will need to combine these recommendations in some consistant way.

Algorithms:
-----------
The program must use a fuzzy control system. You may adjust the fuzzy rules as you see fit.

Hand-In:
--------
You need to hand in typed write-up containing the following:

* An abstract summarizing what you did and what the results were.
* An algorithm section explaining your fuzzy controller. Including,
    * A description of the fuzy sets used - preferably graphical.
    * A description of the fuzzy rules.
    * A description of the defuzzification technique.
* A results section. Including,
    * A presentation of the 'average' results. E.g. what was the success rate?
    * A comparison to the ANN from Project #3a
    * A discussion of how the program behaved. Did it have any strengths or weaknesses?
    * A conclusion section.
