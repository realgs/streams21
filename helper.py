def helps(command):
    command_list = ["exit", "reset", "profit", "price", "archive", "property", "send"]
    if command not in command_list:
        print("There is no such command. Try again...")
        return

    help_file = open(f"sources/{command}.txt", "r")
    help_data = help_file.read()
    help_file.close()
    print(help_data)
