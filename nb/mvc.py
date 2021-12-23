from . import model as nb_model
from . import view as nb_view
from . import controller as nb_controller


def run():
    # Create package-level global variables
    global model
    global view
    global ctrl

    # Create mvc objects
    model = nb_model.Model()
    view = nb_view.View()
    ctrl = nb_controller.Controller()

    # Give mvc objectss access to each other
    model.start()
    view.start()
    ctrl.start()

    # Run the UI
    ctrl.run()
