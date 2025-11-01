import random as rd

def greetings ():
    greetings = "Hi"

    return greetings

Response = greetings()

print (Response)

options = ["rock", "scissors", "paper"]

def get_choices():
    player_choice = input("Enter your choice (rock, paper, scissors) :")
    computer_choice = rd.choice(options)
    choices = {"player" : player_choice, "computer" : computer_choice}

    return choices

def check_win(player, computer):
    print (f"You chose {player}, computer chose {computer}")

    if player == computer:
        return "It's a draw!"
    elif player == "rock":
        if computer == "scissors":
            return "rock smashes scissors, You win!"
        else:
            return "paper covers rock, You lose..."
    elif player == "scissors":
        if computer == "rock":
            return "rock smashes scissors, You lose..."
        else:
            return "scissors cuts paper, You win!"
    elif player == "paper":
        if computer == "scissors":
            return "scissors cuts paper, You lose..."
        else:
            return "paper covers rocks, You win!"

choices = get_choices()

PRS = check_win(choices["player"], choices["computer"])

print (PRS)