from card import RankCard, SuitCard

def generate_card_list():
    card_list = []
    for rank in range(6, 11):
        for colour in ["R", "B"]:
            for _ in range(2):
                card = RankCard(colour, rank)
                card_list.append(card)
    for suit, colour in ["CB", "SB", "HR", "DR"]:
        for _ in range(4):
            card = SuitCard(colour, suit)
            card_list.append(card)
    return card_list