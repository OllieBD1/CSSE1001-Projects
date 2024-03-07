import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable
from model import SokobanModel, Tile, Entity
from a2_support import *
from a3_support import *
from model import *

class FancyGameView(AbstractGrid):
    """
    Inherits from AbstractGrid via a3_support.py.
    The FancyGameView is a grid displaying the game map
    (e.g. all tiles and entities, including the player). 

    Args:
        __init__: Initialises FancyGameView.
        display: Creates the display of the game board.        
    """

    def __init__(self, master: tk.Frame | tk.Tk, dimensions: tuple[int, int], \
    size: tuple[int, int], maze_file: str, **kwargs) -> None:
        """
        Sets up the FancyGameView to be an AbstractGrid with the appropriate 
        dimensions and size, and creates an instance attribute of an empty
        dictionary to be used as an image cache.

        Args:
            master (tk.Frame | tk.Tk): The master frame for this Canvas.
            dimensions (tuple[int, int]): (#rows, #columns)
            size: (width in pixels, height in pixels)
        """

        super().__init__(master, dimensions, size)
        #, dimensions, size, **kwargs)
        self.image_cache = {}

    def display(self, maze: Grid, entities: Entities, player_position: Position ):
        """
        Clears the game view, then creates the images for the tiles and entities.
        If an entity is at a specific location, there is a FLOOR tile undeneath. 
        If an entity is at a position, the tile image is rendered beneath the entity.
        The get_image function from a3_support.py is used to create these images.

        Args:
        maze (Grid): A two-dimensional grid representing the game board with different tile types.
        entities (Entities): A dictionary containing positions and corresponding entity IDs.
        player_position (Position): The current position of the player in the game.
        """
        

        self.clear() #Clears the game view.

        for row_index, row in enumerate(maze): #Placing images for each tile on canvas.
            for col_index, col in enumerate(row):
                if isinstance(col, Floor):
                    image_path = "images/Floor.png" 
                elif isinstance(col, Wall):
                    image_path = "images/W.png"
                elif isinstance(col, Goal):
                    image_path = "images/G.png"
                    
                tile_image = get_image(image_path, self.get_cell_size(), self.image_cache)
                self.create_image(self.get_midpoint((row_index, col_index)),\
                image = tile_image)

        for entity_pos, entity_id in entities.items(): #Placing images for each entity.
            if isinstance(entity_id, Crate):
                image_path = "images/C.png" 
            elif isinstance(entity_id, MovePotion):
                image_path = "images/M.png"
            elif isinstance(entity_id, StrengthPotion):
                image_path = "images/S.png"
            elif isinstance(entity_id, FancyPotion):
                image_path = "images/F.png"
            elif isinstance(entity_id, Coin):
                image_path = "images/$.png"
            entity_image = get_image(image_path, self.get_cell_size(), self.image_cache)
            self.create_image(self.get_midpoint(entity_pos), image = entity_image)

        player_image = get_image("images/P.png", self.get_cell_size(), self.image_cache)
        #Places image for player.
        self.create_image(self.get_midpoint(player_position), image = player_image)

class FancyStatsView(AbstractGrid):
    """
    Inherits from AbstractGrid via a3_support.py.
    It is a grid with 3 rows and 3 columns. 
    Top row displays the text 'Player Stats' in a bold font in the second column. 
    Second row displays titles for the stats, 
    and third row displays the values for those stats. 
    The FancyStatsView should span the entire width of the game and shop combined.

    Args:
        master (tk.Tk | tk.Frame): The master frame for this view.
    """

    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """
        Sets up this FancyStatsView to be an AbstractGrid with the
        appropriate number of rows and columns, and the appropriate
        width and height (see a3 support.py).

        Args:
            master (tk.Tk | tk.Frame): The master frame for this view.
        """
        self.rows = 3
        self.cols = 3

        width = MAZE_SIZE + SHOP_WIDTH
        height = STATS_HEIGHT

        super().__init__(master, dimensions=(self.rows, self.cols), size=(width, height))
        self.draw_stats(0,0,0)

    def draw_stats(self, moves_remaining: int, strength: int, money: int) -> None:
        """
        Clears the FancyStatsView and redraws it to display the
        provided moves remaining, strength, and money.

        Args:
            moves_remaining (int): The player's remaining moves.
            strength (int): The player's strength.
            money (int): The player's money.
        """

        self.clear() #Clears the FancyStatsView

        titles = ["Moves remaining:", "Strength:", "Money:"]
        values = [moves_remaining, strength, f'${money}']
        self.create_text(self.get_midpoint((0, 1)), text = "Player Stats", font = TITLE_FONT)
        for i in range(3):
            self.create_text(self.get_midpoint((1, i)), text = titles[i])
            self.create_text(self.get_midpoint((2, i)), text = str(values[i]))

class Shop(tk.Frame):
    """
    Inherits from tk.Frame.
    The Shop is a frame displaying relevant information and 
    buttons for all the buyable items in the game.
    The Shop contains a title at the top and a frame 
    for each buyable item (each potion).
    """

    def __init__(self, master: tk.Frame, game) -> None:
        """
        Initializes the shop as a tk.Frame with a title.

        Args:
            master (tk.Frame): The master frame for this shop.
        """

        self.game = game
        super().__init__(master, width = SHOP_WIDTH)
        self.create_shop_title("Shop")
        self.create_buyable_item("Strength Potion", 5,lambda item_id="S": self.game.buy_item(item_id))
        self.create_buyable_item("Move Potion", 5, lambda item_id="M": self.game.buy_item(item_id))
        self.create_buyable_item("Fancy Potion", 10, lambda item_id="F": self.game.buy_item(item_id))

    def create_shop_title(self, title_text: str):
        """
        Creates the title for the shop frame.

        Args:
            title_text (str): "Shop"
        """

        title_label = tk.Label(self, text = title_text, font = (TITLE_FONT))
        title_label.pack(side=tk.TOP)

    def create_buyable_item(self, item: str, cost: int, callback: Callable[[], None])\
    -> None:
        """
        Creates a new frame within the shop frame and then creates a label 
        and button, bound to the provided callback within the child frame.

        Args:
            item (str): The name of the item.
            cost (int): The cost of the item.
            callback (Callable[[], None]): The callback function ran when items bought.
        """
        item_frame = tk.Frame(self)
        item_frame.pack(side = tk.TOP, padx = 5, pady = 5, fill = tk.BOTH)

        item_label_text = item + ": $" + str(cost)
        item_label = tk.Label(item_frame, text=item_label_text)
        item_label.pack(side = tk.LEFT, padx = 5)

        buy_button = tk.Button(item_frame, text = "Buy", command=callback)
        buy_button.pack(side = tk.LEFT)

class FancySokobanView():
    """
    Provides a wrapper around the smaller GUI components.
    Provides methods through which the controller can update these components.
    """

    def __init__(self, master: tk.Tk, dimensions: tuple[int, int],\
    size: tuple[int, int], maze_file: str, game) -> None:
        """
        Initialises a new Sokoban view.

        Args:
            master (tk.Tk): The master Tk window.
            dimensions (tuple[int, int]): Dimensions of the view.
            size (tuple[int, int]): Size of the view.
            maze_file (str): Path to the maze file.
        """

        self.master = master
        self.master.title("Extra Fancy Sokoban")

        self.game = game

        self.banner = self.title_banner(master, "images/banner.png")
        banner_label = tk.Label(master, image = self.banner)
        banner_label.pack(side=tk.TOP)

        game_frame = tk.Frame(master, width = MAZE_SIZE+SHOP_WIDTH)
        game_frame.pack(side=tk.TOP)

        shop = Shop(game_frame, self.game)
        shop.pack(side=tk.RIGHT, fill=tk.Y)

        self.maze, self.entities, self.player_pos = self.helper(maze_file)

        self.game_grid = FancyGameView(game_frame, (7, 8), (450, 450), maze_file)
        self.game_grid.display(self.maze, self.entities, self.player_pos)
        self.game_grid.pack(side=tk.RIGHT)

        self.stats_view = FancyStatsView(master)
        self.display_stats(0,0,0)
        self.stats_view.pack(side=tk.BOTTOM)

    def title_banner(self, master, image_path:str):
        """
        Creates a banner for the view.

        Args:
            master (_type_): The master window.
            image_path (str, optional): "banner.png"
        """
        image_cache = {}
        banner = get_image("images/banner.png", (MAZE_SIZE+SHOP_WIDTH,BANNER_HEIGHT), image_cache)
        return banner
        
    def helper(self, maze_file):
        """
        Helper method to initialize the game view.
        Loads data from the provided maze file.

        Args:
            maze_file (str): The path to the maze file.

        Returns:
            Tuple[Grid, Entities, Position]: Contains maze, entities, player position.
        """

        model = SokobanModel(maze_file)
        entities = model.get_entities()
        maze = model.get_maze()
        player_pos = model.get_player_position()
        return maze, entities, player_pos

    def display_game(self, maze, entities, player_position):
        """
        Clears and redraws the game view.

        Args:
            maze (Grid): The game's maze grid.
            entities (Entities): The game's entities.
            player_position (Position): The player's position.
        """

        self.game_grid.display(maze,entities,player_position)

    def display_stats(self, moves, strength, money):
        """
        Clears and redraws the stats view.

        Args:
            moves (int): The player's remaining moves.
            strength (int): The player's strength.
            money (int): The player's money.
        """
        
        self.stats_view.draw_stats(moves, strength, money)

class ExtraFancySokoban():
    """
    The controller class for the overall game. 
    Creates and maintains instances of the model and view classes,
    event handling, and facilitating communication between the model
    and view classes. 

    Args:
        root (tk.Tk): The main Tkinter window.
        maze_file (str): The path to the maze file used for the game.
    """

    def __init__(self, root: tk.Tk, maze_file: str):
        """
        Initializes by creating instances of SokobanModel and FancySokobanView,
        sets up shop items, binding keypress events, and initializing the game state.

        Args:
            root (tk.Tk): The main Tkinter window.
            maze_file (str): The path to the maze file used for the game.
        """

        self.root = root
        self.root.title("ExtraFancySokoban")

        self.model = SokobanModel(maze_file)

        self.view = FancySokobanView(self.root, (8,7), (450,450), maze_file, self)

        shop_items = self.model.get_shop_items()

        self.root.bind('w', self.handle_keypress)
        self.root.bind('s', self.handle_keypress)
        self.root.bind('a', self.handle_keypress)
        self.root.bind('d', self.handle_keypress)
        self.root.bind('u', self.handle_keypress)

        self.redraw()

    def buy_item(self, item_id):
        """
        1. Take an item id as a parameter
        2. Tells the model to attempt to buy that item
        3. Tells the entire view to redraw

        Args:
            item_id (POTION): Potions displayed in the shop.
        """
        print(self)
        if self.model.attempt_purchase(item_id):
            self.redraw()

    def redraw(self):
        """
        Redraws the game view and stats view based on the current model
        """

        self.view.display_game(self.model.get_maze(), self.model.get_entities(),\
        self.model.get_player_position())
        self.view.display_stats(self.model.get_player_moves_remaining(),\
        self.model.get_player_strength(), self.model.get_player_money())

    def handle_keypress(self, event):
        """
        An event handler to be called when a keypress event occurs. 
        Attempt the move as per the key pressed, and then redraw the view.
        If the game has been won or lost after the move, 
        this method cause a messagebox to display a win or loss message to the user
        and ask to play again with yes or no. If the user selects yes,
        the game should be reset If the user selects no, the program should terminate.

        Args:
            event: The keypress event.
        """

        key_direction_mapping = {
            'w': UP,
            's': DOWN,
            'a': LEFT,
            'd': RIGHT,
            'u': 'u'
        }

        key = event.keysym.lower()
        direction = key_direction_mapping.get(key, None)

        if direction is not None:
            if self.model.attempt_move(direction):
                self.redraw()
                
                if self.model.has_won():
                    if messagebox.askyesno(message="You won! Play again?"):
                        self.reset_game()
                    else:
                        self.quit_game()
                    
                elif self.model.get_player_moves_remaining()<=0:
                    if messagebox.askyesno(message="You lost! Play again?"):
                        self.reset_game()
                    else:
                        self.quit_game()
        else:
            pass

    def reset_game(self):
        """
        Reset the game.
        """

        self.model.reset()
        self.redraw()

    def quit_game(self):
        """
        Quit the game gracefully.
        """

        self.root.quit()

def play_game(root: tk.Tk, maze_file: str) -> None:
    ExtraFancySokoban(root, maze_file)

    root.mainloop()

def main() -> None:
    """
    The main function.
    """

    root = tk.Tk()

    maze_file = "maze_files/maze2.txt" # Any file from maze_files.

    play_game(root, maze_file)

if __name__ == "__main__":
    main()