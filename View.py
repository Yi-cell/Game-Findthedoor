# View
class AbstractGrid(tk.Canvas):
    """An abstract view class, providing base functionality for many of the view classes"""

    def __init__(self,master,rows,cols,width,height,**kwargs):
        """
        Parameters:
            master(tk.Widget): widget that place the grid.
            rows(int): the row number of grid
            cols(int): the column number of grid
            width(int): the size of the grid
            height(int): the size of the grid
        """
        super().__init__(master,width = width, height = height, **kwargs)
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self._radius = (self._width / self._cols) / 2
        self._radiusy = (self._height / self._rows) / 2
        self._length = self._radius *2 
        self._lengthy = self._radiusy * 2

    def get_bbox(self,position):
        """ Returns the bounding box for the (row,col) position
           
            Parameter:
                position (tuple<int,int>): rows and cols positions
           
            Return:
                pixel tuple(<int,int>): the top left pixel point and the right bottom pixel point
        
        """
        left_up_point = self.get_position_center(position)[0] - self._radius,self.get_position_center(position)[1] - self._radiusy
        right_down_point = self.get_position_center(position)[0] + self._radius,self.get_position_center(position)[1] + self._radiusy
        
        return left_up_point,right_down_point

    def pixel_to_position(self,pixel):
        """ Convert the x, y pixel position (in graphics units) to a (row, col) position.
            
            Parameters:
                pixel (tuple<int,int>): pixel position
            
            Return:
                position (tuple<int,int>): rows and cols positions
        """
        position_x = int(pixel[0] // self._length)
        position_y = int(pixel[1] // self._lengthy)
        return position_x, position_y
    def get_position_center(self,position):
        """ Gets the graphics coordinates for the center of the cell at the given (row,col) position.
            
            Parameters:
                position (tuple<int,int>): rows and cols positions
            
            Return:
                pixel (tuple<int,int>): the center pixel position given the rows and cols
        """
        x = (position[1] * 2 +1) *self._radius 
        y = (position[0] * 2 +1) *self._radiusy 
        return x,y
    def annotate_position(self,position,text):
        """ Annotates the cell at the given (row,col) position with the provided text.
            
            Parameters:
                position (tuple<int,int>): rows and cols positions
                text (str): the name of the rectangles             
        """      
        return self.create_text((self.get_position_center(position)),text = text)

class DungeonMap(AbstractGrid):

    """Entities are drawn on the map using coloured rectangles at different (row,column) position"""
    def __init__(self,master,size,width=600,**kwargs):
        """
        """
        super().__init__(master,size,size,width,width,**kwargs)
        
    def draw_grid(self,dungeon,player_position):
        """Draws the dungeon on the DungeonMap based on dungeon, and draws the
           player at the specified (row,col) position.

           Parameter:
               dungeon (<list>): game information
               player_position (tuple<int,int>): rows and cols position of player
        """
        self.delete(tk.ALL)

        x = self.get_bbox(player_position) # create the player rectangle
        self.create_rectangle(x,fill = 'medium spring green')
        self.annotate_position(player_position,'Ibis')
        
        for position in dungeon: # create the entity rectangles by dungeon (game information)
            entity = dungeon[position].get_id()
            bbox = self.get_bbox(position)
            if entity == KEY:
                self.create_rectangle(bbox,fill = 'yellow')
                self.annotate_position(position,'Trash')
            elif entity == DOOR:
                self.create_rectangle(bbox,fill = 'red')
                self.annotate_position(position,'Nest')
            elif entity == MOVE_INCREASE:
                self.create_rectangle(bbox,fill = 'orange')
                self.annotate_position(position,'Banana')
            elif entity == WALL:
                self.create_rectangle(bbox,fill = 'dark gray')  

class KeyPad(AbstractGrid):
    """ Represents the GUI keypad"""
    
    def __init__(self,master,width=200,height=100,**kwargs):
        """
        """
        super().__init__(master,2,3,width,height,**kwargs)
        
        self.create_rectangle(self.get_bbox([0,1]),fill = 'dark gray')
        self.create_rectangle(self.get_bbox([1,0]),fill = 'dark gray')
        self.create_rectangle(self.get_bbox([1,1]),fill = 'dark gray')
        self.create_rectangle(self.get_bbox([1,2]),fill = 'dark gray')
        self.annotate_position([0,1],'N')
        self.annotate_position([1,0],'W')
        self.annotate_position([1,1],'S')
        self.annotate_position([1,2],'E')
    
    def pixel_to_direction(self,pixel):
        """
        Converts the x,y pixel position to the direction of the arrow depicted at that position

        Parameters:
            pixel (tuple<int,int>): the <Button-1> pixel position
        
        """
        position = self.pixel_to_position(pixel)
        
        if position == (0,1):
            return 'a'
        elif position == (1,0):
            return 'w'
        elif position == (1,1):
            return 's'
        elif position == (2,1):    
            return 'd'
        else:
            return None
class AdvancedDungeonMap(AbstractGrid):  
    """Entities are drawn on the map using images at different (row,column) position"""
    def __init__(self,master,size,width=600,**kwargs):
        """
        """
        super().__init__(master,size,size,width,width,**kwargs)
        loadimages = self.load_images()  # images dictionary
        self._resize_images = {} # resize images dictionary
        for key in loadimages:
            nvalue = loadimages[key].resize((int(self._length), int(self._length)), Image.ANTIALIAS)
            nvalue1 = ImageTk.PhotoImage(nvalue)        
            self._resize_images.update({key:nvalue1})
        
    def load_images(self):
        """Load imagees files into memory"""

        self.images = {
            "O":Image.open('images/player.gif'),
            "#":Image.open('images/wall.gif'),
            "M":Image.open('images/moveIncrease.gif'),
            "clock":Image.open('images/clock.gif'),
            "lives":Image.open('images/lives.gif'),
            "lightning":Image.open('images/lightning.gif'),
            "key":Image.open('images/key.gif'),
            "D":Image.open( 'images/door.gif'),
            "empty":Image.open('images/empty.gif'),
        }   
        return self.images

    def draw_grid(self,dungeon,player_position):
        """Draws the dungeon on the DungeonMap based on dungeon, and draws the
           player at the specified (row,col) position
        """
        self.delete(tk.ALL)
        # create the 'empty' images
        for i in range(8):
            for j in range(8):
                position = (i,j)
                y = self.get_position_center(position)
                self.create_image(y, image=self._resize_images['empty'])
        # create the player images
        x = self.get_position_center(player_position)
        self.create_image(x, image=self._resize_images[PLAYER])
        # create the entity images
        for position in dungeon:           
            entity = dungeon[position].get_id()
            c = self.get_position_center(position)
            if entity == KEY:
                self.create_image(c, image=self._resize_images['key'])
            elif entity == DOOR:
                self.create_image(c, image=self._resize_images['D'])
            elif entity == MOVE_INCREASE:
                self.create_image(c, image=self._resize_images['M'])
            elif entity == WALL:
                self.create_image(c, image=self._resize_images['#'])
        
     

class StatusBar(tk.Frame):
    """Include the game information (time, moves remainings) and game buttons """
    def __init__(self, master):
        """
        Create a status bar which contains game information.

        """
        super().__init__(master)
        self._master = master
        # create frame 1 with the 'New game' and 'Quit' button
        self.frame1 = tk.Frame(self)
        self.frame1.pack( side = tk.LEFT,padx = 50)
        self.new_game_button = tk.Button(self.frame1, text='New game', command = self.new_game)
        self.new_game_button.pack(side=tk.TOP)
        self.quit_game_button = tk.Button(self.frame1, text='Quit', command = self.quit_game)
        self.quit_game_button.pack(side=tk.TOP)
        # create frame 2 with the clock image and time_info.
        self.frame2 = tk.Frame(self)  
        self.frame2.pack(side = tk.LEFT,padx = 50)
        self._clock = Image.open('images/clock.gif')
        self._clock = self._clock.resize((50,50), Image.ANTIALIAS)
        self._clock = ImageTk.PhotoImage(self._clock)
        self._clock_label = tk.Label(self.frame2,image = self._clock)
        self._clock_label.pack(side = tk.LEFT)
        
        self.time_info = tk.Label(self.frame2, text = 'Time elapsed')
        self.time_info.pack(side = tk.TOP)
        self.clock = tk.Label(self.frame2, text = '0m 0s')
        self.clock.pack(side = tk.TOP)     
        # create frame 3 with the lightning image and remain_left.
        self.frame3 = tk.Frame(self)
        self.frame3.pack(side = tk.LEFT,padx = 50)
        self._lightning = Image.open('images/lightning.gif')   
        self._lightning = self._lightning.resize((50,50), Image.ANTIALIAS)
        self._lightning = ImageTk.PhotoImage(self._lightning)
        self._lightning_label = tk.Label(self.frame3,image = self._lightning)
        self._lightning_label.pack(side = tk.LEFT)

        self.remain_left = tk.Label(self.frame3, text='Moves left')
        self.remain_left.pack(side=tk.TOP)
        self.moves_remaining = tk.Label(self.frame3, text='12 moves remaining')
        self.moves_remaining.pack(side=tk.TOP) 
        
    # redefine in GameApp
    def new_game(self):       
        pass
    def quit_game(self):  
        pass

class NStatusBar(StatusBar):
    """ Lives remaining bar """
    def __init__(self,master):
        super().__init__(master)
        self._master = master
        self.frame1.pack( side = tk.LEFT,padx = 25)
        self.frame2.pack(side = tk.LEFT,padx = 25)
        self.frame3.pack(side = tk.LEFT,padx = 25)
        self.frame4 = tk.Frame(self)     
        self.frame4.pack(side = tk.LEFT, padx =10)
        self.lives = Image.open('images/lives.gif')
        self._lives = self.lives.resize((50,50), Image.ANTIALIAS)
        self._lives = ImageTk.PhotoImage(self._lives)
        self._lives_label = tk.Label(self.frame4, image = self._lives)
        self._lives_label.pack(side = tk.LEFT)
        self._lives_remaining = tk.Label(self.frame4, text = 'Lives remaining: 3')
        self._lives_remaining.pack(side = tk.TOP)
        self._use_life_button = tk.Button(self.frame4, text='Use life', command = self.use_life)
        self._use_life_button.pack(side=tk.TOP)

    def use_life(self):
        pass
