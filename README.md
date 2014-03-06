The SFGame Project
==================

This is a game project, written in python, using pygame, to setup a 
game engine for a board (tile-based), 2D, turn-based game, having the following goals:

- Learn game development and components.
- Use mathematical procedures to optimize code.
- Build an engine flexible enough to be extended for different purposes. 
This will be part of a random generator game, based on small story scripts to generate
random levels and players. 

One other major goal is to document the learning process and procedures 
As part of this learning process, here are some fields that may be explored:
 
`Time-based movement`_
`Sprite Rendering`_
`Matrices and linear algebra`_ (may include some `Image Treatment` procedures)
`Procedural Generated Content`_

Others will be filled in as the process goes on.

It uses:
- python 2.7
- pygame 1.9
- numpy and scipy

At first I'm not considering online, multiplayer purposes, but as the project evolves,
this could be added in.

The initial purpose now is to develop the base engine, but can be considered in a near
future:
- Use of `OpenGL` (3D project in 2D)
- Portability to Mobile, Android in particular

Installation
------------

For now, just get the source code using::
  git clone <project url>
  
and run::
  cd sfgame
  python game.py
  
This will be improved along the process

Issues
------
This project is beginning stage and everyone is invited to learn from it, use it
and contribute. Feel free to open issues on Github, email me or using at
*#sfgame* in FreeNode


Learning Process
----------------
Procedures and articles will be linked from this README or from the internal README
in each package, which contain how classes are organized, what techniques are used
for some methods and other interesting information. 

The goal is to have a tutorial guide that curious people may easily learn from it, 
and also help people who are willing to use or contribute to this code.

References
----------

.. _`Python game tutorial`: http://thepythongamebook.com/en:pygame:start
.. _`Time-based movement`
.. _`Sprite Rendering`: http://programarcadegames.com/python_examples/sprite_sheets/ 
.. _`Matrices and linear algebra`: http://wiki.scipy.org/Tentative_NumPy_Tutorial
.. _`Image Treatment`: http://scipy-lectures.github.io/advanced/image_processing/
.. _`Procedural Generated Content`: http://www.gamasutra.com/blogs/TanyaXShort/20140204/209176/Level_Design_in_Procedural_Generation.php
