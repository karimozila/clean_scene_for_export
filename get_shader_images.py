import maya.cmds as cmds
def get_shader_images(shader) :
    children = {}
    file_ls = []
    aiImage_dict = {}

    def _traverse(node, children):
        
        connections = cmds.listConnections(
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

aiImage_dict , file_ls =  get_shader_images("aiStandardSurface2")
if len(file_ls) :
    print file_ls , "you have maya file textures .. plz convert to arnold"
else :
    print aiImage_dict