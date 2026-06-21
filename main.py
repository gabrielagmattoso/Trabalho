
import pygame
import sys
import math
import random
import json
import os

LARGURA  = 960
ALTURA   = 640
FPS      = 60
TITULO   = "Bolo do Lara 🎂"

ARQUIVO_RECORDES = "recordes_bolo_lara.json"

BRANCO     = (255, 255, 255)
PRETO      = ( 25,  25,  35)
CINZA      = (180, 185, 205)
VERMELHO   = (255,  45,  85)
VERDE      = ( 30, 220,  90)
AMARELO    = (255, 220,   0)
AZUL       = ( 60, 190, 255)   
ROSA       = (255,  80, 180)
LARANJA    = (255, 120,   0)
ROXO       = (170,  60, 255)
TURQUESA   = (  0, 220, 200)
MARROM     = (190, 100,  30)
MARROM_ESC = (120,  55,  10)

INGREDIENTES = [
    {"nome": "Farinha",  "emoji": "🌾", "cor": (255, 245, 160)},
    {"nome": "Açúcar",   "emoji": "🍬", "cor": (255, 140, 200)},
    {"nome": "Ovos",     "emoji": "🥚", "cor": (255, 215,  60)},
    {"nome": "Manteiga", "emoji": "🧈", "cor": (255, 185,  30)},
    {"nome": "Leite",    "emoji": "🥛", "cor": (160, 215, 255)},
]

DECORACOES = [
    {"nome": "Chantilly", "emoji": "🍦", "cor": (200, 235, 255)},
    {"nome": "Morango",   "emoji": "🍓", "cor": (255,  70, 100)},
    {"nome": "Chocolate", "emoji": "🍫", "cor": (150,  70,  15)},
    {"nome": "Granulado", "emoji": "🎊", "cor": (255, 150,  10)},
]

FASES = [
    {"nome": "ingredientes", "pontos": 100, "tempo": 9.0,  "bonus": 80},
    {"nome": "misturar",     "pontos": 150, "tempo": 10.0,  "bonus": 60},
    {"nome": "assar",        "pontos": 150, "tempo": 10.0, "bonus": 70},
    {"nome": "decorar",      "pontos": 200, "tempo": 5.0,  "bonus": 40},
]

PENALIDADE_ERRO  = 40
PENALIDADE_TEMPO = 50 

def carregar_recordes():
    
    if os.path.exists(ARQUIVO_RECORDES):
        try:
            with open(ARQUIVO_RECORDES) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def salvar_recorde(nome, pontuacao, estrelas):
    
    lista = carregar_recordes()
    lista.append({"nome": nome, "pontuacao": pontuacao, "estrelas": estrelas})
    lista.sort(key=lambda x: x["pontuacao"], reverse=True)
    with open(ARQUIVO_RECORDES, "w") as f:
        json.dump(lista[:10], f)

def desenhar_fundo_gradiente(tela, cor_topo, cor_base):
    
    for y in range(ALTURA):
        t = y / ALTURA
        cor = (
            int(cor_topo[0] * (1 - t) + cor_base[0] * t),
            int(cor_topo[1] * (1 - t) + cor_base[1] * t),
            int(cor_topo[2] * (1 - t) + cor_base[2] * t),
        )
        pygame.draw.line(tela, cor, (0, y), (LARGURA, y))

def desenhar_botao(tela, fonte, rect, texto, cor, cor_hover, mouse_pos):
  
    hover = rect.collidepoint(mouse_pos)
    cor_atual = cor_hover if hover else cor
    pygame.draw.rect(tela, cor_atual, rect, border_radius=14)
    pygame.draw.rect(tela, MARROM_ESC, rect, 3, border_radius=14)
    txt = fonte.render(texto, True, BRANCO)
    tela.blit(txt, txt.get_rect(center=rect.center))
    return hover

def desenhar_barra_tempo(tela, fonte, restante, total, x, y, largura=200):
    
    proporcao = max(0.0, restante / total)

    if proporcao > 0.5:
        cor = VERDE
    elif proporcao > 0.25:
        cor = AMARELO
    else:
        cor = VERMELHO

    pygame.draw.rect(tela, (50, 50, 60),  pygame.Rect(x, y, largura, 18), border_radius=9)
    pygame.draw.rect(tela, cor,           pygame.Rect(x, y, int(largura * proporcao), 18), border_radius=9)
    pygame.draw.rect(tela, MARROM_ESC,    pygame.Rect(x, y, largura, 18), 2, border_radius=9)

    if proporcao < 0.25 and (pygame.time.get_ticks() // 200) % 2 == 0:
        pygame.draw.rect(tela, VERMELHO, pygame.Rect(x - 3, y - 3, largura + 6, 24), 3, border_radius=11)

    label = fonte.render(f"⏱ {restante:.1f}s", True, BRANCO)
    tela.blit(label, label.get_rect(centerx=x + largura // 2, centery=y + 9))

def desenhar_estrelas(tela, cx, cy, quantidade, anim):
    for i in range(5):
        sx    = cx - 112 + i * 56
        cor   = AMARELO if i < quantidade else CINZA
        raio  = 22
        pontos = []
        for j in range(10):
            ang = -math.pi / 2 + j * math.pi / 5
            r   = raio if j % 2 == 0 else raio // 2
            pontos.append((sx + r * math.cos(ang), cy + r * math.sin(ang)))
        pygame.draw.polygon(tela, cor, pontos)
        pygame.draw.polygon(tela, MARROM, pontos, 2)

class Particula:
    
    def __init__(self, x, y, cor=None):
        self.x    = x
        self.y    = y
        self.vx   = random.uniform(-5, 5)    
        self.vy   = random.uniform(-8, -2)   
        self.vida = random.randint(40, 90)   
        self.cor  = cor or random.choice([VERMELHO, AMARELO, VERDE, ROSA, LARANJA, AZUL, ROXO])
        self.raio = random.randint(4, 10)

    def atualizar(self):
        self.x   += self.vx
        self.vy  += 0.22         
        self.y   += self.vy
        self.vida -= 1

    def desenhar(self, tela):
        alpha = max(0, int(255 * self.vida / 90))
        s = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, alpha), (self.raio, self.raio), self.raio)
        tela.blit(s, (int(self.x) - self.raio, int(self.y) - self.raio))

class Popup:
    

    def __init__(self, x, y, texto, cor=VERDE, tamanho=22):
        self.x     = x
        self.y     = float(y)
        self.texto = texto
        self.cor   = cor
        self.vida  = 100
        self.fonte = pygame.font.SysFont("Arial", tamanho, bold=True)

    def atualizar(self):
        self.y    -= 1.8
        self.vida -= 1

    def desenhar(self, tela):
        alpha = max(0, int(255 * self.vida / 100))
        s = self.fonte.render(self.texto, True, self.cor)
        s.set_alpha(alpha)
        tela.blit(s, s.get_rect(centerx=int(self.x), y=int(self.y)))


class Lara:
    

    def __init__(self, x, y):
        self.x       = x
        self.y       = y
        self.fala    = ""
        self.timer   = 0       
        self.anim    = 0       
        self.piscando = 0      

    def falar(self, texto, duracao=270):
        self.fala  = texto
        self.timer = duracao

    def atualizar(self):
        self.anim += 1
        if self.timer > 0:
            self.timer -= 1
        self.piscando = max(0, self.piscando - 1)
        if random.random() < 0.005: 
            self.piscando = 8

    def desenhar(self, tela, fonte):
        
        oy = int(math.sin(self.anim * 0.04) * 5)
        bx = self.x
        by = self.y + oy

        pygame.draw.ellipse(tela, (238, 238, 238), pygame.Rect(bx - 30, by + 60, 60, 75))

        pygame.draw.rect(tela, (225, 185, 145), pygame.Rect(bx - 10, by + 50, 20, 18))

        pygame.draw.ellipse(tela, (225, 185, 145), pygame.Rect(bx - 30, by + 8, 60, 52))

        pygame.draw.arc(tela, (165, 125, 72),
                        pygame.Rect(bx - 28, by + 6, 56, 22),
                        math.pi * 0.15, math.pi * 0.85, 7)
        pygame.draw.ellipse(tela, (165, 125, 72), pygame.Rect(bx - 34, by + 18, 20, 28))
        pygame.draw.ellipse(tela, (165, 125, 72), pygame.Rect(bx + 14, by + 18, 20, 28))

        alt_olho = 2 if self.piscando > 0 else 11
        pygame.draw.ellipse(tela, BRANCO, pygame.Rect(bx - 20, by + 27, 14, alt_olho))
        pygame.draw.ellipse(tela, BRANCO, pygame.Rect(bx +  6, by + 27, 14, alt_olho))
        if self.piscando == 0:
            pygame.draw.circle(tela, MARROM_ESC, (bx - 13, by + 33), 5)
            pygame.draw.circle(tela, MARROM_ESC, (bx + 13, by + 33), 5)
            pygame.draw.circle(tela, BRANCO,     (bx - 11, by + 31), 2)
            pygame.draw.circle(tela, BRANCO,     (bx + 15, by + 31), 2)

        pygame.draw.arc(tela, (120, 80, 40), pygame.Rect(bx - 22, by + 20, 18, 9),
                        math.pi * 0.2, math.pi * 0.8, 3)
        pygame.draw.arc(tela, (120, 80, 40), pygame.Rect(bx +  4, by + 20, 18, 9),
                        math.pi * 0.2, math.pi * 0.8, 3)

        pygame.draw.ellipse(tela, (200, 155, 115), pygame.Rect(bx - 6, by + 38, 12, 9))
        pygame.draw.arc(tela, (180, 80, 60),
                        pygame.Rect(bx - 15, by + 44, 30, 14),
                        math.pi + 0.3, 2 * math.pi - 0.3, 3)

        
        pygame.draw.rect(tela, (252, 252, 252), pygame.Rect(bx - 22, by - 22, 44, 36), border_radius=8)
        pygame.draw.rect(tela, (200, 200, 200), pygame.Rect(bx - 22, by - 22, 44, 36), 2, border_radius=8)
        pygame.draw.rect(tela, VERMELHO, pygame.Rect(bx - 22, by + 2, 44, 6))

        if self.timer > 0 and self.fala:
            self._desenhar_balao(tela, fonte, bx, by)

    def _desenhar_balao(self, tela, fonte, bx, by):
        
        linhas = self.fala.split("\n")
        pad    = 12

        
        fonte_balao   = pygame.font.SysFont("Arial", 15)
        largura_balao = max(fonte_balao.size(l)[0] for l in linhas) + pad * 2
        altura_balao  = len(linhas) * 22 + pad * 2

        bx_b = bx + 45
        
        if bx_b + largura_balao > LARGURA - 10:
            bx_b = LARGURA - largura_balao - 10
        by_b = by - altura_balao - 15   # acima da cabeça

        pygame.draw.rect(tela, BRANCO,     pygame.Rect(bx_b, by_b, largura_balao, altura_balao), border_radius=12)
        pygame.draw.rect(tela, MARROM_ESC, pygame.Rect(bx_b, by_b, largura_balao, altura_balao), 2, border_radius=12)

        pts = [(bx_b + 18, by_b + altura_balao),
               (bx_b +  6, by_b + altura_balao + 12),
               (bx_b + 34, by_b + altura_balao)]
        pygame.draw.polygon(tela, BRANCO, pts)
        pygame.draw.lines(tela, MARROM_ESC, False, [pts[0], pts[1], pts[2]], 2)

        for i, linha in enumerate(linhas):
            s = fonte_balao.render(linha, True, MARROM_ESC)
            tela.blit(s, (bx_b + pad, by_b + pad + i * 22))


class Ingrediente:
    
    TAM = 88   

    def __init__(self, x, y, dados):
        self.dados    = dados
        self.inicio_x = x  
        self.inicio_y = y
        self.rect     = pygame.Rect(x, y, self.TAM, self.TAM)
        self.arrastando = False
        self.entregue   = False
        self.sacudindo  = 0   
        self.anim       = random.uniform(0, math.pi * 2)
        self._drag_ox   = 0   
        self._drag_oy   = 0

    def iniciar_arrasto(self, pos):
        self.arrastando = True
        self._drag_ox   = self.rect.x - pos[0]
        self._drag_oy   = self.rect.y - pos[1]

    def mover(self, pos):
        if self.arrastando:
            self.rect.x = pos[0] + self._drag_ox
            self.rect.y = pos[1] + self._drag_oy

    def soltar(self):
        self.arrastando = False
        self.rect.x     = self.inicio_x
        self.rect.y     = self.inicio_y

    def sacudir(self):
        self.sacudindo = 14

    def atualizar(self):
        self.anim += 0.06
        if self.sacudindo > 0:
            self.sacudindo -= 1

    def desenhar(self, tela, fonte_emoji, fonte_nome, mouse_pos):
        if self.entregue:
            s = pygame.Surface((self.TAM, self.TAM), pygame.SRCALPHA)
            pygame.draw.rect(s, (*CINZA, 80), (0, 0, self.TAM, self.TAM), border_radius=18)
            tela.blit(s, (self.inicio_x, self.inicio_y))
            return

        hover   = self.rect.collidepoint(mouse_pos)
        shake_x = random.randint(-3, 3) if self.sacudindo > 0 else 0
        bob_y   = int(math.sin(self.anim) * 4) if not self.arrastando else 0

        r = self.rect.copy()
        r.x += shake_x
        r.y += bob_y

        cor = tuple(min(255, c + 25) for c in self.dados["cor"]) if (hover or self.arrastando) else self.dados["cor"]
        pygame.draw.rect(tela, cor, r, border_radius=20)

        borda = VERMELHO if self.sacudindo > 0 else (LARANJA if self.arrastando else MARROM)
        pygame.draw.rect(tela, borda, r, 3, border_radius=20)

        emoji = fonte_emoji.render(self.dados["emoji"], True, PRETO)
        tela.blit(emoji, emoji.get_rect(centerx=r.centerx, y=r.y + 10))

        nome = fonte_nome.render(self.dados["nome"], True, MARROM_ESC)
        tela.blit(nome, nome.get_rect(centerx=r.centerx, y=r.bottom - 22))

class Tigela:
    
    def __init__(self, cx, cy):
        self.cx   = cx
        self.cy   = cy
        self.raio = 85
        self.rect = pygame.Rect(cx - self.raio, cy - 44, self.raio * 2, self.raio + 54)

        self.ingredientes_adicionados = []
        self.cor_massa  = (240, 215, 170)  
        self.anim       = 0
        self.giros      = 0.0              
        self.angulo_ant = None             
        self.girando    = False

    def receber_ingrediente(self, dados):
        
        self.ingredientes_adicionados.append(dados)
        c = self.cor_massa
        d = dados["cor"]
        self.cor_massa = (
            int(c[0] * 0.65 + d[0] * 0.35),
            int(c[1] * 0.65 + d[1] * 0.35),
            int(c[2] * 0.65 + d[2] * 0.35),
        )

    def calcular_giros(self, pos):
        
        dx   = pos[0] - self.cx
        dy   = pos[1] - self.cy
        dist = math.hypot(dx, dy)

        if 10 < dist < self.raio:
            angulo = math.atan2(dy, dx)
            if self.angulo_ant is not None:
                delta = angulo - self.angulo_ant
                
                if delta >  math.pi: delta -= 2 * math.pi
                if delta < -math.pi: delta += 2 * math.pi
                self.giros += abs(delta)
            self.angulo_ant = angulo
            self.girando    = True
        else:
            self.angulo_ant = None
            self.girando    = False
        return self.giros

    def desenhar(self, tela, fonte_emoji):
        self.anim += 1
        pygame.draw.ellipse(tela, (175, 145, 105),
                            pygame.Rect(self.cx - self.raio + 7, self.cy - 28 + 9,
                                        self.raio * 2 - 14, self.raio + 32))
        
        pygame.draw.ellipse(tela, (220, 195, 160),
                            pygame.Rect(self.cx - self.raio, self.cy - 28,
                                        self.raio * 2, self.raio + 32))

        if self.ingredientes_adicionados:
            altura_massa = min(len(self.ingredientes_adicionados) * 16, self.raio - 12)
            rect_massa   = pygame.Rect(
                self.cx - self.raio + 15,
                self.cy + self.raio - altura_massa - 10,
                (self.raio - 15) * 2,
                altura_massa
            )
            pygame.draw.ellipse(tela, self.cor_massa, rect_massa)

            if self.girando:
                for i in range(6):
                    a  = self.anim * 0.16 + i * math.pi / 3
                    bx = int(self.cx + math.cos(a) * 30)
                    by = int(self.cy + 22 + math.sin(a) * 15)
                    pygame.draw.circle(tela, BRANCO, (bx, by), 4)

        pygame.draw.ellipse(tela, (195, 160, 120),
                            pygame.Rect(self.cx - self.raio, self.cy - 44,
                                        self.raio * 2, 34))
        pygame.draw.ellipse(tela, MARROM,
                            pygame.Rect(self.cx - self.raio, self.cy - 44,
                                        self.raio * 2, 34), 4)

        if self.ingredientes_adicionados:
            fp = pygame.font.SysFont("Arial", 13, bold=True)
            t  = fp.render(f"{len(self.ingredientes_adicionados)}/5 ingredientes", True, MARROM_ESC)
            tela.blit(t, t.get_rect(centerx=self.cx, y=self.cy + self.raio + 6))

class Forno:
    
    LARGURA  = 210
    ALTURA_F = 190

    def __init__(self, cx, cy):
        self.cx   = cx
        self.cy   = cy
        self.rect = pygame.Rect(cx - self.LARGURA // 2, cy - self.ALTURA_F // 2,
                                self.LARGURA, self.ALTURA_F)
        self.tempo_total = 0
        self.tempo_atual = 0.0
        self.ativo       = False
        self.pronto      = False
        self.tem_massa   = False
        self.anim        = 0

    def colocar_massa(self, duracao):
        self.tempo_total = duracao
        self.tempo_atual = 0.0
        self.ativo       = True
        self.pronto      = False
        self.tem_massa   = True

    def atualizar(self, dt):
        self.anim += 1
        if self.ativo and not self.pronto:
            self.tempo_atual += dt
            if self.tempo_atual >= self.tempo_total:
                self.tempo_atual = self.tempo_total
                self.pronto      = True
                self.ativo       = False

    def progresso(self):
        return min(1.0, self.tempo_atual / self.tempo_total) if self.tempo_total else 0.0

    def rect_botao_tirar(self):
        return pygame.Rect(self.cx - 75, self.cy + 88, 150, 36)

    def desenhar(self, tela, fonte):
        cor_forno = (60, 120, 60) if self.pronto else (75, 75, 90)
        pygame.draw.rect(tela, cor_forno, self.rect, border_radius=16)
        pygame.draw.rect(tela, MARROM_ESC, self.rect, 4, border_radius=16)

        janela = pygame.Rect(self.cx - 58, self.cy - 60, 116, 85)
        pygame.draw.rect(tela, (25, 25, 38), janela, border_radius=10)
        pygame.draw.rect(tela, (90, 90, 110), janela, 3, border_radius=10)

        if self.tem_massa:
            p  = self.progresso()
            r2 = int(200 + p * 45)
            g2 = int(155 - p * 70)
            b2 = int(100 - p * 55)
            pygame.draw.ellipse(tela, (min(255, r2), max(0, g2), max(25, b2)),
                                pygame.Rect(self.cx - 40, self.cy - 25, 80, 36))

        cx_m, cy_m = self.cx, self.cy + 58
        raio_m = 30
        pygame.draw.circle(tela, (45, 45, 58), (cx_m, cy_m), raio_m)

        if self.progresso() > 0:
            cor_arco = VERDE if self.pronto else LARANJA
            angulo_0 = -math.pi / 2
            angulo_1 = angulo_0 + 2 * math.pi * self.progresso()
            n_pts    = max(2, int(44 * self.progresso()))
            pts      = [(cx_m, cy_m)]
            for i in range(n_pts + 1):
                a = angulo_0 + (angulo_1 - angulo_0) * i / n_pts
                pts.append((cx_m + raio_m * math.cos(a), cy_m + raio_m * math.sin(a)))
            if len(pts) >= 3:
                pygame.draw.polygon(tela, cor_arco, pts)
        pygame.draw.circle(tela, (95, 95, 112), (cx_m, cy_m), raio_m, 3)

        if self.pronto:
            txt = fonte.render("✅", True, VERDE)
        elif self.ativo:
            txt = fonte.render(str(max(0, int(self.tempo_total - self.tempo_atual))), True, BRANCO)
        else:
            txt = fonte.render("⏱", True, CINZA)
        tela.blit(txt, txt.get_rect(center=(cx_m, cy_m)))

        if self.tem_massa and self.pronto:
            cor_btn = VERDE
            label   = "Tirar do forno!"
        elif self.tem_massa:
            cor_btn = CINZA
            label   = "Assando..."
        else:
            cor_btn = CINZA
            label   = "Aguardando massa..."

        pygame.draw.rect(tela, cor_btn,
                         pygame.Rect(self.cx - 75, self.cy + 88, 150, 36), border_radius=10)
        s = fonte.render(label, True, BRANCO)
        tela.blit(s, s.get_rect(centerx=self.cx, centery=self.cy + 106))

class MassaArrastavel:
    LARGURA_M  = 120
    ALTURA_M   = 50

    def __init__(self, x, y, cor):
        self.rect       = pygame.Rect(x, y, self.LARGURA_M, self.ALTURA_M)
        self.cor        = cor
        self.arrastando = False
        self._drag_ox   = 0
        self._drag_oy   = 0
        self.anim       = 0

    def iniciar_arrasto(self, pos):
        self.arrastando = True
        self._drag_ox   = self.rect.x - pos[0]
        self._drag_oy   = self.rect.y - pos[1]

    def mover(self, pos):
        if self.arrastando:
            self.rect.x = pos[0] + self._drag_ox
            self.rect.y = pos[1] + self._drag_oy

    def atualizar(self):
        self.anim += 1

    def desenhar(self, tela, fonte):
        bob_y = int(math.sin(self.anim * 0.08) * 4) if not self.arrastando else 0
        r     = self.rect.copy()
        r.y  += bob_y

        pygame.draw.ellipse(tela, self.cor, r)
        pygame.draw.ellipse(tela, LARANJA if self.arrastando else MARROM, r, 3)

        txt = fonte.render("Massa pronta! →", True, MARROM_ESC)
        tela.blit(txt, txt.get_rect(center=r.center))


class ItemDecoracao:
   
    TAM = 82

    def __init__(self, x, y, dados):
        self.rect        = pygame.Rect(x, y, self.TAM, self.TAM)
        self.dados       = dados
        self.selecionado = False
        self.anim        = random.uniform(0, math.pi * 2)

    def atualizar(self):
        self.anim += 0.05

    def desenhar(self, tela, fonte_emoji, fonte_nome, mouse_pos):
        bob_y = int(math.sin(self.anim) * 3)
        r     = self.rect.copy()
        r.y  += bob_y

        hover = self.rect.collidepoint(mouse_pos)
        if self.selecionado:
            cor = tuple(min(255, c + 35) for c in self.dados["cor"])
        elif hover:
            cor = tuple(min(255, c + 18) for c in self.dados["cor"])
        else:
            cor = self.dados["cor"]

        pygame.draw.rect(tela, cor, r, border_radius=18)
        borda   = VERDE if self.selecionado else MARROM
        espessura = 4 if self.selecionado else 2
        pygame.draw.rect(tela, borda, r, espessura, border_radius=18)

        emoji = fonte_emoji.render(self.dados["emoji"], True, PRETO)
        tela.blit(emoji, emoji.get_rect(centerx=r.centerx, y=r.y + 8))

        nome = fonte_nome.render(self.dados["nome"], True, MARROM_ESC)
        tela.blit(nome, nome.get_rect(centerx=r.centerx, y=r.bottom - 20))

        if self.selecionado:
            check = fonte_nome.render("✓", True, VERDE)
            tela.blit(check, (r.right - 20, r.y + 4))

class TelaInicial:

    def __init__(self):
        self.anim         = 0
        self.lara         = Lara(120, 340)
        self.lara.falar("Olá! Sou o Lara!\nVamos fazer um bolo? ", 99999)
        self.fonte_titulo = pygame.font.SysFont("Arial", 54, bold=True)
        self.fonte_media  = pygame.font.SysFont("Arial", 22)
        self.fonte_botao  = pygame.font.SysFont("Arial", 26, bold=True)
        self.fonte_peq    = pygame.font.SysFont("Arial", 15)
        self.particulas   = []
        self.ver_recordes = False

        cx = LARGURA // 2
        self.rect_jogar    = pygame.Rect(cx - 120, 455, 240, 58)
        self.rect_recordes = pygame.Rect(cx -  80, 528, 160, 42)
        self.rect_sair     = pygame.Rect(cx -  80, 583, 160, 38)

    def processar(self, evento, pos):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.ver_recordes:
                self.ver_recordes = False
                return None
            if self.rect_jogar.collidepoint(pos):    return "jogo"
            if self.rect_recordes.collidepoint(pos): self.ver_recordes = True
            if self.rect_sair.collidepoint(pos):     return "sair"
        return None

    def atualizar(self, pos):
        self.anim += 1
        self.lara.atualizar()
        if random.random() < 0.18:
            self.particulas.append(Particula(random.randint(0, LARGURA), -10))
        self.particulas = [p for p in self.particulas if p.vida > 0]
        for p in self.particulas:
            p.atualizar()

    def desenhar(self, tela, pos):
        desenhar_fundo_gradiente(tela, (255, 150, 200), (255, 220, 120))
        for p in self.particulas:
            p.desenhar(tela)

        oy = int(math.sin(self.anim * 0.04) * 6)
        t1 = self.fonte_titulo.render("🎂 Bolo do Lara", True, AMARELO)
        t2 = self.fonte_media.render("O melhor prof vai te ajudar a fazer um bolo no menor tempo", True, BRANCO)
        tela.blit(t1, t1.get_rect(centerx=LARGURA // 2, y=52 + oy))
        tela.blit(t2, t2.get_rect(centerx=LARGURA // 2, y=128))

        painel = pygame.Rect(340, 168, 500, 270)
        pygame.draw.rect(tela, (255, 240, 255), painel, border_radius=22)
        pygame.draw.rect(tela, ROSA, painel, 4, border_radius=22)

        th = self.fonte_media.render("Como jogar:", True, VERMELHO)
        tela.blit(th, (360, 183))

        instrucoes = [
            ("🌾 Ingredientes", "Arraste na ordem certa para a tigela"),
            ("🌀 Misture",      "Gire o mouse dentro da tigela"),
            ("🔥 Asse",         "Arraste a massa para o forno"),
            ("🎨 Decore",       "Clique nas decorações e finalize!"),
        ]
        for i, (titulo, desc) in enumerate(instrucoes):
            s1 = self.fonte_media.render(titulo, True, ROXO)
            s2 = self.fonte_peq.render(desc, True, MARROM_ESC)
            tela.blit(s1, (360, 218 + i * 48))
            tela.blit(s2, (360 + s1.get_width() + 8, 225 + i * 48))

        self.lara.desenhar(tela, self.fonte_peq)

        desenhar_botao(tela, self.fonte_botao, self.rect_jogar,    "🎂 JOGAR!",   ROSA,            (200, 40, 140), pos)
        desenhar_botao(tela, self.fonte_peq,   self.rect_recordes, "🏆 Recordes", ROXO,            (130, 30, 200), pos)
        desenhar_botao(tela, self.fonte_peq,   self.rect_sair,     "Sair",        (130, 80, 60),   (100, 60,  40), pos)

        if self.ver_recordes:
            self._desenhar_recordes(tela)

    def _desenhar_recordes(self, tela):
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        tela.blit(overlay, (0, 0))

        painel = pygame.Rect(245, 98, 470, 410)
        pygame.draw.rect(tela, (255, 248, 225), painel, border_radius=22)
        pygame.draw.rect(tela, ROSA, painel, 4, border_radius=22)

        fonte = pygame.font.SysFont("Arial", 17)
        t = fonte.render("🏆 Top 10 Recordes", True, MARROM_ESC)
        tela.blit(t, t.get_rect(centerx=LARGURA // 2, y=116))

        recordes = carregar_recordes()
        medalhas = ["🥇", "🥈", "🥉"]
        for i, rec in enumerate(recordes[:10]):
            medalha = medalhas[i] if i < 3 else f"{i + 1}."
            estrelas = "⭐" * rec.get("estrelas", 0)
            cor_linha = [AMARELO, CINZA, MARROM][i] if i < 3 else MARROM_ESC
            linha = fonte.render(f"{medalha} {rec['nome'][:12]:<12}  {rec['pontuacao']} pts  {estrelas}",
                                  True, cor_linha)
            tela.blit(linha, linha.get_rect(centerx=LARGURA // 2, y=152 + i * 30))

        if not recordes:
            s = fonte.render("Nenhum recorde ainda! Seja o primeiro!", True, CINZA)
            tela.blit(s, s.get_rect(centerx=LARGURA // 2, y=250))

        fechar = self.fonte_peq.render("(clique para fechar)", True, CINZA)
        tela.blit(fechar, fechar.get_rect(centerx=LARGURA // 2, y=480))
class TelaJogo:
    """
    Gerencia as 4 fases do jogo:
      0 = Ingredientes  1 = Misturar  2 = Assar  3 = Decorar
    """
    FASE_INGREDIENTES = 0
    FASE_MISTURAR     = 1
    FASE_ASSAR        = 2
    FASE_DECORAR      = 3

    TIGELA_CX = 400
    TIGELA_CY = 320
    FORNO_CX  = 560  
    FORNO_CY  = 300  

    def __init__(self):
      
        self.fonte_grande = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonte_media  = pygame.font.SysFont("Arial", 19, bold=True)
        self.fonte_peq    = pygame.font.SysFont("Arial", 14)
        self.fonte_emoji  = pygame.font.SysFont("Segoe UI Emoji", 34)
        self.fonte_emoji2 = pygame.font.SysFont("Segoe UI Emoji", 14)

        self.pontuacao   = 0
        self.erros       = 0
        self.bonus_total = 0
        self.fase        = self.FASE_INGREDIENTES
        self.fase_ok     = False       
        self.prox_ing    = 0           
        self.anim        = 0

        self.particulas = []
        self.popups     = []

        self.lara   = Lara(60, 480)
        self.tigela = Tigela(self.TIGELA_CX, self.TIGELA_CY)
        self.forno  = Forno(self.FORNO_CX, self.FORNO_CY)
        self.massa  = None  

        self.giros_alvo = 5 * 2 * math.pi

        self._criar_ingredientes()
        self._criar_decoracoes()
        self._iniciar_timer()

        self.lara.falar("Coloque os ingredientes\nna tigela na ordem certa! 🍳")


    def _criar_ingredientes(self):
        self.sprites = []
        posicoes_y = [140, 235, 330, 430, 525]
        for i, dados in enumerate(INGREDIENTES):
            y = posicoes_y[i] if i < len(posicoes_y) else 140 + i * 95
            self.sprites.append(Ingrediente(90, y, dados))

    def _criar_decoracoes(self):
        self.itens_decoracao = []
        for i, dados in enumerate(DECORACOES):
            self.itens_decoracao.append(ItemDecoracao(190 + i * 155, 430, dados))
        self.rect_finalizar = pygame.Rect(LARGURA // 2 - 110, 535, 220, 50)

    def _iniciar_timer(self):
        cfg = FASES[self.fase]
        self.tempo_total     = cfg["tempo"]
        self.tempo_restante  = cfg["tempo"]
        self.tempo_notificou = False  

    def _adicionar_popup(self, x, y, texto, cor=VERDE, tamanho=22):
        self.popups.append(Popup(x, y, texto, cor, tamanho))

    def _penalizar(self, mensagem, x=470, y=300):
        self.pontuacao = max(0, self.pontuacao - PENALIDADE_ERRO)
        self.erros    += 1
        self._adicionar_popup(x, y, f"-{PENALIDADE_ERRO} {mensagem}", VERMELHO, 24)
        self.lara.falar(random.choice([
            "Ordem errada!😱",
            "Cuidado! Siga a receita! ",
            "Ops! Perdeu pontos! ",
        ]))

    def _concluir_fase(self):
        self.fase_ok = True
        cfg = FASES[self.fase]

        pts_fase = 0 if self.fase == self.FASE_INGREDIENTES else cfg["pontos"]

        bonus_fase = int(cfg["bonus"] * (self.tempo_restante / self.tempo_total))

        self.pontuacao   += pts_fase + bonus_fase
        self.bonus_total += bonus_fase

        for _ in range(40):
            self.particulas.append(Particula(LARGURA // 2, ALTURA // 2))

        total_somado = pts_fase + bonus_fase
        msg = f"+{total_somado} pts" if total_somado > 0 else "Fase concluída!"
        if bonus_fase > 0:
            msg += f" (⚡+{bonus_fase} bônus)"
        self._adicionar_popup(LARGURA // 2, 190, msg, VERDE, 26)

        falas = {
            0: ["Todos os ingredientes! 🎉", "Perfeito! Continue!"],
            1: ["Massa misturada! 🌀", "Que velocidade!"],
            2: ["Bolo assado! 🔥", "Cheiroso! Incrível!"],
            3: ["Bolo decorado! 🎨", "Obra de arte! 🏆"],
        }
        self.lara.falar(random.choice(falas.get(self.fase, ["Muito bem!"])))

    def _avancar_fase(self):
        self.fase   += 1
        self.fase_ok = False
        self._iniciar_timer()

        if self.fase == self.FASE_MISTURAR:
            self.tigela.giros     = 0.0
            self.tigela.angulo_ant = None
            self.lara.falar("Agora gire o mouse na tigela\npara misturar! 🌀")

        elif self.fase == self.FASE_ASSAR:
            self.massa = MassaArrastavel(
                self.TIGELA_CX - 60,
                self.TIGELA_CY - 25,
                self.tigela.cor_massa
            )
            self.lara.falar("Arraste a massa para o forno\ne espere assar! 🔥")

        elif self.fase == self.FASE_DECORAR:
            self.lara.falar("Decore o bolo! Escolha o que\nquiser e finalize! 🎨")

    def processar(self, evento, pos):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            # Botão "Próximo passo" (aparece após concluir a fase)
            if self.fase_ok:
                if self.fase >= 3:
                    return "final"
                btn_prox = pygame.Rect(LARGURA // 2 - 115, ALTURA - 72, 230, 50)
                if btn_prox.collidepoint(pos):
                    self._avancar_fase()
                return None

            if self.fase == self.FASE_INGREDIENTES:
                for spr in self.sprites:
                    if spr.rect.collidepoint(pos) and not spr.entregue:
                        spr.iniciar_arrasto(pos)
                        break

            elif self.fase == self.FASE_ASSAR:
                if self.massa and not self.forno.tem_massa:
                    if self.massa.rect.collidepoint(pos):
                        self.massa.iniciar_arrasto(pos)
                elif self.forno.tem_massa and self.forno.pronto:
                    if self.forno.rect_botao_tirar().collidepoint(pos):
                        self._concluir_fase()

            elif self.fase == self.FASE_DECORAR:
                for item in self.itens_decoracao:
                    if item.rect.collidepoint(pos):
                        item.selecionado = not item.selecionado
                if self.rect_finalizar.collidepoint(pos):
                    if any(d.selecionado for d in self.itens_decoracao):
                        self._concluir_fase()
                    else:
                        self._penalizar("Escolha pelo menos 1 decoração!", LARGURA // 2, 380)

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:

            if self.fase == self.FASE_INGREDIENTES:
                for i, spr in enumerate(self.sprites):
                    if spr.arrastando:
                        if spr.rect.colliderect(self.tigela.rect):
                            if i == self.prox_ing:
                                # Ingrediente correto!
                                spr.entregue   = True
                                spr.arrastando = False
                                spr.rect.x     = spr.inicio_x
                                spr.rect.y     = spr.inicio_y
                                self.tigela.receber_ingrediente(spr.dados)
                                self.prox_ing += 1
                                self.pontuacao += 20
                                self._adicionar_popup(self.TIGELA_CX, self.TIGELA_CY - 50, "+20 pts", TURQUESA)
                                if self.prox_ing == len(INGREDIENTES):
                                    self._concluir_fase()
                                else:
                                    prox_nome = INGREDIENTES[self.prox_ing]["nome"]
                                    self.lara.falar(f"Ótimo! Agora o(a)\n{prox_nome}! 👍")
                            else:
                                # Ingrediente errado!
                                spr.soltar()
                                spr.sacudir()
                                self._penalizar("ordem errada!", self.TIGELA_CX, self.TIGELA_CY)
                        else:
                            spr.soltar()
                        break

            elif self.fase == self.FASE_ASSAR and self.massa and not self.forno.tem_massa:
                if self.massa.arrastando:
                    if self.massa.rect.colliderect(self.forno.rect):
                        self.forno.colocar_massa(8)
                        self.massa = None
                        self.lara.falar("Bolo no forno! 🔥\nEspere assar!")
                    else:
                        self.massa.arrastando = False
                        self._penalizar("Leve até o forno!", self.FORNO_CX, self.FORNO_CY)

        elif evento.type == pygame.MOUSEMOTION:
            if self.fase == self.FASE_INGREDIENTES:
                for spr in self.sprites:
                    if spr.arrastando:
                        spr.mover(pos)
            elif self.fase == self.FASE_ASSAR and self.massa:
                self.massa.mover(pos)

        return None

    def atualizar(self, pos, dt):
        self.anim += 1
        self.lara.atualizar()

        if not self.fase_ok:
            self.tempo_restante = max(0.0, self.tempo_restante - dt)
            if self.tempo_restante <= 0 and not self.tempo_notificou:
                self.tempo_notificou = True
                self.pontuacao = max(0, self.pontuacao - PENALIDADE_TEMPO)
                self.erros    += 1
                self._adicionar_popup(LARGURA // 2, 175, f"-{PENALIDADE_TEMPO} TEMPO ESGOTADO!", VERMELHO, 26)
                self.lara.falar("Tempo esgotado! ⏰\nContinue mesmo assim!")

        self.particulas = [p for p in self.particulas if p.vida > 0]
        for p in self.particulas:
            p.atualizar()
        self.popups = [p for p in self.popups if p.vida > 0]
        for p in self.popups:
            p.atualizar()

        if self.fase == self.FASE_INGREDIENTES:
            for spr in self.sprites:
                spr.atualizar()

        elif self.fase == self.FASE_MISTURAR and not self.fase_ok:
            giros = self.tigela.calcular_giros(pos)
            if giros >= self.giros_alvo:
                self._concluir_fase()

        elif self.fase == self.FASE_ASSAR:
            self.forno.atualizar(dt)
            if self.massa:
                self.massa.atualizar()

        elif self.fase == self.FASE_DECORAR:
            for item in self.itens_decoracao:
                item.atualizar()

    def desenhar(self, tela, pos):
        fundos = [
            (255, 232, 170),   
            (170, 255, 210),   
            (255, 195, 130),   
            (215, 165, 255),   
        ]
        cores_header = [(255, 50, 110), (20, 175, 115), (215, 75, 0), (135, 25, 215)]
        cores_rodape = [(255, 135, 50), (25, 185, 125), (255, 95, 25), (155, 55, 225)]

        tela.fill(fundos[self.fase])

        pygame.draw.rect(tela, cores_header[self.fase], pygame.Rect(0, 0, LARGURA, 82))
        pygame.draw.rect(tela, tuple(max(0, c - 45) for c in cores_header[self.fase]),
                         pygame.Rect(0, 80, LARGURA, 4))

        pygame.draw.rect(tela, cores_rodape[self.fase], pygame.Rect(0, ALTURA - 55, LARGURA, 55))

        nomes = ["🌾 Ingredientes", "🌀 Misturar", "🔥 Assar", "🎨 Decorar"]
        tf = self.fonte_grande.render(nomes[self.fase], True, BRANCO)
        tela.blit(tf, tf.get_rect(centerx=LARGURA // 2 - 60, y=14))

        self._desenhar_hud(tela)
        self._desenhar_receita(tela)

        if self.fase == self.FASE_INGREDIENTES:
            self._desenhar_fase_ingredientes(tela, pos)
        elif self.fase == self.FASE_MISTURAR:
            self._desenhar_fase_misturar(tela)
        elif self.fase == self.FASE_ASSAR:
            self._desenhar_fase_assar(tela, pos)
        elif self.fase == self.FASE_DECORAR:
            self._desenhar_fase_decorar(tela, pos)

        for p in self.particulas:
            p.desenhar(tela)
        for p in self.popups:
            p.desenhar(tela)

        self.lara.desenhar(tela, self.fonte_peq)

        if self.fase_ok:
            label = "Ver resultado! 🎂" if self.fase >= 3 else "Próximo passo ➡"
            rect_btn = pygame.Rect(LARGURA // 2 - 115, ALTURA - 72, 230, 50)
            desenhar_botao(tela, self.fonte_media, rect_btn, label, LARANJA, (200, 80, 0), pos)
            ok = self.fonte_media.render("✅ Fase concluída!", True, VERDE)
            tela.blit(ok, ok.get_rect(centerx=LARGURA // 2, y=ALTURA - 108))

    def _desenhar_hud(self, tela):
        pts = self.fonte_media.render(f"⭐ {self.pontuacao} pts", True, BRANCO)
        tela.blit(pts, (LARGURA - 320, 10))
        if self.erros > 0:
            er = self.fonte_peq.render(f"❌ {self.erros} erro(s)", True, AMARELO)
            tela.blit(er, (LARGURA - 320, 34))
        if not self.fase_ok:
            desenhar_barra_tempo(tela, self.fonte_peq,
                                 self.tempo_restante, self.tempo_total,
                                 LARGURA - 210, 10, 200)

    def _desenhar_receita(self, tela):
        rx, ry, rw, rh = LARGURA - 198, 88, 188, 310
        s = pygame.Surface((rw, rh), pygame.SRCALPHA)
        s.fill((255, 252, 240, 215))
        tela.blit(s, (rx, ry))
        pygame.draw.rect(tela, LARANJA, pygame.Rect(rx, ry, rw, rh), 3, border_radius=12)

        fonte_t = pygame.font.SysFont("Arial", 13, bold=True)
        fonte_i = pygame.font.SysFont("Arial", 12)
        t = fonte_t.render("📋 Receita", True, MARROM_ESC)
        tela.blit(t, t.get_rect(centerx=rx + rw // 2, y=ry + 6))
        pygame.draw.line(tela, MARROM, (rx + 8, ry + 22), (rx + rw - 8, ry + 22), 1)

        itens_receita = [
            ("🌾", "Farinha"), ("🍬", "Açúcar"), ("🥚", "Ovos"),
            ("🧈", "Manteiga"), ("🥛", "Leite"),
            ("🌀", "Misturar"), ("🔥", "Assar"), ("🎨", "Decorar"),
        ]

        concluidos = set()
        if self.fase > self.FASE_INGREDIENTES:
            for j in range(5): concluidos.add(j)
        if self.fase > self.FASE_MISTURAR: concluidos.add(5)
        if self.fase > self.FASE_ASSAR:    concluidos.add(6)
        if self.fase == self.FASE_INGREDIENTES:
            for j in range(self.prox_ing): concluidos.add(j)

        atuais = {
            self.FASE_INGREDIENTES: set(range(5)),
            self.FASE_MISTURAR:     {5},
            self.FASE_ASSAR:        {6},
            self.FASE_DECORAR:      {7},
        }.get(self.fase, set())

        for i, (emoji, label) in enumerate(itens_receita):
            py = ry + 28 + i * 35

            if i in atuais:
                pygame.draw.rect(tela, (255, 238, 100),
                                 pygame.Rect(rx + 4, py - 2, rw - 8, 30), border_radius=7)
                pygame.draw.rect(tela, LARANJA,
                                 pygame.Rect(rx + 4, py - 2, rw - 8, 30), 2, border_radius=7)

            cor_check = VERDE if i in concluidos else (AMARELO if i in atuais else CINZA)
            pygame.draw.circle(tela, cor_check, (rx + 13, py + 11), 7)
            mk = fonte_i.render("✓" if i in concluidos else str(i + 1), True, BRANCO)
            tela.blit(mk, mk.get_rect(center=(rx + 13, py + 11)))

            e = self.fonte_emoji2.render(emoji, True, PRETO)
            tela.blit(e, (rx + 24, py + 3))

            cor_texto = CINZA if i in concluidos else (MARROM if i in atuais else MARROM_ESC)
            ns = fonte_i.render(label, True, cor_texto)
            tela.blit(ns, (rx + 44, py + 8))
            if i in concluidos:
                pygame.draw.line(tela, CINZA, (rx + 44, py + 14),
                                 (rx + 44 + ns.get_width(), py + 14), 1)

    def _desenhar_fase_ingredientes(self, tela, pos):
        if self.prox_ing < len(INGREDIENTES):
            nome_prox = INGREDIENTES[self.prox_ing]["nome"]
            lbl = self.fonte_media.render(f"👉 Próximo: {nome_prox}", True, MARROM_ESC)
            tela.blit(lbl, lbl.get_rect(centerx=self.TIGELA_CX, y=120))

        for spr in self.sprites:
            spr.desenhar(tela, self.fonte_emoji, self.fonte_peq, pos)

        ox = int(math.sin(self.anim * 0.09) * 9)
        seta = self.fonte_grande.render("→", True, MARROM)
        tela.blit(seta, (190 + ox, self.TIGELA_CY - 16))

        self.tigela.desenhar(tela, self.fonte_emoji)

    def _desenhar_fase_misturar(self, tela):
        self.tigela.desenhar(tela, self.fonte_emoji)

        pct = min(1.0, self.tigela.giros / self.giros_alvo)
        bx  = self.TIGELA_CX - 105
        by  = ALTURA - 118
        pygame.draw.rect(tela, CINZA,    pygame.Rect(bx, by, 210, 24), border_radius=12)
        pygame.draw.rect(tela, TURQUESA, pygame.Rect(bx, by, int(210 * pct), 24), border_radius=12)
        pygame.draw.rect(tela, MARROM,   pygame.Rect(bx, by, 210, 24), 2, border_radius=12)
        lb = self.fonte_peq.render(f"Misturando: {int(pct * 100)}%", True, MARROM_ESC)
        tela.blit(lb, lb.get_rect(centerx=self.TIGELA_CX, y=by + 28))

        ang = self.anim * 0.11
        for i in range(9):
            a   = ang + i * math.pi / 4.5
            bx2 = int(self.TIGELA_CX + math.cos(a) * 54)
            by2 = int(self.TIGELA_CY + 20 + math.sin(a) * 26)
            s   = pygame.Surface((13, 13), pygame.SRCALPHA)
            alpha = int(255 * (1 - i / 9))
            pygame.draw.circle(s, (*MARROM, alpha), (6, 6), 6)
            tela.blit(s, (bx2 - 6, by2 - 6))

    def _desenhar_fase_assar(self, tela, pos):
        self.forno.desenhar(tela, self.fonte_peq)
        if self.massa and not self.forno.tem_massa:
            self.massa.desenhar(tela, self.fonte_peq)
            # Seta animada apontando do centro para o forno
            ox = int(math.sin(self.anim * 0.09) * 8)
            seta = self.fonte_grande.render("→", True, MARROM)
            tela.blit(seta, (self.TIGELA_CX + 70 + ox, self.FORNO_CY - 10))

    def _desenhar_fase_decorar(self, tela, pos):
        self._desenhar_bolo(tela, LARGURA // 2 - 60, 220)
        for item in self.itens_decoracao:
            item.desenhar(tela, self.fonte_emoji, self.fonte_peq, pos)
        if not self.fase_ok:
            desenhar_botao(tela, self.fonte_peq, self.rect_finalizar,
                           "✅ Finalizar Bolo!", VERDE, (20, 170, 60), pos)

    def _desenhar_bolo(self, tela, cx, cy):
        # Camadas do bolo
        pygame.draw.ellipse(tela, (175, 115, 50), pygame.Rect(cx - 82, cy + 32, 164, 46))
        pygame.draw.rect(tela,    (175, 115, 50), pygame.Rect(cx - 82, cy,      164, 46))
        pygame.draw.ellipse(tela, (215, 155, 82), pygame.Rect(cx - 82, cy - 14, 164, 36))
        pygame.draw.ellipse(tela, ( 65,  38, 12), pygame.Rect(cx - 80, cy - 16, 160, 32))

        for gx in range(-62, 72, 25):
            pygame.draw.ellipse(tela, (65, 38, 12),
                                pygame.Rect(cx + gx - 9, cy + 2, 18, 22))

        selecionados = [d for d in self.itens_decoracao if d.selecionado]
        for i, item in enumerate(selecionados):
            offset = -55 + i * 36
            e = self.fonte_emoji.render(item.dados["emoji"], True, PRETO)
            tela.blit(e, e.get_rect(centerx=cx + offset, y=cy - 32))

        pygame.draw.rect(tela, (242, 232, 78), pygame.Rect(cx - 5, cy - 44, 10, 28))
        chama_y = int(math.sin(self.anim * 0.16) * 2)
        pygame.draw.ellipse(tela, (255, 138, 0),   pygame.Rect(cx - 7, cy - 58 + chama_y, 14, 20))
        pygame.draw.ellipse(tela, (255, 242, 100), pygame.Rect(cx - 5, cy - 54 + chama_y,  9, 14))

class TelaNome:
    def __init__(self, pontuacao, estrelas):
        self.pontuacao  = pontuacao
        self.estrelas   = estrelas
        self.nome       = ""
        self.anim       = 0
        self.cursor     = 0     # pisca o cursor de texto
        self.fonte_g    = pygame.font.SysFont("Arial", 36, bold=True)
        self.fonte_m    = pygame.font.SysFont("Arial", 24)
        self.fonte_p    = pygame.font.SysFont("Arial", 18)
        self.rect_salvar = pygame.Rect(LARGURA // 2 - 90, 400, 180, 52)
        self.particulas = [Particula(random.randint(0, LARGURA), random.randint(0, ALTURA))
                           for _ in range(40)]

    def processar(self, evento, pos):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and self.nome.strip():
                return self._salvar()
            elif evento.key == pygame.K_BACKSPACE:
                self.nome = self.nome[:-1]
            elif evento.unicode.isprintable() and len(self.nome) < 16:
                self.nome += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_salvar.collidepoint(pos) and self.nome.strip():
                return self._salvar()
        return None

    def _salvar(self):
        salvar_recorde(self.nome.strip(), self.pontuacao, self.estrelas)
        return "final_exibir"

    def atualizar(self, pos):
        self.anim   += 1
        self.cursor  = (self.cursor + 1) % 60
        self.particulas = [p for p in self.particulas if p.vida > 0]
        for p in self.particulas:
            p.atualizar()
        if random.random() < 0.2:
            self.particulas.append(Particula(random.randint(0, LARGURA), 0))

    def desenhar(self, tela, pos):
        desenhar_fundo_gradiente(tela, (255, 150, 200), (255, 220, 120))
        for p in self.particulas:
            p.desenhar(tela)

        t1 = self.fonte_g.render("🏆 Novo Recorde!", True, AMARELO)
        t2 = self.fonte_m.render(f"Pontuação: {self.pontuacao} pts  {'⭐' * self.estrelas}", True, BRANCO)
        t3 = self.fonte_p.render("Digite seu nome:", True, BRANCO)
        tela.blit(t1, t1.get_rect(centerx=LARGURA // 2, y=130))
        tela.blit(t2, t2.get_rect(centerx=LARGURA // 2, y=192))
        tela.blit(t3, t3.get_rect(centerx=LARGURA // 2, y=260))

        caixa = pygame.Rect(LARGURA // 2 - 165, 287, 330, 54)
        pygame.draw.rect(tela, BRANCO, caixa, border_radius=14)
        pygame.draw.rect(tela, LARANJA, caixa, 3, border_radius=14)
        txt_cursor = self.nome + ("|" if self.cursor < 30 else "")
        s = self.fonte_m.render(txt_cursor, True, PRETO)
        tela.blit(s, s.get_rect(centery=caixa.centery, x=caixa.x + 14))

        desenhar_botao(tela, self.fonte_m, self.rect_salvar, "✅ Salvar!", VERDE, (20, 170, 60), pos)

class TelaFinal:
    def __init__(self, pontuacao, erros, bonus):
        self.pontuacao = pontuacao
        self.erros     = erros
        self.bonus     = bonus
        self.anim      = 0
        self.fonte_g   = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_m   = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonte_n   = pygame.font.SysFont("Arial", 19)
        self.fonte_p   = pygame.font.SysFont("Arial", 14)

        PONTOS_MAXIMOS = 850
        pct           = min(100, int(pontuacao / PONTOS_MAXIMOS * 100))
        self.estrelas = min(5, round(pct / 20))
        self.pct      = pct

        if pct >= 90:   self.mensagem = "INCRÍVEL! Mestre da confeitaria! 🏆"
        elif pct >= 70: self.mensagem = "Muito Bem! Bolo perfeito! 🎉"
        elif pct >= 50: self.mensagem = "Quase lá! Próximo vai! 👍"
        elif pct >= 30: self.mensagem = "Continue praticando! 😄"
        else:           self.mensagem = "Não desista! 💪"

        self.lara = Lara(110, 315)
        self.lara.falar(f"Parabéns! {self.estrelas} estrela(s)!\n{self.mensagem}", 99999)

        cx = LARGURA // 2
        self.rect_novo   = pygame.Rect(cx - 210, 570, 220, 50)
        self.rect_rank   = pygame.Rect(cx +  20, 570, 170, 50)
        self.particulas  = [Particula(random.randint(0, LARGURA), random.randint(0, ALTURA))
                            for _ in range(65)]
        self.ver_recordes = False

    def processar(self, evento, pos):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.ver_recordes:
                self.ver_recordes = False
                return None
            if self.rect_novo.collidepoint(pos):  return "reiniciar"
            if self.rect_rank.collidepoint(pos):  self.ver_recordes = True
        return None

    def atualizar(self, pos):
        self.anim += 1
        self.lara.atualizar()
        self.particulas = [p for p in self.particulas if p.vida > 0]
        for p in self.particulas:
            p.atualizar()
        if random.random() < 0.3:
            self.particulas.append(Particula(random.randint(0, LARGURA), 0))

    def desenhar(self, tela, pos):
        desenhar_fundo_gradiente(tela, (255, 240, 200), (255, 180, 120))
        for p in self.particulas:
            p.desenhar(tela)
        oy = int(math.sin(self.anim * 0.04) * 5)
        self._desenhar_bolo(tela, LARGURA // 2, 120 + oy)

        t1 = self.fonte_g.render("🎂 Bolo Pronto!", True, VERMELHO)
        t2 = self.fonte_m.render(self.mensagem, True, MARROM)
        tela.blit(t1, t1.get_rect(centerx=LARGURA // 2, y=248))
        tela.blit(t2, t2.get_rect(centerx=LARGURA // 2, y=302))

        # Painel de pontuação
        painel = pygame.Rect(LARGURA // 2 - 225, 338, 450, 115)
        pygame.draw.rect(tela, (255, 248, 220), painel, border_radius=16)
        pygame.draw.rect(tela, LARANJA, painel, 3, border_radius=16)

        penalidade = self.erros * PENALIDADE_ERRO
        total_base = 100 + sum(f["pontos"] for f in FASES[1:])
        colunas = [
            ("⭐ Pontos base", f"{total_base} pts",                  MARROM_ESC),
            ("⚡ Bônus vel.",  f"+{self.bonus} pts",                 VERDE),
            ("❌ Penalidades", f"-{penalidade} pts",                 VERMELHO),
            ("🏆 TOTAL",      f"{self.pontuacao} pts ({self.pct}%)", MARROM),
        ]
        for i, (label, valor, cor) in enumerate(colunas):
            lx = LARGURA // 2 - 205 + (i % 2) * 230
            ly = 350 + (i // 2) * 42
            tela.blit(self.fonte_p.render(label, True, CINZA),  (lx, ly))
            tela.blit(self.fonte_n.render(valor, True, cor),    (lx, ly + 16))

        desenhar_estrelas(tela, LARGURA // 2, 466, self.estrelas, self.anim)

        self.lara.desenhar(tela, self.fonte_p)
        desenhar_botao(tela, self.fonte_n, self.rect_novo,  "🔄 Jogar Novamente!", ROSA,  (200, 40, 140), pos)
        desenhar_botao(tela, self.fonte_p, self.rect_rank,  "🏆 Recordes",         ROXO,  (130, 30, 200), pos)

        if self.ver_recordes:
            self._desenhar_recordes(tela)

    def _desenhar_bolo(self, tela, cx, cy):
        pygame.draw.ellipse(tela, (168, 108, 48), pygame.Rect(cx - 76, cy + 28, 152, 44))
        pygame.draw.rect(tela,    (168, 108, 48), pygame.Rect(cx - 76, cy,      152, 44))
        pygame.draw.ellipse(tela, (205, 145, 76), pygame.Rect(cx - 76, cy - 13, 152, 33))
        pygame.draw.ellipse(tela, ( 58,  33, 11), pygame.Rect(cx - 74, cy - 15, 148, 29))
        for gx in range(-56, 66, 23):
            pygame.draw.ellipse(tela, (58, 33, 11),
                                pygame.Rect(cx + gx - 8, cy, 16, 18))
        for mx in [-42, 0, 42]:
            pygame.draw.circle(tela, (200, 38, 58), (cx + mx, cy - 21), 11)
            pygame.draw.line(tela,   (45, 138, 45), (cx + mx, cy - 31), (cx + mx + 4, cy - 42), 3)
        pygame.draw.rect(tela, (240, 230, 78), pygame.Rect(cx - 5, cy - 50, 9, 29))
        chama_y = int(math.sin(self.anim * 0.18) * 3)
        pygame.draw.ellipse(tela, (255, 138, 0),   pygame.Rect(cx - 7, cy - 66 + chama_y, 14, 20))
        pygame.draw.ellipse(tela, (255, 242, 100), pygame.Rect(cx - 5, cy - 62 + chama_y,  9, 14))

    def _desenhar_recordes(self, tela):
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        tela.blit(overlay, (0, 0))
        p = pygame.Rect(245, 98, 470, 410)
        pygame.draw.rect(tela, (255, 248, 225), p, border_radius=22)
        pygame.draw.rect(tela, ROSA, p, 4, border_radius=22)
        fi = pygame.font.SysFont("Arial", 17)
        t  = fi.render("🏆 Top 10 Recordes", True, MARROM_ESC)
        tela.blit(t, t.get_rect(centerx=LARGURA // 2, y=116))
        recordes = carregar_recordes()
        medalhas = ["🥇", "🥈", "🥉"]
        for i, rec in enumerate(recordes[:10]):
            m = medalhas[i] if i < 3 else f"{i + 1}."
            e = "⭐" * rec.get("estrelas", 0)
            cor_l = [AMARELO, CINZA, MARROM][i] if i < 3 else MARROM_ESC
            l = fi.render(f"{m} {rec['nome'][:12]:<12}  {rec['pontuacao']} pts  {e}", True, cor_l)
            tela.blit(l, l.get_rect(centerx=LARGURA // 2, y=152 + i * 30))
        if not recordes:
            s = fi.render("Nenhum recorde ainda!", True, CINZA)
            tela.blit(s, s.get_rect(centerx=LARGURA // 2, y=250))
        f2 = self.fonte_p.render("(clique para fechar)", True, CINZA)
        tela.blit(f2, f2.get_rect(centerx=LARGURA // 2, y=480))

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela  = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()

        self._pts     = 0
        self._erros   = 0
        self._bonus   = 0
        self._estrelas = 0

        self._ir_para("inicial")

    def _ir_para(self, estado):
        self.estado = estado
        if estado == "inicial":
            self.cena = TelaInicial()
        elif estado == "jogo":
            self.cena = TelaJogo()
        elif estado == "inserir_nome":
            self.cena = TelaNome(self._pts, self._estrelas)
        elif estado == "final":
            self.cena = TelaFinal(self._pts, self._erros, self._bonus)

    def rodar(self):
        while True:
            dt  = self.clock.tick(FPS) / 1000.0 
            pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                resultado = self.cena.processar(evento, pos)

                if resultado == "jogo":
                    self._ir_para("jogo")
                elif resultado == "final":
                    self._pts      = self.cena.pontuacao
                    self._erros    = self.cena.erros
                    self._bonus    = self.cena.bonus_total
                    pct            = min(100, int(self._pts / 2000 * 100))
                    self._estrelas = min(5, round(pct / 20))
                    self._ir_para("inserir_nome")
                elif resultado == "final_exibir":
                    self._ir_para("final")
                elif resultado == "reiniciar":
                    self._ir_para("jogo")
                elif resultado == "sair":
                    pygame.quit()
                    sys.exit()

            if self.estado == "jogo":
                self.cena.atualizar(pos, dt)
            else:
                self.cena.atualizar(pos)

            self.cena.desenhar(self.tela, pos)
            pygame.display.flip()

if __name__ == "__main__":
    Jogo().rodar()
