# Import your handlers here
from service import Iris, Intro


# Configuration for web API implementation
def config(api):
    # Instantiate handlers
    intro = Intro()
    iris = Iris()

    # Map routes
    api.add_route('/iris', intro)
    api.add_route('/iris/{index:int(min=0)}', iris)
