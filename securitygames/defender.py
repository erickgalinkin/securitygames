class Defender:
    def __init__(self):
        pass

    def act(self, net):
        # TODO: Implement defender functionality
        return True

    def _do_nothing(self):
        print("Defender took no action.")
        return True


class ObliviousDefender(Defender):
    def __init__(self):
        super(ObliviousDefender, self).__init__()
        pass

    def act(self, net):
        return self._do_nothing()
