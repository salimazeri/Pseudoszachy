# -*- coding: utf-8 -*-     

from random import choice

class Bezszachy():
    licznik = 0
    szachownica = [["w0","s0","g0","k0","h0","g0","s0","w0"]]+[[None]*8 for i in range(6)]+[["w1","s1","g1","k1","h1","g1","s1","w1"]]
    #0: czarny, 1: bialy, w: wieza, s: skoczek, g: goniec, k: krol, h: hetman
        
        
    def kierunek(self,y,x,kolor,kier):
        wektory = {"u":(-1,0),"ur":(-1,1),"r":(0,1),"rd":(1,1),"d":(1,0),"dl":(1,-1),"l":(0,-1),"lu":(-1,-1)}
        legalne = []
        Y, X = wektory[kier]
        y += Y
        x += X
        while 0 <= y < 8 and 0 <= x < 8:
            if not self.szachownica[y][x]:
                legalne.append((y,x))
            elif kolor in self.szachownica[y][x]:
                break
            else:
                #trafiamy na figure przeciwnika
                legalne.append((y,x))
                break
            y += Y
            x += X
        return legalne
        
        
    def wieza(self,y,x,kolor):
        #kompiluje liste miejsc na ktore moze przesunac sie wieza w aktualnej sytuacji
        #y: rzad, x: kolumna
        lista = []
        for kierunek in ["u","r","d","l"]:
            lista += self.kierunek(y,x,kolor,kierunek)
        return lista
        
        
    def skoczek(self,y,x,kolor):
        lista = []
        for Y, X in [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]:
            if 0 <= y+Y < 8 and 0 <= x+X < 8 and (not self.szachownica[y+Y][x+X] or kolor not in self.szachownica[y+Y][x+X]):
                lista.append((y+Y,x+X))
        return lista
    
    
    def goniec(self,y,x,kolor):
        lista = []
        for kierunek in ["ur","rd","dl","lu"]:
            lista += self.kierunek(y,x,kolor,kierunek)
        return lista
    
    
    def krol(self,y,x,kolor):
        lista = []
        for Y, X in [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:
            if 0 <= y+Y < 8 and 0 <= x+X < 8 and (not self.szachownica[y+Y][x+X] or kolor not in self.szachownica[y+Y][x+X]):
                lista.append((y+Y,x+X))
        return lista
    
    
    def hetman(self,y,x,kolor):
        lista = []
        for kierunek in ["u","ur","r","rd","d","dl","l","lu"]:
            lista += self.kierunek(y,x,kolor,kierunek)
        return lista
            
    ruchy = {"w": wieza, "s": skoczek, "g": goniec, "k": krol, "h": hetman}
    
    
    def wszystkie(self,kolor):
        #zwraca liste wszystkich mozliwych ruchow dla gracza w formacie ((ystart,xstart),(y,x))
        figury = []
        for y, rzad in enumerate(self.szachownica):
            #print y, rzad
            for x, pole in enumerate(rzad):
                if pole and kolor in pole:
                    #jesli pole to nie None i figura ktora tam stoi ma nasz kolor
                    figury.append((pole,y,x))
        ruchy = []
        for pole,y,x in figury:
            typ, kolor = pole
            for Y, X in self.ruchy[typ](self,y,x,kolor):
                ruchy.append(((y,x),(Y,X)))
        if figury and not ruchy:
            return "remis"
        return ruchy
        
    
    def __repr__(self):
        string = "  a  b  c  d  e  f  g  h   \n"
        for index, wiersz in enumerate(self.szachownica):
            string += str(index+1)+" "
            for pole in wiersz:
                string += (pole if pole else "[]")+" "
            string += "\n"
        return string
        
    def graj(self):
        while self.licznik < 1000:
            for kolor in "10":
                ruchy = self.wszystkie(kolor)
                if ruchy == "remis":
                    return "remis po %s ruchach" %self.licznik
                if not ruchy:
                    return "%s wygrywa po %s ruchach" %("bialy" if kolor == "0" else "czarny",self.licznik)
                else:
                    stare, nowe = choice(ruchy)
                    self.szachownica[nowe[0]][nowe[1]] = self.szachownica[stare[0]][stare[1]]
                    self.szachownica[stare[0]][stare[1]] = None
                    print (self)
            self.licznik += 2
        return "remis po 1000 ruchow"
    
        
meh = Bezszachy()
# print meh
#meh.ruch("0")
# print meh.skoczek(0,1,"0")
# print meh.wieza(1,2,"0")
#bbb = meh.wieza2(1,2,"0")
print (meh.graj())
