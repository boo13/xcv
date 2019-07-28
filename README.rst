
**XCV**
===========
🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller

----

**The project's goal is to make game-based OpenCV experiments easier.**

By avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

-----------------------

.. image:: https://img.shields.io/travis/boo13/xcv.svg
   :target: https://img.shields.io/travis/boo13/xcv.svg
   :alt: Travis
 
.. image:: https://readthedocs.org/projects/xcv/badge/?version=latest
   :target: https://xcv.readthedocs.io
   :alt: Read the Docs
 
.. image:: https://img.shields.io/github/license/boo13/xcv
   :target: https://github.com/boo13/xcv/blob/master/LICENSE
   :alt: GitHub
    
.. image:: https://img.shields.io/github/repo-size/boo13/xcv
   :alt: GitHub repo size


:Authors: 👻
:Version: 0.1.0
:Documentation: https://xcv.readthedocs.io

----

What does XCV do?
=================

.. image:: blog/images/sampleImage.png

In-Game Tracking
================
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| Template Image                                                 | Template Name                      | Usage                                                                                                                                                                                                  | Size           | ROI |
+================================================================+====================================+========================================================================================================================================================================================================+================+=====+
| .. image:: templates/myTeamBadge.jpg                           | **My Team Badge**                  | Determine which side of the game sreen I am defending                                                                                                                                                  | *24px X 24px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/myTeamScoreboardName.png                  | **My Team Scoreboard Name**        | Determine which side of the scoreboard we're on, ``Game.HomeTeam`` or ``Game.AwayTeam`` And is currently the first indication that we are ``GameState.InGame``                                         | *25px X 8px*   |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/HomeScore/0.png                           | **Home Score**                     | Digits 0-11 currently used, matched via template matching with moderate success                                                                                                                        | *25px X 8px*   |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/HomeScore/0.png                           | **Away Score**                     | Digits 0-1 currently used, matched via template matching with not-so-great success                                                                                                                     | *25px X 8px*   |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+

.. image:: blog/images/screenshot_SinglePlayerMenu.png

Menu Tracking
=============
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| Template Image                                                 | Template Name                      | Usage                                                                                                                                                                                                                                                                                      | Size           | ROI |
+================================================================+====================================+============================================================================================================================================================================================================================================================================================+================+=====+
| .. image:: templates/SquadManagement.png                       | **Squad Management Menu**          | Indicates the Squad Management Screen                                                                                                                                                                                                                                                      | *22px X 13px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/Menu/InGameMenu_ResumeMatch_Off.png       | **In-Game Menu - OFF**             | Indicates the InGameMenu Screen. Also indicates if we are ``off`` the ``ResumeMatch`` button.                                                                                                                                                                                              | *30px X 30px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/Menu/InGameMenu_ResumeMatch_On.png        | **In-Game Menu - ON**              | Indicates the InGameMenu Screen. Also indicates if we are ``on`` the ``ResumeMatch`` button.                                                                                                                                                                                               | *30px X 30px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/45min.png                                 | **In-Game Menu - Half-Time**       | Matching this template indicates the InGameMenu Screen is at ``45.00``\ , it's not a perfect method for indicating if we are at Half-time (since pausing the game in stoppage time will send a false indication), but it's good-enough for now.                                            | *31px X 14px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/90min.png                                 | **In-Game Menu - Full-Time**       | Matching this template indicates the InGameMenu Screen is at ``90.00``\ , it's not perfect (see above.)                                                                                                                                                                                    | *31px X 14px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/StartBtn.png                              | **Pre-Game Start Menu**            | We see this screen in FUT>Single-Player Season>Pre-Game Menu. It is one of the rare instances that a menu screen requires pressing the ``Start`` button to continue. Matching this template indicates we are in ``GameState.PreGameStartMenu`` and we need to send ``xcontroller.Start`` | *128px X 27px* |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+
| .. image:: templates/HomeMenu_Cart.png                         | **FUT Home Menu**                  | We use the little shopping-cart icon in the top-right corner of the screen as our Main Menu indicator. Matching this template image indicates we are in ``GameState.FUTMainMenu``                                                                                                        | *16px X 13px*  |     |
+----------------------------------------------------------------+------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-----+

Hardware
=============

.. image:: blog/images/Pins_Image.jpg
   :alt: Pins_Image
 


CLI
=============

``python3 xcv``

Options:
  -v, --verbose                        Display debug information
  --port TEXT                          Controller port, default is /dev/cu.SLAB_USBtoUART
  -auto, --autopilot                   Initiate xcv sequence
  --push                               Enter button to push (A, B, X, Y, S, l, r, w, a, s, d, o, p)
  --count INTEGER                      Time in seconds before commands
  -dry, --dryrun                       For testing without xbox controller connected
  --help                               Show this message and exit.
  --debug                              List USB ports and check the serial connection


TO-DO
=====

- [ ] **GUI** - Re-implement HUD
- [ ] **GUI** - Implement new, framed, GUI (using PysimpleGui)
- [ ] **GUI** - Implement Button Press Received by Game Controller script (via Martin O'Hanlon)
- [ ] **README** - Add more screenshots
- [ ] **TESTS** - Get tests working again
- [ ] **CLI** - Implement Dry-Run
- [ ] **CLI** - Fix problem with Start button not responding (check wiring)
- [ ] **GAME** - In-Game Player Tracking


Thanks
=======

https://github.com/Sentdex/pygta5

I'm a big fan of @sentdex - his tutorials have helped me learn python for years now. I owe special thanks here though, his project 'python plays GTA V' series directly inspired me to figure out my own version of it, which started me on this journey.

https://github.com/jrosebr1/imutils

I use his FPS class from imutils. Also - I've learned a ton from @jrosebr1 and his site: http://www.pyimagesearch.com 

https://github.com/nefarius/ViGEm

I first tried to implement virtual controllers, such as this solution. Truth be told... this project came from my inability to get ViGEm to work.

https://github.com/elgertam/cookiecutter-pipenv

This package was created with a version of this Cookiecutter project template

https://www.stuffaboutcode.com

Martin O'Hanlon - For his class ``XboxController``, which I use for reading values from an xbox controller