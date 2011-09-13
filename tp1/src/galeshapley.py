__author__ = 'esteban'

from _collections import deque
from stable_matches import parse_preferences, CoupleMatcher

class GaleShapleyMatcher (CoupleMatcher):

    def __init__(self, men_likes, women_likes):
        CoupleMatcher.__init__(self, men_likes, women_likes)
        self.couples = []
        self.load_priorities()

    def load_priorities(self):
        self.men_queues = []
        for man_likes in self.men_likes:
            self.men_queues.append(deque(man_likes))

    def declare_to(self, man, woman):
        partner = self.women_partners[woman]
        likes = self.women_likes[woman]
        if partner is None:
            self.couples.append((man, woman))
            self.remaining_men.remove(man)
            self.women_partners[woman] = man
            return
        if likes.index(man) < likes.index(partner):
            self.remaining_men.append(partner)
            self.couples.remove((partner, woman))
            self.couples.append((man, woman))
            self.remaining_men.remove(man)
            self.women_partners[woman] = man


    def pair_couples(self):
        self.remaining_men = range(len(self.men_likes))
        self.women_partners = []
        for i in range(len(self.women_likes)): self.women_partners.append(None)

        while len(self.remaining_men) > 0:
            for man in self.remaining_men:
                self.declare_to(man, self.men_queues[man].popleft())

        return self.couples


[men_numbers, women_numbers, men_likes, women_likes] = parse_preferences(open("preferences.txt"))

matcher = GaleShapleyMatcher(men_likes, women_likes)
couples = matcher.pair_couples()

def find_key(dic, val):
    return [k for k, v in dic.iteritems() if v == val][0]

def name_couple(couple):
    return find_key(men_numbers, couple[0]), find_key(women_numbers, couple[1])

named_couples = map(name_couple, couples)
print(named_couples)
