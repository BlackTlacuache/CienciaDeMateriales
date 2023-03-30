#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re


# In[2]:


file = './datos/PeriodicTableofElementsCRadiusIones.xlsx'
df = pd.read_excel(file)
simbolo = df['Symbol'].to_list()
df = df.set_index('Symbol')


# In[3]:


class Elemento:
    def __init__(self, num_atomico, elemento, masa_atomica, neutrones, protones, electrones, periodo, grupo, fase, radioctividad, natural, tipo, radio_atomico, electronegatividad, primera_ionizacion, densidad, fusion, evaporacion, cantidad_isotopos, descubridor, año, calor_especifico, num_orbitas, num_valencia, estructura, ion, radio_ionico):
        self.num_atomico = num_atomico
        self.elemento = elemento
        self.masa_atomica = masa_atomica
        self.neutrones = neutrones
        self.protones = protones
        self.electrones = electrones
        self.periodo = periodo
        self.grupo = grupo
        self.fase = fase
        self.radioctividad = radioctividad
        self.natural = natural
        self.tipo = tipo
        self.radio_atomico = radio_atomico
        self.electronegatividad = electronegatividad
        self.primera_ionizacion = primera_ionizacion
        self.densidad = densidad
        self.fusion = fusion
        self.evaporacion = evaporacion
        self.cantidad_isotopos = cantidad_isotopos
        self.descubridor = descubridor
        self.año = año
        self.calor_especifico = calor_especifico
        self.num_orbitas = num_orbitas
        self.num_valencia = num_valencia
        self.estructura = estructura
        self.ion = ion
        self.radio_ionico = radio_ionico
        
        #Constantes
        self.cons_avogadro = 6.023*10**23
        self.cons_coulomb = 9*10**9
        self.cons_carga_elemental = 0.16*10**(-18)
    
    def numAtomosEnVol(uwu, VolEnvase):
        return np.format_float_scientific(uwu.densidad *VolEnvase * uwu.cons_avogadro / uwu.masa_atomica)
    
    def atomosEnPeso(element, peso):
        return (peso / element.masa_atomica)*element.cons_avogadro
    
    def densidadCompuestos(volumen,*elementos):
        return sum([x.masa_atomica for x in elementos]) / volumen
    
    def dimensionDeCubo(element):
        return (element.masa_atomica/element.densidad)**(1/3)
    
    def masaCompuesto(*element):
        return sum([x.masa_atomica for x in element])
    
    def confElectronica(element):
        tabla = ['1s2','2s2','2p6','3s2','3p6','4s2','3d10', '4p6', '5s2','4d10','5p6', '6s2', '4f14', '5d10', '6p6', '7s2', '5f14', '6d10', '7p6', '6f14', '7d10', '7f14']
        uwu = 0
        lim = element.num_atomico
        confElectr = []
        for i in tabla:
            p = re.findall(r'-?\d+\.?\d*', i)
            confElectr.append(i)
            owo = int(p[1])
            if uwu < lim - owo:
                uwu+=owo
            else:
                confElectr.pop()
                lx = abs(lim - uwu)
                if len(i) == 3:
                    i = i.replace(i[-1], str(lx))
                else:
                    for o in range(len(i)-2):
                        i = i.replace(i[-1], '')
                    i = i+str(abs(lim - uwu))
                confElectr.append(i)
                break
        return confElectr
    
    def numCoordinacion(element1, element2):
        if element1.radio_atomico > element2.radio_atomico:
            R = element1.radio_atomico
            r = element2.radio_atomico
        else:
            R = element2.radio_atomico
            r = element1.radio_atomico
        Ratio = r/R
        angulo = np.arccos(R/(r+R))*(180/np.pi) 

        if Ratio > 0 and Ratio < 0.155:
            NumCoordi = 2
            estructura = 'Lineal'
        elif Ratio >= 0.155 and Ratio < 0.225:
            NumCoordi = 3
            estructura = 'Trigonal Plana'
        elif Ratio >= 0.225 and Ratio < 0.414:
            NumCoordi = 4
            estructura = 'Tetraédrica o cuadrada planar'
        elif Ratio >= 0.414 and Ratio < 0.732:
            NumCoordi = 6
            estructura = 'Octaédrica'
        elif Ratio >= 0.732 and Ratio < 1:
            NumCoordi = 8
            estructura = 'Cubica Centrada en el Cuerpo'
        elif Ratio == 1:
            NumCoordi = 12
            estructura = '?'
    
        return Ratio , angulo , NumCoordi, estructura
    
    def hummeRothery(element1, element2):
        ratio = (element2.radio_atomico - element1.radio_atomico)/element1.radio_atomico
        diff_electr = element1.electronegatividad - element2.electronegatividad
        return ratio * 100, diff_electr

    def fuerzaCoulomb(estado1, estado2, *element):
        return -(Elemento.cons_coulomb* (Elemento.cons_carga_elemental)**2 * estado1 * estado2)/(sum([x.radio_atomico for x in element]))
    
    def densidadCalculada(forma,element):
        if forma == 'bcc':
            a = 4*element.radio_atomico/np.sqrt(3)
            c = 2
        elif forma == 'fcc':
            a = 4*element.radio_atomico/np.sqrt(2)
            c = 4
        elif forma == 'hcp':
            a = 2*element.radio_atomico
            c = 6
        densida = ((c*element.masa_atomica )/((a**3)*element.cons_avogadro)) * (10**7)**3/(1)
        return densida
    

    def densidadCompuesto(elemento1, elemento2, at1, at2):
        masa_compuesto = at1*elemento1.masa_atomica + at2 * elemento2.masa_atomica
        return (masa_compuesto/elemento2.cons_avogadro)/(2*elemento2.radio_atomico+2*elemento1.radio_atomico)**3 *(10**7)**3
    
    def interpretacionCompuestos(uwu):
        pattern2 = r'[A-Z][a-z]*'
        elementos = re.findall(pattern2,uwu)

        cantidades = re.split(pattern2,uwu)
        cantidades.pop(0)
        cantidades = [x.replace('', '1') if x == '' else x for x in cantidades]
        
        return elementos, cantidades 
    
    def estadoCompuestos(densidad,*element): 
        
        pass


# In[4]:


df = df.fillna('')
nombre = []
for i in simbolo:
    # globals()[i]= Elemento.CrearElemento(df.iloc[i].to_list()) 
    globals()[i]= Elemento(df.loc[i, 'AtomicNumber'],df.loc[i, 'Element'],df.loc[i, 'AtomicMass'],df.loc[i, 'NumberofNeutrons'],df.loc[i, 'NumberofProtons'],df.loc[i, 'NumberofElectrons'],df.loc[i, 'Period'],df.loc[i, 'Group'],df.loc[i, 'Phase'],df.loc[i, 'Radioactive'],df.loc[i, 'Natural'], df.loc[i, 'Type'],df.loc[i, 'AtomicRadius2'],df.loc[i, 'Electronegativity'],df.loc[i, 'FirstIonization'],df.loc[i, 'Density'],df.loc[i, 'MeltingPoint'],df.loc[i, 'BoilingPoint'],df.loc[i, 'NumberOfIsotopes'],df.loc[i, 'Discoverer'],df.loc[i, 'Year'],df.loc[i, 'SpecificHeat'],df.loc[i,'NumberofShells'],df.loc[i, 'NumberofValence'],df.loc[i, 'Estructura'], df.loc[i,'Ion'], df.loc[i,'IonicRadius']) 


# In[5]:


print(Elemento.numAtomosEnVol(Au,86.868), 'Átomos')


# In[6]:


print(Elemento.densidadCompuestos(2.237**3, Mg, O) , 'g/cm^3')


# In[7]:


print(Elemento.dimensionDeCubo(Mg), 'cm^3')


# In[8]:


print(f"La suma de la masa de ", Elemento.masaCompuesto(Mg, O), 'g')


# In[9]:


print(f"La longitud de un lado de un cubo de una mol de {Cu.elemento} es:",Elemento.dimensionDeCubo(Cu), 'cm')
print(f"La longitud de un lado de un cubo de una mol de {Pb.elemento} es:",Elemento.dimensionDeCubo(Pb), 'cm')


# In[10]:


Na.radio_atomico + Cl.radio_atomico


# In[11]:


element = In
print(f'El elemento tiene número atómico {element.num_atomico} y su configuración electrónica es:\n{In.confElectronica()}')


# In[12]:


Elemento.numCoordinacion(Cl, Na)


# In[13]:


Elemento.atomosEnPeso(Ag,100)


# In[14]:


Xe.confElectronica()


# In[15]:


Br.confElectronica()


# In[16]:


Elemento.numCoordinacion(Cl, Na)


# In[17]:


Elemento.hummeRothery(Cu,Zn)


# In[18]:


Elemento.densidadCalculada('bcc',Fe)


# ### Pruebas para intentar hacer otra función
# Lo que necesito es hacer que los posibles iones se puedan sumar o restar los estados es decir que del compuesto H2O se pueda determinar que O gana 2 electrones quedando O^-2 y H pierde un electrón, por lo que queda H^1, lo que llevo es lo siguiente:

# In[19]:


ionic = Elemento.interpretacionCompuestos('SiO2')


# In[20]:


estados = [globals()[x].ion for x in ionic[0]]


# In[21]:


# estados[0]
for i in range(len(estados)):
    print(type(estados[0]))
    # if type(ionic[1][i]) == list:
    #     int(ionic[1][0]) * int(estados[0])


# In[26]:


get_ipython().system('jupyter nbconvert --to python ./cienciMateriales.ipynb')

