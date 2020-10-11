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

deafults={
"Angle_Limit":66.0,
"Method":'ANGLE_BASED',
"Fill_Holes":True,
"Correct_Aspect":True,
"Use_Subdivision_Surface":False,
"Margin":0.001,
}

def mainCorrectUv():
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
        
    bpy.ops.uv.smart_project(angle_limit=deafults["Angle_Limit"])

    
    area=bpy.context.area.ui_type
    bpy.context.area.ui_type = 'UV'
    bpy.ops.uv.select_all(action='SELECT')
    bpy.context.area.ui_type =area
    
    bpy.ops.uv.seams_from_islands()
    bpy.ops.uv.unwrap(method=deafults["Method"], fill_holes=deafults["Fill_Holes"], correct_aspect=deafults["Correct_Aspect"], use_subsurf_data=deafults["Use_Subdivision_Surface"], margin=deafults["Margin"])
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
    
    
    
    Angle_Limit=bpy.props.FloatProperty(name="Angle Limit",default=66.0,min=1,max=89,precision=3)
    
    
    Method :bpy.props.EnumProperty(
        name="Method",
        default='ANGLE_BASED',
        items=[
            ('ANGLE_BASED',"Angle Based",""),
            ('CONFORMAL',"Conformal",""),
        ]
    )
    
    Fill_Holes=bpy.props.BoolProperty(name="Fill Holes",default=True)
    Correct_Aspect=bpy.props.BoolProperty(name="Correct Aspect",default=True)
    Use_Subdivision_Surface=bpy.props.BoolProperty(name="Use Subdivision Surface",default=False)
    
    Margin=bpy.props.FloatProperty(name="Margin",default=0.001,min=0,max=1,precision=3)
    
    
    def execute(self,context):
        
        if even[0]:
            even[0]=False
            
            deafults["Angle_Limit"]=self.Angle_Limit
            deafults["Method"]=self.Method
            deafults["Fill_Holes"]=self.Fill_Holes
            deafults["Correct_Aspect"]=self.Correct_Aspect
            deafults["Use_Subdivision_Surface"]=self.Use_Subdivision_Surface
            deafults["Margin"]=self.Margin
            
            mainCorrectUv()
        else:
            even[0]=False
            bpy.ops.wm.correct_uv("INVOKE_DEFAULT")
        return {"FINISHED"}
    
    def invoke(self,context,event):
        self.Angle_Limit=deafults["Angle_Limit"]
        self.Method=deafults["Method"]
        self.Fill_Holes=deafults["Fill_Holes"]
        self.Correct_Aspect=deafults["Correct_Aspect"]
        self.Use_Subdivision_Surface=deafults["Use_Subdivision_Surface"]
        self.Margin=deafults["Margin"]
        even[0]=True
        
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
