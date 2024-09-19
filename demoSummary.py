from Summary import Summary


class game:

    def play(self):
        spellSummary = Summary()

        word = "apple"
        attempts = 4

        spellSummary.addSummary(word, attempts)

        spellSummary.showSummary()


game = game()
game.play()