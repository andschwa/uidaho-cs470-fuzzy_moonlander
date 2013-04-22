from fuzz.visualization import VisManager
from fuzzy_control import FuzzyControl

controller = FuzzyControl()

sets = {'height': controller.height_sets,
        'y_velocity': controller.y_velocity_sets,
        'position': controller.position_sets,
        'x_velocity': controller.x_velocity_sets}

plugins = {}

for name, num in sets.items():
    for key, item in num.items():
        plugins[name+'_'+key] = VisManager.create_backend(item)

for name, plugin in plugins.items():
    print(name, plugin)
    (vis_format, vis_data) = plugin.visualize()
    with (open("{}.{}".format(name, vis_format), "wb")) as fp:
            fp.write(vis_data)
