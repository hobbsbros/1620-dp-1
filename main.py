# 16.20 DP 1

from math import cos, sin, radians

# Bolts
# Cost in dollars per pound
# Mass in grams
# Capacities in N
BOLTS = [
    {
        "name": "A",
        "cost": 20,
        "mass": 200,
        "pullout": 7000,
        "shear": 7000,
    },
    {
        "name": "B",
        "cost": 25,
        "mass": 200,
        "pullout": 6000,
        "shear": 8000,
    },
    {
        "name": "C",
        "cost": 10,
        "mass": 150,
        "pullout": 4000,
        "shear": 6000,
    },
    {
        "name": "D",
        "cost": 20,
        "mass": 125,
        "pullout": 2500,
        "shear": 5000,
    },
    {
        "name": "E",
        "cost": 115,
        "mass": 125,
        "pullout": 5000,
        "shear": 6000,
    },
    {
        "name": "F",
        "cost": 50,
        "mass": 100,
        "pullout": 3000,
        "shear": 5000,
    },
]

# Mass of payload (in kg)
PAYLOAD = 2100

# Launch acceleration (in g)
LAUNCH_ACCELERATION = 3

# Mount angle (in deg)
ANGLE = 15

# The cost of space shuttle launch (in $/g)
LAUNCH_COST_PER_G = 0

# Factor of safety
FOS = 1.3

# Pullout multiplier
PULLOUT_MULTIPLIER = sin(radians(ANGLE))

# Shear multiplier
SHEAR_MULTIPLIER = cos(radians(ANGLE))

# Payload weight (in N)
PAYLOAD_WEIGHT = PAYLOAD * 9.81 * (1 + LAUNCH_ACCELERATION)

# Pounds per gram (unit conversion)
GRAMS_TO_POUNDS = 0.00220462

def fos(bolts):
    """
    Compute the overall design factor of safety for a list of bolts
    """
    # Calculate total number of bolts
    total = 0
    for bolt, count in enumerate(bolts):
        total += count

    # If total is zero, FOS is zero
    if not total:
        return 0

    # Calculate weight per bolt (assume equal distribution of load)
    weight_per_bolt = PAYLOAD_WEIGHT / total
    pullout = PULLOUT_MULTIPLIER * weight_per_bolt
    shear = SHEAR_MULTIPLIER * weight_per_bolt

    # Overall FOS is equal to lowest single FOS
    fos = None

    for bolt, count in enumerate(bolts):
        # Only check if there is at least one bolt of this type
        if not count:
            continue

        # Check pullout condition
        pullout_fos = BOLTS[bolt]["pullout"] / pullout
        if fos is None or pullout_fos < fos:
            fos = pullout_fos

        # Check shear condition
        shear_fos = BOLTS[bolt]["shear"] / shear
        if fos is None or shear_fos < fos:
            fos = shear_fos

    return fos

def check(bolts):
    """
    Check whether or not the factor of safety constraint is satisfied
    """
    return fos(bolts) >= FOS

def cost(bolts):
    """
    Calculate the cost of a given bolt configuration
    """
    cost = 0
    
    for bolt, count in enumerate(bolts):
        cost += count * BOLTS[bolt]["cost"] * BOLTS[bolt]["mass"] * GRAMS_TO_POUNDS
        cost += count * BOLTS[bolt]["mass"] * LAUNCH_COST_PER_G

    return cost

def generate_children(bolts):
    """
    Generates "child" options for a bolt configuration
    """
    children = []

    for new in range(len(BOLTS)):
        child = list(bolts)
        child[new] += 1
        children.append(tuple(child))

    return children

def index(agenda, item, lower=None, upper=None):
    """
    Determine the binary insertion index
    """
    # Initialize lower and upper bounds of search
    if lower is None:
        lower = 0
    if upper is None:
        upper = len(agenda) - 1

    if not agenda:
        return 0

    # If our window is closed, we're done
    if lower == upper:
        if cost(agenda[lower]) > cost(item):
            return lower
        else:
            return lower + 1

    # Otherwise, find the middle of our window
    i = (lower + upper) // 2
    if cost(agenda[i]) < cost(item):
        return index(agenda, item, i+1, upper)
    elif cost(agenda[i]) > cost(item):
        return index(agenda, item, lower, i)
    else:
        return i

def solve(start = (0,) * len(BOLTS)):
    """
    Identify the lowest cost solution
    """
    agenda = [start]
    seen = {start}

    while agenda:
        # Get the first item off of the agenda
        this = agenda.pop(0)

        print(f"{this} | FOS {fos(this)} | ${cost(this)}")

        # Check constraint
        if check(this):
            return this

        # Otherwise, generate children
        children = generate_children(this)
        for child in children:
            if child not in seen:
                agenda.insert(index(agenda, child), child)
                seen.add(child)

    return None

if __name__ == "__main__":
    solve()