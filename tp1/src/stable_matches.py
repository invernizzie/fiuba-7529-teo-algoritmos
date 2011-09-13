__author__ = 'esteban'

def parse_preferences(file):
    men_lines = [file.readline().rstrip() for i in range(4)]
    file.readline()
    women_lines = [file.readline().rstrip() for i in range(4)]

    men_numbers = {}
    women_numbers = {}
    for i in range(4):
        men_numbers[men_lines[i].partition(":")[0]] = i
        women_numbers[women_lines[i].partition(":")[0]] = i

    men = []
    women = []
    for i in range(4):
        men.append([women_numbers[name] for name in men_lines[i].partition(" ")[2].rsplit(",")])
        women.append([men_numbers[name] for name in women_lines[i].partition(" ")[2].rsplit(",")])

    return men_numbers, women_numbers, men, women

class CoupleStabilityChecker:

    def __init__(self, men_likes, women_likes):
        self.men_likes = men_likes
        self.women_likes = women_likes

    def are_married(self, man, woman):                                                      # n: candidates, m: couples
        return (man, woman) in self.couples                                                 # m

    def partner_of_man(self, man):
        couple = filter(lambda c: c[0] == man, self.couples)                                # m
        if len(couple) > 0:
            return couple[0][1]
        return None

    def partner_of_woman(self, woman):
        couple = filter(lambda c: c[1] == woman, self.couples)                              # m
        if len(couple) > 0:
            return couple[0][0]
        return None

    def _prefers(self, likes, partner, candidate):
        return partner is not None and likes.index(candidate) < likes.index(partner)        # n

    def man_prefers(self, man, woman):
        return self._prefers(self.men_likes[man], self.partner_of_man(man), woman)          # n + m

    def woman_prefers(self, woman, man):
        return self._prefers(self.women_likes[woman], self.partner_of_woman(woman), man)    # n + m

    def are_stable(self, couples):
        self.couples = couples
        for man in range(4):                                                                # n
            for woman in range(4):                                                          # n
                if not self.are_married(man, woman) and \
                   self.man_prefers(man, woman) and \
                   self.woman_prefers(woman, man):                                          # m + 2 (n + m) ~ n + m
                    return False
        return True

class CoupleMatcher:

    def __init__(self, men_likes, women_likes):
        self.men_likes = men_likes
        self.women_likes = women_likes
        self.checker = CoupleStabilityChecker(men_likes, women_likes)