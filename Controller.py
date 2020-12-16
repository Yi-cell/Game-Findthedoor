# Controller

class GameApp(object):
    """manage necessary communication between any model and view classes"""
    def __init__(self,master,task = 'MASTERS', dungeon_name = 'game2.txt'):       
        """Create game app within the master widget"""

        master.title("Key Cave Adventrue Game")
        self._master = master        
        self._game = GameLogic()
        self._task = task
        self._dungeon =self._game.get_game_information()
        self._filename = None
        # The title 
        label = tk.Label(self._master, text = "Key Cave Adventrue Game", bg ='medium spring green')
        label.config(height = 1, font = ((None, 20)))
        label.pack(side = tk.TOP,fill = tk.X)
        # Extract the player object from the model part (gamelogic)      
        self.player = self._game.get_player()
        self.player_position = self.player.get_position()
        # Display all game objects and update the player status info
        if self._task == 'TASK_ONE':

            self._dungeon1 =DungeonMap(self._master,self._game.get_dungeon_size(),background = 'light grey')
            self._dungeon1.pack(side = tk.LEFT)
            self._keypad = KeyPad(self._master)
            self._keypad.pack(side = tk.LEFT,fill = tk.X)
            # Bind the events
            self._dungeon1.bind_all('<Key>',self.key_press) 
            self._keypad.bind_all('<Button-1>',self.left_click)
            # Draw the grid on the canvas
            self._dungeon1.draw_grid(self._dungeon, self.player_position)

        elif self._task == 'TASK_TWO':

            # Create menu bar       
            menubar = tk.Menu(self._master)
            master.config(menu=menubar)     
            # File menu in menu bar
            filemenu = tk.Menu(menubar)
            menubar.add_cascade(label='File', menu=filemenu)
            filemenu.add_command(label = 'Save game', command = self.save_game)
            filemenu.add_command(label = 'Load game', command = self.load_game)
            filemenu.add_command(label = 'New game', command = self.new_game)
            filemenu.add_command(label = 'Quit', command = self.quit_game) 
          
            self.frame1 = tk.Frame(self._master) # frame1 for the canvas and keypad
            self.frame2 = tk.Frame(self._master) # frame2 for the statusbar 

            self._dungeon2 =AdvancedDungeonMap(self.frame1, self._game.get_dungeon_size())
            self._dungeon2.pack(side = tk.LEFT)  
            self._keypad = KeyPad(self.frame1)
            self._keypad.pack(side = tk.LEFT,fill = tk.X)
            # Bind the events
            self._dungeon2.bind_all('<Key>',self.key_press1) 
            self._keypad.bind_all('<Button-1>',self.left_click1)
            # Draw the grid on the canvas   
            self._dungeon2.draw_grid(self._dungeon, self.player_position)
            # Create the player status bar
            self._status = StatusBar(self.frame2)      
            self._status.pack()
            # Add the command 
            self._status.new_game_button.config(command=self.new_game)
            self._status.quit_game_button.config(command=self.quit_game) 
                  
            # Time and moves remainings
            self.current_time = time.time()

            def config():            
                self._minute = int((time.time() - self.current_time) / 60)
                self._seconds = int(time.time() - self.current_time - self._minute * 60)
                self._status.clock.config(text="{}m {}s".format(self._minute, self._seconds))          
                self._status.clock.after(1000, config) 
            config()   

            def config1():       
                self._status.moves_remaining.config(text="{0} moves remaining".format(self.player.moves_remaining()))
                self._master.after(10, config1)
            config1()    

            # Pack the frames 
            self.frame1.pack()
            self.frame2.pack(side = tk.LEFT)  

        elif self._task == 'MASTERS':   

            menubar = tk.Menu(self._master)# For MASTER menubar
            master.config(menu=menubar)     
            filemenu = tk.Menu(menubar)
            menubar.add_cascade(label='File', menu=filemenu)
            filemenu.add_command(label = 'Save game', command = self.save_game)
            filemenu.add_command(label = 'Load game', command = self.load_game)
            filemenu.add_command(label = 'New game', command = self.new_game)
            filemenu.add_command(label = 'Quit', command = self.quit_game)
            filemenu.add_command(label = 'High scores', command = self.high_scores)  

            self.frame1 = tk.Frame(self._master) # frame1 for the canvas and keypad
            self.frame2 = tk.Frame(self._master) # frame2 for the statusbar 

            self._dungeon2 =AdvancedDungeonMap(self.frame1, self._game.get_dungeon_size())
            self._dungeon2.pack(side = tk.LEFT)  
            self._keypad = KeyPad(self.frame1)
            self._keypad.pack(side = tk.LEFT,fill = tk.X)
            # Bind the events
            self._dungeon2.bind_all('<Key>',self.key_press2) 
            self._keypad.bind_all('<Button-1>',self.left_click2)
            # Draw the grid on the canvas   
            self._dungeon2.draw_grid(self._dungeon, self.player_position)
            # Create the player status bar            
            self._statusn = NStatusBar(self.frame2)          
            self._statusn.pack()
            # Add the command 
            self._statusn.new_game_button.config(command=self.new_game)
            self._statusn.quit_game_button.config(command=self.quit_game) 
            self._statusn._use_life_button.config(command=self.use_life)      
            # Time and moves remainings
            self.current_time = time.time()
            self._lives = 3
            self.config()
            self.config1()
            self.config2()
            # Pack the frames 
            self.frame1.pack()
            self.frame2.pack(side = tk.LEFT)  
            
            

    def config(self):
        """Time adjust"""
        self._minute = int((time.time() - self.current_time) / 60)
        self._seconds = int(time.time() - self.current_time - self._minute * 60)
        self._statusn.clock.config(text="{}m {}s".format(self._minute, self._seconds))
        self._statusn.clock.after(1000, self.config)

    def config1(self):
        """Moves remaining adjust"""
        self._statusn.moves_remaining.config(text="{0} moves remaining".format(self.player.moves_remaining()))
        self._master.after(10, self.config1)

    def config2(self):
        """Lives reamining adjust"""
        self._statusn._lives_remaining.config(text="Lives remaining: {0}".format(self._lives))
        self._master.after(10,self.config2)

    def use_life(self):
        """ Increase the move remainings"""
        if self._lives > 0:
            self._lives = self._lives - 1
            self.config2
            self._game.get_player().change_move_count(1)
        

    def quit_game(self):
        """ Quit the current game """
        reply = messagebox.askquestion(type=messagebox.YESNO, title='Quit', message='Do you really want to quit the game?')
        if reply == messagebox.YES:
            quit()
        if reply == messagebox.NO:
            pass       
        
    def save_game(self):
        """ Save the current game as a .txt file"""
        filename = filedialog.asksaveasfilename()
        self._filename = filename 
        fd = open(self._filename,'w')
        game_information = str(self._game.get_game_information())
        player_position = str(self.player_position)
        movesremains = str(self.player.moves_remaining())
        minitues = str(self._minute)
        seconds = str(self._seconds)
        fd.write(game_information + '%')
        fd.write(player_position + '%')
        fd.write(movesremains +'%')
        fd.write(minitues +'%')
        fd.write(seconds +'%')
        fd.close()

    def load_game(self):
        """ Load the previous game """
        filename = filedialog.askopenfilename()
        fd = open(filename,'r')
        files = fd.readline().split('%')
        self._dungeon = eval(files.pop(0))
        self.player_position = tuple(eval(files.pop(0)))
        self._game.get_player().set_position(self.player_position)
        self.player._move_count = int(files.pop(0))
        self._dungeon2.draw_grid(self._dungeon, self.player_position)
        self._minute = int(files.pop(0))
        self._seconds = int(files.pop(0))
        self.config()
        self.config1()

    def new_game(self): 
        """ New game - reset"""
        self.player_position = self._game.get_positions(PLAYER)[0]
        self._game.get_player().set_position(self.player_position)
        self._game.get_game_information()[(1,6)] = Key()
        self._game.get_game_information()[(6,3)] = Door()
        self._game.get_game_information()[(6,6)] = MoveIncrease()
        self._game.set_win(False) # set game false 
        # Draw new game
        self._dungeon2.draw_grid(self._dungeon,self.player_position)
        self._game.get_player().reset_move_count(GAME_LEVELS['game2.txt']) # reset move counts
        if self._task == 'MASTERS':
            self._lives = 3 
            self.config2()
        self.current_time = time.time()  

    def enter_end(self):

        """ the entry window ask the name"""
        self.newWindow = tk.Toplevel(self._master)
        self.newWindow.title("You Win!")
        newWindow_label = tk.Label(self.newWindow,text="You won in {0}m and {1}s! Enter your name:".format(self._minute,self._seconds))
        newWindow_label.pack(side = tk.TOP)
        self.newWindow_entry = tk.Entry(self.newWindow)
        self.newWindow_entry.pack(side = tk.TOP)
        neWindow_button = tk.Button(self.newWindow, text = 'Enter', command = self._enter)
        neWindow_button.pack(side = tk.TOP)

    def _enter(self):
        """Add the name in list"""
        self.name = []
        self.name.append(self.newWindow_entry.get())
        self.newWindow.destroy()

    def high_scores(self):
        """High scores in menun"""
        self.top = tk.Toplevel(self._master,width=80,height = 80)
        self.top.title("Top 3")
        top_label = tk.Label(self.top,text="Hight Scores", bg = 'medium spring green')
        top_label.config(height =1, font = ((None,20)))
        top_label.pack(side = tk.TOP,fill = tk.X)
        first_player = tk.Label(self.top, text = '{0}:{1}s'.format(self.name[0],self._seconds))
        first_player.pack(side = tk.TOP)
        sec_player = tk.Label(self.top, text = '{0}:{1}s'.format(self.name[1],self._seconds))
        sec_player.pack(side = tk.TOP)
        th_player = tk.Label(self.top, text = '{0}:{1}s'.format(self.name[2],self._seconds))
        th_player.pack(side = tk.TOP)

        top_button = tk.Button(self.top, text = 'Done',command = self.done)
        top_button.pack(side = tk.TOP)

    def done(self):
        """Close Toplevel"""
        self.top.destroy()

        
       
    def key_press(self,event):
        """TASK-ONE keypress""" 
        if  self._game.won() == False:
            if self.player.moves_remaining() > 0:
                if event.char in DIRECTIONS:      
                    if not self._game.collision_check(event.char):
                        self._game.move_player(event.char)
                        entity = self._game.get_entity(self.player.get_position()) 
                        self.player = self._game.get_player()
                        self.player_position = self.player.get_position()
                        self._dungeon1.delete(tk.ALL)   
                        if entity is not None:
                                    entity.on_hit(self._game)
                                    if self._game.won():
                                        messagebox.showinfo(title='You won!', message='You have finished the level !')                             
                        self._dungeon1.draw_grid(self._dungeon, self.player_position)                  
                    self.player.change_move_count(-1)                   
                else:
                    print(INVALID)
                if self._game.check_game_over():
                    messagebox.showinfo(title='You lose!', message=LOSE_TEST)
                    return
                 
    def key_press1(self,event):
        """TASK-TWO keypress"""
        if self._game.won() == False:
            if self.player.moves_remaining() > 0:
                if event.char in DIRECTIONS:      
                    if not self._game.collision_check(event.char):
                        self._game.move_player(event.char)
                        entity = self._game.get_entity(self.player.get_position()) 
                        self.player = self._game.get_player()
                        self.player_position = self.player.get_position()
                        self._dungeon2.delete(tk.ALL)   
                        if entity is not None:
                            entity.on_hit(self._game)                 
                            if self._game.won():
                                reply = messagebox.askquestion(type=messagebox.YESNO, title='You won!', message= "You have finished the level with a score of {0}\n\n Would you like to play again?".format(self._seconds))
                                if reply == messagebox.YES:
                                    self.new_game()                                  
                                elif reply == messagebox.NO:
                                    quit()                                                    
                        self._dungeon2.draw_grid(self._dungeon, self.player_position)               
                    self.player.change_move_count(-1)
                else:
                    print(INVALID)
                if self._game.check_game_over():
                    messagebox.showinfo(title='You lose!', message=LOSE_TEST)                   
                    return

    def key_press2(self,event):
        """MASTERS keypress"""
        if self._game.won() == False:  
            if self.player.moves_remaining() > 0:        
                if event.char in DIRECTIONS:      
                    if not self._game.collision_check(event.char):
                        self._game.move_player(event.char)
                        entity = self._game.get_entity(self.player.get_position()) 
                        self.player = self._game.get_player()
                        self.player_position = self.player.get_position()
                        self._dungeon2.delete(tk.ALL)   
                        if entity is not None:
                            entity.on_hit(self._game)                   
                            if self._game.won():
                                self.enter_end() # the entry                        
                        self._dungeon2.draw_grid(self._dungeon, self.player_position)              
                    self.player.change_move_count(-1)
                else:
                    print(INVALID)
                if self._game.check_game_over():
                    messagebox.showinfo(title='You lose!', message=LOSE_TEST)              
                    return

    def left_click(self,event):
        """TASK-ONE click control"""
        if self._game.won() == False:
            if self.player.moves_remaining() > 0:
                c = event.x,event.y
                x = self._keypad.pixel_to_direction(c)
                if x in DIRECTIONS:      
                    if not self._game.collision_check(x):
                        self._game.move_player(x)
                        entity = self._game.get_entity(self.player.get_position()) 
                        self.player = self._game.get_player()
                        self.player_position = self.player.get_position()
                        self._dungeon1.delete(tk.ALL)   
                        if entity is not None:
                                    entity.on_hit(self._game)
                                    if self._game.won():
                                        messagebox.showinfo(title='You won!', message='You have finished the level !')                             
                        self._dungeon1.draw_grid(self._dungeon, self.player_position)                  
                    self.player.change_move_count(-1)      
                if self._game.check_game_over():
                    messagebox.showinfo(title='You lose!', message=LOSE_TEST)
                    return

    def left_click1(self,event):
        """TASK-TWO click control"""
        if self._game.won() == False:
            if self.player.moves_remaining() > 0:             
                c = event.x,event.y
                x = self._keypad.pixel_to_direction(c)
                if x in DIRECTIONS:      
                    if not self._game.collision_check(x):
                        self._game.move_player(x)
                        entity = self._game.get_entity(self.player.get_position()) 
                        self.player = self._game.get_player()
                        self.player_position = self.player.get_position()
                        self._dungeon2.delete(tk.ALL)   
                        if entity is not None:
                                    entity.on_hit(self._game)                         
                                    if self._game.won():
                                        reply = messagebox.askquestion(type=messagebox.YESNO, title='You won!', message= "You have finished the level with a score of {0}\n\n Would you like to play again?".format(self._seconds))
                                        if reply == messagebox.YES:
                                            self.new_game()                                  
                                        if reply == messagebox.NO:
                                            quit()                                                    
                        self._dungeon2.draw_grid(self._dungeon, self.player_position)                    
                    self.player.change_move_count(-1)    
                if self._game.check_game_over():                  
                    messagebox.showinfo(title='You lose!', message=LOSE_TEST)
                    return

    def left_click2(self,event):
        """MASTERS click control"""
        if self._game.won() == False:
            if self.player.moves_remaining() > 0:
                c = event.x,event.y
                x = self._keypad.pixel_to_direction(c)
                if x in DIRECTIONS:      
                    if not self._game.collision_check(x):
                        self._game.move_player(x)
                        entity = self._game.get_entity(self.player.get_position()) 
                        self.player = self._game.get_player()
                        self.player_position = self.player.get_position()
                        self._dungeon2.delete(tk.ALL)   
                        if entity is not None:
                                    entity.on_hit(self._game)                         
                                    if self._game.won():
                                        self.enter_end()
                        self._dungeon2.draw_grid(self._dungeon, self.player_position)                
                    self.player.change_move_count(-1)    
                if self._game.check_game_over():                   
                    messagebox.showinfo(title='You lose!', message=LOSE_TEST)
                    return
