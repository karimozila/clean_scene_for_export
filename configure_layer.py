import hou

file_name = "C:/Users/Windows/Desktop/asset/houdini.hip"
def houdini_fix(usd_temp_path , houdini_save_path ):
    asset_prefix = usd_temp_path.split("/")[-1]
    usd_asset_path = usd_temp_path.replace(usd_temp_path.split("/")[-1] , usd_temp_path.split("/")[-1].replace("temp" , "asset"))
    hou.hipFile.setName(houdini_save_path)

    # Get stage root node
    stage = hou.node('/stage/')


    sublayer = stage.createNode('sublayer')
    sublayer_file_path = sublayer.parm("filepath1")
    sublayer_file_path.set("C:/Users/Windows/Desktop/asset/temp.usda")


    graft = stage.createNode('graftstages')
    graft_prim_path = graft.parm("primpath")
    graft_prim_path.set("script_graft_name")
    graft_dest_path = graft.parm("destpath")
    graft_dest_path.set("")
    graft.setInput(1,sublayer)


    configure = stage.createNode('configurelayer')
    configure_set_default_prim = configure.parm("setdefaultprim")
    configure_set_default_prim.set(True)
    configure_default_prim = configure.parm("defaultprim")
    configure_default_prim.set("script_defaultprim")
    configure.setInput(0,graft)


    python = stage.createNode('pythonscript')
    python_script = python.parm("python")
    python_script.set("#my python script")
    python.setInput(0,configure)


    usd_rop = stage.createNode('usd_rop')

    usd_rop_lop_output = usd_rop.parm("lopoutput")
    usd_rop_lop_output.set("C:/Users/Windows/Desktop/asset/asset.usd")
    usd_rop_save_style = usd_rop.parm("savestyle")
    usd_rop_save_style.set('flattenstage')


    usd_rop.setInput(0,python)

    hou.hipFile.save(file_name)

    usd_rop_excute = usd_rop.parm("execute")
    usd_rop_excute.pressButton()

