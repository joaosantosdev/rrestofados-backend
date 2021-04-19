class Pagination():
    items = []
    total = 0
    page = 0

    def __init__(self, items, total, page):
        self.items = items
        self.total = total
        self.page = page