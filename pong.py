import pygame
import random

# Initialisera pygame
pygame.init()

# Skärminställningar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pingis med strategiska racketar!")

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Spelvariabler
ball_speed_x = 7
ball_speed_y = 7
ball_radius = 10
racket_width = 15
racket_height = 100
player1_score = 0
player2_score = 0
player1_hits = 0
player2_hits = 0
player1_money = 0
player2_money = 0
max_hits = 3
max_money = 5
winning_score = 3  # För att vinna krävs det 3 poäng
server = 1  # Den spelare som serverar (1 = Player 1, 2 = Player 2)
ball_served = False  # Om bollen är serverad än eller inte

# Skapa spelobjekt
ball = pygame.Rect(screen_width // 2 - ball_radius, screen_height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
player1_racket = pygame.Rect(30, screen_height // 2 - racket_height // 2, racket_width, racket_height)
player2_racket = pygame.Rect(screen_width - 30 - racket_width, screen_height // 2 - racket_height // 2, racket_width, racket_height)
coin = pygame.Rect(random.randint(100, screen_width - 100), random.randint(100, screen_height - 100), 20, 20)

# Racket växthantering
growth_amount = 10  # Mängd racketväxt per gång

# Funktioner för att spela
def move_ball():
    global ball_speed_x, ball_speed_y, player1_hits, player2_hits, player1_money, player2_money, player1_score, player2_score, server, ball_served

    # Om bollen inte har serverats, vänta på att spelaren trycker space för att serva
    if not ball_served:
        return

    # Flytta bollen
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Boll träffar väggar
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Boll träffar racketarna
    if ball.colliderect(player1_racket):
        ball_speed_x *= -1
        player1_hits += 1
        ball_speed_x, ball_speed_y = handle_racket_hit(player1_racket, ball)
        increase_ball_speed()

    if ball.colliderect(player2_racket):
        ball_speed_x *= -1
        player2_hits += 1
        ball_speed_x, ball_speed_y = handle_racket_hit(player2_racket, ball)
        increase_ball_speed()

    # Om bollen går utanför planen
    if ball.left <= 0:
        player2_score += 1
        server = 2  # Player 2 får serva nästa gång
        reset_ball()
    elif ball.right >= screen_width:
        player1_score += 1
        server = 1  # Player 1 får serva nästa gång
        reset_ball()

    # Samla på pengarna
    if ball.colliderect(coin):
        coin.x = random.randint(100, screen_width - 100)
        coin.y = random.randint(100, screen_height - 100)
        if ball_speed_x > 0:
            player1_money += 1
            grow_racket(1)  # Player 1 växer racketen varje gång den träffar en peng
        else:
            player2_money += 1
            grow_racket(2)  # Player 2 växer racketen varje gång den träffar en peng

def handle_racket_hit(racket, ball):
    """Hantera hur bollen reagerar beroende på träffpunkten på racketen."""
    racket_center = racket.centery
    ball_center = ball.centery
    racket_top = racket.top
    racket_bottom = racket.bottom

    # Beräkna träffens relativa position på racketen
    hit_position = (ball_center - racket_center) / (racket_height / 2)  # Ger ett värde mellan -1 och 1

    # Justera bollens hastighet beroende på var den träffade racketen
    max_angle = 8  # Maximal vinkel vid träff på racketens kant
    ball_speed_y = hit_position * max_angle

    # Retur av nya bollhastigheter
    return ball_speed_x, ball_speed_y

def grow_racket(player):
    """Funktion för att växa racketen för spelaren som samlar på pengen."""
    global player1_racket, player2_racket

    if player == 1:
        player1_racket.height += growth_amount  # Väx racketen varje gång bollen träffar en peng
    elif player == 2:
        player2_racket.height += growth_amount  # Väx racketen varje gång bollen träffar en peng

def reset_ball():
    global ball_speed_x, ball_speed_y, ball_served
    ball_served = False  # Bollen är inte serverad än

def handle_player_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_racket.top > 0:
        player1_racket.y -= 10
    if keys[pygame.K_s] and player1_racket.bottom < screen_height:
        player1_racket.y += 10

    if keys[pygame.K_UP] and player2_racket.top > 0:
        player2_racket.y -= 10
    if keys[pygame.K_DOWN] and player2_racket.bottom < screen_height:
        player2_racket.y += 10

    # Om bollen inte har serverats ännu och space trycks, serva bollen
    if keys[pygame.K_SPACE] and not ball_served:
        serve_ball()

def serve_ball():
    global ball_speed_x, ball_speed_y, ball_served

    if server == 1:
        ball.x = player1_racket.right
        ball.y = player1_racket.centery
        ball_speed_x = 7  # Sätt en initial fart
        ball_speed_y = random.choice([7, -7])  # Slumpa riktning på Y
    elif server == 2:
        ball.x = player2_racket.left - ball_radius * 2
        ball.y = player2_racket.centery
        ball_speed_x = -7  # Sätt en initial fart för andra spelaren
        ball_speed_y = random.choice([7, -7])  # Slumpa riktning på Y

    ball_served = True  # Bollen är nu serverad

def increase_ball_speed():
    global ball_speed_x, ball_speed_y

    # Öka hastigheten på bollen långsamt efter varje träff
    increase_amount = 1.02  # 2% ökning per träff (långsamt)
    ball_speed_x *= increase_amount
    ball_speed_y *= increase_amount

def reset_racket_sizes():
    """Återställ racketstorlekar till originalstorlek."""
    global player1_racket, player2_racket
    player1_racket.height = racket_height
    player2_racket.height = racket_height

def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1_racket)
    pygame.draw.rect(screen, WHITE, player2_racket)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, GREEN, coin)

    # Poängvisning (Mindre text)
    font = pygame.font.SysFont('Arial', 24)  # Mindre textstorlek
    text1 = font.render(f"Player 1: {player1_score}", True, WHITE)
    text2 = font.render(f"Player 2: {player2_score}", True, WHITE)
    screen.blit(text1, (50, 20))
    screen.blit(text2, (screen_width - 200, 20))

    # Visa vem som serverar
    if server == 1:
        serve_text = font.render("Player 1 Serverar", True, WHITE)
    else:
        serve_text = font.render("Player 2 Serverar", True, WHITE)
    screen.blit(serve_text, (screen_width // 2 - serve_text.get_width() // 2, 20))

    # Visa hur mycket pengar varje spelare har (Längst ner på skärmen)
    money_font = pygame.font.SysFont('Arial', 20)  # Ännu mindre textstorlek för pengar
    money_text1 = money_font.render(f"Player 1 Money: {player1_money}", True, WHITE)
    money_text2 = money_font.render(f"Player 2 Money: {player2_money}", True, WHITE)
    screen.blit(money_text1, (50, screen_height - 40))  # Pengar för Player 1 längst ner
    screen.blit(money_text2, (screen_width - 250, screen_height - 40))  # Pengar för Player 2 längst ner

    pygame.display.flip()

def draw_winner(winner):
    font = pygame.font.SysFont('Arial', 50)
    winner_text = font.render(f"{winner} Vinner!", True, WHITE)
    play_again_text = font.render("Tryck R för att spela igen", True, WHITE)
    screen.fill(BLACK)
    screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 3))
    screen.blit(play_again_text, (screen_width // 2 - play_again_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()

# Funktion för att visa startskärmen
def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont('Arial', 50)
    start_text = font.render("Starta Spel", True, WHITE)
    instructions_text = pygame.font.SysFont('Arial', 30).render("Tryck ENTER för att börja", True, WHITE)
    
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 3))
    screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, screen_height // 2))

    pygame.display.flip()

# Spelloop
clock = pygame.time.Clock()

# Visa startskärm och vänta på användarens input
show_start_screen()
waiting_for_input = True
while waiting_for_input:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Tryck ENTER för att starta spelet
                waiting_for_input = False

# Spelet börjar här
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    handle_player_input()
    move_ball()
    draw_game()

    # Kontrollera om någon har vunnit
    if player1_score >= winning_score:
        draw_winner("Player 1")
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset spelet om Player 1 vinner
                        player1_score = 0
                        player2_score = 0
                        player1_money = 0
                        player2_money = 0
                        ball_speed_x = 7
                        ball_speed_y = 7
                        server = 1
                        reset_ball()
                        reset_racket_sizes()
                        waiting_for_input = False

    elif player2_score >= winning_score:
        draw_winner("Player 2")
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset spelet om Player 2 vinner
                        player1_score = 0
                        player2_score = 0
                        player1_money = 0
                        player2_money = 0
                        ball_speed_x = 7
                        ball_speed_y = 7
                        server = 2
                        reset_ball()
                        reset_racket_sizes()
                        waiting_for_input = False

    clock.tick(60)

pygame.quit()
