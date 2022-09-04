from typing import Callable, Dict


def get_definition_checker(true_definition: str) -> Callable:
    def definition_checker(definition: str) -> None:
        if definition == true_definition:
            print("Correct! Good job :)")
        else:
            print("Afraid that's incorrect. Try another answer?")
    return definition_checker


def check_definition_1(your_answer: str) -> None:
    get_definition_checker("Sequential decision-making problems")(your_answer)


def check_definition_2(your_answer: str) -> None:
    get_definition_checker("A process in which time is modelled with discrete steps")(your_answer)


def check_definition_3(your_answer: str) -> None:
    get_definition_checker("States, actions & rewards")(your_answer)


def check_definition_4(your_answer: str) -> None:
    get_definition_checker("The sum of future rewards")(your_answer)


def get_mini_exercise_checker(real_state: str, real_action: str, real_reward: str, success_message: str) -> Callable:
    def mini_exercise_checker(state: str, action: str, reward: str):
        error_msg = ""
        if state != real_state:
            error_msg += "\n\nError: The state is incorrect - think about what fully represents the state of the game."
        if action != real_action:
            error_msg += "\n\nError: The action is incorrect - think... what are the different actions you can take?"
        if reward != real_reward:
            error_msg += "\n\nError: The reward is incorrect - what's the goal? What tells the agent how well or badly it is doing?"
        if error_msg:
            print(error_msg[2:])
        else:
            print(success_message)

    return mini_exercise_checker


def check_exercise_1(state: str, action: str, reward: str):
    # Chess game
    checker = get_mini_exercise_checker(
        "Spaces filled at the bottom of the board, current piece shape, current piece location",
        "Whether to move the piece right, left or keep it where it is",
        "The number of points you've scored",
        "Congratulations, you got it right!\n\nMove onto the next mini-exercise!",
        )
    checker(state, action, reward)


def check_exercise_2(state: str, action: str, reward: str):
    # Robot
    checker = get_mini_exercise_checker(
        "Robot location & orientation, layout of the room it's in & the goal location it's aiming to reach",
        "Acceleration/deceleration and tyre angle change",
        "Whether it has reached the goal location",
        "Another one bites the dust... congrats, that's right!\n\n1 more mini-exercise left!",
    )
    checker(state, action, reward)


def check_exercise_3(state: str, action: str, reward: str):
    # Advertising
    checker = get_mini_exercise_checker(
        "All user information incl. physical information, online behaviour & website they're on",
        "Advert that can be shown",
        "Whether the user clicks the advert & whether the user buys the advertised product",
        "Nailed it! Good job!",
    )
    checker(state, action, reward)


def check_barry_boeings(policy: Dict[str, str]) -> None:
    if len(policy) != 3:
        print(f"Incorrect number of state-value pairs in policy. Expected 3.\n\nPolicy: {policy}\n\n")
    if any(
        state not in policy
        for state in ["Faulty", "Out of Operation", "In Operation"]
    ):
        print(
            f'A state is missing from this policy!\n\n'
            f'Valid states: ["Faulty", "Out of Operation", "In Operation"]\n\n'
            f'States in policy: {list(policy)}'
        )
        return
    if any(action not in ["Fly", "Repair"] for action in policy.values()):
        print(
            f'Invalid action in policy!\n\n'
            f'Valid actions: ["Fly", "Repair"]\n\n'
            f'Actions in policy: {list(policy.values())}'
        )
        return
    if policy["In Operation"] != "Fly":
        print("Invalid action chosen! Only action available when 'In Operation' is 'Fly'.")
        return
    if policy["Faulty"] != "Repair":
        print("Incorrect action chosen for one state!")
        return
    if policy["Out of Operation"] != "Repair":
        print("Invalid action chosen! Only action available when 'Out of Operation' is 'Repair'.")
        return
    print(
        "Congrats, you got it correct!!\n\nJust 1 more exercise left :)"
    )


def check_barry_flight_paths(policy: Dict[str, str]) -> None:
    POSS_STATES = ["New York", "London", "Amsterdam", "Tel Aviv", "Cairo", "Bangkok"]
    POSS_ACTIONS = ["London", "Amsterdam", "Tel Aviv", "Cairo", "Bangkok", "Hong Kong"]
    POSS_STATE_ACTION = {
        "New York": ["London", "Amsterdam"],
        "London": ["Cairo", "Tel Aviv"],
        "Amsterdam": ["Tel Aviv", "Cairo"],
        "Tel Aviv": ["Bangkok", "Cairo", "Hong Kong"],
        "Cairo": ["Bangkok"],
        "Bangkok": ["Hong Kong"],
    }
    OPTIMAL_POLICY = {"New York": "Amsterdam", "London": "Cairo", "Amsterdam": "Tel Aviv", "Tel Aviv": "Cairo", "Cairo": "Bangkok", "Bangkok": "Hong Kong"}
    if len(policy) != len(POSS_STATES):
        print(f"Incorrect number of state-value pairs in policy. Expected 7.\n\nPolicy: {policy}\n\n")
    if any(
        state not in policy
        for state in POSS_STATES
    ):
        print(
            f'A state is missing from this policy!\n\n'
            f'Valid states: {POSS_STATES}\n\n'
            f'States in policy: {list(policy)}'
        )
        return
    if any(action not in POSS_ACTIONS for action in policy.values()):
        print(
            f'Invalid action in policy!\n\n'
            f'Valid actions: {POSS_ACTIONS}\n\n'
            f'Actions in policy: {list(policy.values())}'
        )
        return
    for state, action in policy.items():
        if action not in POSS_STATE_ACTION[state]:
            print(f"Cannot fly from {state} to {action}! Possible options from {state} are: {POSS_STATE_ACTION[state]}")
            return

    for state, action in policy.items():
        if action != OPTIMAL_POLICY[state]:
            print(f"Flying from {state} to {action} isn't the optimal flight to take from {state} :/")
            return

    print("Congrats, you've completed the first tutorial & all exercises!!\n\nReturn to Replit to 'SUBMIT' (top right corner)")
