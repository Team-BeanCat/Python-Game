import reader   #local import from reader.py
from os import system
from glob import glob

def clear():
    system("cls")

def login():
    users = [user.split("\\")[-1].split(".")[0] for user in glob("saves/*.json")]   # Get a list of all the users (available json files)

    while True:
        clear()
        print("Please login as a user:")
        print("0. New user\n")
        for i in range(len(users)):     #Print all the available users with numbers next to them
            print(f"{i + 1}. {users[i]}")
        usernum = input("\n")

        try:
            usernum = int(usernum)  #Attempt to convert it to an int and make sure it is a valid number that corrosponds to a user.
            if usernum <= len(users):
                break
        except: continue

    if usernum != 0:        #If it doesn't equal 0 (not new character) grab the username from the user
        username = users[usernum - 1]
    else:   #New character
        clear()
        username = input("Please enter a username: ")
        data = {"name": username, "world": "home", "location": "00"}    #Set the new character to the default starting location
        with open(f".\\saves\\{username}.json", "w+") as f:             #Save it
            reader.dump(data, f, indent=4)

    return reader.user(username)        #Return the user object for the current logged in user




if __name__ == '__main__':
    user = login()      #Call the login function to get a user, this returns a user object
    world = reader.world(user.data["world"])    #Grab the current world data
    running = True
    while running:
        
        while True:
            clear() #Clear the screen
            print(world.message(user.location()).format(user.data["name"])) #Print the message for the current world location
            print()
            options = world.options(user.location())    #Grab the options for the world
            for i in range(len(options)):
                print(f"{str(i + 1)}. {options[i]}")     #Print the options for the current world with a number before them

            option = input("\n")    #Get the user's choice

            try:
                if int(option) <= len(world.options(user.location())) and int(option) > 0:  #Check if the number is a valid choice
                    break
            except: continue


        #World type key:
        #   story - the standard; move to a different location of the world
        #   jump - jump to the start of a different world
        #   end - the end of the game
        if world.data[user.location()]["type"] == "story":  #If its a story type then update the user's location
            user.data["location"] = world.locations(user.location())[int(option) - 1]

        if world.data[user.location()]["type"] == "jump":   #If its a jump then reset the user's location and update the world
            user.data["world"] = world.locations(user.location())[int(option) - 1]
            user.data["location"] = "00"
            world = reader.world(user.data["world"])        #Load the new world

        if world.data[user.location()]["type"] == "end":    #If its a end type
            print(world.message(user.location()))   #Print the message for the end (since its an if and not an elif this will run regardless of if you are transported or not)
            user.data["world"] = "home"     #Reset the user's position
            user.data["location"] = "00"
            running = False         #Exit the game

        user.save() #Save the user's data every question

    input("Thanks for playing! Press enter to exit.")