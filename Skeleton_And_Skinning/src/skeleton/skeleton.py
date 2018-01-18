import pygame
import math
import json

from src.skeleton.m_vector import M_Vector
from src.skeleton.bone import Bone

''' Trieda reprezentujuca cely skeletonu a skinningu'''
class Skeleton:

    # Konstruktor
    def __init__(self):
        pygame.init()
        self._bones = []         # Pole obsahuje vsetky objekty (Bone) kosti skeletonu
        self._root = None        # Kost, ktora je root
        self.OnlyDrawBone = None # Pomocna premenna, pre vizualizaciu kosti, ktorej sa urcuje este koncovy bod
        self._skin = []          # Pole pre vektory skinningu
        self._skinPoints = []    # Body pre vykreslenie skinningu
        self._next_bone_id = 0   # Identifikator, ktory bude priradeny novej kosti a inkrementnuty
        self._screen = None      # Graficka plocha kniznice pyGame

    # Zviditelni a vrat kost, na ktoru ukazuje mys
    def OnHoverBone(self, X, Y):
        for bone in self._bones:
            if bone.IsOnHover(X, Y):   # Ak ukazuje mys na kost
                bone.DrawEndPoints()   # Vzviditelnu kost
                return bone
            else:
                bone.RemoveEndPoints() # Vypni zviditelnovani kosti, ak na nu neukazujes
        return None

    # Zviditelni bod vektora a vrat vektro, na ktoru ukazuje mys
    def OnHoverMVector(self, x, y):
        for _m_vect in self._skin:
            if _m_vect.OnHover(x, y):     # Ak mys ukazuje na bod vektora
                _m_vect._selected = True  # Povedz vektoru skinu ze je vybraty
                return _m_vect
            _m_vect._selected = False
        return None

    # Prekresli vsetky kosti
    def Redraw(self):
        if self.OnlyDrawBone:
            self.OnlyDrawBone.Draw()
        for bone in self._bones:
            bone.Draw()

    # Pridavanie kosti do skeletonu
    def AddBone(self, screen, sVector, eVector, parent = None):
        # Vypocitaj dlzku kosti, vzdialenost prveho bodu kosti od bodu, kde bolo kliknute mysou, evklidovska vzdialenost
        cLength = math.sqrt((sVector[0] - eVector[0]) ** 2 + (sVector[1] - eVector[1]) ** 2)
        # Vypocitaj uhol medzi prvym bodom a bodom, kde bolo klinute mysou ####################
        xDelta = eVector[0] - sVector[0]                                                    ###
        yDelta = eVector[1] - sVector[1]                                                    ###
        radian = math.atan2(yDelta, xDelta)##### Vypocet arc tan medzi rozdielmi x's a y's ####
        if parent == None: # Ak nie je urceny root, tak asi je toto root
            if self._root == None: # Ak neexistuje este root, tak to pridaj
                # Vytvor kost a pridaj do skeletonu
                self._bones.append(Bone(self._next_bone_id ,screen, cLength, radian, sVector, None))
                self._root = self._bones[-1]
                self._next_bone_id += 1
        else:
            # Ak ma otca, tak pridaj kost s tym, ze ma otca
            self._bones.append(Bone(self._next_bone_id, screen, cLength, radian, None, parent))
            self._next_bone_id += 1

    # Kost, ktorej este nie je urceni koncovy bod
    # Vypocet rovnaky ako pri pridavani kosti 'AddBone(...)'
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

    # Kresli skin, vykresli polygon, ktory je tvoreny bodmi (vektromi) skinningu
    def DrawMesh(self, screen):
        if len(self._skin) > 2: # Musia byt aspon 3 body, aby sa mohol dat vykreslit polygon
            pygame.draw.polygon(screen, pygame.Color('yellow'), self._skinPoints, 0)
        for _v_skin in self._skin: # Prekresli body (vektory) skinnigu
            _v_skin.Draw(screen)

    # Pridaj vektor skin-u
    def AddM_Vertex(self, pVertex):
        n_M_Vertex = M_Vector(pVertex)               # Vytvor objekt na zaklade vektora, klinutia mysi
        n_M_Vertex.Calculate_Weights(self._bones)    # Priradenie vah na zaklade bodov
        self._skin.append(n_M_Vertex)                # Pridaj do pola skin-u
        self._skinPoints.append(n_M_Vertex._pVector) # Pridaj do pola bodov skinu

    # Transformacia skinu do novych suradnic na zakladne pohybu kosti
    def TranformSkin(self):
        for _m_Vertex in self._skin:
            _m_Vertex.Tranformation()

    # Prepocitanie world matrix pre kost
    def RecalculateBoneWMatrix(self):
        for bone in self._bones:
            bone.ReCalwMatrix()

    # Vymazanie kosti, pri mazani kosti sa mazu aj vsetky jeho deti
    def DeleteBone(self, bone):
        boneToDel = self.GetBoneChildren(bone) + [bone] # Ziskaj kosti pod vybranou kostou
        # Zmazanie kosti, ktore maju byt zmazane z self._bones -> nastavenie na None
        for _bone in boneToDel:
            for i in range(len(self._bones)):
                if _bone == self._bones[i]:
                    self._bones[i] = None
                    break
        self.RefreshSkeleton()                          # Refresh skeletonu -> zmaz z self._bones hodnoty None
        if len(self._bones) == 0:                       # Ak sa zmaze vsetko, tak aj zmaz roota
            self._root = None

    # Vymazanie vektora skinu
    def DeleteMVector(self, mVector):
        for i in range(len(self._skin)):
            if mVector == self._skin[i]:
                self._skin[i] = None                    # Nastav dany skin na None
                break
        self.RefreshSkinning()                          # Refresh skinu -> vyhodenie None hodnot z self._skin

    # Vrat vsetky podkosti kosti v stromovej strukture skeletonu
    # Rekurzivne
    def GetBoneChildren(self, bone) -> list:
        if bone != None and len(bone._children) != 0:
            children = [] + bone._children
            for _child in bone._children:
                children += self.GetBoneChildren(_child)
            return children
        return []

    # Refresh skeletonu, vyhodi vsetky None hodnoty z self._bones
    def RefreshSkeleton(self):
        cBones = []
        for _bone in self._bones:
            if _bone != None:
                cBones.append(_bone)
        self._bones = cBones

    # Refresh skinnigu, vyhodi vsetky None hodnoty z self._skinnigu
    def RefreshSkinning(self):
        cSkin = list(self._skin)
        self._skinPoints = []
        self._skin = []
        for _m_vect in cSkin:
            if _m_vect != None:
                self._skin.append(_m_vect)
                self._skinPoints.append(_m_vect._pVector)

    # Prepocitaj vahy daneho vektora
    def RecalculateMVectorWeights(self, mVector):
        mVector.RecalculateWeights(self._bones)

    #Uloz do JSON formatu cely skeleton
    def DoSaveData(self, f):
        print(json.dumps(self, default=dict, sort_keys=True, indent=4), file=f)
        f.close()

    # Pretazenie metody __iter__, iterovanie hodnot, ktore chceme ulozit do JSON suboru
    def __iter__(self):
        seq = ['bones', 'root', 'skin', 'next_bone_id']
        val = [self._bones, self._root, self._skin, self._next_bone_id]

        for i in range(len(seq)):
            yield (seq[i], val[i])

    # Nacitaj skeleton z JSON suboru
    def DoLoadFile(self, f):
        try:
            jsonSkeleton = json.load(f) # Nacitaj subor do dist struktury
            new_bones = []
            h_b = dict()
            # Prechadzaj vsetky ulozene kosti a vytvor objekty
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
            # Prechadzaj vsetky ulozene vektory skinu a vytvoe objekty
            if 'skin' in jsonSkeleton:
                skin = jsonSkeleton['skin']
                for vector in skin:
                    p_vector = [float(vector['x']), float(vector['y'])]
                    inf_bones = [h_b[str(i)] for i in vector['inf_bones']]
                    weights = [float(i) for i in vector['weights']]
                    m_vertex = M_Vector(p_vector)
                    m_vertex._weights = weights
                    m_vertex._infBones = inf_bones
                    new_skin.append(m_vertex)

            # Nastav sucastny objekt skeletonu za nacitany a prekresli
            new_next_numner = int(jsonSkeleton['next_bone_id'])
            self._skin = new_skin
            self._bones = new_bones
            self._next_bone_id = new_next_numner

            self.RefreshSkinning()
            self.Redraw()
        except:
            raise 'Chyba pri nacitani suboru!'