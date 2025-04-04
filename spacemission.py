import pygame
import random
import time


# Initialisera pygame
pygame.init()

# Skärmstorlek
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Raketspel")

# Ladda bilder
rocket_image = pygame.image.load("rocket.png")  # Ladda raketbilden
stone_image_1 = pygame.image.load("stone_1.png")  # Ladda första stenbilden
stone_image_2 = pygame.image.load("stone_2.png")  # Ladda andra stenbilden
stone_image_3 = pygame.image.load("stone_3.png")  # Ladda tredje stenbilden
bubble_image = pygame.image.load("bubble.png")  # Ladda bubbla
bubble_image2 = pygame.image.load("bubble.png")  # Ladda bubbla för odödlighet
money_image = pygame.image.load("money.png")  # Ladda bild på pengarna
background_images = [
   pygame.image.load("background1.jpg"),  # Första bakgrunden
   pygame.image.load("background2.jpg"),  # Andra bakgrunden
   pygame.image.load("background3.jpg"),  # Tredje bakgrunden
   pygame.image.load("background4.jpg"),  # Fjärde bakgrunden
   pygame.image.load("background5.jpg")   # Femte bakgrunden
]

# Förstora bakgrunderna för att passa hela skärmen
background_images = [pygame.transform.scale(bg, (screen_width, screen_height)) for bg in background_images]

# Raketens inställningar (större raket)
rocket_width = 80
rocket_height = 100
rocket_speed = 5

# Hinder (Stenar) inställningar (större stenar)
stone_width = 80
stone_height = 80
stone_speed = 0  # Börjar med en viss hastighet

# Bubblor inställningar
bubble_width = 80
bubble_height = 80
bubble_speed = 0  # Börjar med en viss hastighet

# Pengar inställningar
money_width = 50
money_height = 50

# Spelinställningar
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

# Poäng
score = 0
collected_money = 0  # Håller reda på samlade pengar


# Raketen klass
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(rocket_image, (rocket_width, rocket_height))  # Skala raketbilden
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - rocket_height - 10)
        self.invincible = False  # Flagga för odödlighet
        self.invincible_start_time = None  # När odödligheten började

    def update(self, x_direction):
        """Flytta raketen baserat på användarens input (höger/vänster)."""
        if self.rect.left > 0 and x_direction == -1:  # Förhindra att den går utanför vänstra skärmen
            self.rect.x -= rocket_speed
        if self.rect.right < screen_width and x_direction == 1:  # Förhindra att den går utanför högra skärmen
            self.rect.x += rocket_speed

        # Kolla om odödligheten har gått ut
        if self.invincible:
            if time.time() - self.invincible_start_time > 5:  # 5 sekunder
                self.invincible = False


# Stenklass
class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Slumpmässig val av stenbild
        stone_type = random.choice([stone_image_1, stone_image_2, stone_image_3])
        self.image = pygame.transform.scale(stone_type, (stone_width, stone_height))  # Skala stenbilden
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - stone_width)
        self.rect.y = -stone_height  # Starta från toppen

        # Ge varje sten en slumpmässig hastighet
        self.speed = random.randint(3, 8)  # Hastigheten varierar mellan 3 och 8

    def update(self):
        """Flytta stenen nedåt med hastighet."""
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = -stone_height
            self.rect.x = random.randint(0, screen_width - stone_width)  # Stenarna kommer från olika platser
            self.speed = random.randint(1, 2) + stone_speed  # Slumpa ny hastighet när den spawnar på nytt


# bubble
class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))  # Skala bubbla-bilden
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - bubble_width)
        self.rect.y = -bubble_height  # Starta från toppen
        
        # Ge varje bubbla en slumpmässig hastighet
        self.speed = 3
        
        # Tidsinställningar för att starta bubblan
        self.time_when_started = time.time()  # Tidpunkt när bubblan startar
        self.set_random_delay()  # Sätt en initial slumpmässig fördröjning

        self.is_falling = False  # Flagga för att hålla reda på om bubblan börjar falla

    def set_random_delay(self):
        """Slumpa en fördröjning mellan 5 och 10 sekunder."""
        self.delay_time = random.uniform(20, 35)

    def update(self):
        """Flytta bubblan nedåt med hastighet efter en fördröjning."""
        if not self.is_falling:
            # Kolla om fördröjningstiden har passerat
            if time.time() - self.time_when_started >= self.delay_time:
                self.is_falling = True  # Bubblan börjar falla efter fördröjningen
        else:
            # Om bubblan har börjat falla, flytta den nedåt
            self.rect.y += self.speed
            
            # Om bubblan är utanför skärmen, sätt tillbaka den till toppen med en ny slumpmässig fördröjning
            if self.rect.top > screen_height:
                self.rect.y = -bubble_height
                self.rect.x = random.randint(0, screen_width - bubble_width)  # Slumpa en ny startposition
                self.time_when_started = time.time()  # Uppdatera starttiden för nästa fördröjning
                self.set_random_delay()  # Sätt en ny slumpmässig fördröjning
                self.is_falling = False  # Vänta på nästa fördröjning


# Bubble2 (odödlighetsbubblan) klass
class InvincibleBubble(pygame.sprite.Sprite):
    def __init__(self, rocket):
        super().__init__()
        self.image = pygame.transform.scale(bubble_image2, (100, 100))  # Skala bubbla2 till 100x100
        self.rect = self.image.get_rect()
        self.rocket = rocket  # Håll referens till raketen
        self.rect.center = rocket.rect.center  # Sätt initialt till raketens position

    def update(self):
        """Uppdatera bubbla2s position till raketens position när raketen är odödlig."""
        if self.rocket.invincible:
            self.rect.center = self.rocket.rect.center  # Flytta bubbla2 till raketens position
        else:
            self.rect.y = -100  # Placera bubbla2 utanför skärmen när raketen inte är odödlig


# Pengaklass
class Money(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(money_image, (money_width, money_height))  # Skala pengabilden
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - money_width)
        self.rect.y = -money_height  # Starta från toppen
        self.speed = random.randint(2, 4)  # Slumpmässig hastighet för pengarna

    def update(self):
        """Flytta pengarna nedåt."""
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = -money_height
            self.rect.x = random.randint(0, screen_width - money_width)  # Pengarna kommer från olika platser


# Funktion för att kolla kollisionsdetektering med en "bufferzon"
def check_collision_with_buffer(rocket, stones, buffer_zone=-100):
    """Kollar om raketen kolliderar med någon sten, med en bufferzon för att ge lite utrymme."""
    for stone in stones:
        # Skapa en rektangel som är större än stenens rektangel, så att raketen kan vara närmare utan att kollidera
        expanded_stone_rect = stone.rect.inflate(buffer_zone, buffer_zone)
    
        if rocket.rect.colliderect(expanded_stone_rect):
            return True  # Kollisionshändelse
    return False


# Funktion för att kolla om raketen samlar pengar
def check_collision_with_money(rocket, money_group):
    """Kollar om raketen samlar pengar."""
    global score, collected_money
    for money in money_group:
        if rocket.rect.colliderect(money.rect):
            score += 10  # Öka poäng när raketen samlar pengar
            collected_money += 1  # Öka antalet samlade pengar
            money.rect.y = -money_height  # Återställ pengarna till toppen
            money.rect.x = random.randint(0, screen_width - money_width)  # Slumpa positionen på nytt
            update_stone_speeds()


# Uppdatera stenarnas hastighet baserat på antalet samlade pengar
def update_stone_speeds():
    """Öka hastigheten på stenarna för varje peng som samlas, utan maxhastighet."""
    global stone_speed
    stone_speed += 0.1


# Funktion för att ändra bakgrund baserat på poäng
def change_background():
    """Ändra bakgrunden baserat på poäng."""
    if score >= 400:
        return background_images[4]
    elif score >= 300:
        return background_images[3]
    elif score >= 200:
        return background_images[2]
    elif score >= 100:
        return background_images[1]
    else:
        return background_images[0]


# Funktion för startskärmen
def draw_start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 48)
    text = font.render("Raketspel", True, (255, 255, 255))
    start_text = pygame.font.SysFont('Arial', 24).render("Tryck SPACE för att börja", True, (255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 3))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()


# Funktion för slutskärmen
def draw_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 48)
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    score_text = pygame.font.SysFont('Arial', 24).render(f"Poäng: {score}", True, (255, 255, 255))
    play_again_text = pygame.font.SysFont('Arial', 24).render("Tryck SPACE för att spela igen", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(play_again_text, (screen_width // 2 - play_again_text.get_width() // 2, screen_height // 1.5))
    pygame.display.flip()


# Funktion för att starta om spelet
def reset_game():
    global score, collected_money, stone_speed

    # Nollställ poäng och samlade pengar
    score = 0
    collected_money = 0
    stone_speed = 5

    # Skapa grupper för raket, stenar och pengar
    all_sprites = pygame.sprite.Group()
    stones = pygame.sprite.Group()
    bubbles = pygame.sprite.Group()
    bubbles2 = pygame.sprite.Group()
    money_group = pygame.sprite.Group()

    # Skapa raket och lägg till den i all_sprites-gruppen
    rocket = Rocket()
    all_sprites.add(rocket)

    # Skapa stenar
    for _ in range(5):  # Starta med 5 stenar
        stone = Stone()
        all_sprites.add(stone)
        stones.add(stone)

    # Skapa bubbla
    bubble = Bubble()
    all_sprites.add(bubble)
    bubbles.add(bubble)

    # Skapa bubbla2
    bubble2 = InvincibleBubble(rocket)
    all_sprites.add(bubble2)
    bubbles2.add(bubble2)

    # Skapa pengar
    for _ in range(3):  # Starta med 3 pengar
        money = Money()
        all_sprites.add(money)
        money_group.add(money)

    return all_sprites, stones, bubbles, bubbles2, money_group, rocket


# Spelets huvudfunktion
def game():
    global score, collected_money, stone_speed, bubble_image2
    running = True
    x_direction = 0  # Ingen rörelse från början

    # Startskärm
    draw_start_screen()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_input = False

    # Återställ spelet
    all_sprites, stones, bubbles, bubbles2, money_group, rocket = reset_game()

    while running:
        # Hantera händelser
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Använda piltangenter för att styra raketen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_direction = -1  # Flytta åt vänster
        elif keys[pygame.K_RIGHT]:
            x_direction = 1  # Flytta åt höger
        else:
            x_direction = 0  # Inget rörelse

        # Uppdatera raketens rörelse
        rocket.update(x_direction)

        # Uppdatera hinder
        stones.update()

        # Uppdatera bubblor
        bubbles.update()

        bubbles2.update()

        # Uppdatera pengar
        money_group.update()

        # Kolla om raketen kolliderar med någon sten (med bufferzon), om raketen inte är odödlig
        if not rocket.invincible and check_collision_with_buffer(rocket, stones):
            running = False  # Om kollision sker, avsluta spelet

        # Kolla om raketen samlar pengar
        check_collision_with_money(rocket, money_group)

        # Kolla om raketen samlar en bubbla och aktivera odödlighet
        for bubble in bubbles:
            if rocket.rect.colliderect(bubble.rect):
                rocket.invincible = True
                rocket.invincible_start_time = time.time()  # Starta odödlighets-timern
                bubble.rect.y = -bubble_height  # Återställ bubbla till toppen
                bubble.rect.x = random.randint(0, screen_width - bubble_width)
                bubble.time_when_started = time.time()  # Uppdatera starttiden för nästa fördröjning
                bubble.set_random_delay()  # Sätt en ny slumpmässig fördröjning
                bubble.is_falling = False  # Vänta på nästa fördröjning
            
        # Ändra bakgrund baserat på poäng
        current_background = change_background()

        # Rita bakgrund
        screen.blit(current_background, (0, 0))  # Rita bakgrundsbilden (nu i full skärm)

        # Rita alla sprites (raketen, stenar och pengar)
        all_sprites.draw(screen)

        # Visa poäng
        score_text = font.render(f"Poäng: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Uppdatera skärmen
        pygame.display.flip()

        # Sätt upp spelets hastighet (FPS)
        clock.tick(60)  # 60 bilder per sekund

    # När spelet är slut, visa slutpoäng och slutskärm
    draw_game_over_screen()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Om SPACE trycks igen, starta spelet på nytt
                game()

    pygame.quit()

# Starta spelet
game()
