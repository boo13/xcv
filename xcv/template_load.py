from pathlib import Path
import cv2

path = Path('xcv/templates')

my_team_badge_path = path / "myTeamBadge.jpg"

print(path.exists())
print(my_team_badge_path.is_file())

my_team_badge = cv2.imread(my_team_badge_path, 0)

# cv2.imshow("image", my_team_badge)