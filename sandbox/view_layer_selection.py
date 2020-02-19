import bpy
    
class SelectionHandler(object):
    def __init__(self):
        self.selection_tracker = []

handle = SelectionHandler()

subscribe_to = bpy.types.LayerObjects, "active"

def notify_test(*args):
    context = args[0]
    handle = args[1]

    selection_tracker = handle.selection_tracker

    active = context.view_layer.objects.active

    # If there is nothing active
    if not active:
        # Remove the previously tracked selection
        selection_tracker = []
        print("Nothing is selected")
        return

    selected = list(context.view_layer.objects.selected)

    if selected:
        # The selected objects list also contains the active object
        selected.remove(active)
 
    if not selection_tracker:
        selection_tracker.append(active)
    else:
        selection_tracker[0] = active

    if not selected:
        selection_tracker = selection_tracker[0:1]
        print(selection_tracker)
        return
    
    new_objects = set(selected) - set(selection_tracker[1:])
    objects_to_remove = set(selection_tracker[1:]) - set(selected)

    for o in objects_to_remove:
        selection_tracker.remove(o)

    for o in reversed(selected):
        if o in new_objects:
            selection_tracker.append(o)
    
    selection_tracker = [selection_tracker[0]] + list(reversed(selection_tracker[1:]))
    
    print(selection_tracker)


bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=handle,
    args=(bpy.context, handle),
    notify=notify_test,
)
