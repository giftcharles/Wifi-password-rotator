# generate random passwords
import random

def GeneratePassword():
    prefix = "Normet2019-"

    letters = list('abcdefghijklmnopqrstuvwxyz')

    number = random.randrange(100,1000)

    randomLetter = random.choice(letters)

    randomPass = prefix + randomLetter + str(number)

    print(randomPass)


# 