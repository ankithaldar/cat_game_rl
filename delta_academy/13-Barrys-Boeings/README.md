### Exercise #1 - Barry's Boeings

You've ended up in the orbit of Barry. He's the CEO at a major airline called **BarryJet** (haven't you heard of it?).

Boeing have sold him planes with faulty ailerons, but the replacement parts they sell are also faulty! After every flight they become faulty, and after 2 flights without repair, they go out of operation.

The MDP diagram below describes how one plane will be affected by flying and how much each action costs.

![Barry's dilema as an MDP](barrys_mdp.png)

He wants you to figure out the right policy for this MDP - what action should he take in each state?

As in the above example, represent it as a Python dictionary, called `boeing_policy`.

Fill out `main.py` with your answer!