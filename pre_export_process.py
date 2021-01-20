import maya.cmds as mc

def combine_nodes (nodes_ls):
    combined_node = mc.polyUnite(nodes_ls)
    mc.delete(combined_node , ch=1)
    return combined_node

# get hierarchy for sake of preview output       
def list_all_children(nodes):
    """Quite slow but accurate - just use Select > Select Hierarchy as trick.."""
    
    sel = cmds.ls(sl=1)
    cmds.select(nodes, hierarchy=True, replace=True)
    hierarchy = cmds.ls(selection=True, long=True)
    cmds.select(sel, replace=True)
    return hierarchy

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



# selection = mc.ls(dag=1,o=1,s=1,sl=1)
def run(selection):
    mat_shp_dict = material_shape_dict(selection)
    for mat , shps in mat_shp_dict.items() :
        print mat , shps
        new_shp = combine_nodes (shps)
        

run(mc.ls(dag=1,o=1,s=1,sl=1))
# run textures check
# aiImage_dict , file_ls =  get_shader_images("aiStandardSurface2")
# if len(file_ls) :
#     print file_ls , "you have maya file textures .. plz convert to arnold"
# else :
#     print aiImage_dict