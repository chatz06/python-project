import pygame, sys
from button import Button

pygame.init()

# Παίρνουμε την ανάλυση της οθόνης
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Ορίζουμε την ανάλυση της οθόνης για το full screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")

# Φορτώνουμε το background και προσαρμόζουμε το μέγεθός του στην ανάλυση της οθόνης
BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Κλιμακώνουμε την εικόνα στο μέγεθος της οθόνης

# Φορτώνουμε άλλες εικόνες και τις κλιμακώνουμε αναλόγως
play_button_image = pygame.image.load("assets/Play Rect.png")
play_button_image = pygame.transform.scale(play_button_image, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 10))  # Κλιμακώνουμε το κουμπί

quit_button_image = pygame.image.load("assets/Quit Rect.png")
quit_button_image = pygame.transform.scale(quit_button_image, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 10))  # Κλιμακώνουμε το κουμπί

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        from marathon import marathon
        #PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        #PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        #SCREEN.blit(PLAY_TEXT, PLAY_RECT)
    
               
        PLAY_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
                    
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                      
        pygame.display.update()
    

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Ενημερώνουμε τα κουμπιά με τις κλιμακωμένες εικόνες
        PLAY_BUTTON = Button(image=play_button_image, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), 
                            text_input="PLAY", font=get_font(75), base_color="#ffffff", hovering_color="Black")
       
        QUIT_BUTTON = Button(image=quit_button_image, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), 
                            text_input="QUIT", font=get_font(75), base_color="#ffffff", hovering_color="Black")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
