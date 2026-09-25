import math

class Pagination:
    """
    Pagination helper for web views.
    Handles page bounds, offsets, limits, and sliding window page generation.
    """
    ALLOWED_PER_PAGE = [10, 25, 50, 100]

    def __init__(self, page=1, per_page=25, total_records=0, default_per_page=25):
        try:
            per_page = int(per_page)
        except (ValueError, TypeError):
            per_page = default_per_page
        if per_page not in self.ALLOWED_PER_PAGE:
            per_page = default_per_page

        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1

        self.per_page = per_page
        self.total_records = max(0, int(total_records))
        self.total_pages = max(1, math.ceil(self.total_records / self.per_page))
        self.page = max(1, min(page, self.total_pages))
        self.offset = (self.page - 1) * self.per_page

        self.has_prev = self.page > 1
        self.has_next = self.page < self.total_pages
        self.prev_page = self.page - 1 if self.has_prev else None
        self.next_page = self.page + 1 if self.has_next else None

        self.start_index = self.offset + 1 if self.total_records > 0 else 0
        self.end_index = min(self.offset + self.per_page, self.total_records)

    @property
    def pages(self):
        """
        Sliding window of page numbers with '...' for skipped ranges.
        For <= 7 total pages, returns [1, 2, ..., N].
        For > 7 total pages, returns e.g. [1, '...', 4, 5, 6, '...', 10].
        """
        if self.total_pages <= 7:
            return list(range(1, self.total_pages + 1))

        page_list = [1]
        start = max(2, self.page - 2)
        end = min(self.total_pages - 1, self.page + 2)

        if start > 2:
            page_list.append('...')
        for p in range(start, end + 1):
            page_list.append(p)
        if end < self.total_pages - 1:
            page_list.append('...')
        page_list.append(self.total_pages)

        return page_list
