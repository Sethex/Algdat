#!/usr/bin/python3
# coding=utf-8

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall tall i generert instans.
numbers_lower = 3
# Høyest mulig antall tall i generert instans.
numbers_upper = 8
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

import random

def randomized_partition(arr, low, high):
    pivot_index = random.randint(low, high)
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] >= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def randomized_select(arr, low, high, k):
    if low == high:
        return [arr, low]
    
    pivot_index = randomized_partition(arr, low, high)
    num_greater_or_equal = pivot_index - low + 1
    
    if num_greater_or_equal == k:
        return [arr, pivot_index]
    elif k < num_greater_or_equal:
        return randomized_select(arr, low, pivot_index - 1, k)
    else:
        return randomized_select(arr, pivot_index + 1, high, k - num_greater_or_equal)

def k_largest(A, n, k):
    if k == 0:
        return []
    result = randomized_select(A, 0, n - 1, k)
    return result[0][0:result[1]+1]


# Sett med hardkodete tester på format: (A, k)
tests = [
    # ([], 0),
    ([1], 0),
    ([1], 1),
    ([1, 2], 1),
    ([-1, -2], 1),
    ([-1, -2, 3], 2),
    ([1, 2, 3], 2),
    ([3, 2, 1], 2),
    ([3, 3, 3, 3], 2),
    ([4, 1, 3, 2, 3], 2),
    ([4, 5, 1, 3, 2, 3], 4),
    ([9, 3, 6, 1, 7, 3, 4, 5], 4),
]

def gen_examples(k, lower, upper):
    for _ in range(k):
        A = [
                random.randint(-50, 50)
                for _ in range(random.randint(lower, upper))
            ]
        yield A, random.randint(0, len(A))


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        numbers_lower,
        numbers_upper,
    ))

failed = False
for A, k in tests:
    answer = sorted(A, reverse=True)[:k][::-1]
    student = k_largest(A[:], len(A), k)

    if type(student) != list:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Metoden må returnere en liste
Ditt svar: {student}
""")
    else:
        student.sort()
        if student != answer:
            if failed:
                print("-"*50)
            failed = True
            print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
