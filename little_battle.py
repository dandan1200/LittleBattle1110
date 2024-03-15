import sys

class PlayerResources():
  def __init__(self,gold,food,wood):
    self.gold = gold
    self.food = food
    self.wood = wood
  
  def add(self,resource):
    if resource == "WW":
      self.wood += 2
    elif resource == "FF":
      self.food += 2
    elif resource == "GG":
      self.gold += 2
  
  def get_name(self,name):
    if name == "WW":
      return "Wood"
    if name == "GG":
      return "Gold"
    if name == "FF":
      return "Food"

class PlayerArmies():
  def __init__(self):
    self.spearmans = []
    self.archers = []
    self.knights = []
    self.scouts = []
  
  def add_army(self,army,x,y):
    if army == "S":
      self.spearmans.append((x,y))
    elif army == "A":
      self.archers.append((x,y))
    elif army == "K":
      self.knights.append((x,y))
    elif army == "T":
      self.scouts.append((x,y))
    
  def check_no_armies(self):
    if len(self.spearmans) == 0 and len(self.archers) == 0 and len(self.knights) == 0 and len(self.scouts) == 0:
      return True
    else:
      return False
    
  def total(self):
    total = self.spearmans + self.archers + self.knights + self.scouts
    return total

  def get_army_in_loc(self,x,y):
    if (x,y) in self.spearmans:
      return "S"
    if (x,y) in self.archers:
      return "A"
    if (x,y) in self.knights:
      return "K"
    if (x,y) in self.scouts:
      return "T"

  def army_destroyed(self,x,y):
    if (x,y) in self.spearmans:
      self.spearmans.remove((x,y))
    if (x,y) in self.archers:
      self.archers.remove((x,y))
    if (x,y) in self.knights:
      self.knights.remove((x,y))
    if (x,y) in self.scouts:
      self.scouts.remove((x,y))
  
class Player():
  def __init__(self,name,resources,armies,home_x,home_y,valid_locations):
    self.name = name
    self.resources = resources
    self.armies = armies
    self.home_base = (home_x,home_y)
    self.valid_locations = valid_locations

  def get_locations(self):
    return self.valid_locations.copy()
  
# Recruit prices of format - [Army type, wood required, food required, gold required]
recruit_prices = [["S",1,1,0],["A",1,0,1],["K",0,1,1],["T",1,1,1]]

# Please implement this function according to Section "Read Configuration File"
def load_config_file(filepath):
  # It should return width, height, waters, woods, foods, golds based on the file
  # Complete the test driver of this function in file_loading_test.py
  #__
  #Open file - raise error if file not found  
  fl = open(filepath,"r")
  #__
  
  validFile = True

  #__
  #Check content order error
  lines = fl.readlines()
  if "Frame: " in lines[0] and "Water: " in lines[1] and "Wood: " in lines[2] and "Food: " in lines[3] and "Gold: " in lines[4]:
    validFile = True
  else:
    raise SyntaxError("Invalid Configuration File: format error!")
  #__

  #__
  #Check frame format error
  if lines[0][8] != "x" and len(lines[0]) != 10:
    raise SyntaxError("Invalid Configuration File: frame should be in format widthxheight!")
  if lines[0][7].isdigit() != True or lines[0][9].isdigit() != True:
    raise SyntaxError("Invalid Configuration File: frame should be in format widthxheight!")

  #__

  #__
  #Check frame between 5 and 7 error
  if int(lines[0][7]) < 5 or int(lines[0][7]) > 7 or int(lines[0][9]) < 5 or int(lines[0][9]) > 7:
    raise ArithmeticError("Invalid Configuration File: width and height should range from 5 to 7!")
  else:
    width = int(lines[0][7])
    height = int(lines[0][9])
  #__
  width, height = int(lines[0][7]), int(lines[0][9])
  lines.pop(0)
  #__
  #Check for non-integar values error
  for x in lines:
    lstrip,rstrip = x.split(":")
    rstrip = rstrip.replace(" ","").strip()
    if rstrip.isdigit() == False:
      raise ValueError("Invalid Configuration File: {} contains non integer characters!".format(lstrip))
  #__

  #__
  #Check for uneven number of elements
  for x in lines:
    lstrip,rstrip = x.split(":")
    rstrip = rstrip.replace(" ","").strip()
    if len(rstrip) % 2 != 0:
      raise SyntaxError("Invalid Configuration File: {} has an odd number of elements!".format(lstrip))
  #__

  #__
  #Check pos within map error
  for x in lines: 
    lstrip,rstrip = x.split(":")
    rstrip = rstrip.replace(" ","").strip()
    for i in range(len(rstrip)):
      if i % 2 == 0:
        if int(rstrip[i]) < 0 or int(rstrip[i]) > height:
          raise ArithmeticError("Invalid Configuration File: {} contains a position that is out of map".format(lstrip))
      else:
        if int(rstrip[i]) < 0 or int(rstrip[i]) > width:
          raise ArithmeticError("Invalid Configuration File: {} contains a position that is out of map".format(lstrip))
  #__

  #__
  #Check not on home bases or surrounding positions
  for x in lines: 
    lstrip,rstrip = x.split(":")
    rstrip = rstrip.replace(" ","").strip()
    i = 0
    while i < len(rstrip):
      if (int(rstrip[i]) == 1 and int(rstrip[i+1]) == 1):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == 1 and int(rstrip[i+1]) == 0):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == 1 and int(rstrip[i+1]) == 2):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == 2 and int(rstrip[i+1]) == 1):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == 0 and int(rstrip[i+1]) == 1):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == width-2 and int(rstrip[i+1]) == height-2):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == width-1 and int(rstrip[i+1]) == height-2):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == width-2 and int(rstrip[i+1]) == height-1):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == width-3 and int(rstrip[i+1]) == height-2):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
      elif (int(rstrip[i]) == width-2 and int(rstrip[i+1]) == height-3):
        raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")

      i+=2
  #__

  #__
  #Check positions arent doubled
  list_of_locations = []
  list_for_return = [[],[],[],[]]
  for x in lines:
    lstrip,rstrip = x.split(":")
    rstrip = rstrip.replace(" ","").strip()
    for i in range(0,len(rstrip),2):
      if (rstrip[i],rstrip[i+1]) in list_of_locations:
        raise SyntaxError("Invalid Configuration File: Duplicate position ({}, {})!".format(rstrip[i],rstrip[i+1]))
      else:
        list_of_locations.append((rstrip[i],rstrip[i+1]))
        list_for_return[lines.index(x)].append((int(rstrip[i]),int(rstrip[i+1])))
  #__

  fl.close()
  waters, woods, foods, golds = list_for_return[0], list_for_return[1], list_for_return[2], list_for_return[3] # list of position tuples
  print("Configuration file config.txt was loaded.")
  return width, height, waters, woods, foods, golds

def initialise_map_and_players(width,height,waters,woods,foods,golds):
  # Take input from file and construct 2D list of map.
  map_ls = []
  for y in range(height):
    map_ls.append([])
    for x in range(width):
      map_ls[y].append("  ")
  
  for x in waters:
    map_ls[x[1]][x[0]] = "~~"
  
  for x in woods:
    map_ls[x[1]][x[0]] = "WW"

  for x in foods:
    map_ls[x[1]][x[0]] = "FF"

  for x in golds:
    map_ls[x[1]][x[0]] = "GG"

  map_ls[1][1] = "H1" 
  map_ls[height-2][width-2] = "H2"
  

  print("Game Started: Little Battle! (enter QUIT to quit the game)")
  return map_ls

def recruit_armies(player,width,height):
  # Function for recruit armies section of turn. Take inputs for what army and position and validates.

  print("\n[Your Asset: Wood - " + str(player.resources.wood) + " Food - " + str(player.resources.food) + " Gold - " + str(player.resources.gold)+"]")
  
  
  #Check for sufficient resources
  sufficient_resources = True
  for x in recruit_prices:
    
    if player.resources.wood < x[1] or player.resources.food < x[2] or player.resources.gold < x[3]:
      sufficient_resources = False
      
    else: 
      sufficient_resources = True
      break
  if sufficient_resources == False:
    print("No resources to recruit any armies.")
    return

  #Check for sufficient space for armies
  if player.name == "1":
    if map_ls[0][1] != "  " and map_ls[1][0] != "  " and map_ls[1][2] != "  " and map_ls[2][1] != "  ":
      print("No place to recruit new armies.")
      return
  else:
    if map_ls[height-1][width-2] != "  " and map_ls[height-2][width-1] != "  " and map_ls[height-2][width-3] != "  " and map_ls[height-3][width-2] != "  ":
      print("No place to recruit new armies.")
      return

  valid_recruit = False
  valid_answers = ['S','A','K','T','NO','DIS','PRIS','QUIT']
  while valid_recruit == False:
    print("\nWhich type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter ‘NO’ to end this stage.")
    recruitment = input()
    if recruitment not in valid_answers:
      valid_recruit = False
      print("Sorry, invalid input. Try again.")
    elif recruitment == "NO":
      return
    elif recruitment == "DIS":
      display_map(map_ls)
    elif recruitment == "PRIS":
      print_prices()
    elif recruitment == "QUIT":
      exit()
    else:
      valid_recruit = True
      for x in recruit_prices:
        if recruitment in x:
          if player.resources.wood < x[1] or player.resources.food < x[2] or player.resources.gold < x[3]:
            valid_recruit = False
            print("Insufficient resources. Try again.")
            break
          else:
            price_index_for_recruit = recruit_prices.index(x)
            valid_recruit = True
            break 
         
  # Sufficient resources at this point

  recruit_name = get_army_name(recruitment)
    
  valid_coords = False
  while valid_coords == False:
    print("\nYou want to recruit a {}. Enter two integers as format ‘x y’ to place your army.".format(recruit_name))
    coords_input = input()

    try:
      new_x,new_y = coords_input.split(" ")

      valid_army_placement = player.get_locations()

      for x in valid_army_placement:
        if map_ls[x[1]][x[0]] != "  ":
          valid_army_placement.pop(valid_army_placement.index(x))

      coords_tuple = (new_x,new_y)
      #error check the coordinate entry
      if new_x.isdigit() != True and new_y.isdigit() != True:
        print("Sorry, invalid input. Try again.")
        
      elif (int(new_x),int(new_y)) not in valid_army_placement:
        print("You must place your newly recruited unit in an unoccupied position next to your home base. Try again.")
        
      
      else:
        new_x = int(new_x)
        new_y = int(new_y)
        valid_coords == True
        print("\nYou has recruited a {}.".format(recruit_name))
        player.resources.wood -= recruit_prices[price_index_for_recruit][1]
        player.resources.food -= recruit_prices[price_index_for_recruit][2]
        player.resources.gold -= recruit_prices[price_index_for_recruit][3]
        map_ls[new_y][new_x] = "{}{}".format(recruitment,player.name)
        player.armies.add_army(recruitment,new_x,new_y)
        recruit_armies(player,width,height) 
        return
      
    except ValueError:  
      if coords_input == "PRIS":
        print_prices()
      elif coords_input == "DIS":
        display_map(map_ls)
      elif coords_input == "QUIT":
        exit()
      else:
        print("Sorry, invalid input. Try again.")

def move_armies(player,opp_player,year,width,height):
  # Function for move armies section of turn. Takes input for starting and ending coordinates and validates
  print("\n===Player {}'s Stage: Move Armies===".format(player.name))
  movable_armies = player.armies.total()
  while len(movable_armies) > 0:

    valid_move = False
    while valid_move == False:

      if player.armies.check_no_armies() == True:
        print("\nNo Army to Move: next turn")
        return
      else:
        print_armies_to_move(player,movable_armies)
        try:
          print("\nEnter four integers as a format ‘x0 y0 x1 y1’ to represent move unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.")
          coords_input = input()

          x1,y1,x2,y2 = coords_input.split(" ")

          #Testing validity of the coordinates

          #are the coordinates digits
          if x1.isdigit() != True or y1.isdigit() != True or x2.isdigit() != True or y2.isdigit() != True:
            raise ValueError
          
          x1 = int(x1)
          y1 = int(y1)
          x2 = int(x2)
          y2 = int(y2)

          #trying to move over own base
          if (x2,y2) == player.home_base:
            raise ValueError

          #are the first coordinates a location of an army.
          if (x1,y1) not in movable_armies:
            raise ValueError
          
          #is the move location not occupied by own army.
          if (x2,y2) in player.armies.total():
            raise ValueError
          
          #is the move location off the map
          if x2 > width-1 or x2 < 0 or y2 > height-1 or y2 < 0:
            raise ValueError
          
          #move distance test for scouts
          if (x1,y1) in player.armies.scouts:
            #Is the move distance more than allowed in any direction
            if abs(x1-x2) > 2 or abs(y1-y2) > 2:
              raise ValueError
            #is the move either left right up or down
            elif (bool(abs(x1-x2) != 0) + bool((y1-y2) != 0)) != 1:
              raise ValueError
          else:
            #same as above for other armies
            if abs(x1-x2) > 1 or abs(y1-y2) > 1:
              raise ValueError
            elif (bool(abs(x1-x2) != 0) + bool((y1-y2) != 0)) != 1:
              raise ValueError
          
          
          valid_move = True 

        except ValueError:
          if coords_input == "PRIS":
            print_prices()
          elif coords_input == "DIS":
            display_map(map_ls)
          elif coords_input == "QUIT":
            exit()
          elif coords_input == "NO":
            return
          else:
            print("Invalid move. Try again.")
        

    #Valid move entered
    movable_armies.remove((x1,y1))
    attacker = player.armies.get_army_in_loc(x1,y1)

    if (abs(x1-x2) < 2 and abs(y1-y2) < 2) == False :
      scout_move(player,opp_player,x1,y1,x2,y2,attacker,year)
    else:
      check_single_move(player,opp_player,x1,y1,x2,y2,attacker,year,None)
          
  print("\nNo Army to Move: next turn.")

def scout_move(player,opp_player,x1,y1,x2,y2,attacker,year):
  #check middle pos:
  if x1-x2 == 2:
    tx2 = x2 + 1
    ty2 = y2
  elif x1-x2 == -2:
    tx2 = x2 - 1
    ty2 = y2
  elif y1-y2 == 2:
    ty2 = y2 + 1
    tx2 = x2
  elif y1-y2 == -2:
    ty2 = y2 - 1
    tx2 = x2
  #if middle space is empty or ok to pass over
  if map_ls[ty2][tx2] == "  " or (tx2,ty2) in player.armies.total() or (tx2,ty2) == player.home_base:
    check_single_move(player,opp_player,x1,y1,x2,y2,attacker,year,None)
    return
 
  #if middle space is enemy army
  elif (tx2,ty2) in opp_player.armies.total():
    defender = opp_player.armies.get_army_in_loc(tx2,ty2) 
        
    #move to same type army
    if attacker == defender:
      print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
      print("We destroyed the enemy {} with massive loss!".format(get_army_name(defender)))
      player.armies.army_destroyed(x1,y1)
      opp_player.armies.army_destroyed(tx2,ty2)
      map_ls[y2][x2] = "  "
      map_ls[y1][x1] = "  "
      return False

    #Lose battle with move
    elif battle_win(attacker,defender) == False:
      player.armies.army_destroyed(x1,y1)
      map_ls[y1][x1] = "  "
      print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
      print("We lost the army {} due to your command!".format(get_army_name(attacker)))
      return True
  
  elif (tx2,ty2) == opp_player.home_base:
    print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))

    print("The army {} captured the enemy’s capital.".format(get_army_name(attacker)))
    print("\nWhat’s your name, commander?")
    commander_name = input()
    print("\n***Congratulation! Emperor {} unified the country in {}.***".format(commander_name, year))
    exit()
  
  elif map_ls[ty2][tx2] == "~~":
    print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
    print("We lost the army {} due to your command!".format(get_army_name(attacker)))
    player.armies.army_destroyed(x1,y1)
    map_ls[y1][x1] = "  "
    return

  else:
    #player moves to resource
    mid_res_print = "Good. We collected 2 {}.".format(player.resources.get_name(map_ls[ty2][tx2]))
    player.resources.add(str(map_ls[ty2][tx2]))
    map_ls[ty2][tx2] = "  "
    check_single_move(player,opp_player,x1,y1,x2,y2,attacker,year,mid_res_print)
    return
    
def check_single_move(player,opp_player,x1,y1,x2,y2,attacker,year,mid_res_print):

  if map_ls[y2][x2] == "  ":
    map_ls[y2][x2] = player.armies.get_army_in_loc(x1,y1) + player.name
    map_ls[y1][x1] = "  "
    player.armies.add_army(player.armies.get_army_in_loc(x1,y1),x2,y2)
    player.armies.army_destroyed(x1,y1)
    print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))

    if mid_res_print != None:
      print(mid_res_print)
    
    return False
      
  #move to water
  elif map_ls[y2][x2] == "~~":
    map_ls[y1][x1] = "  "
    player.armies.army_destroyed(x1,y1)
    print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
    if mid_res_print != None:
      print(mid_res_print)
    print("We lost the army {} due to your command!".format(get_army_name(attacker)))
    return True

  #if player moves to player.
  elif (x2,y2) in opp_player.armies.total():
    defender = opp_player.armies.get_army_in_loc(x2,y2) 
    
        
    #move to same type army
    if attacker == defender:
      print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
      if mid_res_print != None:
        print(mid_res_print)
      print("We destroyed the enemy {} with massive loss!".format(get_army_name(defender)))
      player.armies.army_destroyed(x1,y1)
      opp_player.armies.army_destroyed(x2,y2)
      map_ls[y2][x2] = "  "
      map_ls[y1][x1] = "  "
      return False

    #Win battle with move
    elif battle_win(attacker,defender) == True:
      opp_player.armies.army_destroyed(x2,y2)
      map_ls[y2][x2] = player.armies.get_army_in_loc(x1,y1) + player.name
      map_ls[y1][x1] = "  "
      player.armies.add_army(player.armies.get_army_in_loc(x1,y1),x2,y2)
      player.armies.army_destroyed(x1,y1)
      print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
      if mid_res_print != None:
        print(mid_res_print)
      print("Great! We defeated the enemy {}!".format(get_army_name(defender)))
      return False

    #Lose battle with move
    elif battle_win(attacker,defender) == False:
      player.armies.army_destroyed(x1,y1)
      map_ls[y1][x1] = "  "
      print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
      if mid_res_print != None:
        print(mid_res_print)
      print("We lost the army {} due to your command!".format(get_army_name(attacker)))
      return True

  elif (x2,y2) == opp_player.home_base:
    print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
    if mid_res_print != None:
      print(mid_res_print)
    print("The army {} captured the enemy’s capital.".format(get_army_name(attacker)))
    print("\nWhat’s your name, commander?")
    commander_name = input()
    print("\n***Congratulation! Emperor {} unified the country in {}.***".format(commander_name, year))
    exit()

  else:
    #player moves to resource
    print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(get_army_name(attacker),x1,y1,x2,y2))
    if mid_res_print != None:
      print(mid_res_print)
    print("Good. We collected 2 {}.".format(player.resources.get_name(map_ls[y2][x2])))
    player.resources.add(str(map_ls[y2][x2]))
    map_ls[y2][x2] = player.armies.get_army_in_loc(x1,y1) + player.name
    map_ls[y1][x1] = "  "
    player.armies.add_army(player.armies.get_army_in_loc(x1,y1),x2,y2)
    player.armies.army_destroyed(x1,y1)
    return False

def battle_win(a,b):
  if b == "T":
    return True
  elif a == "S" and b == "K":
    return True
  elif a == "A" and b == "S":
    return True
  elif a == "K" and b == "A":
    return True
  else:
    return False

def get_army_name(army):
  if army == "S":
    return "Spearman"
  elif army == "A":
    return "Archer"
  elif army == "K":
    return "Knight"
  elif army == "T":
    return "Scout"  

def print_prices():
  #prints list of resources and the prices
  """
  Example:
  Recruit Prices:
    Spearman (S) - 1W, 1F
    Archer (A) - 1W, 1G
    Knight (K) - 1F, 1G
    Scout (T) - 1W, 1F, 1G
  """
  print("""Recruit Prices:
  Spearman (S) - 1W, 1F
  Archer (A) - 1W, 1G
  Knight (K) - 1F, 1G
  Scout (T) - 1W, 1F, 1G""")
 
def display_map(map_ls):
  # Displays map and contents on the screen.
  """
  Example:
   X00 01 02 03 04X
  Y+--------------+
 00|~~|  |  |  |  |
 01|  |H1|  |FF|GG|
 02|WW|  |GG|  |~~|
 03|  |~~|  |H2|  |
 04|FF|  |WW|  |  |
  Y+--------------+

  """
  print("Please check the battlefield, commander.")
  line = "  X00"
  for x in range(1, width):
    line += " 0{}".format(x)
  
  line +="X"
  print(line)
  line = " Y+" + "-"*(width*2 + width-1) + "+"
  print(line)
  
  line = ""
  for y in range(height):
    line = "0{}|".format(y)
    for x in range(width):
      if map_ls[y][x] == "":
        line += "  |"
      else:
        line += map_ls[y][x] + "|"
      
    print(line)

    
  line = " Y+" + "-"*(width*2 + width-1) + "+"
  print(line)  

def print_armies_to_move(player, movable_armies):
  # shows the positions of your armies that haven’t moved in this stage in the order of recruitment time
  """
    Example:
    Armies to Move:
    Spearman: (x1, y1), (x2, y2)
    Archer: (x3, y3)
    Knight: (x4, y4), (x5, y5)
    Scout: (x6, y6)"""
  print("\nArmies to Move:")

  spearman = [0,"  Spearman: "]
  archers = [0,"  Archer: "]
  knights = [0,"  Knight: "]
  scouts = [0,"  Scout: "]

  for x in movable_armies:
    if x in player.armies.spearmans:
      spearman[1] += (str(x) + ", ")
      spearman[0] += 1
    if x in player.armies.archers:
      archers[1] += (str(x) + ", ")
      archers[0] += 1
    if x in player.armies.knights:
      knights[1] += (str(x) + ", ")
      knights[0] += 1
    if x in player.armies.scouts:
      scouts[1] += (str(x) + ", ")
      scouts[0] += 1
    
  if spearman[0] > 0:
    print(spearman[1][:-2])
  if archers[0] > 0:
    print(archers[1][:-2])
  if knights[0] > 0:
    print(knights[1][:-2])
  if scouts[0] > 0:
    print(scouts[1][:-2])

  
#MAIN LINE
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 little_battle.py <filepath>")
    sys.exit()

  width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
  map_ls = initialise_map_and_players(width,height,waters,woods,foods,golds)
  #Initial print sequence
  print()
  display_map(map_ls)
  print("(enter DIS to display the map)\n")
  print_prices()
  print("(enter PRIS to display the price list)")

  initial_resources = PlayerResources(2,2,2)
  initial_resources2 = PlayerResources(2,2,2)
  initial_armies = PlayerArmies()
  initial_armies2 = PlayerArmies()
  valid_loc = [(1,0),(0,1),(2,1),(1,2)]
  valid_loc2 = [(width-2,height-1),(width-1,height-2),(width-3,height-2),(width-2,height-3)]
  players = []
  players.append(Player("1",initial_resources,initial_armies,1,1,valid_loc))
  players.append(Player("2",initial_resources2,initial_armies2,width-2,height-2,valid_loc2))

  #Start turns
  year = 617
  game_over = False
  #Turn = 0 -> player 1
  #Turn = 1 -> player 2
  turn = 0
  opp_turn = 1
  while game_over == False:
    print("\n-Year {}-".format(year))
    print("\n+++Player {}'s Stage: Recruit Armies+++".format(turn+1))
    recruit_armies(players[turn],width,height)
    move_armies(players[turn],players[opp_turn],year,width,height) 
    
    temp = turn
    turn = opp_turn
    opp_turn = temp

    if turn == 0:
      year += 1
    