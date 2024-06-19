# File for Game class

import pygame
import random

class Game:
  def __init__(self, bird_img, pipe_img, background_img, ground_img):
    self.man = pygame.image.load(bird_img).convert_alpha()
    self.man_rect = self.man.get_rect(center = (70, 180))
    self.spike = pygame.image.load(pipe_img).convert_alpha()
    self.background = pygame.image.load(background_img).convert_alpha()
    self.ground= pygame.image.load(ground_img).convert()
    self.ground_position = 0
    self.active = True
    self.gravity = 0.05
    self.man_movement = 0
    self.rotated_man = pygame.Surface((0, 0))
    self.spikes = []
    self.spike_height = [280, 425, 562]
    self.score = 0
    self.font = pygame.font.SysFont(None, 48)
    self.high_score = 0

  def resize_images(self):
    self.man = pygame.transform.scale(self.man, (80, 102))
    self.spike = pygame.transform.scale(self.spike, (80, 438))
    self.ground = pygame.transform.scale(self.ground, (470, 160))
    self.background = pygame.transform.scale(self.background, (400, 720))

  def show_background(self, screen):
    screen.blit(self.background, (0,0))

  def show_ground(self, screen):
    screen.blit(self.ground, (self.ground_position, 650))
    screen.blit(self.ground, (self.ground_position + 470, 650))

  def move_ground(self):
    self.ground_position -= 1
    if self.ground_position <= -400:
      self.ground_position = 0

  def show_man(self, screen):
    screen.blit(self.rotated_man, self.man_rect)

  def update_man(self):
    self.man_movement += self.gravity
    self.rotated_man = self.rotate_man()
    self.man_rect.centery += self.man_movement

  def rotate_man(self):
    new_man = pygame.transform.rotozoom(self.man, -self.man_movement * 3, 1)
    return new_man

  def flap(self):
    self.man_movement = 0
    self.man_movement -= 2.5

  def add_spike(self):
    random_spike_pos = random.choice(self.spike_height)
    bottom_spike = self.spike.get_rect(midtop = (600, random_spike_pos))
    top_spike = self.spike.get_rect(midbottom = (600, random_spike_pos - 211))
    self.spikes.append(bottom_spike)
    self.spikes.append(top_spike)

  def move_spike(self):
    for spike in self.spikes:
      spike.centerx -= 1.75
      if spike.centerx <= -40:
        self.spikes.remove(spike)

  def show_spike(self, screen):
    for spike in self.spikes:
      if spike.bottom >= 700:
        screen.blit(self.spike, spike)
      else:
        flip_spike = pygame.transform.flip(self.spike, False, True)
        screen.blit(flip_spike, spike)

  def check_collision(self):
    for spike in self.spikes:
      if self.man_rect.colliderect(spike):
        self.active = False

    if self.man_rect.top <= -100 or self.man_rect.bottom >= 650:
      self.active = False

  def update_score(self):
    self.score += 0.01

  def show_score(self, game_state, screen, color):
    score_surface = self.font.render('Score: {:d}'.format(int(self.score)), True, color)
    score_rect = score_surface.get_rect(center=(200, 75))
    screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
      restart_text1 = self.font.render('Press Space Bar', True, color)
      restart_rect1 = restart_text1.get_rect(center=(200, 280))
      screen.blit(restart_text1, restart_rect1)

      restart_text2 = self.font.render('to Play Again', True, color)
      restart_rect2 = restart_text2.get_rect(center=(200, 340))
      screen.blit(restart_text2, restart_rect2)

      high_score_surface = self.font.render('High Score: {:d}'.format(int(self.high_score)), True, color)
      high_score_rect = high_score_surface.get_rect(center=(200, 610))
      screen.blit(high_score_surface, high_score_rect)

  def game_over(self, screen, color):
    self.update_high_score()
    self.show_score('game_over', screen, color)

  def update_high_score(self):
    if self.score > self.high_score:
      self.high_score = self.score

  def restart(self):
    self.active = True
    del self.spikes[:]
    self.man_rect.center = (70, 180)
    self.man_movement = 0
    self.score = 0