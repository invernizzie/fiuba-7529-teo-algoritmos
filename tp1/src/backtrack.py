__author__ = 'esteban'

from stable_matches import parse_preferences, CoupleStabilityChecker, CoupleMatcher

class BacktrackingMatcher (CoupleMatcher):

    def __init__(self, men_likes, women_likes):
        CoupleMatcher.__init__(self, men_likes, women_likes)
        self.couples = []

    def add_couple(self, available_men, available_women):

        if not len(available_men): return True

        man = available_men[0]
        available_men = available_men[1:]
        for i in range(len(available_women)):
            woman = available_women[i]
            couple = man, woman                                                     # cte
            if self.checker.are_stable(self.couples + [couple]):                    # n^3
                self.couples.append(couple)                                         # cte
                remaining_women = available_women[:i] + available_women[i+1:]       # cte
                if self.add_couple(available_men, remaining_women):                 # f(n - 1)
                    return True
                self.couples.remove(couple)                                         # n

        return False

    def pair_couples(self):
        
        self.add_couple(range(len(self.women_likes)), range(len(self.men_likes)))

        return self.couples


[men_numbers, women_numbers, men_likes, women_likes] = parse_preferences(open("preferences.txt"))

matcher = BacktrackingMatcher(men_likes, women_likes)
couples = matcher.pair_couples()

def find_key(dic, val):
    return [k for k, v in dic.iteritems() if v == val][0]

def name_couple(couple):
    return find_key(men_numbers, couple[0]), find_key(women_numbers, couple[1])

named_couples = map(name_couple, couples)
print(named_couples)
