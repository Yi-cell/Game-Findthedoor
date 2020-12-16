
# Model 
class Entity:
    """ """

    _id = "Entity"

    def __init__(self):
        """
        Something the player can interact with
        """
        self._collidable = True

    def get_id(self):
        """ """
        return self._id

    def set_collide(self, collidable):
        """ """
        self._collidable = collidable

    def can_collide(self):
        """ """
        return self._collidable

    def __str__(self):
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        return str(self)


class Wall(Entity):
    """ """

    _id = WALL
    
    def __init__(self):
        """ """
        super().__init__()
        self.set_collide(False)


class Item(Entity):
    """ """
    def on_hit(self, game):
        """ """
        raise NotImplementedError


class Key(Item):
    """ """

    _id = KEY

    def on_hit(self, game):
        """ """
        player = game.get_player()
        player.add_item(self)
        game.get_game_information().pop(player.get_position())


class MoveIncrease(Item):
    """ """

    _id = MOVE_INCREASE

    def __init__(self,moves=5):
        """ """
        super().__init__()
        self._moves = moves

    def on_hit(self, game):
        """ """
        player = game.get_player()
        player.change_move_count(self._moves)
        game.get_game_information().pop(player.get_position())


class Door(Entity):
    """ """
    _id = DOOR

    def on_hit(self, game):
        """ """
        player = game.get_player()
        for item in player.get_inventory():
            if item.get_id() == KEY:
                game.set_win(True)
                game.get_game_information().pop(player.get_position())
                return
        messagebox.showinfo(title='No Key!', message="You don't have the key")


class Player(Entity):
    """ """

    _id = PLAYER

    def __init__(self, move_count):
        """ """
        super().__init__()
        self._move_count = move_count
        self._inventory = []
        self._position = None
    def reset_move_count(self,count):
        """"""
        self._move_count = count

    def set_position(self, position):
        """ """
        self._position = position

    def get_position(self):
        """ """
        return self._position

    def change_move_count(self, number):
        """
        Parameters:
            number (int): number to be added to move count
        """
        self._move_count += number

    def moves_remaining(self):
        """ """
        
        return self._move_count
        

    def add_item(self, item):
        """Adds item (Item) to inventory
        """
        self._inventory.append(item)

    def get_inventory(self):
        """ """
        return self._inventory



class GameLogic:
    """ """
    def __init__(self, dungeon_name="game2.txt"):
        """ """
        self._dungeon = self.load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False

    def load_game(self,filename):
        """
        Create a 2D array of string representing the dungeon to display.   
        Parameters:
            filename (str): A string representing the name of the level.
        Returns:
            (list<list<str>>): A 2D array of strings representing the 
                dungeon.
        """
        dungeon_layout = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                dungeon_layout.append(list(line))
        return dungeon_layout

    def get_positions(self, entity):
        """ """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def init_game_information(self):
        """ """
        player_pos = self.get_positions(PLAYER)[0]
        key_position = self.get_positions(KEY)[0]
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)
        
        self._player.set_position(player_pos)

        information = {
            key_position: Key(),
            door_position: Door(),
        }

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information

    def get_player(self):
        """ """
        return self._player

    def get_entity(self, position):
        """ """
        return self._game_information.get(position)

    def get_entity_in_direction(self, direction):
        """ """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def get_game_information(self):
        """ """
        return self._game_information

    def get_dungeon_size(self):
        """ """
        return self._dungeon_size

    def move_player(self, direction):
        """ """
        new_pos = self.new_position(direction)
        self.get_player().set_position(new_pos)

    def collision_check(self, direction):
        """
        Check to see if a player can travel in a given direction
        Parameters:
            direction (str): a direction for the player to travel in.

        Returns:
            (bool): False if the player can travel in that direction without colliding otherwise True.
        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True
        
        return not (0 <= new_pos[0] < self._dungeon_size and 0 <= new_pos[1] < self._dungeon_size)

    def new_position(self, direction):
        """ """
        x, y = self.get_player().get_position()
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def check_game_over(self):
        """ """
        return self.get_player().moves_remaining() <= 0

    def set_win(self, win):
        """ """
        self._win = win

    def won(self):
        """ """
        return self._win
    
