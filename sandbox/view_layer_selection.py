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

    if not context.view_layer.objects.active:
        return

    print("Notify changed!")

    if not context.view_layer.objects.active in selection_tracker:
        if not selection_tracker:
            selection_tracker.append(context.view_layer.objects.active)
        else:
            selection_tracker[0] = context.view_layer.objects.active

    if not context.view_layer.objects.selected:
        selection_tracker = selection_tracker[0:1]
        print(selection_tracker)
        return
    
    selected = list(context.view_layer.objects.selected)

    selected.remove(context.view_layer.objects.active)
    
    new_objects = set(selected) - set(selection_tracker[1:])
    objects_to_remove = set(selection_tracker[1:]) - set(selected)

    for o in objects_to_remove:
        selection_tracker.remove(o)

    for o in selected:
        if o in new_objects:
            selection_tracker.append(o)

    print(selection_tracker)


bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=handle,
    args=(bpy.context, handle),
    notify=notify_test,
)
