print("-" * 50)

import bpy

depgraph = bpy.context.evaluated_depsgraph_get()

for ob_inst in depgraph.object_instances:
    #print(ob_inst.,)
    
    if ob_inst.is_instance:
        print(ob_inst.object.name, 
              ob_inst.parent.name, 
              ob_inst.instance_object.name,
              tuple(ob_inst.matrix_world.translation),
              ob_inst.orco,
              tuple(ob_inst.uv)
              )
    else:
        print(ob_inst.object.name, 
              ob_inst.instance_object.name if ob_inst.instance_object else None
              )
