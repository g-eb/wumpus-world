from wumpus_world.game.Map import Map
from wumpus_world.game.FieldType import FieldType

newMap = Map(10,10)
newMap.randomMap()

for row in range(newMap.height):
    for col in range(newMap.width):
        print(newMap.fields[row][col].getGraphic(), end = "")
    print()
