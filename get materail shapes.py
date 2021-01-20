print "________"
def material_shape_dict():
    material_shape_dict = {}
    shape_material_dict = {}
    shapes_sel = mc.ls(dag=1,o=1,s=1,sl=1)
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
    
print material_shape_dict()
