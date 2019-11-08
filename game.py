import reader
from os import system
from glob import glob

def clear():
    system("cls")

def login():
    users = [user.split("\\")[-1].split(".")[0] for user in glob("saves/*.json")]   # Get a list of all the users

    while True:
        clear()
        print("Please login as a user:")
        print("0. New user\n")
        for i in range(len(users)):
            print(f"{i + 1}. {users[i]}")
        usernum = input("\n")

        try:
            usernum = int(usernum)
            if usernum <= len(users):
                break
        except: continue

    if usernum != 0:
        username = users[usernum - 1]
    else:
        clear()
        username = input("Please enter a username: ")
        data = {"name": username, "world": "home", "location": "00"}
        with open(f".\\saves\\{username}.json", "w+") as f:
            reader.dump(data, f, indent=4)

    return reader.user(username)




if __name__ == '__main__':
    user = login()
    world = reader.world(user.data["world"])
    running = True
    while running:
        
        while True:
            clear()
            print(world.message(user.location()).format(user.data["name"]))
            print("\n".join(world.options(user.location())))      #Print the options for the current world
            option = input("\n")

            try:
                if int(option) <= len(world.options(user.location())) and int(option) > 0:
                    break
            except: continue

        if world.data[user.location()]["type"] == "story":
            user.data["location"] = world.locations(user.location())[int(option) - 1]

        if world.data[user.location()]["type"] == "jump":
            user.data["location"] = "00"
            user.data["world"] = world.locations(user.location())[int(option) - 1]
            world = reader.world(user.data["world"])

        if world.data[user.location()]["type"] == "end":
            print(world.message(user.location()))
            running = False

        user.save()

    input("Thanks for playing!")