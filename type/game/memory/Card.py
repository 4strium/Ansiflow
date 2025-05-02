class Card : pass

def create(id, visual, couple_id):
  card_export = Card()

  card_export.id = id
  card_export.visual = visual
  card_export.couple_id = couple_id

  return card_export

def get_id(card_inp): return card_inp.id
def get_visual(card_inp): return card_inp.visual
def get_couple_id(card_inp): return card_inp.couple_id

def set_id(card_inp, n_id): card_inp.id = n_id
def set_visual(card_inp, n_visual): card_inp.visual = n_visual
def set_couple_id(card_inp, n_couple): card_inp.couple_id = n_couple
