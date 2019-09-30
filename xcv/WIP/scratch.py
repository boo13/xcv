def countdown(secs):

    # if secs is 0:  # In case we pass in a 0 from CLI
    #     logger.info(rocketLaunchList[3])
    # else:
    #     logger.info(launch)

    # rocketLaunch = [
    #     "... ",
    #     " .. ",
    #     "  . ",
    #     "XCV!\n",
    # ]
    for i in range(secs + 1):
        print(f"T-Minus: {secs}")
        secs - 1



xcontroller_commands = ["LSX", "LSY", "RSX". "RSY", "LTrigger", "RTrigger", "A", "B", "X", "Y", "Start", "Select", "Xbox", "DUp", "DDown", "DLeft", "DRight", "LBumper", "RBumper", "LSPush", "RSPush"]



cv_system = CVSystem()
serial_api = SerialAPI()
game_stats = GameStats()
game_actions = GameActions()

# class ButtonPressMixin:
#     pass

# class StickPositionChangeMixin:
#     pass

@dataclass
class buttons:
        btnA: bool = False

class _SerialAPI:
        """
        
        """
        pass

        def send(self, btn):
        
        pass

        def _check_pending_send(self, buttons):
        pass

        def _send_pending_send(self, checekdbuttons)
        pass

        @property
        def port(self):
        pass

class GameActions:
        pass





# class SerialError(Exception):
#     pass

        

    
if __name__ == "__main__":
    countdown(5)

