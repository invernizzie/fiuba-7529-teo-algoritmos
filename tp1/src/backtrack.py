__author__ = 'esteban'

from stable_matches import parse_preferences, CoupleStabilityChecker

class BacktrackingMatcher:

    def __init__(self, men_likes, women_likes):
        self.men_likes = men_likes
        self.women_likes = women_likes
        self.couples = []
        self.checker = CoupleStabilityChecker(men_likes, women_likes)

    def add_couple(self, available_men, available_women):

        if not len(available_men): return True

        current_man = 0
        current_woman = 0

        for man in available_men:
            for woman in available_women:
                couple = man, woman
                if self.checker.are_stable(self.couples + [couple]):
                    self.couples.append(couple)
                    remaining_men = filter(lambda x: x != man, available_men)
                    remaining_women = filter(lambda x: x != woman, available_women)
                    if self.add_couple(remaining_men, remaining_women):
                        return True
                    self.couples.remove(couple)

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
