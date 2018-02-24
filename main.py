import os
import random 
import matplotlib.pyplot as plt 
from seaborn import set, despine 
from kivy import require 
from string import ascii_letters 
from PIL import Image 
from math import ceil 
from time import time 
from decorator import timeout 
from kivy.app import App 
from kivy.uix.popup import Popup 
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.button import Button 
from kivy.properties import BooleanProperty, ObjectProperty 
from matplotlib import rcParams 
from sympy import * 
from sympy.abc import * 
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, \
    implicit_multiplication_application, convert_xor 
from sympy_abs_sign_addon import adjust 

set(style='ticks') 
require('1.9.1') 

itera = 0 
Error = False 
wrt = 'dx'  
tt = 15 
axesscope = 20 
language = 'eng' 

outpexpr, inpexpr, main, history, setting, one, two, three, languagelabel, \
englishbutton, germanbutton, clearbutton, clearlabel, globlabel, \
axeslabel, timeoutlabel, returnbutton, recomputebutton, recomputebutton1, \
recomputebutton2, mostrec, prev, more, back, settingsbutton, histbutton, clearbuttonmain, \
integratebutton, differentiatebutton, graphpopup, plotreturn, clearpopup, content_text, \
yesbutton, nobutton = (ObjectProperty(None),) * 35 


def render(expr:str, path:str, err:bool) -> None:
    rcParams['text.usetex'] = True if 'begin' in expr or err is True else False
    rcParams['text.latex.unicode'] = True if 'begin' in expr or err is True else False
    rcParams['text.latex.preamble'] = r'\usepackage{amsmath}' \
        if 'begin' in expr or err is True else r'\usepackage{unicode-math}'
    
    fig = plt.figure() 
    ax = plt.axes([0, 0, 1, 1]) 
    r = fig.canvas.get_renderer() 
    print(expr) 
    t = ax.text(0.5, 0.5, r'${}$'.format(expr), fontsize=50, fontweight='bold', color='white',
                horizontalalignment='center', verticalalignment='center')
    
    bb = t.get_window_extent(renderer=r) 
    w, h = bb.width / fig.dpi, ceil(bb.height / fig.dpi) 
    fig.set_size_inches((0.1 + w, 0.1 + h))
                                           
    fig.set_facecolor('
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    ax.grid(False) 
    ax.set_axis_off() 
    plt.savefig(path, facecolor=fig.get_facecolor()) 
                                                     
    plt.clf() 

    w, h = pillow(path, 1) 
    print(w)  

    if w > 8000: 
        raise Exception('oversized')

    clear()

def plot() -> str:
    global axesscope 
    axesscope = int(axesscope) 
    path = generatepath() 

    rawline = access(1, 'raw.txt').split("¦")[0] 
    raweqn = str(parse(rawline)) 
    ycoords = [] 
    xcoords = [i for i in xfrange(-(axesscope), axesscope, 0.1)] 
    tempycoords = list(map(lambda x: trymap(x, raweqn), xcoords)) 
                                             
    for j in tempycoords: 
        try:
            int(j) 
            ycoords.append(j)  
                         
        except Exception:  
            xcoords[tempycoords.index(j)] = 'NaN' 
            continue  

    xcoords = list(filter(('NaN').__ne__, xcoords)) 

    while len(xcoords) != len(ycoords): 
        if len(xcoords) > len(ycoords): 
            xcoords.pop() 
        else:
            ycoords.pop() 

    print(xcoords)  
    print(ycoords)  

    fig, ax = plt.subplots() 
    fig.set_size_inches(8, 8) 

    try:
        assert xcoords != [] and ycoords != [0] 
        ax.plot(xcoords, ycoords) 

    except Exception as ex: 
        print(ex) 
        ax.grid(False) 
        ax.set_axis_off() 
        plt.title(r'Expression Unplottable' if language == 'eng' else 'Ausdruck nicht plottbar', fontsize=40, y=1.025)
        
    else:
        plt.xlim(-(axesscope), axesscope) 
        plt.ylim(-(axesscope), axesscope) 
        ax.grid(True) 
        ax.set_aspect('equal') 
        despine(ax=ax, offset=-224) 
        plt.title(r'${}$'.format(latex(parse(rawline))), fontsize=40, y=1.025) 
                                                                
    finally: 
        plt.savefig(path) 
        plt.clf() 
        return path 

def parse(i:str) -> str: 
    psyn = {'arctan': 'atan', 'arccot': 'acot', 'arcsin': 'asin',
            'arccos': 'acos', 'arcsec': 'asec', 'arccsc': 'acsc',
            'e': 'E'}
                    
    for k, v in psyn.items(): 
        if k in i: 
            if k == 'e': 
                for l,j in enumerate(i): 
                    if j == 'e' and i[l + 1] == '^': i = i[:l] + v + i[l+1:]
                    
                    continue 

            else: i = i.replace(k, v) 

    parsed = parse_expr(i, transformations=(
        standard_transformations + (convert_xor, implicit_multiplication_application,)))
    

    return parsed 

def generatepath() -> str:
    randpath = ''.join(random.sample(ascii_letters * 6, 6)) + '.png' 
                                                              
    return randpath 

def integration(expr:str, comp:object, ul:str, ll:str) -> tuple: 
    if 'nan' in str(comp): 
        print('it is') 
        raise Exception('definiteerror') 
                                        
    elif ul != '' or ll != '': 
        expr = r"\int_{" + ul + "}^{" + ll + "}" + str(expr) + r" \ " + wrt
        
        try: float(ul), float(ll), float(comp.evalf()) 
        except Exception:                              
            comp = r"\equiv " + str(latex(comp))  
        else:                                     
            if 'Piecewise' not in str(comp):  
                comp = r"\equiv " + str(latex(comp)) + r"\equiv " + str(comp.evalf()) 
                                                                
            else: comp = r"\equiv " + str(latex(comp)) 

    else:
        comp = r"\equiv " + str(comp) + "+ C" 
        expr = r"\int " + expr + r" \ " + wrt 
    return expr, comp 

def differentiation(expr:str, comp:str) -> tuple: 
    expr = r"\frac{d}{" + wrt + "}\ " + expr 
    comp = r"\equiv " + comp 
    return expr, comp 

def commit(expr:str, rawexpr:str) -> None: 
    with open('save.txt', 'a') as save:  
        save.write(expr) 
        save.write('\n') 
    with open('raw.txt', 'a') as save:  
        save.write(rawexpr) 
        save.write('\n') 
    print(expr)  

def access(x:int, file:str) -> str: 
    with open(file) as save: 
        lines = save.readlines() 
        outp = lines[-x].rstrip() 
    return outp 

def increment(x:int) -> None: 
    global itera 
    itera += x 

def pillow(path:str, scale:float) -> tuple: 
    w, h = Image.open(path).size 
                                 
    f = lambda i, j: (i * scale, j * scale) 
                                            
    return f(w, h)  

def xfrange(start:int, stop:int, step:float) -> tuple: 
    i = 0  
    while start + i * step < stop: 
        yield start + i * step   
        i += 1 

def trymap(x:float, e:str) -> eval or str: 
    if wrt != 'dx' and 'x' in e: e = '%' 
                                                                          
    e = e.replace(wrt.replace('d', ''), 'x') 
    f = lambda x: eval(e)   
    try:
        f(x) 
        return eval(e) 
    except Exception: 
        return 'NaN' 

@timeout(tt)  
def formatinp(calculation:str, mode:str, ul:str, ll:str): 
    ref_calculation = adjust(eval(wrt.replace('d', '')), wrt, calculation, mode)
    
    if ul and ll != '': 
        if mode != 'itgr':  
            raise Exception('limiterror') 
        integr = integrate(parse(ref_calculation), (Symbol(wrt.replace('d', '')), parse(ul), parse(ll)))
        
        return integration(latex(parse(calculation)), integr, ul, ll) 
    else: 
        if ul != '' or ll != '': 
            raise Exception('onelimit') 
        return integration(latex(parse(calculation)), latex(integrate(parse(ref_calculation),
            Symbol(wrt.replace('d', '')))), ul, ll) \
            if mode == 'itgr' \
            else differentiation(latex(parse(calculation)), latex(diff(parse(ref_calculation),
            Symbol(wrt.replace('d', '')))))
            
                       
def clear() -> None:
    try:
        files = os.listdir(".")
        
        for f in files: 
            if os.path.isfile(f): 
                t = os.stat(f) 
                      
                if t.st_ctime < time() - 20 and f.endswith('.png'): 
                      os.remove(f) 
                      
    except Exception: 
        pass


class MainScreen(Screen): 
    def calculate(self:object, calculation:str, mode:str, ul:str, ll:str) -> str:
        
        global Error 
        self.calculation = calculation 
        self.helix = generatepath() 
        self.cyndy = generatepath() 
        if calculation != '': 
            try: 
                latexexpr, self.computeexpr = formatinp(calculation, mode, str(ul), str(ll))
                render(latexexpr, self.cyndy, Error) 
                commit(latexexpr, calculation + '¦' + str(ul) + '¦¦' + str(ll) + ';')
                            
            except Exception as e: 
                self.e = e 
                print(e) 
                Error = True 

                if 'oversized' in str(e.args): 
                    print('yes')  
                    render(r'\text{Image too large to render}\ '
                    if language == 'eng'
                    else r'\text{Bild zu Gross zu rendern}\ ', self.cyndy, Error)
                    
                    
                elif 'limiterror' in str(e.args): 
                    render(r'\text{Cannot differentiate with limits}\ '
                    if language == 'eng'
                    else r'\text{Unmoeglich mit Grenzen abzuleiten}\ ', self.cyndy, Error)
                    
                elif 'definiteerror' in str(e.args): 
                    expr, none = integration(parse(calculation), 0, ul, ll) 
                    render(expr, self.cyndy, False) 
                    commit(expr, calculation + '¦' + str(ul) + '¦¦' + str(ll) + ';') 
                elif 'onelimit' in str(e.args): 
                    render(r"\text{Input 2 limits to integrate}\ "
                    if language == 'eng'
                    else r'\text{Gib 2 Grenzen ein um zu integrieren}\ ' , self.cyndy, Error)
                    
                elif 'thread' in str(e.args): 
                    render(r'\text{Fatal Error}\ '
                    if language == 'eng'
                    else r'\text{Unbehebbarer Fehler}\ ', self.cyndy, Error)
                    

                else: 
                    render((r'\text{Timeout}\ '
                    if language == 'eng' else r'\text{Zeitfehler}\ ')
                    if 'timeout' in str(e.args) else (r'\text{Syntax Error}\ '
                    if language == 'eng' else r'\text{Syntaktischer Fehler}\ '), self.cyndy, Error)                                     
        else: 
            Error = True 
            try: int(j) 
            except TypeError as ve: self.e = ve 
            
            
            render(r'\text{No Input}\ ' if language == 'eng' else r'\text{Keine Eingabe}\ ', self.cyndy, True)
            
        return self.cyndy 

    def displ(self) -> str:
        global Error 
        if Error is False: 
            try:
                print(self.computeexpr, 'displ')  
                                                 
                if r'\int' in self.computeexpr in self.computeexpr: 
                    render(r'\text{Integral does not compute}\ '
                    if language == 'eng'
                    else r'\text{Integral unmoeglich zu errechnen}\ ', self.helix, True)
                    
                elif r'\frac{d}{d' in self.computeexpr in self.computeexpr: 
                    render(r'\text{Derivative does not compute}\ '
                    if language == 'eng'
                    else r'\text{Ableitung unmoeglich zu errechnen}\ ', self.helix, True)
                    
                else:
                    render(self.computeexpr
                    if language == 'eng'
                    else self.computeexpr.replace('for', 'fuer').replace('otherwise', 'sonst'), self.helix, Error)
                                      
            except Exception as q: 
                if 'oversized' in str(q.args): 
                    render(r'\text{Image too large to render}\ '
                    if language == 'eng'
                    else r'\text{Bild zu Gross zu rendern}\ ', self.helix, True)
                    
                else:
                    render(r'\text{Nothing to show}\ ' 
                                                       
                                                       
                    if language == 'eng'
                    else r'\text{Nichts anzuzeigen}\ ', self.helix, True)

        else: 
            if 'definiteerror' in str(self.e.args): 
                render(r"\text{Integral doesn't converge}\ "
                if language == 'eng'
                else r'\text{Integral konvergiert nicht}\ ', self.helix, Error)
                
            else: 
                render(r'\text{Nothing to show}\ '
                if language == 'eng'
                else r'\text{Nichts anzuzeigen}\ ', self.helix, Error)
                
        Error = False 
        return self.helix 

    def remaster(self, dt:int) -> None: 
        self.parent.ids.main.inpexpr.width, \
        self.parent.ids.main.inpexpr.height = pillow(self.cyndy, 0.70) 
        self.parent.ids.main.outpexpr.width, \
        self.parent.ids.main.outpexpr.height = pillow(self.helix, 0.70 if ('sign(' not in str(self.calculation)
                                                                       or 'begin' not in self.computeexpr) else 0.48)
        
        self.parent.ids.main.inpexpr.opacity, self.parent.ids.main.outpexpr.opacity = 1, 1
        
        self.parent.ids.main.differentiatebutton.enabled = True 
        self.parent.ids.main.integratebutton.enabled = True 
        print('remastered') 

    def graphpopupopen(self) -> None: 
        GraphPopupClass().open() 


class HistScreen(Screen): 
    def retrieval(self, n:int) -> str: 
        if n: 
            path = generatepath() 
            try: render(str(access(itera + n, 'save.txt')), path, False) 
            
            except Exception: render(r'\text{no further item}\ '
                              if language == 'eng'
                              else r'\text{Nichts weiteres}\ ', path, True)
            
            
            if n == 1: 
                print('one') 
                self.one.width, self.one.height = pillow(path, 0.70)
                

            elif n == 2: 
                print('two') 
                self.two.width, self.two.height = pillow(path, 0.70)
                
            else: 
                print('three')
                self.three.width, self.three.height = pillow(path, 0.70)
                
            return path
        

    def recompute(self, n:int) -> None: 
        global wrt 
        rawline = access(itera + n, 'raw.txt') 
        rawcalc = rawline.split("¦")[0] 
        line = access(itera + n, 'save.txt') 
        ul = '' if '\int_{' not in line or '{}^{}' in line \
            else rawline[rawline.find("¦") + 1:rawline.find("¦¦")]
        
        
        
        ll = '' if '\int_{' not in line or '{}^{}' in line \
            else rawline[rawline.find("¦¦") + 2:rawline.find(";")]
        
        
        
        print(rawcalc, ul, ll) 
                               
        oldwrt = wrt 
        wrt = line[-2:] if 'int' in line else line[9:11] 
                                                         
        self.parent.ids.main.inpexpr.source \
            = MainScreen.calculate(self, rawcalc, 'itgr' if 'int' in line else 'diff', ul, ll)
        
        self.parent.ids.main.outpexpr.source = MainScreen.displ(self)
        
        MainScreen.remaster(self, 0) 
        wrt = oldwrt 

class GraphPopupClass(Popup): 
    def getsource(self) -> str:
        self.plotreturn.text = 'Geh zurueck' if language == 'ger' else 'Go back'
        self.graphpopup.title = 'Diagramm' if language == 'ger' else 'Plot'
        
        
        return plot() 
                     

class ClearPopupClass(Popup): 
    def init(self) -> None: 
        
        self.clearpopup.title = 'Achtung' if language == 'ger' else 'Warning'
        self.content_text.text = 'Errechnungen sind nur im Klartext abgespeichert. ' \
        'Die Chronik zu loeschen wird keinen Freiraum schaffen, moechtest du echt fortfahren?' if language == 'ger' \
        else 'Calculations are stored in plain text form, making the application easier to manage, clearing the ' \
        'history will not clear space, do you really want to clear?'
        self.yesbutton.text = 'Yes' if language == 'eng' else 'Ja' 
        self.nobutton.text = 'No' if language == 'eng' else 'Nein' 
        super().open() 

class SettingsScreen(Screen): 
    def wrt(self, inp:str) -> None:  
        global wrt  
        if inp: 
            if inp in ascii_letters and len(inp) == 1: 
                wrt = "d" + inp 
            else: pass 
    def tt(self, inp:int) -> None: 
        global tt 
        try:
            assert inp > 0 
            int(inp) 
        except Exception: pass 
        else: tt = inp 

    def axesscope(self, inp:int) -> None: 
        global axesscope 
        try: int(inp) 
        except Exception: print('error')
        else: axesscope = abs(inp) 

    def clearpopupopen(self) -> None:
        ClearPopupClass().init() 

    def changelanguage(self, lang:str) -> None: 
        global language
        (self.languagelabel.text, self.englishbutton.text, self.germanbutton.text, self.clearbutton.text,
         self.clearlabel.text, self.globlabel.text, self.axeslabel.text, self.timeoutlabel.text,
         self.returnbutton.text, self.parent.ids.history.recomputebutton.text,
         self.parent.ids.history.recomputebutton1.text, self.parent.ids.history.recomputebutton2.text,
         self.parent.ids.history.mostrec.text, self.parent.ids.history.prev.text,
         self.parent.ids.history.more.text, self.parent.ids.history.back.text,
         self.parent.ids.main.settingsbutton.text, self.parent.ids.main.clearbuttonmain.text,
         self.parent.ids.main.histbutton.text, self.parent.ids.main.integratebutton.text,
         self.parent.ids.main.differentiatebutton.text) \
            = ("Sprache", "Englisch", "Deutsch", "Loeschen", "Chronik loeschen",
               "Globale wrt Variable, Standardeinstellung: x", "Achsen Reichweite, Standardeinstellung: 20",
               "Zeitueberschreitung(sek), Standardeinstellung: 15", "zurueck", "wieder errechnen", "wieder errechnen",
               "wieder errechnen", "aktuellste", "vorig", "mehr", "zurueck", "Einstellungen", "Loeschen", "Chronik",
               "Integrieren", "Ableiten") if lang == 'ger' \
            else ("Language", "English", "German", "Clear", "Clear history", "Global wrt variable, default: x",
                  "Axes extent, default: 20", "Timeout time(sec), default: 15", "return", "recompute", "recompute",
                  "recompute", "most recent", "load previous", "load more", "go back", "Settings", "Clear", "History",
                  "Integrate", "Differentiate")            
        
        language = 'eng' if lang == 'eng' else 'ger'
        
        
class DeactivatableButton(Button): 
    enabled = BooleanProperty(True) 

    def on_enabled(self, instance:object, value:bool) -> None: 
                                                               
        if value: 
            self.background_color = [1, 1, 1, 1] 
            self.color = [1, 1, 1, 1] 
        else: 
            self.background_color = [1, 1, 1, .3] 
            self.color = [1, 1, 1, .5] 

    def on_touch_down(self, touch:object) -> bool: 
        if self.enabled:                           
            return super(self.__class__, self).on_touch_down(touch)
            

class CustButton(Button): 
    pass 


class Manager(ScreenManager): 
    pass 


class CalculatorApp(App): 
    def build(self) -> object:
        
        sm = Manager()  
        return sm 

    def clearhist(self) -> None:
        open('save.txt', 'w').close() 
        open('raw.txt', 'w').close() 

    def incritera(self , i:int) -> None: 
        global itera 
        increment(i) 
        itera = 0 if itera < 0 or i == 4 else itera

    def getenabled(self) -> bool: 
        return True if itera > 0 else False 


if __name__ == '__main__': 
    calcApp = CalculatorApp() 
    calcApp.run() 
