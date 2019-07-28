
# **XCV**

![Travis](https://img.shields.io/travis/boo13/xcv.svg) ![Read the Docs](https://readthedocs.org/projects/xcv/badge/?version=latest) ![GitHub](https://img.shields.io/github/license/boo13/xcv) ![GitHub repo size](https://img.shields.io/github/repo-size/boo13/xcv)
___

🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller

*__The project's goal is to make OpenCV experiments easier, by avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.__*

* Free software: MIT license
* Documentation: https://xcv.readthedocs.io.

___
# What does XCV do?
___

![sampleImage.png](/blog/images/sampleImage.png)

# In-Game Tracking

| Template Image  | Template Name  | Usage |  Size | ROI |
|---|---|---|---|---|
|![myTeamBadge.jpg](/templates/myTeamBadge.jpg) | **My Team Badge** | Determine which side of the game sreen I am defending | _24px X 24px_
|![myTeamScoreboardName.png](/templates/myTeamScoreboardName.png) | **My Scoreboard Name** | Determine which side of the scoreboard we're on, `Game.HomeTeam` or `Game.AwayTeam` And is currently the first indication that we are `GameState.InGame` | _25px X 8px_
|  | **Home Score** | Digits 0-11 currently used, matched via template matching with moderate success |  | |
|  | **Away Score** | Digits 0-1 currently used, matched via template matching with not-so-great success |  | |
___

# Menu Tracking
| Template Image  | Template Name  | Usage |  Size | ROI |
|---|---|---|---|---|
|![SquadManagement.png](/templates/SquadManagement.png) | **Squad Management Menu** | Indicates the Squad Management Screen | _22px X 13px_ |  |
|![InGameMenu_ResumeMatch_Off.png](/templates/Menu/InGameMenu_ResumeMatch_Off.png) | **In-Game Menu - OFF**  | Indicates the InGameMenu Screen. Also indicates if we are `off` the `ResumeMatch` button. | _30px X 30px_ |  |
|![InGameMenu_ResumeMatch_On.png](/templates/Menu/InGameMenu_ResumeMatch_On.png) | **In-Game Menu - OFF**  | Indicates the InGameMenu Screen. Also indicates if we are `on` the `ResumeMatch` button. | _30px X 30px_ |  |
| ![45min.png](/templates/45min.png) | **In-Game Menu - Half-Time** | Matching this template indicates the InGameMenu Screen is at `45.00`, it's not a perfect method for indicating if we are at Half-time (since pausing the game in stoppage time will send a false indication), but it's good-enough for now. | _31px X 14px_ |
|![90min.png](/templates/90min.png) | **In-Game Menu - Full-Time** | Matching this template indicates the InGameMenu Screen is at `90.00`, it's not perfect (see above.) | _31px X 14px_ | |
|![StartBtn.png](/templates/StartBtn.png) | **Pre-Game Start Menu** | _We see this screen in FUT>Single-Player Season>Pre-Game Menu. It is one of the rare instances that a menu screen requires pressing the `Start` button to continue._ Matching this template indicates we are in `GameState.PreGameStartMenu` and we need to send `xcontroller.Start` | _128px X 27px_ | |
|![HomeMenu_Cart.png](/templates/HomeMenu_Cart.png) | **FUT Home Menu** | _We use the little shopping-cart icon in the top-right corner of the screen as our Main Menu indicator._ Matching this template image indicates we are in `GameState.FUTMainMenu` | _16px X 13px_ |  |

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

- [X] Reliably detect FIFA's game mode (In Menu, In Game, etc.)  
- [X] Get caught up on documenting the README

# Credits

* <https://github.com/Sentdex/pygta5> - _I'm a big fan of @sentdex - his tutorials have helped me learn python for years now. I owe special thanks here though, his project 'python plays GTA V' series directly inspired me to figure out my own version of it, which started me on this journey._
* <https://github.com/nefarius/ViGEm> - _I first tried to implement virtual controllers, such as this solution. Truth be told... this project came from my inability to get ViGEm to work._
* <https://github.com/elgertam/cookiecutter-pipenv> - _This package was created with a version of this Cookiecutter project template_
