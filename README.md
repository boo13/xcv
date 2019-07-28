
# xcv

![Travis](https://img.shields.io/travis/boo13/xcv.svg) ![Read the Docs](https://readthedocs.org/projects/xcv/badge/?version=latest) ![GitHub](https://img.shields.io/github/license/boo13/xcv) ![GitHub repo size](https://img.shields.io/github/repo-size/boo13/xcv)
___

🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller

*__The project's goal is to make OpenCV experiments easier, by avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.__*

* Free software: MIT license
* Documentation: https://xcv.readthedocs.io.

# Features

# In-Game Tracking
![sampleImage.png](/blog/images/sampleImage.png)
___
![myTeamBadge.jpg](/templates/myTeamBadge.jpg) **My Team Badge**

Matching this template image shows me...

* which side of the game sreen I am defending

Size: _24px X 24px_

___
![myTeamScoreboardName.png](/templates/myTeamScoreboardName.png) **My Scoreboard Name**

Matching this template image shows me...

* which side of the scoreboard I'm on
* if I'm `Game.HomeTeam` or `Game.AwayTeam`
* and is currently the first indication that we are `GameState.InGame`

Size: _25px X 8px_

___

# Menu Tracking

![SquadManagement.png](/templates/SquadManagement.png) **Squad Management Menu**

Matching this template indicates the Squad Management Screen

Size: _22px X 13px_

___
![InGameMenu_ResumeMatch_Off.png](/templates/Menu/InGameMenu_ResumeMatch_Off.png) Off ![InGameMenu_ResumeMatch_On.png](/templates/Menu/InGameMenu_ResumeMatch_On.png) On **In-Game Menu**

Matching this template indicates the InGameMenu Screen

Also indicates if we are `off` or `on` the `ResumeMatch` button

Size: _30px X 30px_

___
![45min.png](/templates/45min.png) **In-Game Menu - Half-Time**

Matching this template indicates the InGameMenu Screen is at `45.00`, it's not a perfect method for indicating if we are at Half-time (since pausing the game in stoppage time will send a false indication), but it's good-enough for now.

Size: _31px X 14px_

___

![90min.png](/templates/90min.png) **In-Game Menu - Full-Time**

Matching this template indicates the InGameMenu Screen is at `90.00`, it's not perfect (see above.)


Size: _31px X 14px_

___
![StartBtn.png](/templates/StartBtn.png) **Pre-Game Start Menu**

_We see this screen in FUT>Single-Player Season>Pre-Game Menu. It is one of the rare instances that a menu screen requires pressing the `Start` button to continue._

Matching this template image shows me...

* We are in `GameState.PreGameStartMenu`
* Indicates we need to send `xcontroller.Start`

Size: _128px X 27px_

___
![HomeMenu_Cart.png](/templates/HomeMenu_Cart.png) **FUT Home Menu**

_We use the little shopping-cart icon in the top-right corner of the screen as our Main Menu indicator._

Matching this template image shows me...

* Indicates we are in `GameState.FUTMainMenu`

Size: _16px X 13px_


# TO-DO

### General To Do

- [ ] Re-implement HUD
- [ ] Implement GUI
- [ ] Implement Button Press Received by Game Controller script (via Martin O'Hanlon)
- [ ] Add more photos
- [ ] Get tests working again

### CLI To Do

- [ ] Implement Dry-Run
- [ ] Fix problem with Start button not responding (check wiring)

### Game To Do

- [ ] In-Game Player Tracking

## DONE

[X] Reliably detect FIFA's game mode (In Menu, In Game, etc.)  
[X] Get caught up on documenting the README

# Credits

* <https://github.com/elgertam/cookiecutter-pipenv> - This package was created with a version of this Cookiecutter project template_
* <https://github.com/Sentdex/pygta5> - I just loved this project and tutorial series Sentdex put together. He's helped me learn python over the years, but this project felt like something I wanted to do my own version of, with a different game, and that started me on this journey._
* <https://github.com/nefarius/ViGEm> - I first tried to implement virtual controllers, such as this solution. Truth be told this project idea came from my inability to get ViGEm to work._
