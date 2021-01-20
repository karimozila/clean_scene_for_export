import maya.cmds as mc
from shutil import copy2  
import os    
def make_dir(dir_path):
    if not os.path.exists(dir_path) :
        os.makedirs(dir_path)
        return dir_path

def material_shape_dict(shapes_sel):
    material_shape_dict = {}
    shape_material_dict = {}
    for shape in shapes_sel :
        shading_grps = mc.listConnections(shape,type='shadingEngine')
        if len(shading_grps) > 1 :
            print "please assign material by object" , shape
        else :
            shader = mc.ls(mc.listConnections(shading_grps),materials=1)[0]
            shape_material_dict[str(shape)] = str(shader)
    
    shapes = shape_material_dict.keys()
    shaders = shape_material_dict.values()
    for shader in  set(shaders) :
        shader_shapes = [f for f in shapes if shape_material_dict.get(f) == shader]
        material_shape_dict[shader] = shader_shapes
    return material_shape_dict
    
def get_shader_images(shader) :
    children = {}
    file_ls = []
    aiImage_dict = {}

    def _traverse(node, children):
        
        connections = mc.listConnections(
            node, 
            source=True, 
            destination=False, 
            skipConversionNodes=True) or {}
        
        for child in connections:
            if mc.nodeType(child) == "file" :
                file_ls.append(child)
            if mc.nodeType(child) == "aiImage" :
                tx = mc.getAttr("%s.filename" % child)
                aiImage_dict[child] = tx
            children[child] = {}
                
    def get_nodes(node, children):
        
        _traverse(node, children)
        
        for child in children:
            _traverse(child, children[child])

    get_nodes(shader, children)
    
    return aiImage_dict , file_ls
    # print children  
    # print file_ls  
    # print aiImage_dict  

def edit_textures(shader , asset_path) :
    aiImage_dict , file_ls =  get_shader_images(shader)
    if len(file_ls) :
        mc.error("%s is maya file textures .. plz convert to arnold"%file_ls)
        return False
    else :
        change_file_path(aiImage_dict)
        return True

def change_file_path( aiImage_dict , asset_path ):
    for node , image_path in aiImage_dict.items() :
        # if tx exists copy to asset_path and 
        tx_name = image_path[:len(image_path.split(".")[-1])*-1]+"tx"
        if os.path.isfile(tx_name) :
            copy2(tx_name , make_dir(os.path.join(asset_path , node )) )
            mc.setAttr("%s.filename" % node , os.path.join(asset_path , node ).replce("\\","/")+tx_name.split("/")[-1] )

        else :
            mc.error("%s convert texture to tx first"%image_path)




    
def run_check(shapes_sel , asset_name):
    for shape in shapes_sel :
        shading_grps = mc.listConnections(shape,type='shadingEngine')
    if len(shading_grps) > 1 :
        mc.error( "please %s must have one material by object .." %shape)
    else :
        shader = mc.ls(mc.listConnections(shading_grps),materials=1)[0]
        if edit_textures(shader , asset_name):
            if shader.endswith('_mat_01') and shading_grps.endswith('_sg_01') :
                # export()
                pass
            else :
                if shader.lower().endswith('_mat') :
                    shader = mc.rename(shader , shader.lower()+"_01" )
                    mc.rename(shading_grps ,shader.replace("_mat","_sg") )
                else :
                    shader = mc.rename(shader , shader.lower()+"_mat_01" )
                    mc.rename(shading_grps , shader.replace("_mat","_sg"))



# copy files

# check before if tx exists beside image

# scene name
scene_name = mc.file(q=True, sn=True)
if scene_name :
    if "03_Workflow" in scene_name :
        scene_name.split("/")
        asset_name = scene_name.split("/")[scene_name.split("/").index("Assets")+1]
        # print "proceed"
        selection = mc.ls(dag=1,o=1,s=1,sl=1)
        if len(selection) :
            run_check(selection , asset_name )
        else :
            mc.error( "select something")

    else :
        mc.error( "sorry we need prism")
else :
    mc.error( "sorry you need to save before")
