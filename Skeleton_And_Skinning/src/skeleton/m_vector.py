import pygame
import math
import numpy as np
# Trieda M_Vector, sluzi na reprezentaciu jedneho vektora skin-u
class M_Vector:

    '''Konstruktor'''
    def __init__(self, pVector):
        self._pVector = pVector # suradnice [x, y]
        self._weights = []      # pole pre vahy vplyvnych kosti
        self._infBones = []     # pole pre kosti, ktore maju vplyv na pohyb vektora
        self._selected = False  # pomocna premenna pri manipulacii s vektrom
        self._filter_constant = 1.3 # konstanta pre fitrovanie vah a kosti

    # Vykreslenie objektu do grafickej plochy
    def Draw(self, screen):
        pygame.draw.circle(screen, pygame.Color('purple'),[int(self._pVector[0]), int(self._pVector[1])], 5 if self._selected else 3, 0)

    # Pohyb zmena pozicie na zaklade novej pozicie kosti, ktore maju
    # vplyv na pohyb vektora.'''
    def Tranformation(self):
        # Inicializacia vektora
        np_PVector = np.array([0.0, 0.0, 0.0])
        old_PVector = self._pVector + [1]
        # Prechadzaj vsetky vplyvne kosti
        for i in range(len(self._infBones)):
            # Nasobenie matice (world matrix danej kosti) vplyvnej kosti s vektorom sucastnej pozicie -> vysledok prevahovani na zaklade vplyvu
            # kosti a pricitany medzi vysledku
            np_PVector += (np.dot(self._infBones[i]._wMatrix, old_PVector) *  self._weights[i])

        # Vysledok suctu nasobenia sa nastavi ako novy vektor
        self._pVector[0] = np_PVector[0]
        self._pVector[1] = np_PVector[1]

    # Predzaj vsetky kosti, vypocital vzdialenost od kosti a na zaklade vzdialenosti prirad vahy
    def Calculate_Weights(self, bones):
        distances_from_bones = []
        new_inf_bones = []
        weights_of_bones = []
        # Vypocitaj vzdialenosti od vsetkych danych kosti
        for _bone in bones:
            distance_bone = self.DistancePointLine(self._pVector[0], self._pVector[1], _bone._sVector[0],_bone._sVector[1], _bone._eVector[0], _bone._eVector[1])
            distances_from_bones.append(distance_bone) # vzdialenost uloz do pola
            new_inf_bones.append(_bone)                # uloz danu kost do pola

        copy_inf_bones = []
        copy_distances_bones = []

        # Najdi minimalnu vzdialenost
        min_distance = min(distances_from_bones)

        # Filtrovanie kosti a vah na zaklade fitrovacej kostanty
        # Prechadzaj vsetky kosti a ponechaj iba tie ktore su mensie ako (filter_constant * dana vzdialenost)
        # napriklad ak je filtrovacia kostanta 1.1, tak su ponechane iba kosti, ktorym vzdialenost je mensia ako
        # 1.1 * minimalna vzdialenost
        for i in range(len(distances_from_bones)):
            if (min_distance * self._filter_constant) > distances_from_bones[i]:
                copy_distances_bones.append(distances_from_bones[i])
                copy_inf_bones.append(new_inf_bones[i])

        new_inf_bones = copy_inf_bones
        distances_from_bones = copy_distances_bones
        # Vypocitaj sumu vzdialenosti, uz filtrovanych vzdialenosti
        sum_distance = sum(distances_from_bones)
        # Urc vahy na zaklade inveznej percentualnej hodnoty, na zaklade vypocitane na zaklade vztahu
        # (suma zdialenosti - vzdialenost)/suma zdialenosti, mensia vzdialenost ma vacsiu vahu
        for distance in distances_from_bones:
            weights_of_bones.append((sum_distance-distance)/sum_distance)
        # Ak je len jedna kosti, tak jej daj vahu jedna
        if len(weights_of_bones) == 1:
            self._weights = [1]
        else:
            # Suma inverznych percentualnych vah
            sum_inv_weight = sum(weights_of_bones)
            # Invezne percentualne vahy na sucet do 1
            self._weights = [weigh/sum_inv_weight for weigh in weights_of_bones]

        self._infBones = new_inf_bones

    # 1/2 Funkcia pre vypocet vzdialenosti bodu od priamky
    # prevzate z http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba

    def lineMagnitude(self, x1, y1, x2, y2):
        lineMagnitude = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return lineMagnitude

    # 2/2 Funkcia pre vypocet vzdialenosti bodu od priamky
    # prevzate z http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
    def DistancePointLine(self, px, py, x1, y1, x2, y2):
        # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
        LineMag = self.lineMagnitude(x1, y1, x2, y2)

        if LineMag < 0.00000001:
            DistancePointLine = 9999
            return DistancePointLine

        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (LineMag * LineMag)

        if (u < 0.00001) or (u > 1):
            # // closest point does not fall within the line segment, take the shorter distance
            # // to an endpoint
            ix = self.lineMagnitude(px, py, x1, y1)
            iy = self.lineMagnitude(px, py, x2, y2)
            if ix > iy:
                DistancePointLine = iy
            else:
                DistancePointLine = ix
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            DistancePointLine = self.lineMagnitude(px, py, ix, iy)

        return DistancePointLine

    # Prepocitaj vahy a urob transformaciu vektora
    def RecalculateWeights(self, bones):
        self.Calculate_Weights(bones)
        self.Tranformation()

    # Ak je vzdialenost pozicie mysi od vektora mensia ako 5, tak True, inak False
    def OnHover(self, x, y):
        return math.sqrt((x-self._pVector[0])**2 + (y-self._pVector[1])**2) < 5

    # Pouzivane pri tahani vektora pri editacii, nastavia sa nova pozicia vektora
    def Drag(self, nwPvector):
        self._pVector = nwPvector

    # Pretazena metoda pre iterovanie hodnot triedy, ktore chceme ukladat do JSON suboru
    def __iter__(self):
        seq = ['x', 'y', 'inf_bones', 'weights']
        val = [self._pVector[0], self._pVector[1]] + [[ b._id for b in self._infBones ]] + [[ w for w in self._weights ]]

        for i in range(4):
            yield (seq[i], val[i])
