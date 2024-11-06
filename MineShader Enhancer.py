import bpy

bl_info = {
    "name": "MineShader Minecraft Texture Editor",
    "author": "Baris.msi",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Tool Shelf > MineShader",
    "description": "Enhances Minecraft textures with improved subsurface settings.",
    "category": "Material",
}

# Function to rename materials for Minecraft textures
def rename_minecraft_materials(selected_objects):
    for obj in selected_objects:
        if obj.type == 'MESH':
            for mat_slot in obj.material_slots:
                mat = mat_slot.material
                if mat and "minecraft" not in mat.name.lower():
                    mat.name = f"Minecraft_{mat.name}"

# Function to adjust Principled BSDF node settings with customizable weight, radius, and scale
def adjust_principled_nodes(subsurface_weight, subsurface_radius_x, subsurface_radius_y, subsurface_radius_z, subsurface_scale):
    for mat in bpy.data.materials:
        if mat.use_nodes and "minecraft" in mat.name.lower():
            for node in mat.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    # Update Subsurface Weight
                    node.inputs[7].default_value = subsurface_weight
                    # Update Subsurface Radius (X, Y, Z)
                    node.inputs[8].default_value = (subsurface_radius_x, subsurface_radius_y, subsurface_radius_z)
                    # Update Subsurface Scale
                    node.inputs[9].default_value = subsurface_scale

# Update functions to automatically adjust properties on slider change
def update_subsurface_weight(self, context):
    adjust_principled_nodes(
        context.scene.subsurface_weight,
        context.scene.subsurface_radius_x,
        context.scene.subsurface_radius_y,
        context.scene.subsurface_radius_z,
        context.scene.subsurface_scale
    )

def update_subsurface_radius_x(self, context):
    update_subsurface_weight(self, context)

def update_subsurface_radius_y(self, context):
    update_subsurface_weight(self, context)

def update_subsurface_radius_z(self, context):
    update_subsurface_weight(self, context)

def update_subsurface_scale(self, context):
    update_subsurface_weight(self, context)

# Operator to apply texture settings
class TextureEditOperator(bpy.types.Operator):
    bl_idname = "object.texture_edit"
    bl_label = "Apply Minecraft Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}
        
        rename_minecraft_materials(selected_objects)
        adjust_principled_nodes(
            context.scene.subsurface_weight,
            context.scene.subsurface_radius_x,
            context.scene.subsurface_radius_y,
            context.scene.subsurface_radius_z,
            context.scene.subsurface_scale
        )
        self.report({'INFO'}, "Principled BSDF settings applied for selected Minecraft textures")
        return {'FINISHED'}

# Panel class to add UI elements
class MINECRAFT_TEXTURE_PT_panel(bpy.types.Panel):
    bl_label = "MineShader Texture Enhancer"
    bl_idname = "MINECRAFT_TEXTURE_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MineShader"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Minecraft Texture Settings", icon="MATERIAL")
        
        # Action button
        layout.operator("object.texture_edit", text="Apply Texture Settings", icon="SHADING_TEXTURE")

        layout.separator()

        # Subsurface Settings with artistic layout
        layout.label(text="Subsurface Settings", icon="NODE_MATERIAL")
        
        col = layout.column(align=True)
        col.prop(context.scene, "subsurface_weight", text="Weight")
        col.separator()
        
        row = layout.row(align=True)
        row.label(text="Radius:")
        row.prop(context.scene, "subsurface_radius_x", text="X", slider=True)
        row.prop(context.scene, "subsurface_radius_y", text="Y", slider=True)
        row.prop(context.scene, "subsurface_radius_z", text="Z", slider=True)
        
        layout.separator()
        
        col = layout.column(align=True)
        col.prop(context.scene, "subsurface_scale", text="Scale")

# Register and unregister functions
def register():
    bpy.utils.register_class(TextureEditOperator)
    bpy.utils.register_class(MINECRAFT_TEXTURE_PT_panel)
    bpy.types.Scene.subsurface_weight = bpy.props.FloatProperty(
        name="Subsurface Weight",
        description="Adjust the subsurface weight for Minecraft textures",
        default=1.0,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
        update=update_subsurface_weight
    )
    bpy.types.Scene.subsurface_radius_x = bpy.props.FloatProperty(
        name="Radius X",
        description="Adjust the X component of the subsurface radius",
        default=0.5,
        min=0.0,
        max=100.0,
        update=update_subsurface_radius_x
    )
    bpy.types.Scene.subsurface_radius_y = bpy.props.FloatProperty(
        name="Radius Y",
        description="Adjust the Y component of the subsurface radius",
        default=0.5,
        min=0.0,
        max=100.0,
        update=update_subsurface_radius_y
    )
    bpy.types.Scene.subsurface_radius_z = bpy.props.FloatProperty(
        name="Radius Z",
        description="Adjust the Z component of the subsurface radius",
        default=0.5,
        min=0.0,
        max=100.0,
        update=update_subsurface_radius_z
    )
    bpy.types.Scene.subsurface_scale = bpy.props.FloatProperty(
        name="Subsurface Scale",
        description="Adjust the subsurface scale for Minecraft textures",
        default=0.31,
        min=0.0,
        max=10.0,
        update=update_subsurface_scale
    )

def unregister():
    bpy.utils.unregister_class(TextureEditOperator)
    bpy.utils.unregister_class(MINECRAFT_TEXTURE_PT_panel)
    del bpy.types.Scene.subsurface_weight
    del bpy.types.Scene.subsurface_radius_x
    del bpy.types.Scene.subsurface_radius_y
    del bpy.types.Scene.subsurface_radius_z
    del bpy.types.Scene.subsurface_scale

if __name__ == "__main__":
    register()
