import bpy
import os
import uuid
from bpy.props import StringProperty, EnumProperty, PointerProperty

# --- TEMPLATES YAML POUR UNITY ---

MAT_TEMPLATE = """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!21 &2100000
Material:
  serializedVersion: 8
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_Name: [MAT_NAME]
  m_Shader: {fileID: 4800000, guid: 6e4ae4064600d784cac1e41a9e6f2e59, type: 3}
  m_Parent: {fileID: 0}
  m_ModifiedSerializedProperties: 0
  m_ValidKeywords:
  - _DISABLE_SSR_TRANSPARENT
  - _NORMALMAP
  - _NORMALMAP_TANGENT_SPACE
  m_InvalidKeywords: []
  m_LightmapFlags: 4
  m_EnableInstancingVariants: 0
  m_DoubleSidedGI: 0
  m_CustomRenderQueue: 2225
  stringTagMap: {}
  disabledShaderPasses: []
  m_LockedProperties: 
  m_SavedProperties:
    serializedVersion: 3
    m_TexEnvs:
    - _BaseColorMap:
        m_Texture: {fileID: 2800000, guid: [BC_GUID], type: 3}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _NormalMap:
        m_Texture: {fileID: 2800000, guid: [N_GUID], type: 3}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    m_Ints: []
    m_Floats:
    - _AlphaCutoffEnable: 0
    - _BlendMode: 0
    - _CullMode: 2
    - _CullModeForward: 2
    - _DoubleSidedEnable: 0
    - _DstBlend: 0
    - _MaterialID: 1
    - _Metallic: 0
    - _OpaqueCullMode: 2
    - _ReceivesSSR: 1
    - _Smoothness: 0.5
    - _SrcBlend: 1
    - _SupportDecals: 1
    - _SurfaceType: 0
    - _TransparentCullMode: 2
    - _TransparentZWrite: 0
    - _UseShadowThreshold: 0
    - _ZTestDepthEqualForOpaque: 3
    - _ZTestGBuffer: 4
    - _ZTestTransparent: 4
    - _ZWrite: 1
    m_Colors:
    - _BaseColor: {r: 1, g: 1, b: 1, a: 1}
    - _Color: {r: 1, g: 1, b: 1, a: 1}
    - _EmissionColor: {r: 1, g: 1, b: 1, a: 1}
"""

PREFAB_TEMPLATE = """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &100000
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  serializedVersion: 6
  m_Component:
  - component: {fileID: 400000}
  - component: {fileID: 330000}
  - component: {fileID: 230000}
  m_Layer: 0
  m_Name: _[NAME]
  m_TagString: Untagged
  m_Icon: {fileID: 0}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &400000
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 100000}
  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}
  m_LocalPosition: {x: 0, y: 0, z: 0}
  m_LocalScale: {x: 1, y: 1, z: 1}
  m_Children: []
  m_Father: {fileID: 0}
  m_RootOrder: 0
  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}
--- !u!33 &330000
MeshFilter:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 100000}
  m_Mesh: {fileID: 4300000, guid: [MESH_GUID], type: 3}
--- !u!23 &230000
MeshRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 100000}
  m_Enabled: 1
  m_CastShadows: 1
  m_ReceiveShadows: 1
  m_DynamicOccludee: 1
  m_StaticShadowCaster: 0
  m_MotionVectors: 1
  m_LightProbeUsage: 1
  m_ReflectionProbeUsage: 1
  m_RayTracingMode: 2
  m_RayTraceProcedural: 0
  m_RenderingLayerMask: 1
  m_RendererPriority: 0
  m_Materials:
  - {fileID: 2100000, guid: [MAT_GUID], type: 3}
"""

META_TEMPLATE_FBX = """fileFormatVersion: 2
guid: [GUID]
ModelImporter:
  serializedVersion: 21300
  materials:
    materialImportMode: 0
"""

META_TEMPLATE_MAT = """fileFormatVersion: 2
guid: [GUID]
NativeFormatImporter:
  mainObjectFileID: 2100000
"""

META_TEMPLATE_TEX_BC = """fileFormatVersion: 2
guid: [GUID]
TextureImporter:
  textureType: 0
  sRGBTexture: 1
"""

META_TEMPLATE_TEX_N = """fileFormatVersion: 2
guid: [GUID]
TextureImporter:
  textureType: 1
  sRGBTexture: 0
"""

# --- UTILS ---

def get_texture_from_material(mat, slot_name):
    if not mat or not mat.use_nodes:
        return None
    
    nodes = mat.node_tree.nodes
    principled = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    
    if not principled:
        return None
        
    socket = principled.inputs.get(slot_name)
    if not (socket and socket.is_linked):
        return None
    
    # On récupère le nœud branché sur le socket
    node = socket.links[0].from_node
    
    # Si c'est un nœud "Normal Map", on regarde ce qui est branché sur son entrée "Color"
    if node.type == 'NORMAL_MAP':
        color_socket = node.inputs.get("Color")
        if color_socket and color_socket.is_linked:
            node = color_socket.links[0].from_node
            
    # On vérifie si le nœud final est bien une texture image
    if node.type == 'TEX_IMAGE':
        return node.image
        
    return None

def save_resized_image(image, path, res):
    if not image:
        return
    
    # Force le chargement de l'image en mémoire pour éviter les textures blanches
    try:
        _ = image.pixels[0] if len(image.pixels) > 0 else None
    except:
        pass
        
    temp_image = image.copy()
    temp_image.scale(res, res)
    
    # Configuration pour la sauvegarde
    temp_image.filepath_raw = path
    temp_image.file_format = 'PNG'
    
    try:
        temp_image.save()
    except:
        # Fallback si save() échoue (ex: images générées)
        settings = bpy.context.scene.render.image_settings
        old_format = settings.file_format
        settings.file_format = 'PNG'
        temp_image.save_render(filepath=path)
        settings.file_format = old_format
        
    bpy.data.images.remove(temp_image)

# --- OPERATOR ---

class UNITY_OT_bulk_export(bpy.types.Operator):
    bl_idname = "export.unity_bulk"
    bl_label = "Export to Unity"
    bl_description = "Export meshes, textures, materials and prefabs for Unity HDRP"

    def execute(self, context):
        scene = context.scene
        props = scene.unity_bulk_props
        
        export_path = bpy.path.abspath(props.export_dir)
        if not os.path.exists(export_path):
            os.makedirs(export_path, exist_ok=True)

        resolution = int(props.resolution)
        
        target_collection = props.collection
        if target_collection:
            objects = [obj for obj in target_collection.objects if obj.type == 'MESH']
        else:
            objects = [obj for obj in bpy.data.objects if obj.type == 'MESH' and obj.visible_get()]

        if not objects:
            self.report({'WARNING'}, "No meshes found to export")
            return {'CANCELLED'}

        # --- MODE FUSION (MERGE) ---
        if props.merge_materials and len(objects) > 1:
            export_name = props.collection.name if props.collection else "MergedExport"
            print(f"Merging: {export_name}")
            
            # Dossier unique
            obj_dir = os.path.join(export_path, export_name)
            os.makedirs(obj_dir, exist_ok=True)
            
            # Duplication et Fusion
            for o in context.view_layer.objects:
                o.select_set(False)
            for o in objects:
                o.select_set(True)
            
            # On duplique pour ne pas détruire la scène originale
            bpy.ops.object.duplicate()
            merged_obj = context.active_object
            bpy.ops.object.join()
            merged_obj.name = export_name
            
            # Reset location
            merged_obj.location = (0, 0, 0)
            
            # UV Packing
            context.view_layer.objects.active = merged_obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.pack_islands(margin=0.001)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            fbx_guid = uuid.uuid4().hex
            mat_guid = uuid.uuid4().hex
            bc_guid = uuid.uuid4().hex
            n_guid = uuid.uuid4().hex

            # Export FBX
            fbx_path = os.path.join(obj_dir, f"{export_name}.fbx")
            bpy.ops.export_scene.fbx(
                filepath=fbx_path,
                use_selection=True,
                apply_scale_options='FBX_SCALE_ALL',
                use_mesh_modifiers=True,
                mesh_smooth_type='FACE',
                add_leaf_bones=False,
                axis_forward='-Z',
                axis_up='Y'
            )
            with open(fbx_path + ".meta", "w") as f:
                f.write(META_TEMPLATE_FBX.replace("[GUID]", fbx_guid))
            
            # Textures (On prend celles du premier matériau trouvé avant la fusion ou on laisse vide pour bake)
            # Pour la nomenclature demandée :
            mat_name = f"M_{export_name}"
            bc_filename = f"T_{export_name}_BC.png"
            n_filename = f"T_{export_name}_N.png"
            
            # Création fichiers Unity
            mat_content = MAT_TEMPLATE.replace("[MAT_NAME]", mat_name).replace("[BC_GUID]", bc_guid).replace("[N_GUID]", n_guid)
            with open(os.path.join(obj_dir, f"{mat_name}.mat"), 'w') as f:
                f.write(mat_content)
            with open(os.path.join(obj_dir, f"{mat_name}.mat.meta"), 'w') as f:
                f.write(META_TEMPLATE_MAT.replace("[GUID]", mat_guid))
            
            prefab_content = PREFAB_TEMPLATE.replace("[NAME]", export_name).replace("[MESH_GUID]", fbx_guid).replace("[MAT_GUID]", mat_guid)
            with open(os.path.join(obj_dir, f"_{export_name}.prefab"), 'w') as f:
                f.write(prefab_content)
                
            # Nettoyage de l'objet temporaire
            bpy.data.objects.remove(merged_obj, do_unlink=True)
            
            self.report({'INFO'}, f"Merged export completed: {export_name}")
            return {'FINISHED'}

        # --- MODE BULK (PAR DEFAUT) ---
        for obj in objects:
            mesh_name = obj.name
            
            obj_dir = os.path.join(export_path, mesh_name)
            os.makedirs(obj_dir, exist_ok=True)
            
            mat = obj.active_material if obj.material_slots else None
            bc_tex = get_texture_from_material(mat, "Base Color")
            n_tex = get_texture_from_material(mat, "Normal")
            
            fbx_guid = uuid.uuid4().hex
            mat_guid = uuid.uuid4().hex
            bc_guid = uuid.uuid4().hex if bc_tex else "00000000000000000000000000000000"
            n_guid = uuid.uuid4().hex if n_tex else "00000000000000000000000000000000"
            
            if bc_tex:
                bc_path = os.path.join(obj_dir, f"T_{mesh_name}_BC.png")
                save_resized_image(bc_tex, bc_path, resolution)
                with open(bc_path + ".meta", "w") as f:
                    f.write(META_TEMPLATE_TEX_BC.replace("[GUID]", bc_guid))
            if n_tex:
                n_path = os.path.join(obj_dir, f"T_{mesh_name}_N.png")
                save_resized_image(n_tex, n_path, resolution)
                with open(n_path + ".meta", "w") as f:
                    f.write(META_TEMPLATE_TEX_N.replace("[GUID]", n_guid))

            # Mémoriser la position originale
            original_location = obj.location.copy()
            obj.location = (0, 0, 0)
            context.view_layer.update()

            for o in context.view_layer.objects:
                o.select_set(False)
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            fbx_path = os.path.join(obj_dir, f"{mesh_name}.fbx")
            
            # Export avec application des échelles et modifiers
            bpy.ops.export_scene.fbx(
                filepath=fbx_path,
                use_selection=True,
                apply_scale_options='FBX_SCALE_ALL',
                use_mesh_modifiers=True,
                mesh_smooth_type='FACE',
                add_leaf_bones=False,
                axis_forward='-Z',
                axis_up='Y'
            )
            with open(fbx_path + ".meta", "w") as f:
                f.write(META_TEMPLATE_FBX.replace("[GUID]", fbx_guid))

            # Restaurer la position originale
            obj.location = original_location

            mat_content = MAT_TEMPLATE.replace("[MAT_NAME]", f"M_{mesh_name}").replace("[BC_GUID]", bc_guid).replace("[N_GUID]", n_guid)
            with open(os.path.join(obj_dir, f"M_{mesh_name}.mat"), 'w') as f:
                f.write(mat_content)
            with open(os.path.join(obj_dir, f"M_{mesh_name}.mat.meta"), 'w') as f:
                f.write(META_TEMPLATE_MAT.replace("[GUID]", mat_guid))

            prefab_content = PREFAB_TEMPLATE.replace("[NAME]", mesh_name).replace("[MESH_GUID]", fbx_guid).replace("[MAT_GUID]", mat_guid)
            with open(os.path.join(obj_dir, f"_{mesh_name}.prefab"), 'w') as f:
                f.write(prefab_content)

        self.report({'INFO'}, f"Exported {len(objects)} objects successfully")
        return {'FINISHED'}

# --- UI ---

class UNITY_PT_export_panel(bpy.types.Panel):
    bl_label = "Unity Bulk Export"
    bl_idname = "UNITY_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unity Export'

    def draw(self, context):
        layout = self.layout
        props = context.scene.unity_bulk_props

        layout.prop(props, "collection")
        layout.prop(props, "resolution")
        layout.prop(props, "merge_materials")
        layout.prop(props, "export_dir")
        layout.separator()
        layout.operator("export.unity_bulk", icon='EXPORT', text="Export to Unity")

class UnityBulkProperties(bpy.types.PropertyGroup):
    collection: PointerProperty(name="Collection", type=bpy.types.Collection)
    resolution: EnumProperty(
        name="Resolution",
        items=[('256', '256', ''), ('512', '512', ''), ('1024', '1024', ''), ('2048', '2048', ''), ('4096', '4096', '')],
        default='1024'
    )
    merge_materials: bpy.props.BoolProperty(
        name="Merge Materials",
        description="Join all meshes into one, pack UVs and use a single material",
        default=False
    )
    export_dir: StringProperty(name="Export Path", subtype='DIR_PATH', default=r"C:\Temp")

# --- REGISTRATION ---

classes = (UnityBulkProperties, UNITY_OT_bulk_export, UNITY_PT_export_panel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.unity_bulk_props = PointerProperty(type=UnityBulkProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.unity_bulk_props
