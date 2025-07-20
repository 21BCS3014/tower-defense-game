
import pygame
import math
import sys
import json
from enum import Enum
from typing import List, Tuple
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)

class TowerType(Enum):
    BASIC = 1
    SNIPER = 2
    FREEZE = 3
    EXPLOSIVE = 4
    LASER = 5

class EnemyType(Enum):
    BASIC = 1
    FAST = 2
    TANK = 3
    FLYING = 4
    BOSS = 5

class Enemy:
    def __init__(self, enemy_type: EnemyType, path: List[Tuple[int, int]]):
        self.type = enemy_type
        self.path = path
        self.path_index = 0
        self.position = list(path[0]) if path else [0, 0]
        self.target_position = list(path[1]) if len(path) > 1 else self.position[:]

        # Enemy stats based on type
        stats = {
            EnemyType.BASIC: {"hp": 100, "speed": 2, "reward": 10, "color": RED, "size": 15},
            EnemyType.FAST: {"hp": 60, "speed": 4, "reward": 15, "color": YELLOW, "size": 12},
            EnemyType.TANK: {"hp": 300, "speed": 1, "reward": 25, "color": GRAY, "size": 20},
            EnemyType.FLYING: {"hp": 80, "speed": 3, "reward": 20, "color": BLUE, "size": 14},
            EnemyType.BOSS: {"hp": 800, "speed": 1.5, "reward": 100, "color": PURPLE, "size": 25}
        }

        self.max_hp = stats[enemy_type]["hp"]
        self.hp = self.max_hp
        self.speed = stats[enemy_type]["speed"]
        self.reward = stats[enemy_type]["reward"]
        self.color = stats[enemy_type]["color"]
        self.size = stats[enemy_type]["size"]
        self.alive = True
        self.reached_end = False

    def update(self):
        if not self.alive or self.reached_end:
            return

        # Move towards target position
        dx = self.target_position[0] - self.position[0]
        dy = self.target_position[1] - self.position[1]
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < 5:  # Reached current target
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.reached_end = True
                return
            self.target_position = list(self.path[self.path_index])
        else:
            # Move towards target
            self.position[0] += (dx / distance) * self.speed
            self.position[1] += (dy / distance) * self.speed

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def draw(self, screen):
        if self.alive:
            # Draw enemy circle
            pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.size)

            # Draw health bar
            bar_width = self.size * 2
            bar_height = 4
            bar_x = int(self.position[0] - bar_width // 2)
            bar_y = int(self.position[1] - self.size - 10)

            # Background (red)
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))

            # Health (green)
            health_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Tower:
    def __init__(self, tower_type: TowerType, x: int, y: int):
        self.type = tower_type
        self.position = [x, y]
        self.target = None
        self.last_shot = 0

        # Tower stats based on type
        stats = {
            TowerType.BASIC: {"damage": 30, "range": 100, "fire_rate": 1000, "cost": 50, "color": GREEN},
            TowerType.SNIPER: {"damage": 150, "range": 200, "fire_rate": 2000, "cost": 150, "color": BLUE},
            TowerType.FREEZE: {"damage": 20, "range": 80, "fire_rate": 500, "cost": 100, "color": (0, 255, 255)},
            TowerType.EXPLOSIVE: {"damage": 80, "range": 90, "fire_rate": 1500, "cost": 200, "color": (255, 165, 0)},
            TowerType.LASER: {"damage": 60, "range": 120, "fire_rate": 100, "cost": 300, "color": (255, 0, 255)}
        }

        self.damage = stats[tower_type]["damage"]
        self.range = stats[tower_type]["range"]
        self.fire_rate = stats[tower_type]["fire_rate"]
        self.cost = stats[tower_type]["cost"]
        self.color = stats[tower_type]["color"]

    def find_target(self, enemies: List[Enemy]):
        self.target = None
        closest_distance = float('inf')

        for enemy in enemies:
            if enemy.alive:
                distance = math.sqrt((enemy.position[0] - self.position[0])**2 + 
                                   (enemy.position[1] - self.position[1])**2)
                if distance <= self.range and distance < closest_distance:
                    closest_distance = distance
                    self.target = enemy

    def can_shoot(self, current_time):
        return current_time - self.last_shot >= self.fire_rate

    def shoot(self, current_time):
        if self.target and self.target.alive and self.can_shoot(current_time):
            self.last_shot = current_time

            # Apply damage based on tower type
            if self.type == TowerType.EXPLOSIVE:
                # Explosive damage to nearby enemies
                self._explosive_damage()
            else:
                self.target.take_damage(self.damage)

            return True
        return False

    def _explosive_damage(self):
        # Deal damage to target and nearby enemies (simplified)
        if self.target:
            self.target.take_damage(self.damage)

    def draw(self, screen):
        # Draw tower
        pygame.draw.circle(screen, self.color, self.position, 20)
        pygame.draw.circle(screen, BLACK, self.position, 20, 2)

        # Draw range circle when selected (simplified)
        pygame.draw.circle(screen, self.color, self.position, self.range, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Strategy Game")
        self.clock = pygame.time.Clock()

        # Game state
        self.money = 200
        self.lives = 20
        self.score = 0
        self.wave = 1
        self.game_over = False
        self.victory = False

        # Game objects
        self.towers = []
        self.enemies = []
        self.path = self._create_path()

        # UI
        self.selected_tower_type = TowerType.BASIC
        self.font = pygame.font.Font(None, 36)

        # Wave management
        self.enemies_spawned = 0
        self.enemies_to_spawn = 10
        self.spawn_timer = 0
        self.spawn_delay = 1000  # milliseconds between spawns

    def _create_path(self):
        """Create a simple path for enemies to follow"""
        return [
            (0, 350),
            (200, 350),
            (200, 200),
            (400, 200),
            (400, 500),
            (600, 500),
            (600, 300),
            (800, 300),
            (800, 150),
            (SCREEN_WIDTH, 150)
        ]

    def spawn_enemy(self, current_time):
        if (self.enemies_spawned < self.enemies_to_spawn and 
            current_time - self.spawn_timer >= self.spawn_delay):

            # Choose enemy type based on wave
            if self.wave <= 3:
                enemy_type = EnemyType.BASIC
            elif self.wave <= 6:
                enemy_type = random.choice([EnemyType.BASIC, EnemyType.FAST])
            elif self.wave <= 10:
                enemy_type = random.choice([EnemyType.BASIC, EnemyType.FAST, EnemyType.TANK])
            else:
                enemy_type = random.choice(list(EnemyType))

            enemy = Enemy(enemy_type, self.path)
            self.enemies.append(enemy)
            self.enemies_spawned += 1
            self.spawn_timer = current_time

    def handle_click(self, pos):
        # Try to place a tower
        tower_stats = {
            TowerType.BASIC: 50,
            TowerType.SNIPER: 150,
            TowerType.FREEZE: 100,
            TowerType.EXPLOSIVE: 200,
            TowerType.LASER: 300
        }

        cost = tower_stats[self.selected_tower_type]
        if self.money >= cost:
            # Check if position is valid (not on path, not on another tower)
            valid_position = True
            for tower in self.towers:
                if math.sqrt((tower.position[0] - pos[0])**2 + (tower.position[1] - pos[1])**2) < 50:
                    valid_position = False
                    break

            if valid_position:
                tower = Tower(self.selected_tower_type, pos[0], pos[1])
                self.towers.append(tower)
                self.money -= cost

    def update(self, current_time):
        if self.game_over or self.victory:
            return

        # Spawn enemies
        self.spawn_enemy(current_time)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
            elif not enemy.alive:
                self.money += enemy.reward
                self.score += enemy.reward
                self.enemies.remove(enemy)

        # Update towers
        for tower in self.towers:
            tower.find_target(self.enemies)
            tower.shoot(current_time)

        # Check wave completion
        if self.enemies_spawned >= self.enemies_to_spawn and len(self.enemies) == 0:
            self.wave += 1
            self.enemies_spawned = 0
            self.enemies_to_spawn = min(20, 8 + self.wave * 2)
            if self.wave > 15:
                self.victory = True

    def draw(self):
        self.screen.fill(WHITE)

        # Draw path
        for i in range(len(self.path) - 1):
            pygame.draw.line(self.screen, DARK_GREEN, self.path[i], self.path[i + 1], 10)

        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw UI
        self._draw_ui()

        # Draw game over screen
        if self.game_over:
            self._draw_game_over()
        elif self.victory:
            self._draw_victory()

        pygame.display.flip()

    def _draw_ui(self):
        # Money, lives, score, wave info
        texts = [
            f"Money: ${self.money}",
            f"Lives: {self.lives}",
            f"Score: {self.score}",
            f"Wave: {self.wave}"
        ]

        for i, text in enumerate(texts):
            surface = self.font.render(text, True, BLACK)
            self.screen.blit(surface, (10, 10 + i * 30))

        # Tower selection buttons
        tower_buttons = [
            ("Basic ($50)", TowerType.BASIC, 10, 650),
            ("Sniper ($150)", TowerType.SNIPER, 150, 650),
            ("Freeze ($100)", TowerType.FREEZE, 300, 650),
            ("Explosive ($200)", TowerType.EXPLOSIVE, 450, 650),
            ("Laser ($300)", TowerType.LASER, 650, 650)
        ]

        for text, tower_type, x, y in tower_buttons:
            color = GREEN if tower_type == self.selected_tower_type else GRAY
            pygame.draw.rect(self.screen, color, (x, y, 120, 30))
            surface = pygame.font.Font(None, 24).render(text, True, BLACK)
            self.screen.blit(surface, (x + 5, y + 5))

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        text = self.font.render("GAME OVER!", True, RED)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)

        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(score_text, score_rect)

    def _draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        text = self.font.render("VICTORY!", True, GREEN)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)

        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(score_text, score_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicking on tower selection buttons
                    if 650 <= mouse_pos[1] <= 680:
                        if 10 <= mouse_pos[0] <= 130:
                            self.selected_tower_type = TowerType.BASIC
                        elif 150 <= mouse_pos[0] <= 270:
                            self.selected_tower_type = TowerType.SNIPER
                        elif 300 <= mouse_pos[0] <= 420:
                            self.selected_tower_type = TowerType.FREEZE
                        elif 450 <= mouse_pos[0] <= 570:
                            self.selected_tower_type = TowerType.EXPLOSIVE
                        elif 650 <= mouse_pos[0] <= 770:
                            self.selected_tower_type = TowerType.LASER
                    elif mouse_pos[1] < 600:  # Click in game area
                        self.handle_click(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (self.game_over or self.victory):
                    self.__init__()  # Restart game
        return True

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            running = self.handle_events()
            self.update(current_time)
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
