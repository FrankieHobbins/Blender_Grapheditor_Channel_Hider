import bpy

bl_info = {
"name": "F Channel Muter",
"author": "Frankie",
"version": (0,4),
"blender": (2, 77, 0),
"location": "graph editor hotkeys 1 2 3 and shift 1 2 3",
"description": "in the graph editor use 1 2 3 to toggle location rotation scale channel visibility, shift to make additive",
"warning": "will override hot keys 1 2 3 and shift 1 2 3 in graph editor",
"wiki_url": "",
"category": "Animation",
}

def hidechannel(context, channelname, additive):
    obj = bpy.context.object             #active object
    action = obj.animation_data.action   #current action
    if bpy.context.selected_pose_bones != None:  
        if bpy.context.selected_pose_bones.count != 0:
            for selbone in bpy.context.selected_pose_bones:
                for f in bpy.data.actions[action.name].fcurves:                    
                    if channelname in f.data_path and selbone.name in f.data_path:
                        toggle_vis = not f.hide
                        f.hide = toggle_vis
                    elif selbone.name in f.data_path and additive == False:
                        f.hide = True
    bpy.ops.graph.view_all()
    bpy.ops.anim.channels_expand()

class GraphHideChannel(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "graph.hidechannel"
    bl_label = "Hide Loc in graph editor"
    bl_options = {'REGISTER', 'UNDO'}
    
    channelname = bpy.props.StringProperty(name="Channel Filter", default="none")
    additive = bpy.props.BoolProperty(name="Additive", default=False)
    
    def execute(self, context):
        hidechannel(context, self.channelname, self.additive)      
        return {'FINISHED'}




#copied from keymape export
def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)
        
def register():
    bpy.utils.register_class(GraphHideChannel)
        
    # handle the keymap   
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Graph Editor Generic', space_type='GRAPH_EDITOR', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('graph.hidechannel', 'ONE', 'PRESS')
    kmi_props_setattr(kmi.properties, 'channelname', 'loc')
    kmi_props_setattr(kmi.properties, 'additive', False)
    kmi = km.keymap_items.new('graph.hidechannel', 'TWO', 'PRESS')
    kmi_props_setattr(kmi.properties, 'channelname', 'rot')
    kmi_props_setattr(kmi.properties, 'additive', False)
    kmi = km.keymap_items.new('graph.hidechannel', 'THREE', 'PRESS')
    kmi_props_setattr(kmi.properties, 'channelname', 'scale')
    kmi_props_setattr(kmi.properties, 'additive', False)
    kmi = km.keymap_items.new('graph.hidechannel', 'ONE', 'PRESS', shift=True)
    kmi_props_setattr(kmi.properties, 'channelname', 'loc')
    kmi_props_setattr(kmi.properties, 'additive', True)
    kmi = km.keymap_items.new('graph.hidechannel', 'TWO', 'PRESS', shift=True)
    kmi_props_setattr(kmi.properties, 'channelname', 'rot')
    kmi_props_setattr(kmi.properties, 'additive', True)
    kmi = km.keymap_items.new('graph.hidechannel', 'THREE', 'PRESS', shift=True)
    kmi_props_setattr(kmi.properties, 'channelname', 'scale')
    kmi_props_setattr(kmi.properties, 'additive', True)
    
def unregister():
    bpy.utils.unregister_class(GraphHideChannel)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
#if __name__ == "__main__":
#    register()