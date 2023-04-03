import json
import inspect
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("map_file", help="Path to the map file")
args = parser.parse_args()

class Game:
    def __init__(self, args):
        with open(args.map_file, 'r') as f:
            self.game_map = json.load(f)
        self.current_room = self.game_map[0]
        self.inventory = []
        self.game_won = False
        self.game_lost = False

    def look(self):
        if self.game_won:
            print("You have already won the game!")
            return
        elif self.game_lost:
            print("You have already lost the game!")
            return
        print("> " + self.current_room["name"] + "\n")
        print(self.current_room["desc"] + "\n")
        if "items" in self.current_room:
            print("Items:", ', '.join(self.current_room["items"]) + "\n")
        print("Exits:", ' '.join(self.current_room["exits"].keys()) + "\n")

    def go(self, direction):
        if direction not in self.current_room["exits"]:
            print("There's no way to go", direction)
        else:
            print("You go ",direction)
            room_index = self.current_room["exits"][direction]
            self.current_room = self.game_map[room_index]
            self.look()
        if self.current_room["name"] == "Shaft" and "rope" not in self.inventory:
            print("You fell in the shaft and you can't get out of it so you lose")
            self.game_lost = True
        elif self.current_room["name"] == "Treasure Room" and "gun" not in self.inventory:
            print("You were killed by the guard, you lose.")
            self.game_lost = True

    def get(self, item):
        if "items" in self.current_room and item in self.current_room["items"]:
            self.inventory.append(item)
            self.current_room["items"].remove(item)
            print("You pick up the", item)
        else:
            print("There's no", item, "here.")
        if "keys" and "treasure" in self.inventory:
            print("You can unlock the treasure with your key. You win!")
            self.game_won = True

    def drop(self, item):
        if item in self.inventory:
            self.current_room["items"].append(item)
            self.inventory.remove(item)
            print("You drop the", item)
        else:
            print("You're not carrying a", item)


    def display_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print("  ", item)

    def help(self):
        available_commands = [command for command in dir(Game) if not command.startswith('__') and not command == 'run']
        print("You can run the following commands:")
        for command in available_commands:
            if command == 'display_inventory':
                print("  inventory")
            else:
                function = getattr(self, command)
                args = function.__code__.co_varnames[:function.__code__.co_argcount]
                if len(args) > 1:
                    print(f"  {command} ...")
                else:
                    print(f"  {command}")

   

    def run(self):
        self.look()
        while True:
        
            if self.game_won:
                print("Congratulations! You won the game!")
                break
            elif self.game_lost:
                print("Game over! You lost!")
                break      
            try:
                command = input("What would you like to do?").lower().split()
            except EOFError:
                print("Use 'quit' to exit")
                continue
            if not command:
                continue
            verb = command[0]
            if verb == "go":
                if len(command) < 2:
                    print("Sorry, you need to 'go' somewhere")
                    ans = input()
                    if 'east' in ans:
                        self.go('east')
                else:
                    self.go(command[1])

            elif verb == "get":
                if len(command) < 2:
                    print("Sorry, you need to 'get' something.")
                else:
                    self.get(command[1])

            elif verb == "drop":
                if len(command) < 2:
                    print("What do you want to drop?")
                else:
                    self.drop(command[1])

            elif verb == "inventory":
                self.display_inventory()
            elif verb == "help":
                self.help()
            elif verb == "look":
                self.look() 
            elif verb == "quit":
                print("Goodbye!")
                break
            else:
                print("Sorry, I don't understand that command.")

game = Game(args)
game.run()
