##################################################################################
#Bone space to Armature space - Autorig for Blender 2.79 by RockyMadio           # 
#version 0.1                                                                     #
#                                                                                #
#besure the armature is in the center of viewport                                #
#besure action should be unlinked or not affect original positions of all pieces #
##################################################################################

import bpy
from bpy import ops, context
from bpy.types import Panel, Operator
import math
from mathutils import *

def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 

def EXE():    
    scene = context.scene
    
    #the operation should happen in object mode
    #No matter if you are in edit or pose mode, this line will initialize to object mode
    ops.object.mode_set(mode="OBJECT")  

    #armature object gets selected    
    armatureObject = scene.objects.active 
    
    #armature data
    armature = armatureObject.data

    temporary = [] #this will store the pieces temporarily
    
    child_obs = getChildren( armatureObject )
    
    for obj in child_obs: #iterate all objects parented to armature
        target = obj
        bone = target.parent_bone
        
        #create a vertex group of a child object to match its bone parent
        new_vertex_group = target.vertex_groups.new( bone )
                
        verts = []
        mesh = target.data
        
        #Create vertex group with factor 1.0
        #this operation applies vertex group for every vertice in the object
        for vert in mesh.vertices:
            verts.append(vert.index)
            new_vertex_group.add(verts, 1.0, 'REPLACE')     
            
            matrixcopy = target.matrix_world.copy()
            
            #unparent from bone , parent to armature while keeping original matrix transformation
            
            
                
            target.parent = None              
            target.matrix_world = matrixcopy    
   
            target.parent = armatureObject

        for m in target.modifiers:                
            #if(m.type == "MIRROR"):
            target.modifiers.remove(m)
                
        #blender will select all the pieces 
        context.scene.objects.active = target
        ops.object.parent_clear(type='CLEAR')
        
        
        #remember the pieces
        temporary.append(target)
     
                                
    ctx = context.copy()       
    ctx['active_object'] = temporary[0]

    ctx['selected_objects'] = temporary
    ctx['selected_editable_bases'] = [scene.object_bases[obj.name] for obj in temporary] 
    
    #every selected pieces will be joined into 1 mesh
    ops.object.join(ctx)

    mesh = armatureObject.children[0]   #the active object will be the parent of all selected object
    mesh.select = True

    #blender will select the armature object ( on top of all pieces )
    context.scene.objects.active = armatureObject
    
    #scene cursor will be placed at armature cursor
    context.scene.cursor_location = armatureObject.location
    
    #all selected objects will receive a new origin point ( at cursor )
    ops.object.origin_set(type='ORIGIN_CURSOR')   
    
    #reset every transformation
    ops.object.transform_apply(location=False, rotation=True, scale=True)   
    
    #group all parts with armature deformation
    ops.object.parent_set(type='ARMATURE', keep_transform=False)

    #update
    children = getChildren(armatureObject)
    
EXE()