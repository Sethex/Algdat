#!/usr/bin/python3
# coding=utf-8

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et lite sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å teste på
# et større sett med 500 genererte instanser. For å teste på det
# større settet med genererte instanser, må du (1) laste ned filen med
# testene fra øvingssystemet, (2) legge den samme plass som denne
# python-filen og (3) sette variabelen under til True. Merk at det kan
# ta litt tid å kjøre alle de 500 ekstra testene.
use_extra_tests = False

def cut_sheet(price, width, height):
    if width == 0 or height == 0:
        return 0
    q = float('-inf')

    for currW in range(1, width + 1):
        for currH in range(1, height + 1):
            qMarked = price[(currW, currH)] + cut_sheet(price, width, height-1)
            print("h:",currH, "w:", currW)
            print("Marked: ", qMarked)
            q = max(q, qMarked)
    return q


def sheet_cutting(w, h, price):
    if w == 0 or h == 0:
        return 0
    return cut_sheet(price, w, h)



# Tester på formatet (p, w, h, solution)
tests = [
    ({(1, 1): 1}, 1, 1, 1),
    ({(1, 1): 1, (2, 1): 3, (1, 2): 3, (2, 2): 3}, 2, 2, 6),
    ({(1, 1): 1, (2, 1): 1, (1, 2): 1, (2, 2): 5}, 2, 2, 5),
    
]

failed = False

for prices, w, h, answer in tests:
    student = sheet_cutting(w, h, prices)
    if student != answer:
        if failed:
            print("-"*50)

        failed = True
        print(f"""
Koden feilet for følgende instans:
w: {w}
h: {h}
prices:
{prices}

Ditt svar: {student}
Riktig svar: {answer}
        """)

if use_extra_tests:
    with open("tests_sheet_cutting.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            w, h, price_string, answer = line.strip().split(" | ")
            w, h, answer = int(w), int(h), int(answer)
            prices = {}
            for data_point in price_string.split(","):
                i, j, price = map(int, data_point.split(":"))
                prices[i, j] = price

            extra_tests.append((prices, w, h, answer))

    n_failed = 0
    for prices, w, h, answer in extra_tests:
        student = sheet_cutting(w, h, prices)
        if student != answer:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-"*50)

            failed = True
            if n_failed <= 5:
                print(f"""
Koden feilet for følgende instans:
w: {w}
h: {h}
prices:
{prices}

Ditt svar: {student}
Riktig svar: {answer}
                """)
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")

