from cs50 import get_float

while True:
    dollar = get_float("change owned: ")
    if dollar >= 0:
        break

cents = int( round(dollar * 100))

total_coin = 0

for coins in [25, 10, 5, 1]:
    total_coin += cents // coins
    cents %= coins

print(total_coin)