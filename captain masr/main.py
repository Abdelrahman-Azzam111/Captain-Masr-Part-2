
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions (decreased width)
WIDTH, HEIGHT = 1200, 900  # Decreased map size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Captain Masr's Journey")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load Fonts
font = pygame.font.Font(pygame.font.match_font('arial'), 24)

# Load and Resize Background Image
background_image = pygame.image.load("image/level2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load Character Images
captain_image1 = pygame.image.load("image/cm.png").convert_alpha()
captain_image2 = pygame.image.load("image/caside.png").convert_alpha()
captain_image1 = pygame.transform.scale(captain_image1, (250, 300))  # Increased size
captain_image2 = pygame.transform.scale(captain_image2, (250, 300))  # Increased size

# Game Clock
clock = pygame.time.Clock()
FPS = 60

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Captain Masr Class
class CaptainMasr(pygame.sprite.Sprite):
    def __init__(self, x, y, image, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hp = 100
        self.attack_power = 10
        self.controls = controls
        self.vel_y = 0
        self.jumping = False
        self.gravity = 0.8
        self.projectiles = pygame.sprite.Group()

    def move(self, keys):
        if keys[self.controls['left']]:
            self.rect.x -= 5
        if keys[self.controls['right']]:
            self.rect.x += 5
        if keys[self.controls['jump']] and not self.jumping:
            self.vel_y = -15
            self.jumping = True

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.jumping = False
            self.vel_y = 0

    def shoot(self):
        direction = 10 if self.controls['projectile_dir'] == 'east' else -10
        projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
        self.projectiles.add(projectile)

    def punch(self):
        return random.randint(self.attack_power - 5, self.attack_power + 5)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        # Handle Captain Masr's death
        pass

    def update(self, keys, platforms):
        self.move(keys)
        self.rect.y += self.vel_y
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.rect.y = hits[0].rect.top - self.rect.height
            self.jumping = False
            self.vel_y = 0

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((20, 10))  # Adjusted the size to make it more visible
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += self.direction
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Functions
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main():
    running = True

    # Define controls for each Captain Masr
    controls1 = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'shoot': pygame.K_SPACE, 'projectile_dir': 'east'}
    controls2 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'shoot': pygame.K_RETURN, 'projectile_dir': 'west'}

    # Create Captain Masr
    captain_masr1 = CaptainMasr(200, HEIGHT - 100, captain_image1, controls1)
    captain_masr2 = CaptainMasr(1000, HEIGHT - 100, captain_image2, controls2)

    captains = pygame.sprite.Group()
    captains.add(captain_masr1)
    captains.add(captain_masr2)

    # Create Platforms
    platforms = pygame.sprite.Group()
    platforms.add(Platform(300, 500, 200, 20))
    platforms.add(Platform(800, 400, 200, 20))
    platforms.add(Platform(600, 300, 200, 20))

    while running:
        screen.blit(background_image, (0, 0))  # Draw the resized background image
        draw_text(f"Captain Masr 1 HP: {captain_masr1.hp}", 10, 10, WHITE)
        draw_text(f"Captain Masr 2 HP: {captain_masr2.hp}", WIDTH - 200, 10, WHITE)

        # Draw Captain Masrs
        screen.blit(captain_masr1.image, captain_masr1.rect)
        screen.blit(captain_masr2.image, captain_masr2.rect)

        # Draw Platforms
        platforms.draw(screen)

        captain_masr1.projectiles.update()
        captain_masr2.projectiles.update()
        captain_masr1.projectiles.draw(screen)
        captain_masr2.projectiles.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Move and update Captain Masrs
        captain_masr1.update(keys, platforms)
        captain_masr2.update(keys, platforms)

        # Handle shooting
        if keys[captain_masr1.controls['shoot']]:
            captain_masr1.shoot()
        if keys[captain_masr2.controls['shoot']]:
            captain_masr2.shoot()

        # Check for collisions
        for projectile in captain_masr1.projectiles:
            if captain_masr2.rect.colliderect(projectile.rect):
                captain_masr2.take_damage(captain_masr1.attack_power)
                projectile.kill()

        for projectile in captain_masr2.projectiles:
            if captain_masr1.rect.colliderect(projectile.rect):
                captain_masr1.take_damage(captain_masr2.attack_power)
                projectile.kill()

        if captain_masr1.hp <= 0:
            draw_text("Captain Masr 2 wins!", WIDTH // 2 - 100, HEIGHT // 2 + 100, GREEN)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        if captain_masr2.hp <= 0:
            draw_text("Captain Masr 1 wins!", WIDTH // 2 - 100, HEIGHT // 2 + 100, GREEN)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

