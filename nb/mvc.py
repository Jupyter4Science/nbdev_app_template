import nb.model
import nb.view
import nb.controller


def run():

    # Create mvc objects
    model = nb.model.Model()
    view = nb.view.View()
    ctrl = nb.controller.Controller()

    # Give mvc objectss access to each other
    model.start(ctrl)
    view.start(model, ctrl)
    ctrl.start(model, view)

    # Run the UI
    ctrl.run()
