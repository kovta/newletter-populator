from utils import get_cell_ranges

class NewsletterMasterData:

    def __init__(self):
        """
        Initialize an instance of NewsletterMasterData.
        """
        # Initialize category properties as None
        self.Creative = None
        self.Strategy = None
        self.UX_Design = None
        self.PPC = None
        self.Development = None
        self.Graphic_Design = None
        self.Business_Tech = None
        self.Analytics = None
        self.Programmatic = None

        # Initialize featured content property as None
        self.featured_content = None


def init_master_data(ranges):
    value_ranges = get_cell_ranges(ranges)
