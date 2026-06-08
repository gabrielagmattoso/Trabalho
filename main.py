import pygame
import sys

TELA_LARGURA = 800
TELA_ALTURA = 600
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)

def desenhar_elementos(tela, retangulo_farinha):
    tela.fill(BRANCO)
    pygame.draw.rect(tela, AZUL, retangulo_farinha)
    pygame.display.flip()

def verificar_clique(pos_mouse, retangulo_farinha):
    if retangulo_farinha.collidepoint(pos_mouse):
        print("Acertou! Você clicou na farinha.")
    else:
        print("Errou! Clique fora da área do ingrediente.")

def main():
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Bolo da Lara - Protótipo")

    retangulo_farinha = pygame.Rect(350, 250, 100, 100)

    rodando = True
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicao_mouse = pygame.mouse.get_pos()
                    verificar_clique(posicao_mouse, retangulo_farinha)

        desenhar_elementos(tela, retangulo_farinha)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
