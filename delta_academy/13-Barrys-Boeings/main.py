from ex1_checks import check_barry_boeings

# The states a plane can be in
states = ["Faulty", "Out of Operation", "In Operation"]

# The options BarryJet has with the plane
actions = ["Fly", "Repair"]


# TODO: The bit you write - fill in the policy as a dictionary of {state: action} for all states
boeing_policy = ...


# Leave this line! It checks your answer :)
check_barry_boeings(boeing_policy)
