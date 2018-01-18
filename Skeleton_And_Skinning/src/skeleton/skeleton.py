import pygame
import math
import json

from src.skeleton.m_vertex import M_Vertex
from src.skeleton.bone import Bone

class Skeleton:

    def __init__(self):
        pygame.init()
        self._bones = []
        self._root = None
        self.OnlyDrawBone = None
        self._skin = []
        self._skinPoints = []
        self._next_bone_id = 0
        self._screen = None

    def OnHoverBone(self, X, Y):
        for bone in self._bones:
            if  bone.IsOnHover(X, Y):
                bone.DrawEndPoints()
                return bone
            else:
                bone.RemoveEndPoints()
        return None

    def OnHoverMVector(self, x, y):
        for _m_vect in self._skin:
            if _m_vect.OnHover(x, y):
                _m_vect._selected = True
                return _m_vect
            _m_vect._selected = False
        return None

    def Redraw(self):
        if self.OnlyDrawBone:
            self.OnlyDrawBone.Draw()
        for bone in self._bones:
            bone.Draw()

    def AddBone(self, screen, sVector, eVector,  bone = None):
        cLength = math.sqrt((sVector[0] - eVector[0]) ** 2 + (sVector[1] - eVector[1]) ** 2)
        xDelta = eVector[0] - sVector[0]
        yDelta = eVector[1] - sVector[1]
        radian = math.atan2(yDelta, xDelta)
        if bone == None:
            if self._root == None:
                self._bones.append(Bone(self._next_bone_id ,screen, cLength, radian, sVector, None))
                self._root = self._bones[-1]
                self._next_bone_id += 1
        else:
            self._bones.append(Bone(self._next_bone_id ,screen, cLength, radian, None, bone))
            self._next_bone_id += 1

    def DrawOnly(self, screen, sVector, eVector, bone = None):
        cLength = math.sqrt((sVector[0] - eVector[0]) ** 2 + (sVector[1] - eVector[1]) ** 2)
        xDelta = eVector[0] - sVector[0]
        yDelta = eVector[1] - sVector[1]
        radian = math.atan2(yDelta, xDelta)
        if bone == None:
            b = Bone(None ,screen, cLength, radian, sVector)
        else:
            b = Bone(None, screen, cLength, radian, parent=bone)

        self.OnlyDrawBone = b

    def DrawMesh(self, screen):
        if len(self._skin) > 2:
            pygame.draw.polygon(screen, pygame.Color('yellow'), self._skinPoints, 0)
        for _v_skin in self._skin:
            _v_skin.Draw(screen)

    def AddM_Vertex(self, pVertex):
        n_M_Vertex = M_Vertex(pVertex)
        n_M_Vertex.Calculate_Weights(self._bones)
        self._skin.append(n_M_Vertex)
        self._skinPoints.append(n_M_Vertex._pVector)

    def TranformSkin(self):
        for _m_Vertex in self._skin:
            _m_Vertex.Tranformation()

    def RstWBnsWMatrix(self):
        for _ch in self._bones:
            _ch.ReCalwMatrix()

    def DeleteBone(self, bone):
        boneToDel = self.GetBoneChildren(bone) + [bone]
        for _bone in boneToDel:
            for i in range(len(self._bones)):
                if _bone == self._bones[i]:
                    self._bones[i] = None
                    break
        self.RefreshSkeleton()
        if len(self._bones) == 0:
            self._root = None

    def DeleteMVector(self, mVector):
        for i in range(len(self._skin)):
            if mVector == self._skin[i]:
                self._skin[i] = None
                break
        self.RefreshSkinning()

    def GetBoneChildren(self, bone) -> list:
        if bone != None and len(bone._children) != 0:
            children = [] + bone._children
            for _child in bone._children:
                children += self.GetBoneChildren(_child)
            return children
        return []

    def RefreshSkeleton(self):
        cBones = []
        for _bone in self._bones:
            if _bone != None:
                cBones.append(_bone)
        self._bones = cBones

    def RefreshSkinning(self):
        cSkin = list(self._skin)
        self._skinPoints = []
        self._skin = []
        for _m_vect in cSkin:
            if _m_vect != None:
                self._skin.append(_m_vect)
                self._skinPoints.append(_m_vect._pVector)

    def CallReCalculateMVector(self, mVector):
        mVector.RecalculateWeights(self._bones)


    def DoSaveData(self, f):
        print(json.dumps(self, default=dict, sort_keys=True, indent=4), file=f)
        f.close()

    def __iter__(self):
        seq = ['bones', 'root', 'skin', 'next_bone_id']
        val = [self._bones, self._root, self._skin, self._next_bone_id]

        for i in range(len(seq)):
            yield (seq[i], val[i])

    def DoLoadFile(self, f):
        try:
            jsonSkeleton = json.load(f)
            new_bones = []
            h_b = dict()
            if 'bones' in jsonSkeleton:
                bones = jsonSkeleton['bones']
                root = None
                for bone in bones:
                    b = None
                    if 'parent_id' in bone:
                        b = Bone(int(bone['id']), self._screen, float(bone['length']), float(bone['angle']), None, h_b[bone['parent_id']])
                    else:
                        b = Bone(int(bone['id']), self._screen, float(bone['length']), float(bone['angle']), [float(bone['x']), float(bone['y'])], None)
                        root = b

                    h_b[str(b._id)] =  b
                    new_bones.append(b)

            new_skin = []
            if 'skin' in jsonSkeleton:
                skin = jsonSkeleton['skin']
                for vector in skin:
                    p_vector = [float(vector['x']), float(vector['y'])]
                    inf_bones = [h_b[str(i)] for i in vector['inf_bones']]
                    weights = [float(i) for i in vector['weights']]
                    m_vertex = M_Vertex(p_vector)
                    m_vertex._weights = weights
                    m_vertex._infBones = inf_bones
                    new_skin.append(m_vertex)

            new_next_numner = int(jsonSkeleton['next_bone_id'])
            self._skin = new_skin
            self._bones = new_bones
            self._next_bone_id = new_next_numner

            self.RefreshSkinning()
            self.Redraw()
        except:
            raise 'Chyba pri nacitani suboru!'