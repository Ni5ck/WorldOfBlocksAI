# Foundations of AI - Final Project
# Author: Nicholas Ianni

###################################
# Location class
#
# Class variables:
# stack: the ordered stack at the associated location
# name: the name of the location
###################################

class Location:

    ###############################
    # Constructor
    # Initializes the location with the associated name of the location
    # and the ordered stack at the location
    #
    # Parameters:
    # self: the Location object
    # stack: the ordered stack at the associated location
    # name: the name of the location
    ###############################

    def __init__(self, stack, name):
        self.stack = stack
        self.name = name

    ###############################
    # take_top
    # Takes a block from the top of the stack at this location
    #
    # Parameter:
    # self: the Location object
    #
    # Returns the top object of the stack.
    # Returns '0' and prints an error upon trying to take from an empty stack.
    ###############################

    def take_top(self):
        # If the stack is not empty, return and remove the top item from the stack
        if not(len(self.stack) == 0):
            return self.stack.pop()
        # Otherwise, print an error message
        else:
            print("Error: Tried to take from an empty stack at location " + self.name + ".\n")
            return '0'

    ###############################
    # put_top
    # Puts a specified item on top of the stack at the associated location.
    #
    # Parameters:
    # self: the Location object
    # item: the item from the Arm to put on the top of the stack
    ###############################

    def put_top(self, item):
        self.stack.append(item)

###################################
# Arm class
#
# Class variables:
# place: the arm's current location
# item: the current item the arm is holding (0 means that the arm is empty)
###################################

class Arm:

    ###############################
    # Constructor
    # Initializes the Arm object
    #
    # Parameters:
    # self: the Arm object
    # place: the arm's current location
    # item: the current item the arm is holding (0 means that the arm is empty)
    ###############################

    def __init__(self, place, item):
        self.place = place
        self.item = item

    ###############################
    # move
    # Moves the arm from the arm's inital location to a new location
    #
    # Parameters:
    # self: the Arm object
    # place: the place the arm will move to
    ###############################

    def move(self, place):
        self.place = place

    ###############################
    # pick_up
    # Picks up the block at the arm's current location and returns the updated
    # Location object
    #
    # Parameter:
    # self: the Arm object
    #
    # Returns the updated Location object
    # Prints an error if the arm is currently holding an item
    ###############################

    def pick_up(self):
        # If the Arm is empty (marked by item being 0), take the object
        if self.item == '0':
            self.item = self.place.take_top()
        # Otherwise, print an error message
        else:
            print("Error: Tried to pick up at location " + self.place.name + ".\n")
        # Return the updated Location object
        return self.place

    ###############################
    # put_down
    # Puts the item the arm is holding down onto the location and returns the
    # updated Location object
    #
    # Parameter:
    # self: the Arm object
    #
    # Returns the updated Location object
    # Prints an error is the arm is not currently holding an item
    ###############################

    def put_down(self):
        # If the arm is not empty (not '0'), place the item on top of the stack
        if not(self.item == '0'):
            self.place.put_top(self.item)
            self.item = '0'
        # Otherwise, print an error message
        else:
            print("Error: Tried to put down without an item in the arm.\n")
        # Return the updated Location object
        return self.place

###################################
# State class
#
# Class variables:
# l1: the first Location object at the given state (L1)
# l2: the second Location object at the given state (L2)
# l3: the third Location object at the given state (L3)
# arm: the Arm object at the given state
# num: the state number
###################################

class State:

    ###############################
    # Constructor
    # Initializes the State object
    #
    # Parameters:
    # self: the State object
    # l1: the first Location object at the given state (L1)
    # l2: the second Location object at the given state (L2)
    # l3: the third Location object at the given state (L3)
    # num: the state number
    ###############################

    def __init__(self, l1, l2, l3, num):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        # Starts the arm at L1
        self.arm = Arm(self.l1, '0')
        self.num = num

    ###############################
    # get_relations
    # Returns a list of relations for the given state
    #
    # Parameter:
    # self: the State object
    #
    # Returns a list of relations for the given state
    ###############################

    def get_relations(self):
        # Create a blank list for relations to be appended to
        relations = []

        # Table relation
        # For each location, if the location is not empty, create a relation for
        # the block that is touching the table with the following form:
        # ['t' (Table), (block touching table)]
        if not(len(self.l1.stack) == 0):
            relations.append(['t', self.l1.stack[0]])
        if not(len(self.l2.stack) == 0):
            relations.append(['t', self.l2.stack[0]])
        if not(len(self.l3.stack) == 0):
            relations.append(['t', self.l3.stack[0]])

        # On relation
        # For each location, create a relation for each pair of blocks directly
        # on top of each other with the following form:
        # ['o' (On), (block above), (block below)]
        for i in range(len(self.l1.stack)):
            if not(i+1 == len(self.l1.stack)):
                relations.append(['o', self.l1.stack[i+1], self.l1.stack[i]])
        for i in range(len(self.l2.stack)):
            if not(i+1 == len(self.l2.stack)):
                relations.append(['o', self.l2.stack[i+1], self.l2.stack[i]])
        for i in range(len(self.l3.stack)):
            if not(i+1 == len(self.l3.stack)):
                relations.append(['o', self.l3.stack[i+1], self.l3.stack[i]])

        # Clear relation
        # For each location, if the stack is not empty, create a relation where
        # a block does not have a block on top of it with the following form:
        # ['c' (Clear), (block on top of stack)]
        if not(len(self.l1.stack) == 0):
            relations.append(['c', self.l1.stack[len(self.l1.stack) - 1]])
        if not(len(self.l2.stack) == 0):
            relations.append(['c', self.l2.stack[len(self.l2.stack) - 1]])
        if not(len(self.l3.stack) == 0):
            relations.append(['c', self.l3.stack[len(self.l3.stack) - 1]])

        # Above relation
        # Only check for "Above" if the arm is not empty (marked by item being 0)
        if not(self.arm.item == '0'):
            # For each location, create a relation where the arm is holding an
            # item above a block or stack with the following form:
            # ['a' (Above), (block held by arm), (block on top of stack)]
            if self.arm.place.name == 'L1':
                relations.append(['a', self.arm.item, self.l1.stack[len(self.l1.stack) - 1]])
            elif self.arm.place.name == 'L2':
                relations.append(['a', self.arm.item, self.l2.stack[len(self.l2.stack) - 1]])
            elif self.arm.place.name == 'L3':
                relations.append(['a', self.arm.item, self.l3.stack[len(self.l3.stack) - 1]])

        # Return the list of relations
        return relations

    ###################################
    # print_state
    # Outputs a text interpretation of the given state
    #
    # Parameter:
    # self: the State object
    ###################################

    def print_state(self):
        # Print the state number
        print("State " + str(self.num) + ":")
        # Print the arm in it's current location
        # If the arm is in L1...
        if self.arm.place.name == 'L1':
            # Print the formatted arm stem
            print(" |")
            # If the arm is empty (marked by item being 0), print an empty arm
            if self.arm.item == '0':
                print("/ \\")
            # Otherwise, print an arm with the associated item within the arm
            else:
                print("/" + self.arm.item + "\\")
        # If the arm is in L2...
        elif self.arm.place.name == 'L2':
            # Print the formatted arm stem
            print("    |")
            # If the arm is empty (marked by item being 0), print an empty arm
            if self.arm.item == '0':
                print("   / \\")
            # Otherwise, print an arm with the associated item within the arm
            else:
                print("   /" + self.arm.item + "\\")
        # If the arm is in L3...
        elif self.arm.place.name == 'L3':
            # Print the formatted arm stem
            print("       |")
            # If the arm is empty (marked by item being 0), print an empty arm
            if self.arm.item == '0':
                print("      / \\")
            # Otherwise, print an arm with the associated item within the arm
            else:
                print("      /" + self.arm.item + "\\")
        # If the arm is not recognized at any of these locations, print an error
        else:
            print("Error: Unknown arm location.\n")
        print("")
        # Determine the max index of all the stacks
        maxIndex = len(self.l1.stack)
        if maxIndex < len(self.l2.stack):
            maxIndex = len(self.l2.stack)
        if maxIndex < len(self.l3.stack):
            maxIndex = len(self.l3.stack)
        # Loop for each height of blocks
        for n in range(maxIndex):
            print(" ", end="")
            # If the L1 stack has a block at the given height, print the block
            if maxIndex - n <= len(self.l1.stack):
                print(self.l1.stack[maxIndex - n - 1], end="")
            # Otherwise, make the L1 slot at that height empty
            else:
                print(" ", end="")
            print("  ", end="")
            # If the L2 stack has a block at the given height, print the block
            if maxIndex - n <= len(self.l2.stack):
                print(self.l2.stack[maxIndex - n - 1], end="")
            # Otherwise, make the L2 slot at that height empty
            else:
                print(" ", end="")
            print("  ", end="")
            # If the L3 stack has a block at the given height, print the block
            if maxIndex - n <= len(self.l3.stack):
                print(self.l3.stack[maxIndex - n - 1], end="")
            # Otherwise, make the L3 slot at that height empty
            else:
                print(" ", end="")
            print("")
        # Draw the table an stack locations
        print("=========")
        print(" L1 L2 L3\n")

#######################################
# Planner class
#
# Class variables:
# state: the current state
# state_g: the goal state
# relations_c: the set of relations for the current state (changes each state)
# relations_g: the set of relations for the goal state (created once)
# satisfied: a set of booleans directly mapped to relations_g that denote
# if the associated relation is present in both relations_c and relations_g
#######################################

class Planner:

    ###################################
    # Constructor
    # Initializes the planner object
    #
    # Parameters:
    # self: the Planner object
    # l1i: the initial state's first location
    # l2i: the initial state's second location
    # l3i: the initial state's third location
    # l1g: the goal state's first location
    # l2g: the goal state's second location
    # l3g: the goal state's third location
    ###################################

    def __init__ (self, l1i, l2i, l3i, l1g, l2g, l3g):
        self.state = State(Location(l1i, 'L1'), Location(l2i, 'L2'), Location(l3i, 'L3'), 0)
        self.state_g = State(Location(l1g, 'L1'), Location(l2g, 'L2'), Location(l3g, 'L3'), 0)
        self.relations_c = self.state.get_relations()
        self.relations_g = self.state_g.get_relations()
        self.satisfied = []
        for i in range(len(self.relations_g)):
            self.satisfied.append(False)

    ###################################
    # search4relations
    # Searches the relation list for relations of a specified type
    #
    # Parameters:
    # self: the Planner object
    # relations: the list of relations of the state
    # type: the type of relation to be searched for ->
    # -> 't' for Table, 'o' for On, 'a' for Above, and 'c' for Clear
    #
    # Returns a list of relations from the relation list filtered by the given type
    ###################################

    def search4relations (self, relations, type):
        list = []
        # For each relation in relations, only append to list those relations of
        # the specified type
        for r in range(len(relations)):
            if relations[r][0] == type:
                list.append(relations[r])
        # Return the completed list
        return list

    ###################################
    # search4block
    # For the given state, find which location the block in question is located at
    #
    # Parameters:
    # self: the Planner object
    # state: the state to search within
    # block: the block to find in the given state
    #
    # Returns the location of the block
    # Returns an error if the block is either held by the arm or the block is not found
    ###################################

    def search4block (self, state, block):
        found = False
        location = ''
        # Check L1 for the block
        for i in range(len(state.l1.stack)):
            # If found, change location to L1, change found to true, then stop
            if state.l1.stack[i] == block:
                found = True
                location = 'L1'
                break
        # If the block was not found in L1, check L2 for the block
        if not(found):
            for i in range(len(state.l2.stack)):
                # If found, change location to L2, change found to true, then stop
                if state.l2.stack[i] == block:
                    found = True
                    location = 'L2'
                    break
        # If the block was not found in L1 or L2, check L3 for the block
        if not(found):
            for i in range(len(state.l3.stack)):
                # If found, change location to L3, change found to true, then stop
                if state.l3.stack[i] == block:
                    found = True
                    location = 'L3'
                    break
        # If the block was not found, print an appropriate error message
        if not(found):
            if state.arm.item == block:
                print("Error: search4block used when block was in arm.\n")
            else:
                print("Error: search4block did not find block.\n")
        # Return the location (if an error is printed, an empty string is returned)
        return location

    ###################################
    # compare_relations
    # Compares the relations of a given type and returns an ordered list of
    # relations to solve for. This function also updates the satisfied function
    # for those relations that are already true (with some exception to On
    # relation, as some On relations are deemed only temporarily satisfied).
    #
    # Parameters:
    # self: the Planner object
    # type: the type of relation being tested for
    #
    # Returns an ordered list of relations to solve for of the given type
    # Prints an error and returns an empty set if type is not 't', 'o', or 'c'
    #
    # Side effect: Alters the satisfied list
    ###################################

    def compare_relations (self, type):
        list = []
        # Table relation, 't'
        if type == 't':
            # Find all relations of type Table for the current state
            current = self.search4relations(self.relations_c, 't')
            # Find all relations of type Table for the goal state
            goal = self.search4relations(self.relations_g, 't')
            # For each goal relation of type 't'...
            for i in range(len(goal)):
                # Search for a relation that matches goal[i]
                match = False
                for j in range(len(current)):
                    # If the relations match, set match to true, then stop
                    if goal[i][1] == current[j][1]:
                        match = True
                        break
                # If a match is found...
                if match:
                    # Find the corresponding relation in relations_g, then stop
                    for k in range(len(self.relations_g)):
                        if goal[i][0] == self.relations_g[k][0] and goal[i][1] == self.relations_g[k][1]:
                            self.satisfied[k] = True
                            break
                # If a match is not found...
                else:
                    # Add the goal relation to the list
                    list.append(goal[i])
            # END OF LOOP - list is ready to be returned

        # On relation, 'o'
        elif type == 'o':
            # Find all relations of type On for the current state
            current = self.search4relations(self.relations_c, 'o')
            # Find all relations of type Table for the current state
            current_t = self.search4relations(self.relations_c, 't')
            # Find all relations of type Clear for the current state
            current_c = self.search4relations(self.relations_c, 'c')

            # Find all relations of type On for the goal state
            goal = self.search4relations(self.relations_g, 'o')
            # Find all relations of type Table for the goal state
            goal_t = self.search4relations(self.relations_g, 't')

            # To order the tasks, find the location where a block is both
            # Table and Clear (such a block may not be found)
            found = False
            order = ['L1']
            for i in range(len(current_t)):
                for j in range(len(current_c)):
                    # If a block is both Table and Clear, save the block's location
                    if current_t[i][1] == current_c[j][1]:
                        found = True
                        order[0] = self.search4block(self.state, current_t[i][1])
                        break
                if found:
                    break
            # Complete the order for each case
            if order[0] == 'L1':
                order.append('L3')
                order.append('L2')
            elif order[0] == 'L2':
                order.append('L1')
                order.append('L3')
            elif order[0] == 'L3':
                order.append('L2')
                order.append('L1')
            # If location is blank, an error occured (print error message)
            else:
                print("Error: compare_relations failed from search4block.\n")
            # For each location in order, order the tasks from the bottom
            # to the top of the stack. Also, compare relations along the way.
            for i in range(len(order)):
                    # Find the block on the table at order[i] in the current state
                    bottom = ''
                    for j in range(len(current_t)):
                        if self.search4block(self.state, current_t[j][1]) == order[i]:
                            # Check if the goal state has a matching Table relation
                            for k in range(len(goal_t)):
                                if current_t[j][1] == goal_t[k][1]:
                                    bottom = current_t[j][1]
                    # If the stack is empty or there is no goal of a stack
                    # being formed, no stack will be formed.
                    if not(bottom == ''):
                        # Find the chain of On goal relations until a match cannot be found
                        still_true = True
                        while True:
                            # For each On goal relation, see if the
                            # second parmeter matches bottom
                            match_goal = False
                            for j in range(len(goal)):
                                if bottom == goal[j][2]:
                                    # Specify that a goal relation succeeds the
                                    # bottom block's relation, and shift bottom
                                    # to the top block of the found relation
                                    bottom = goal[j][1]
                                    match_goal = True
                                    # See if there is a match for the goal
                                    # relation in the current state
                                    match_current = False
                                    # If the stack does not hold true up to that
                                    # point, don't check and add the task
                                    if still_true:
                                        for k in range(len(current)):
                                            if current[k][2] == goal[j][2] and current[k][1] == goal[j][1]:
                                                # Specify a match
                                                match_current = True
                                                # Find the relation in relations_g &
                                                # set satisfied to true for the relation
                                                for n in range(len(self.relations_g)):
                                                    if self.relations_g[n][0] == goal[j][0] and self.relations_g[n][1] == goal[j][1]:
                                                        if self.relations_g[n][2] == goal[j][2]:
                                                            self.satisfied[n] = True
                                                            break
                                    # If no match is found...
                                    if not(match_current):
                                        # Set still_true to False and add task
                                        list.append(goal[j])
                                        still_true = False
                            # If a On goal is not found for the bottom block,
                            # stop the loop to start on a new stack
                            if not(match_goal):
                                break
                # END OF LOOP - list is ready to be returned

        # Clear relation, 'c'
        elif type == 'c':
            # Since it is implied that Clear is already solved for, we only
            # check that the current Clear relations match the goal Clear relations
            # Find all relations of type Clear for the current state
            current = self.search4relations(self.relations_c, 'c')
            # Find all relations of type Clear for the goal state
            goal = self.search4relations(self.relations_g, 'c')

            for i in range(len(goal)):
                for j in range(len(current)):
                    if goal[i][1] == current[j][1]:
                        for k in range(len(self.relations_g)):
                            if goal[i][0] == self.relations_g[k][0] and goal[i][1] == self.relations_g[k][1]:
                                self.satisfied[k] = True
                                break
            # END OF LOOP - empty list is returned

        # Print an error and returns an empty set if type is not 't', 'o', or 'c'
        else:
            print("Error: compare_relations only accepts types t, o, and c.\n")
        return list

    ###################################
    # execution_setup
    # Allocates stacks for a given relation task. Stack roles are as follows:
    # Dig - the stack to dig from
    # Junk - the stack that blocks can be temporarily placed on
    # Place Tmp - the temporary location to place the goal block
    # Place - the goal location for the goal block
    #
    # Parameters:
    # self - the Planner object
    # task - the relation task to solve for
    #
    # Returns an ordered list of the stack roles ordered as the following:
    # [Dig, Junk, Place Tmp, Place]
    ###################################

    def execution_setup (self, task):
        list = []
        dig = ''
        junk = ''
        place_tmp = ''
        place = ''
        if task[0] == 't':
            # Define the goal block
            block_g = task[1]
            # Find the block's location to set as Dig
            dig = self.search4block(self.state, block_g)
            # Find a location that block can be placed
            # Find Table relations for both the current and goal state
            current = self.search4relations(self.relations_c, 't')
            goal = self.search4relations(self.relations_g, 't')
            # Find the places that currently satisfy Table
            place_list = []
            for i in range(len(current)):
                for j in range(len(goal)):
                    if current[i][1] == goal[j][1]:
                        # If the current and goal relations match, save the location
                        place_list.append(self.search4block(self.state, current[i][1]))
                        break
            # Set the default place as 'L1'
            place = 'L1'
            # If place_list is empty, set Place to L1
            if len(place_list) == 0:
                place = 'L1'
            # Otherwise, if place_list is on length 1...
            elif len(place_list) == 1:
                # If place_list[0] is L1, set Place to L2
                if place_list[0] == 'L1':
                    place = 'L2'
                # Otherwise, set Place to 'L1'
                else:
                    place = 'L1'
            # Otherwise, place_list is length 2
            else:
                # If place_list[0] or place_list[1] is L1
                if place_list[0] == 'L1' or place_list[1] == 'L1':
                    # If place_list[0] or place_list[1] is L2, set Place to L3
                    if place_list[0] == 'L2' or place_list[1] == 'L2':
                        place = 'L3'
                    # Otherwise, set Place to 'L2'
                    else:
                        place = 'L2'
                # Otherwise, set Place to L1
                else:
                    place = 'L1'
            # Place is set
            # If Dig is the same as Place, find Place Tmp
            if dig == place:
                # If dig is L1, set Place Tmp as L2 and Junk as L3
                if dig == 'L1':
                    place_tmp = 'L2'
                    junk = 'L3'
                # Otherwise, set Place Tmp as L1
                else:
                    place_tmp = 'L1'
                    # If Dig is L2, set Junk as L3
                    if dig == 'L2':
                        junk = 'L3'
                    # Otherwise, set Junk as L2
                    else:
                        junk = 'L2'
            # Otherwise, find a place for Junk
            else:
                # If Dig is L1 or Place is L1...
                if dig == 'L1' or place == 'L1':
                    # If Dig is L2 or Place is L2, set Junk to L3
                    if dig == 'L2' or place == 'L2':
                        junk = 'L3'
                    # Otherwise, set Junk to L2
                    else:
                        junk = 'L2'
                # Otherwise, set Junk to L1
                else:
                    junk = 'L1'
            # Order list as [Dig, Junk, Place Tmp, Place]
            list = [dig, junk, place_tmp, place]
        elif task[0] == 'o':
            # Define the goal block
            block_g = task[1]
            # Find the block's location to set as Dig
            dig = self.search4block(self.state, block_g)
            # Find the block's location to set as Place
            place = self.search4block(self.state, task[2])
            # If Dig is the same as Place, find Place Tmp
            if dig == place:
                # If dig is L1, set Place Tmp as L2 and Junk as L3
                if dig == 'L1':
                    place_tmp = 'L2'
                    junk = 'L3'
                # Otherwise, set Place Tmp as L1
                else:
                    place_tmp = 'L1'
                    # If Dig is L2, set Junk as L3
                    if dig == 'L2':
                        junk = 'L3'
                    # Otherwise, set Junk as L2
                    else:
                        junk = 'L2'
            # Otherwise, find a place for Junk
            else:
                # If Dig is L1 or Place is L1...
                if dig == 'L1' or place == 'L1':
                    # If Dig is L2 or Place is L2, set Junk to L3
                    if dig == 'L2' or place == 'L2':
                        junk = 'L3'
                    # Otherwise, set Junk to L2
                    else:
                        junk = 'L2'
                # Otherwise, set Junk to L1
                else:
                    junk = 'L1'
            # Order list as [Dig, Junk, Place Tmp, Place]
            list = [dig, junk, place_tmp, place]
        else:
            # Print an error that the task was not 't' or 'o' and print an empty list
            print("Error: execution_setup will only accept types 't' or 'o'.\n")
        # Return the ordered list
        return list

    ###################################
    # make_action_block
    # Creates an action block for a given task and stack roles.
    #
    # Action key:
    # u: Pick up block
    # d: Put down block
    # m1: Move arm to L1
    # m2: Move arm to L2
    # m3: Move arm to L3
    #
    # Parameters:
    # self: the Planner object
    # task: the relation to solve for
    # roles: the stack roles given by execution_setup
    #
    # Returns an ordered list denoting actions to be taken in a specific order
    ###################################

    def make_action_block (self, task, roles):
        actions = []
        # If the task is a Table relation...
        if task[0] == 't':
            # Track the depth within the stacks for help with indexing
            depth = 0
            depth_p = 0
            # Track the arm's location throughout the action block
            arm_l = self.state.arm.place.name
            # Track if the goal block is at Place Tmp
            tmp_g = False
            # Track if Dig and Place are the same location
            same = roles[0] == roles[3]
            while True:
                # If Place is L1 and not empty, empty the stack at Place
                if roles[3] == 'L1' and len(self.state.l1.stack) - depth_p != 0:
                    # If the arm is not in L1, move to L1
                    if not(arm_l == 'L1'):
                        actions.append('m1')
                        arm_l = 'L1'
                    # Pick up the top block from L1's stack
                    actions.append('u')
                    # If Dig and Place are the same AND goal block is NOT at
                    # Place Tmp...
                    if same and not(tmp_g):
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l1.stack[len(self.state.l1.stack) - depth_p - 1]:
                            # If Place Tmp is L2, move to L2 and set tmp_g to True
                            if roles[2] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                                tmp_g = True
                            # If Place Tmp is L3, move to L3 and set tmp_g to True
                            elif roles[2] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                                tmp_g = True
                            # Otherwise, print an error message
                            else:
                                print("Error: Place and Place Tmp were assigned to the same place.\n")
                    # Otherwise, find Junk's location
                    else:
                        # If Junk is L2, move to L2
                        if roles[1] == 'L2':
                            actions.append('m2')
                            arm_l = 'L2'
                        # If Junk is L3, move to L3
                        elif roles[1] == 'L3':
                            actions.append('m3')
                            arm_l = 'L3'
                        # Otherwise, print an error message
                        else:
                            print("Error: Place and Junk were assigned to the same place.\n")
                    # Put down the block
                    actions.append('d')
                    # Increment depth_p
                    depth_p += 1
                # If Place is L2 and not empty, empty the stack at Place
                elif roles[3] == 'L2' and len(self.state.l2.stack) - depth_p != 0:
                    # If the arm is not in L2, move to L2
                    if not(arm_l == 'L2'):
                        actions.append('m2')
                        arm_l = 'L2'
                    # Pick up the top block from L2's stack
                    actions.append('u')
                    # If Dig and Place are the same AND goal block is NOT at
                    # Place Tmp...
                    if same and not(tmp_g):
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l2.stack[len(self.state.l2.stack) - depth_p - 1]:
                            # If Place Tmp is L2, move to L2 and set tmp_g to True
                            if roles[2] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                tmp_g = True
                            # If Place Tmp is L3, move to L3 and set tmp_g to True
                            elif roles[2] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                                tmp_g = True
                            # Otherwise, print an error message
                            else:
                                print("Error: Place and Place Tmp were assigned to the same place.\n")
                    # Otherwise, find Junk's location
                    else:
                        # If Junk is L1, move to L1
                        if roles[1] == 'L1':
                            actions.append('m1')
                            arm_l = 'L1'
                        # If Junk is L3, move to L3
                        elif roles[1] == 'L3':
                            actions.append('m3')
                            arm_l = 'L3'
                        # Otherwise, print an error message
                        else:
                            print("Error: Place and Junk were assigned to the same place.\n")
                    # Put down the block
                    actions.append('d')
                    # Increment depth_p
                    depth_p += 1
                # If Place is L3 and not empty, empty the stack at Place
                elif roles[3] == 'L3' and len(self.state.l3.stack) - depth_p != 0:
                    # If the arm is not in L3, move to L3
                    if not(arm_l == 'L3'):
                        actions.append('m3')
                        arm_l = 'L3'
                    # Pick up the top block from L3's stack
                    actions.append('u')
                    # If Dig and Place are the same AND goal block is NOT at
                    # Place Tmp...
                    if same and not(tmp_g):
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l3.stack[len(self.state.l3.stack) - depth_p - 1]:
                            # If Place Tmp is L1, move to L1 and set tmp_g to True
                            if roles[2] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                tmp_g = True
                            # If Place Tmp is L2, move to L2 and set tmp_g to True
                            elif roles[2] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                                tmp_g = True
                            # Otherwise, print an error message
                            else:
                                print("Error: Place and Place Tmp were assigned to the same place.\n")
                    # Otherwise, find Junk's location
                    else:
                        # If Junk is L1, move to L1
                        if roles[1] == 'L1':
                            actions.append('m1')
                            arm_l = 'L1'
                        # If Junk is L2, move to L2
                        elif roles[1] == 'L2':
                            actions.append('m2')
                            arm_l = 'L2'
                        # Otherwise, print an error message
                        else:
                            print("Error: Place and Junk were assigned to the same place.\n")
                    # Put down the block
                    actions.append('d')
                    # Increment depth_p
                    depth_p += 1
                # Otherwise, move on to Place Tmp or Dig operations
                else:
                    # If the goal block is at Place Tmp...
                    if tmp_g:
                        # If Place Tmp is at L1, move to L1 and pick up
                        if roles[2] == 'L1':
                            actions.append('m1')
                            arm_l = 'L1'
                            actions.append('u')
                            # If Place is at L2, move to L2 and put down
                            if roles[3] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # If Place Tmp is at L2, move to L2 and pick up
                        elif roles[2] == 'L2':
                            actions.append('m2')
                            arm_l = 'L2'
                            actions.append('u')
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, Place Tmp is at L3, move to L3 and pick up
                        else:
                            actions.append('m3')
                            arm_l = 'L3'
                            actions.append('u')
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L2, move to L2 and put down
                            else:
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                    # If Dig is L1...
                    elif roles[0] == 'L1':
                        # If the arm is not at L1, move to L1
                        if not(arm_l == 'L1'):
                            actions.append('m1')
                            arm_l = 'L1'
                        # Pick up the block
                        actions.append('u')
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l1.stack[len(self.state.l1.stack) - depth - 1]:
                            # If Place is at L2, move to L2 and put down
                            if roles[3] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, find Junk's location
                        else:
                            # If Junk is at L2, move to L2
                            if roles[1] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                            # If Junk is at L3, move to L3
                            elif roles[1] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                            # Otherwise, print an error message\
                            else:
                                print("Error: Dig and Junk were assigned to the same place.\n")
                            # Put down the block
                            actions.append('d')
                    # If Dig is L2...
                    elif roles[0] == 'L2':
                        # If the arm is not at L2, move to L2
                        if not(arm_l == 'L2'):
                            actions.append('m2')
                            arm_l = 'L2'
                        # Pick up the block
                        actions.append('u')
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l2.stack[len(self.state.l2.stack) - depth - 1]:
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, find Junk's location
                        else:
                            # If Junk is at L1, move to L1
                            if roles[1] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                            # If Junk is at L3, move to L3
                            elif roles[1] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                            # Otherwise, print an error message\
                            else:
                                print("Error: Dig and Junk were assigned to the same place.\n")
                            # Put down the block
                            actions.append('d')
                    # If Dig is L3...
                    elif roles[0] == 'L3':
                        # If the arm is not at L3, move to L3
                        if not(arm_l == 'L3'):
                            actions.append('m3')
                            arm_l = 'L3'
                        # Pick up the block
                        actions.append('u')
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l3.stack[len(self.state.l3.stack) - depth - 1]:
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L2, move to L2 and put down
                            else:
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, find Junk's location
                        else:
                            # If Junk is at L1, move to L1
                            if roles[1] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                            # If Junk is at L2, move to L2
                            elif roles[1] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                            # Otherwise, print an error message\
                            else:
                                print("Error: Dig and Junk were assigned to the same place.\n")
                            # Put down the block
                            actions.append('d')
                    # Otherwise, print an error
                    else:
                        print("Error: Dig was not allocated a location.\n")
                    # Increment depth
                    depth += 1
            # END OF LOOP

        # If the task is an On relation...
        elif task[0] == 'o':
            # Track the depth within the stacks for help with indexing
            depth = 0
            depth_p = 0
            # Track the arm's location throughout the action block
            arm_l = self.state.arm.place.name
            # Track if the goal block is at Place Tmp
            tmp_g = False
            # Track if Dig and Place are the same location
            same = roles[0] == roles[3]
            # Track if the correct block is exposed at Place
            exposed = False
            # If Place is at L1, set exposed's value
            if roles[3] == 'L1':
                exposed = task[2] == self.state.l1.stack[len(self.state.l1.stack) - 1]
            # If Place is at L2, set exposed's value
            elif roles[3] == 'L2':
                exposed = task[2] == self.state.l2.stack[len(self.state.l2.stack) - 1]
            # If Place is at L2, set exposed's value
            elif roles[3] == 'L3':
                exposed = task[2] == self.state.l3.stack[len(self.state.l3.stack) - 1]
            # Otherwise, print an error message
            else:
                print("Error: Place was not found in make_action_block.\n")
            while True:
                # If the goal block is NOT exposed...
                if not(exposed):
                    # If Place is at L1...
                    if roles[3] == 'L1':
                        # If the arm is not in L1, move to L1
                        if not(arm_l == 'L1'):
                            actions.append('m1')
                            arm_l = 'L1'
                        # Pick up the block
                        actions.append('u')
                        # If Dig and Place are the same AND goal block is NOT at
                        # Place Tmp...
                        if same and not(tmp_g):
                            # If the top goal block is picked up, move to Place Tmp
                            if task[1] == self.state.l1.stack[len(self.state.l1.stack) - depth_p - 1]:
                                # If Place Tmp is L2, move to L2 and set tmp_g to True
                                if roles[2] == 'L2':
                                    actions.append('m2')
                                    arm_l = 'L2'
                                    tmp_g = True
                                # If Place Tmp is L3, move to L3 and set tmp_g to True
                                elif roles[2] == 'L3':
                                    actions.append('m3')
                                    arm_l = 'L3'
                                    tmp_g = True
                                # Otherwise, print an error message
                                else:
                                    print("Error: Place and Place Tmp were assigned to the same place.\n")
                        # Otherwise, move to Junk
                        else:
                            # If Junk is L2, move to L2
                            if roles[1] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                            # If Junk is L3, move to L3
                            elif roles[1] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                            # Otherwise, print an error message
                            else:
                                print("Error: Place and Junk were assigned to the same place.\n")
                        # Put down the block
                        actions.append('d')
                        # Increment depth, then check if the goal block is exposed
                        depth_p += 1
                        if task[2] == self.state.l1.stack[len(self.state.l1.stack) - depth_p - 1]:
                            exposed = True
                    # If Place is at L2...
                    elif roles[3] == 'L2':
                        # If the arm is not in L2, move to L2
                        if not(arm_l == 'L2'):
                            actions.append('m2')
                            arm_l = 'L2'
                        # Pick up the block
                        actions.append('u')
                        # If Dig and Place are the same AND goal block is NOT at
                        # Place Tmp...
                        if same and  not(tmp_g):
                            # If the top goal block is picked up, move to Place Tmp
                            if task[1] == self.state.l2.stack[len(self.state.l2.stack) - depth_p - 1]:
                                # If Place Tmp is L1, move to L1 and set tmp_g to True
                                if roles[2] == 'L1':
                                    actions.append('m1')
                                    arm_l = 'L1'
                                    tmp_g = True
                                # If Place Tmp is L3, move to L3 and set tmp_g to True
                                elif roles[2] == 'L3':
                                    actions.append('m3')
                                    arm_l = 'L3'
                                    tmp_g = True
                                # Otherwise, print an error message
                                else:
                                    print("Error: Place and Place Tmp were assigned to the same place.\n")
                        # Otherwise, move to Junk
                        else:
                            # If Junk is L1, move to L1
                            if roles[1] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                            # If Junk is L3, move to L3
                            elif roles[1] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                            # Otherwise, print an error message
                            else:
                                print("Error: Place and Junk were assigned to the same place.\n")
                        # Put down the block
                        actions.append('d')
                        # Increment depth, then check if the goal block is exposed
                        depth_p += 1
                        if task[2] == self.state.l2.stack[len(self.state.l2.stack) - depth_p - 1]:
                            exposed = True
                    # Otherwise, Place is at L3...
                    else:
                        # If the arm is not in L3, move to L3
                        if not(arm_l == 'L3'):
                            actions.append('m3')
                            arm_l = 'L3'
                        # Pick up the block
                        actions.append('u')
                        # If Dig and Place are the same AND goal block is NOT at
                        # Place Tmp...
                        if same and not(tmp_g):
                            # If the top goal block is picked up, move to Place Tmp
                            if task[1] == self.state.l3.stack[len(self.state.l3.stack) - depth_p - 1]:
                                # If Place Tmp is L1, move to L1 and set tmp_g to True
                                if roles[2] == 'L1':
                                    actions.append('m1')
                                    arm_l = 'L1'
                                    tmp_g = True
                                # If Place Tmp is L2, move to L2 and set tmp_g to True
                                elif roles[2] == 'L2':
                                    actions.append('m2')
                                    arm_l = 'L2'
                                    tmp_g = True
                                # Otherwise, print an error message
                                else:
                                    print("Error: Place and Place Tmp were assigned to the same place.\n")
                        # Otherwise, move to Junk
                        else:
                            # If Junk is L1, move to L1
                            if roles[1] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                            # If Junk is L2, move to L2
                            elif roles[1] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                            # Otherwise, print an error message
                            else:
                                print("Error: Place and Junk were assigned to the same place.\n")
                        # Put down the block
                        actions.append('d')
                        # Increment depth, then check if the goal block is exposed
                        depth_p += 1
                        if task[2] == self.state.l3.stack[len(self.state.l3.stack) - depth_p - 1]:
                            exposed = True
                # Otherwise, move on to Place Tmp or Dig operations
                else:
                    # If the top goal block is in Place Tmp...
                    if tmp_g:
                        # If Place Tmp is at L1, move to L1 and pick up
                        if roles[2] == 'L1':
                            actions.append('m1')
                            arm_l = 'L1'
                            actions.append('u')
                            # If Place is at L2, move to L2 and put down
                            if roles[3] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # If Place Tmp is at L2, move to L2 and pick up
                        elif roles[2] == 'L2':
                            actions.append('m2')
                            arm_l = 'L2'
                            actions.append('u')
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, Place Tmp is at L3, move to L3 and pick up
                        else:
                            actions.append('m3')
                            arm_l = 'L3'
                            actions.append('u')
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L2, move to L2 and put down
                            else:
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                    # If Dig is L1...
                    elif roles[0] == 'L1':
                        # If the arm is not at L1, move to L1
                        if not(arm_l == 'L1'):
                            actions.append('m1')
                            arm_l = 'L1'
                        # Pick up the block
                        actions.append('u')
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l1.stack[len(self.state.l1.stack) - depth - 1]:
                            # If Place is at L2, move to L2 and put down
                            if roles[3] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, find Junk's location
                        else:
                            # If Junk is at L2, move to L2
                            if roles[1] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                            # If Junk is at L3, move to L3
                            elif roles[1] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                            # Otherwise, print an error message
                            else:
                                print("Error: Dig and Junk were assigned to the same place.\n")
                            # Put down the block
                            actions.append('d')
                    # If Dig is L2...
                    elif roles[0] == 'L2':
                        # If the arm is not at L2, move to L2
                        if not(arm_l == 'L2'):
                            actions.append('m2')
                            arm_l = 'L2'
                        # Pick up the block
                        actions.append('u')
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l2.stack[len(self.state.l2.stack) - depth - 1]:
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L3, move to L3 and put down
                            else:
                                actions.append('m3')
                                arm_l = 'L3'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, find Junk's location
                        else:
                            # If Junk is at L1, move to L1
                            if roles[1] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                            # If Junk is at L3, move to L3
                            elif roles[1] == 'L3':
                                actions.append('m3')
                                arm_l = 'L3'
                            # Otherwise, print an error message\
                            else:
                                print("Error: Dig and Junk were assigned to the same place.\n")
                            # Put down the block
                            actions.append('d')
                    # If Dig is L3...
                    elif roles[0] == 'L3':
                        # If the arm is not at L3, move to L3
                        if not(arm_l == 'L3'):
                            actions.append('m3')
                            arm_l = 'L3'
                        # Pick up the block
                        actions.append('u')
                        # If the indexed block matches the goal block...
                        if task[1] == self.state.l3.stack[len(self.state.l3.stack) - depth - 1]:
                            # If Place is at L1, move to L1 and put down
                            if roles[3] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                            # Otherwise, Place is at L2, move to L2 and put down
                            else:
                                actions.append('m2')
                                arm_l = 'L2'
                                actions.append('d')
                                # END OF TASK - break loop
                                break
                        # Otherwise, find Junk's location
                        else:
                            # If Junk is at L1, move to L1
                            if roles[1] == 'L1':
                                actions.append('m1')
                                arm_l = 'L1'
                            # If Junk is at L2, move to L2
                            elif roles[1] == 'L2':
                                actions.append('m2')
                                arm_l = 'L2'
                            # Otherwise, print an error message
                            else:
                                print("Error: Dig and Junk were assigned to the same place.\n")
                            # Put down the block
                            actions.append('d')
                    # Otherwise, print an error
                    else:
                        print("Error: Dig was not allocated a location.\n")
                    # Increment depth
                    depth += 1
            # END OF LOOP
        # Otherwise, print an error message
        else:
            print("Error: make_action_block only accepts relation tasks of type 't' or 'o'.\n")
        # Return the ordered list of tasks
        return actions

    ###################################
    # execute_with_output
    # Excecutes the given action block, updates the state and it's relations,
    # and prints a formatted text output.
    #
    # Parameters:
    # self: the Planner object
    # actions: the ordered list of actions given by make_action_block
    ###################################

    def execute_with_output (self, actions):
        for i in range(len(actions)):
            # If the action is to pick up
            if actions[i] == 'u':
                # If the arm is at L1 and L1 is of length 1 or less...
                if self.state.arm.place.name == 'L1' and len(self.state.l1.stack) <= 1:
                    # If the arm is at L1 and L1 is of length 1, define action as pick up
                    if len(self.state.l1.stack) == 1:
                        # Save the block being picked up
                        block_u = self.state.l1.stack[len(self.state.l1.stack) - 1]
                        # Print that the arm has preformed "Pick up" on a block
                        print("Action: Pick up " + block_u + " from L1.\n")
                        # Update L1 and Arm
                        self.state.l1 = self.state.arm.pick_up()
                        # Update relations
                        len_c = len(self.relations_c)
                        for i in range(len_c):
                            # Remove relations with block_u
                            if self.relations_c[len_c - i - 1][1] == block_u:
                                self.relations_c.remove(self.relations_c[len_c - i - 1])
                        # Create an Above empty relation
                        self.relations_c.append(['a', block_u, '0'])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # Otherwise, print an error
                    else:
                        print("Error: Tried action \"Pick Up\" when the stack was empty.\n")
                # If the arm is at L2 and L2 is of length 1 or less...
                elif self.state.arm.place.name == 'L2' and len(self.state.l2.stack) <= 1:
                    # If the arm is at L2 and L2 is of length 1, define action as pick up
                    if len(self.state.l2.stack) == 1:
                        # Save the block being picked up
                        block_u = self.state.l2.stack[len(self.state.l2.stack) - 1]
                        # Print that the arm has preformed "Pick up" on a block
                        print("Action: Pick up " + block_u + " from L2.\n\n")
                        # Update L1 and Arm
                        self.state.l2 = self.state.arm.pick_up()
                        # Update relations
                        len_c = len(self.relations_c)
                        for i in range(len_c):
                            # Remove relations with block_u
                            if self.relations_c[len_c - i - 1][1] == block_u:
                                self.relations_c.remove(self.relations_c[len_c - i - 1])
                        # Create an Above empty relation
                        self.relations_c.append(['a', block_u, '0'])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # Otherwise, print an error
                    else:
                        print("Error: Tried action \"Pick Up\" when the stack was empty.\n")
                # If the arm is at L3 and L3 is of length 1 or less...
                elif self.state.arm.place.name == 'L3' and len(self.state.l3.stack) <= 1:
                    # If the arm is at L3 and L3 is of length 1, define action as pick up
                    if len(self.state.l3.stack) == 1:
                        # Save the block being picked up
                        block_u = self.state.l3.stack[len(self.state.l3.stack) - 1]
                        # Print that the arm has preformed "Pick up" on a block
                        print("Action: Pick up " + block_u + " from L3.\n")
                        # Update L1 and Arm
                        self.state.l3 = self.state.arm.pick_up()
                        # Update relations
                        len_c = len(self.relations_c)
                        for i in range(len_c):
                            # Remove relations with block_u
                            if self.relations_c[len_c - i - 1][1] == block_u:
                                self.relations_c.remove(self.relations_c[len_c - i - 1])
                        # Create an Above empty relation
                        self.relations_c.append(['a', block_u, '0'])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # Otherwise, print an error
                    else:
                        print("Error: Tried action \"Pick Up\" when the stack was empty.\n")
                # Unstack
                else:
                    # If arm is at L1...
                    if self.state.arm.place.name == 'L1':
                        # Save the block being picked up
                        block_u = self.state.l1.stack[len(self.state.l1.stack) - 1]
                        # Save the block below the block being picked up
                        block_d = self.state.l1.stack[len(self.state.l1.stack) - 2]
                        # Print that the arm has preformed "Unstack" on a block
                        print("Action: Unstack " + block_u + " from L1.\n")
                        # Update L1 and Arm
                        self.state.l1 = self.state.arm.pick_up()
                        # Update relations
                        len_c = len(self.relations_c)
                        for i in range(len_c):
                            # Remove relations with block_u
                            if self.relations_c[len_c - i - 1][1] == block_u:
                                self.relations_c.remove(self.relations_c[len_c - i - 1])
                        # Create an Above empty relation
                        self.relations_c.append(['a', block_u, block_d])
                        # Create a Clear relation
                        self.relations_c.append(['c', block_d])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # If arm is at L2...
                    elif self.state.arm.place.name == 'L2':
                        # Save the block being picked up
                        block_u = self.state.l2.stack[len(self.state.l2.stack) - 1]
                        # Save the block below the block being picked up
                        block_d = self.state.l2.stack[len(self.state.l2.stack) - 2]
                        # Print that the arm has preformed "Unstack" on a block
                        print("Action: Unstack " + block_u + " from L2.\n")
                        # Update L1 and Arm
                        self.state.l2 = self.state.arm.pick_up()
                        # Update relations
                        len_c = len(self.relations_c)
                        for i in range(len_c):
                            # Remove relations with block_u
                            if self.relations_c[len_c - i - 1][1] == block_u:
                                self.relations_c.remove(self.relations_c[len_c - i - 1])
                        # Create an Above empty relation
                        self.relations_c.append(['a', block_u, block_d])
                        # Create a Clear relation
                        self.relations_c.append(['c', block_d])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # Arm is at L3...
                    else:
                        # Save the block being picked up
                        block_u = self.state.l3.stack[len(self.state.l3.stack) - 1]
                        # Save the block below the block being picked up
                        block_d = self.state.l3.stack[len(self.state.l3.stack) - 2]
                        # Print that the arm has preformed "Unstack" on a block
                        print("Action: Unstack " + block_u + " from L3.\n")
                        # Update L1 and Arm
                        self.state.l3 = self.state.arm.pick_up()
                        # Update relations
                        len_c = len(self.relations_c)
                        for i in range(len_c):
                            # Remove relations with block_u
                            if self.relations_c[len_c - i - 1][1] == block_u:
                                self.relations_c.remove(self.relations_c[len_c - i - 1])
                        # Create an Above empty relation
                        self.relations_c.append(['a', block_u, block_d])
                        # Create a Clear relation
                        self.relations_c.append(['c', block_d])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
            # If the action is to put down...
            elif actions[i] == 'd':
                # If the arm is at L1 and L1 is empty, define action as "Put Down"
                if self.state.arm.place.name == 'L1' and len(self.state.l1.stack) == 0:
                    # Save the block being put down
                    block_a = self.state.arm.item
                    # Print that the arm has preformed "Put Down" on a block
                    print("Action: Put down " + block_a + " on L1.\n")
                    # Update L1 and Arm
                    self.state.l1 = self.state.arm.put_down()
                    # Update relations
                    self.relations_c.remove(['a', block_a, '0'])
                    # Create a Table relation
                    self.relations_c.append(['t', block_a])
                    # Create a Clear relation
                    self.relations_c.append(['c', block_a])
                    # Increment state number and print state
                    self.state.num += 1
                    self.state.print_state()
                # If the arm is at L2 and L2 is empty, define action as "Put Down"
                elif self.state.arm.place.name == 'L2' and len(self.state.l2.stack) == 0:
                    # Save the block being put down
                    block_a = self.state.arm.item
                    # Print that the arm has preformed "Put Down" on a block
                    print("Action: Put down " + block_a + " on L2.\n")
                    # Update L2 and Arm
                    self.state.l2 = self.state.arm.put_down()
                    # Update relations
                    self.relations_c.remove(['a', block_a, '0'])
                    # Create a Table relation
                    self.relations_c.append(['t', block_a])
                    # Create a Clear relation
                    self.relations_c.append(['c', block_a])
                    # Increment state number and print state
                    self.state.num += 1
                    self.state.print_state()
                # If the arm is at L3 and L3 is empty, define action as "Put Down"
                elif self.state.arm.place.name == 'L3' and len(self.state.l3.stack) == 0:
                    # Save the block being put down
                    block_a = self.state.arm.item
                    # Print that the arm has preformed "Put Down" on a block
                    print("Action: Put down " + block_a + " on L3.\n")
                    # Update L3 and Arm
                    self.state.l3 = self.state.arm.put_down()
                    # Update relations
                    self.relations_c.remove(['a', block_a, '0'])
                    # Create a Table relation
                    self.relations_c.append(['t', block_a])
                    # Create a Clear relation
                    self.relations_c.append(['c', block_a])
                    # Increment state number and print state
                    self.state.num += 1
                    self.state.print_state()
                # Otherwise, define action as "Stack"
                else:
                    # If the arm is at L1...
                    if self.state.arm.place.name == 'L1':
                        # Save the block being put down
                        block_a = self.state.arm.item
                        # Save the block that's currently at the top of the stack
                        block_b = self.state.l1.stack[len(self.state.l1.stack) - 1]
                        # Print that the arm has preformed "Stack"
                        print("Action: Stack " + block_a + " on " + block_b +
                        " at L1.\n")
                        # Update L1 and Arm
                        self.state.l1 = self.state.arm.put_down()
                        # Update relations
                        self.relations_c.remove(['a', block_a, block_b])
                        self.relations_c.remove(['c', block_b])
                        # Create a On relations
                        self.relations_c.append(['o', block_a, block_b])
                        # Create a Clear relation
                        self.relations_c.append(['c', block_a])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # If the arm is at L2...
                    elif self.state.arm.place.name == 'L2':
                        # Save the block being put down
                        block_a = self.state.arm.item
                        # Save the block that's currently at the top of the stack
                        block_b = self.state.l2.stack[len(self.state.l2.stack) - 1]
                        # Print that the arm has preformed "Stack"
                        print("Action: Stack " + block_a + " on " + block_b +
                        " at L2.\n")
                        # Update L1 and Arm
                        self.state.l2 = self.state.arm.put_down()
                        # Update relations
                        self.relations_c.remove(['a', block_a, block_b])
                        self.relations_c.remove(['c', block_b])
                        # Create a On relations
                        self.relations_c.append(['o', block_a, block_b])
                        # Create a Clear relation
                        self.relations_c.append(['c', block_a])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
                    # Otherwise, the arm is at L3...
                    else:
                        # Save the block being put down
                        block_a = self.state.arm.item
                        # Save the block that's currently at the top of the stack
                        block_b = self.state.l3.stack[len(self.state.l3.stack) - 1]
                        # Print that the arm has preformed "Stack"
                        print("Action: Stack " + block_a + " on " + block_b +
                        " at L3.\n")
                        # Update L1 and Arm
                        self.state.l3 = self.state.arm.put_down()
                        # Update relations
                        self.relations_c.remove(['a', block_a, block_b])
                        self.relations_c.remove(['c', block_b])
                        # Create a On relations
                        self.relations_c.append(['o', block_a, block_b])
                        # Create a Clear relation
                        self.relations_c.append(['c', block_a])
                        # Increment state number and print state
                        self.state.num += 1
                        self.state.print_state()
            # If the action is Move to L1
            elif actions[i] == 'm1':
                # Save the block being held
                block_a = self.state.arm.item
                # If L1 is empty, set block_b as '0'
                block_b = '0'
                # Otherwise, save the block that's at the top of L1
                if not(len(self.state.l1.stack) == 0):
                    block_b = self.state.l1.stack[len(self.state.l1.stack) - 1]
                # Save the arm's initial location
                initial = self.state.arm.place.name
                # Print that the arm has preformed "Move"
                print("Action: Move arm from " + initial + " to L1.\n")
                # Move arm to L1
                self.state.arm.move(self.state.l1)
                # Update relations
                len_c = len(self.relations_c)
                for i in range(len_c):
                    # Remove relations with block_a
                    if self.relations_c[len_c - i - 1][1] == block_a:
                        self.relations_c.remove(self.relations_c[len_c - i - 1])
                # Create an Above relation
                self.relations_c.append(['a', block_a, block_b])
                # Increment state number and print state
                self.state.num += 1
                self.state.print_state()
            # If the action is Move to L2
            elif actions[i] == 'm2':
                # Save the block being held
                block_a = self.state.arm.item
                # If L2 is empty, set block_b as '0'
                block_b = '0'
                # Otherwise, save the block that's at the top of L2
                if not(len(self.state.l2.stack) == 0):
                    block_b = self.state.l2.stack[len(self.state.l2.stack) - 1]
                # Save the arm's initial location
                initial = self.state.arm.place.name
                # Print that the arm has preformed "Move"
                print("Action: Move arm from " + initial + " to L2.\n")
                # Move arm to L2
                self.state.arm.move(self.state.l2)
                # Update relations
                len_c = len(self.relations_c)
                for i in range(len_c):
                    # Remove relations with block_a
                    if self.relations_c[len_c - i - 1][1] == block_a:
                        self.relations_c.remove(self.relations_c[len_c - i - 1])
                # Create an Above relation
                self.relations_c.append(['a', block_a, block_b])
                # Increment state number and print state
                self.state.num += 1
                self.state.print_state()
            # If the action is Move to L3
            elif actions[i] == 'm3':
                # Save the block being held
                block_a = self.state.arm.item
                # If L3 is empty, set block_b as '0'
                block_b = '0'
                # Otherwise, save the block that's at the top of L3
                if not(len(self.state.l3.stack) == 0):
                    block_b = self.state.l3.stack[len(self.state.l3.stack) - 1]
                # Save the arm's initial location
                initial = self.state.arm.place.name
                # Print that the arm has preformed "Move"
                print("Action: Move arm from " + initial + " to L3.\n")
                # Move arm to L3
                self.state.arm.move(self.state.l3)
                # Update relations
                len_c = len(self.relations_c)
                for i in range(len_c):
                    # Remove relations with block_a
                    if self.relations_c[len_c - i - 1][1] == block_a:
                        self.relations_c.remove(self.relations_c[len_c - i - 1])
                # Create an Above relation
                self.relations_c.append(['a', block_a, block_b])
                # Increment state number and print state
                self.state.num += 1
                self.state.print_state()
            # Otherwise, print an error message
            else:
                print("Error: execute_with_output received faulty action.\n")
        # END OF LOOP

    ###################################
    # check_satisfaction
    # The last function to be preformed. Checks satisfied list to see if all
    # relations are satisfied.
    #
    # Parameter:
    # self: the Planner object
    #
    # Return True if all relations are true
    # Otherwise, return False
    ###################################

    def check_satisfaction (self):
        check = True
        # For each relation in relation_g...
        for i in range(len(self.satisfied)):
            # If the relation is False, set check to False and break
            if not(self.satisfied[i]):
                check = False
                break
        return check

# END OF Planner CLASS

#######################################
# Main driver
# Takes user input for the initial and goal states and initializes the Planner.
#
# Then for the Table relation, run the compare_relations function, put the
# relations to solve for into the execution_setup function, put the location
# roles returned from execution_setup into the make_action_block function,
# and put the actions from make_action_block into execute_with_output.
# Rerun compare_relations for Table and repeat sequence if necessary.
#
# Next for the On relation, complete the same sequence of compare_relations,
# execution_setup, make_action_block, and execute_with_output.
# Rerun compare_relations for On and repeat sequence if necessary.
#
# Finally, run compare_relations for the Clear relation and run check_satisfaction.
#######################################

print("\nWelcome to WORLD OF BLOCKS")
print("Instructions: Input the stack in bottom to top order with the format \"x,y,z\".")
print("\nInitial state:")
print("Enter the stack at L1: ", end="")
l1i = input()
print("Enter the stack at L2: ", end="")
l2i = input()
print("Enter the stack at L3: ", end="")
l3i = input()
print("\nGoal state:")
print("Enter the stack at L1: ", end="")
l1g = input()
print("Enter the stack at L2: ", end="")
l2g = input()
print("Enter the stack at L3: ", end="")
l3g = input()
print("")
# Reformat inputs to lists
l1_i = l1i.split(',')
l2_i = l2i.split(',')
l3_i = l3i.split(',')
l1_g = l1g.split(',')
l2_g = l2g.split(',')
l3_g = l3g.split(',')
# Remove '' from empty stacks
if len(l1_i) != 0:
    if l1_i[0] == '':
        l1_i = []
if len(l2_i) != 0:
    if l2_i[0] == '':
        l2_i = []
if len(l3_i) != 0:
    if l3_i[0] == '':
        l3_i = []
if len(l1_g) != 0:
    if l1_g[0] == '':
        l1_g = []
if len(l2_g) != 0:
    if l2_g[0] == '':
        l2_g = []
if len(l3_g) != 0:
    if l3_g[0] == '':
        l3_g = []
# Initialize the Planner object
planner = Planner(l1_i, l2_i, l3_i, l1_g, l2_g, l3_g)
# Print the initial state
planner.state.print_state()
# Run compare_relations for the Table relations and save the ordered relation list
relations = planner.compare_relations('t')
# Set up a list for all actions
actions = []
# For each goal relation...
for i in range(len(relations)):
    # Run execution_setup with the given relations and save the outputted roles
    roles = planner.execution_setup(relations[i])
    # Run make_action_block for the given task
    actions = planner.make_action_block(relations[i], roles)
    # Execute actions with output
    planner.execute_with_output(actions)
# While the Table relations have yet to all be solved for
while True:
    # Recompare the relations
    relations = planner.compare_relations('t')
    # If the relation list is empty, exit the loop
    if len(relations) == 0:
        break
    # Otherwise, repeat the sequence
    else:
        # Set up a list for all actions
        actions = []
        # For each goal relation...
        for i in range(len(relations)):
            # Run execution_setup with the given relations and save the outputted roles
            roles = planner.execution_setup(relations[i])
            # Run make_action_block for the given task
            actions = planner.make_action_block(relations[i], roles)
            # Execute actions with output
            planner.execute_with_output(actions)
# END OF LOOP
# While the On relations have yet to all be solved for
while True:
    # Compare the On relations
    relations = planner.compare_relations('o')
    # If the relation list is empty, exit the loop
    if len(relations) == 0:
        break
    # Otherwise, repeat the sequence
    else:
        # Set up a list for all actions
        actions = []
        # For each goal relation...
        for i in range(len(relations)):
            # Run execution_setup with the given relations and save the outputted roles
            roles = planner.execution_setup(relations[i])
            # Run make_action_block for the given task
            actions = planner.make_action_block(relations[i], roles)
            # Execute actions with output
            planner.execute_with_output(actions)
# END OF LOOP
# Compare Clear relations
relations = planner.compare_relations('c')
# Check the satisfaction and output the final results
if planner.check_satisfaction():
    print("Goal state achieved successfully.\n")
# If check_satisfaction comes back false, process was unsuccessful
else:
    print("Operation unsuccessful.\n")
stop = input()
# END OF FILE
