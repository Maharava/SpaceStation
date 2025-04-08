import sys
import os
import random
import math
import pygame

from src.core.input_handler import InputHandler
from src.core.renderer import Renderer
from src.core.physics import Physics
from src.entities.ship import Ship
from src.entities.drones.combat_drone import CombatDrone
from src.entities.drones.scanner_drone import ScannerDrone
from src.entities.resources import ResourceGenerator
from src.entities.survivors import SurvivorGenerator
from src.world.procedural.map_generator import MapGenerator
from src.world.mission import Mission
from src.ui.hud import HUD
from src.ui.menu import Menu
from src.ui.station_interface import StationInterface
from src.utils.config import Config
from src.utils.logger import logger

class Game:
    def __init__(self):
        # Core systems
        self.config = Config()
        self.renderer = Renderer(self.config)
        self.input_handler = InputHandler(self.config)
        self.physics = Physics()
        self.running = False
        
        # Game state
        self.state = "menu"  # menu, station, mission
        
        # Game objects
        self.ship = Ship(self.config.get("screen_width") // 2, self.config.get("screen_height") // 2)
        self.projectiles = []
        self.resources = []
        self.obstacles = []
        self.map_data = None
        self.mission = None
        
        # Drones
        self.ship.active_drones = [
            CombatDrone(self.ship.x - 30, self.ship.y + 30),
            ScannerDrone(self.ship.x + 30, self.ship.y + 30)
        ]
        
        # UI components
        self.hud = HUD(self.renderer)
        self.menu = self.create_main_menu()
        self.station_interface = StationInterface(self.renderer)
        
        # Starting survivor
        self.survivor_generator = SurvivorGenerator()
        self.survivor = self.survivor_generator.generate_survivor()
        self.survivor.rescued = True  # Start with one rescued survivor
        
        # Resource generator
        self.resource_generator = ResourceGenerator()
        
        # Map generator
        self.map_generator = MapGenerator(
            self.config.get("screen_width") * 3,  # Map larger than screen
            self.config.get("screen_height") * 3
        )
        
        # Camera position (for scrolling map)
        self.camera_x = 0
        self.camera_y = 0
    
    def create_main_menu(self):
        """Create and configure the main menu"""
        try:
            menu = Menu(self.renderer)
            menu.set_title("STARBOUND EXILE")
            menu.add_item("Start Game", "start_game")
            menu.add_item("Options", "options")
            menu.add_item("Exit", "exit")
            return menu
        except Exception as e:
            logger.error(f"Error creating main menu: {str(e)}")
            # Create simple fallback menu
            menu = Menu(self.renderer)
            menu.set_title("STARBOUND EXILE")
            menu.add_item("Start Game", "start_game")
            menu.add_item("Exit", "exit")
            return menu
    
    def handle_input(self):
        """Process input based on current game state"""
        try:
            if self.state == "menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    
                    action = self.menu.handle_event(event)
                    if action == "start_game":
                        self.state = "station"
                    elif action == "options":
                        pass  # Options menu not implemented yet
                    elif action == "exit":
                        return False
            
            elif self.state == "station":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    
                    action = self.station_interface.handle_event(event, self.ship, self.ship.active_drones, self.survivor)
                    if action == "start_mission":
                        self.start_mission()
                        self.state = "mission"
            
            elif self.state == "mission":
                # Handle regular gameplay input
                continue_game = self.input_handler.handle_events()
                if not continue_game:
                    return False
                
                # Apply inputs to ship
                if self.input_handler.is_action_pressed("move_up"):
                    self.physics.apply_thrust(self.ship, 0, -1)
                if self.input_handler.is_action_pressed("move_down"):
                    self.physics.apply_thrust(self.ship, 0, 1)
                if self.input_handler.is_action_pressed("move_left"):
                    self.physics.apply_thrust(self.ship, -1, 0)
                if self.input_handler.is_action_pressed("move_right"):
                    self.physics.apply_thrust(self.ship, 1, 0)
                
                # Fire weapon
                if self.input_handler.is_action_pressed("fire"):
                    projectile = self.ship.fire_weapon()
                    if projectile:
                        self.projectiles.append(projectile)
                
                # Scanner drone special action
                if self.input_handler.is_action_pressed("scan"):
                    for drone in self.ship.active_drones:
                        if isinstance(drone, ScannerDrone):
                            drone.perform_scan()
                
                # Return to station (temporary for testing)
                if self.input_handler.is_action_pressed("return"):
                    self.state = "station"
            
            return True
        except Exception as e:
            logger.error(f"Error handling input: {str(e)}")
            return True
    
    def update(self):
        """Update game state based on current mode"""
        try:
            if self.state == "mission":
                # Update ship
                self.ship.update(self.physics)
                
                # Update drones
                for drone in self.ship.active_drones:
                    if isinstance(drone, CombatDrone):
                        projectile = drone.update(self.physics, self.ship, [])  # No enemies yet
                        if projectile:
                            self.projectiles.append(projectile)
                    else:
                        drone.update(self.physics, self.ship)
                
                # Update projectiles
                for proj in self.projectiles[:]:
                    # Move projectile
                    proj['x'] += proj['velocity_x']
                    proj['y'] += proj['velocity_y']
                    proj['lifetime'] -= 1
                    
                    # Remove expired projectiles
                    if proj['lifetime'] <= 0:
                        self.projectiles.remove(proj)
                
                # Check for resource collection
                for resource in self.resources[:]:
                    # Check distance to ship
                    dx = self.ship.x - resource.x
                    dy = self.ship.y - resource.y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance < self.ship.radius + resource.radius:
                        # Try to collect
                        if self.ship.collect_resource(resource):
                            self.resources.remove(resource)
                
                # Check mission objectives
                if self.mission:
                    mission_complete = self.mission.check_objective_completion(self.ship)
                    if mission_complete:
                        # Return to station
                        self.state = "station"
                
                # Update camera position to follow ship
                self.camera_x = self.ship.x - self.config.get("screen_width") // 2
                self.camera_y = self.ship.y - self.config.get("screen_height") // 2
                
                # Keep camera in bounds
                self.camera_x = max(0, min(self.camera_x, self.map_data['width'] - self.config.get("screen_width")))
                self.camera_y = max(0, min(self.camera_y, self.map_data['height'] - self.config.get("screen_height")))
                
                # Detect resource collisions with scanner drones
                for drone in self.ship.active_drones:
                    if isinstance(drone, ScannerDrone):
                        drone.detect_resources(self.resources)
        except Exception as e:
            logger.error(f"Error in game update: {str(e)}")
    
    def render(self):
        """Render game based on current state"""
        try:
            self.renderer.clear_screen()
            
            if self.state == "menu":
                self.menu.render()
            
            elif self.state == "station":
                self.station_interface.render(self.ship, self.ship.active_drones, self.survivor)
            
            elif self.state == "mission":
                # Render background
                self.render_background()
                
                # Render game objects adjusted for camera position
                self.render_game_objects()
                
                # Render HUD
                self.hud.render(
                    self.ship, 
                    self.mission, 
                    self.config.get("screen_width"), 
                    self.config.get("screen_height")
                )
            
            self.renderer.update_display()
        except Exception as e:
            logger.error(f"Error in game rendering: {str(e)}")

    def render_background(self):
        """Render the space background and stars"""
        try:
            # Draw black background
            self.renderer.clear_screen()
            
            # Draw background objects (stars, etc.)
            if self.map_data and 'background_objects' in self.map_data:
                for bg_obj in self.map_data['background_objects']:
                    # Adjust position for camera scrolling
                    screen_x = bg_obj['x'] - self.camera_x
                    screen_y = bg_obj['y'] - self.camera_y
                    
                    # Only draw if on screen
                    if (0 <= screen_x <= self.config.get("screen_width") and
                        0 <= screen_y <= self.config.get("screen_height")):
                        
                        # Draw different background object types
                        if bg_obj['type'] == 'star':
                            # Small white dot for stars
                            brightness = int(255 * bg_obj['brightness'])
                            color = (brightness, brightness, brightness)
                            self.renderer.draw_circle(screen_x, screen_y, bg_obj['size'], color)
                        elif bg_obj['type'] == 'dust':
                            # Small colored circle for dust
                            color = (100, 100, 150, int(100 * bg_obj['brightness']))
                            self.renderer.draw_circle(screen_x, screen_y, bg_obj['size'], color)
                        elif bg_obj['type'] == 'nebula':
                            # Larger colored circle for nebula
                            color = (150, 100, 200, int(50 * bg_obj['brightness']))
                            self.renderer.draw_circle(screen_x, screen_y, bg_obj['size'] * 3, color)
        except Exception as e:
            logger.error(f"Error rendering background: {str(e)}")

    def render_game_objects(self):
        """Render all game objects adjusted for camera position"""
        try:
            # Render obstacles
            if self.map_data and 'obstacles' in self.map_data:
                for obstacle in self.map_data['obstacles']:
                    screen_x = obstacle['x'] - self.camera_x
                    screen_y = obstacle['y'] - self.camera_y
                    
                    # Only draw if on or near screen
                    if (-obstacle['radius'] <= screen_x <= self.config.get("screen_width") + obstacle['radius'] and
                        -obstacle['radius'] <= screen_y <= self.config.get("screen_height") + obstacle['radius']):
                        
                        # Draw different obstacle types
                        if obstacle['type'] == 'asteroid':
                            color = (100, 90, 80)
                        elif obstacle['type'] == 'debris':
                            color = (120, 120, 130)
                        elif obstacle['type'] == 'ice':
                            color = (200, 220, 255)
                        else:
                            color = (150, 150, 150)
                        
                        self.renderer.draw_circle(screen_x, screen_y, obstacle['radius'], color)
            
            # Render resources
            for resource in self.resources:
                screen_x = resource.x - self.camera_x
                screen_y = resource.y - self.camera_y
                
                # Only draw if on or near screen
                if (-resource.radius <= screen_x <= self.config.get("screen_width") + resource.radius and
                    -resource.radius <= screen_y <= self.config.get("screen_height") + resource.radius):
                    
                    # Only show resource if detected by scanner or close to player
                    dx = self.ship.x - resource.x
                    dy = self.ship.y - resource.y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if resource.detected or distance < 200:
                        self.renderer.draw_circle(screen_x, screen_y, resource.radius, resource.color)
            
            # Render points of interest
            if self.map_data and 'points_of_interest' in self.map_data:
                for poi in self.map_data['points_of_interest']:
                    screen_x = poi['x'] - self.camera_x
                    screen_y = poi['y'] - self.camera_y
                    
                    if (-poi['radius'] <= screen_x <= self.config.get("screen_width") + poi['radius'] and
                        -poi['radius'] <= screen_y <= self.config.get("screen_height") + poi['radius']):
                        
                        # Draw different POI types
                        if poi['type'] == 'derelict':
                            color = (180, 120, 80)
                        elif poi['type'] == 'station':
                            color = (80, 180, 150)
                        elif poi['type'] == 'anomaly':
                            color = (200, 100, 200)
                        else:
                            color = (200, 200, 100)
                        
                        self.renderer.draw_circle(screen_x, screen_y, poi['radius'], color)
            
            # Render projectiles
            for projectile in self.projectiles:
                screen_x = projectile['x'] - self.camera_x
                screen_y = projectile['y'] - self.camera_y
                
                if (0 <= screen_x <= self.config.get("screen_width") and
                    0 <= screen_y <= self.config.get("screen_height")):
                    self.renderer.draw_circle(screen_x, screen_y, 3, (255, 200, 50))
            
            # Render drones
            for drone in self.ship.active_drones:
                screen_x = drone.x - self.camera_x
                screen_y = drone.y - self.camera_y
                
                if (-drone.radius <= screen_x <= self.config.get("screen_width") + drone.radius and
                    -drone.radius <= screen_y <= self.config.get("screen_height") + drone.radius):
                    
                    # Determine drone color
                    if isinstance(drone, CombatDrone):
                        color = (255, 50, 50)  # Red for combat drones
                    elif isinstance(drone, ScannerDrone):
                        color = (50, 200, 255)  # Blue for scanner drones
                    else:
                        color = (200, 200, 200)  # Default color
                    
                    self.renderer.draw_circle(screen_x, screen_y, drone.radius, color)
                    
                    # Render scanner radius if active
                    if isinstance(drone, ScannerDrone) and drone.scan_active:
                        pygame.draw.circle(
                            self.renderer.screen,
                            (50, 200, 255, 50),  # Semi-transparent blue
                            (int(screen_x), int(screen_y)),
                            drone.scan_radius,
                            1  # Width of the circle line
                        )
            
            # Render ship
            screen_x = self.ship.x - self.camera_x
            screen_y = self.ship.y - self.camera_y
            self.renderer.draw_circle(screen_x, screen_y, self.ship.radius, (0, 150, 200))
            
            # Draw direction indicator on ship (shows where ship is pointed)
            angle_rad = math.radians(self.ship.rotation)
            indicator_x = screen_x + math.cos(angle_rad) * self.ship.radius
            indicator_y = screen_y + math.sin(angle_rad) * self.ship.radius
            self.renderer.draw_circle(indicator_x, indicator_y, 5, (200, 200, 50))
        except Exception as e:
            logger.error(f"Error rendering game objects: {str(e)}")

    def start_mission(self):
        """Initialize a new mission"""
        try:
            # Generate a new map
            self.map_data = self.map_generator.generate_map(difficulty=1)
            
            # Create a mission
            self.mission = Mission(self.map_data)
            mission_data = self.mission.generate_mission(mission_type="exploration", difficulty=1)
            
            # Position the ship at the center of the screen
            self.ship.x = self.map_data['width'] // 2
            self.ship.y = self.map_data['height'] // 2
            self.ship.velocity_x = 0
            self.ship.velocity_y = 0
            
            # Reset camera position
            self.camera_x = self.ship.x - self.config.get("screen_width") // 2
            self.camera_y = self.ship.y - self.config.get("screen_height") // 2
            
            # Position drones near the ship
            for i, drone in enumerate(self.ship.active_drones):
                angle = 2 * math.pi * i / len(self.ship.active_drones)
                drone.x = self.ship.x + math.cos(angle) * 50
                drone.y = self.ship.y + math.sin(angle) * 50
            
            # Create resources based on map
            self.resources = self.mission.resources
            
            # Reset projectiles
            self.projectiles = []
            
            # Extract obstacles from map data
            self.obstacles = self.map_data.get('obstacles', [])
            
            return True
        except Exception as e:
            logger.error(f"Error starting mission: {str(e)}")
            return False

    def run(self):
        """Main game loop"""
        try:
            self.running = True
            
            while self.running:
                # Input handling
                self.running = self.handle_input()
                
                # Game logic
                self.update()
                
                # Rendering
                self.render()
            
            self.shutdown()
        except Exception as e:
            logger.error(f"Error in main game loop: {str(e)}")
            self.shutdown()

    def shutdown(self):
        """Clean up resources and exit"""
        try:
            # Save any game state if needed
            
            # Shut down renderer (which handles pygame shutdown)
            self.renderer.shutdown()
        except Exception as e:
            logger.error(f"Error shutting down game: {str(e)}")