bl_info = {
    "name": "Correct Uv",
    "author": "Ömer Faruk Öz",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Edit > UV > Correct Uv",
    "description": "make a uv",
    "warning": "",
    "doc_url": "",
    "category": "Edit",
}

import bpy
import bmesh

def mainCorrectUv(method_d,fill_holes_d,correct_aspect_d,use_subsurf_data_d,margin_d):
    objects=[]
    objects.append(bpy.context.active_object.name)
    for object in bpy.context.selected_objects:
        if not object==bpy.context.active_object:
            objects.append(object.name)
    active=bpy.context.active_object
    edges=objects[:]
    
    
    
    for index in range(len(objects)):
        
        bpy.context.view_layer.objects.active=bpy.context.view_layer.objects[objects[index]]
        
        
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        
        
        edges[index]=[]
        number=0
        for v in bm.edges:
            edges[index].append(v.seam)
            number+=1
        
    bpy.ops.uv.smart_project()
    
    area=bpy.context.area.ui_type
    bpy.context.area.ui_type = 'UV'
    bpy.ops.uv.select_all(action='SELECT')
    bpy.context.area.ui_type =area
    
    bpy.ops.uv.seams_from_islands()
    bpy.ops.uv.unwrap(method=method_d, fill_holes=fill_holes_d, correct_aspect=correct_aspect_d, use_subsurf_data=use_subsurf_data_d, margin=margin_d)
    bpy.ops.mesh.mark_seam(clear=True)
    
    
    for index in range(len(objects)):
        
        bpy.context.view_layer.objects.active=bpy.context.view_layer.objects[objects[index]]
        
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        number=0
        for v in bm.edges:
            v.seam=edges[index][number]
            number+=1
    
    bmesh.update_edit_mesh(me, True)










even=[False]

class CorrectUv(bpy.types.Operator):
    bl_label="Correct Uv"
    bl_idname="wm.correct_uv"
    
    
    preset_enum :bpy.props.EnumProperty(
        name="",
        description="Method",
        items=[
            ("OP1","Angle Based",""),
            ("OP2","Conformal",""),
        ]
    )
    
    Fill_Holes=bpy.props.BoolProperty(name="Fill Holes",default=True)
    Correct_Aspect=bpy.props.BoolProperty(name="Correct Aspect",default=True)
    Use_Subdivision_Surface=bpy.props.BoolProperty(name="Use Subdivision Surface",default=False)
    
    Margin=bpy.props.FloatProperty(name="value",default=0.001,min=0,max=1,precision=3)
    
    
    def execute(self,context):
        if even[0]:
            even[0]=False
            method='ANGLE_BASED' if self.preset_enum=="OP1" else 'CONFORMAL'
            mainCorrectUv(method,self.Fill_Holes,self.Correct_Aspect,self.Use_Subdivision_Surface,self.Margin)
        else:
            even[0]=True
            bpy.ops.wm.correct_uv("INVOKE_DEFAULT")
        
        
        return {"FINISHED"}
    
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)






def menu_function(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("wm.correct_uv")
    
    
def register():
    bpy.utils.register_class(CorrectUv)
    bpy.types.VIEW3D_MT_uv_map.append(menu_function)
    
def unregister():
    bpy.utils.unregister_class(CorrectUv)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_function)
    
if __name__ == "__main__":
    register()