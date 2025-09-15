import pygame
from datetime import datetime
from .config.config import WEATHER_MULTIPLIERS

class Player:
    def __init__(self, x, y, income_goal):
       
        self.x = x # Posición inicial del jugador
        self.y = y # Posición inicial del jugador
        self.income_goal = income_goal #Meta de ingresos para ganar el juego
        
        self.inventory = [] #falta la clase Inventory esto es temporal 
        self.max_weight = 5
        self.stamina = 100
        self.reputation = 70
        
        self.total_income = 0
        self.is_exhausted = False
        
        # Atributos para Pygame
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0)) # Un simple cuadrado verde como marcador de posición.
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # Variables para los cálculos de velocidad y resistencia
        self.base_speed = 3
        self.stamina_consumption_base = 0.5
        
    def get_total_weight(self):
        
        # usara el inventario para calcular el peso total
        return 0

    def get_weather_multiplier(self, weather_condition: str):
       
        return WEATHER_MULTIPLIERS.get(weather_condition, 1.0)
        
    def calculate_speed(self, weather_condition: str, surface_weight_tile: float):
        
        total_weight = self.get_total_weight()# implementar
        m_weather = self.get_weather_multiplier(weather_condition)
        m_weight = max(0.8, 1 - 0.03 * total_weight)
        m_rep = 1.03 if self.reputation >= 90 else 1.0
        
        if self.stamina < 30 and self.stamina > 0:
            m_stamina = 0.8
        elif self.stamina <= 0:
            m_stamina = 0.0
        else:
            m_stamina = 1.0

        speed = self.base_speed * m_weather * m_weight * m_rep * m_stamina * surface_weight_tile
        return speed

    def consume_stamina(self, weather_condition: str):
        """
        Calcula el consumo de resistencia por movimiento.
        """
        total_weight = self.get_total_weight() # implementar
        consumption = self.stamina_consumption_base
        
        if total_weight > 3:
            consumption += 0.2 * (total_weight - 3)
        
        if weather_condition in ["rain", "wind"]:
            consumption += 0.1
        elif weather_condition == "storm":
            consumption += 0.3
        elif weather_condition == "heat":
            consumption += 0.2
        
        self.stamina -= consumption
        
        if self.stamina <= 0:
            self.is_exhausted = True
            print("El jugador está exhausto y no puede moverse.")
            
    def recover_stamina(self):
        self.stamina += 5 
        
        if self.stamina > 100:
            self.stamina = 100
        
        if self.stamina >= 30 and self.is_exhausted:
            self.is_exhausted = False
            print("El jugador se ha recuperado y puede moverse de nuevo.")
    
    def move(self, dx, dy, weather_condition, surface_weight_tile):
        """
        Mueve al jugador y consume resistencia.
        """
        if not self.is_exhausted:
            self.x += dx
            self.y += dy
            self.consume_stamina(weather_condition)
        else:
            print("El jugador está agotado. Debe descansar para recuperarse.")
            
    def accept_delivery(self, delivery):
        """
        Acepta un nuevo pedido y lo añade al inventario si no excede el peso máximo.
        """
        delivery_weight = delivery.get("weight", 0)
        current_weight = self.get_total_weight()

        if current_weight + delivery_weight <= self.max_weight:
            self.inventory.append(delivery)# temporal se usara el metodo que este en inventory
            print(f"Pedido {delivery.get('id')} aceptado. Peso actual: {self.get_total_weight()}.")
            return True
        else:
            print("No se puede aceptar el pedido. Excede el peso máximo.")
            return False
        
    def dropoff_delivery(self, delivery, current_time):
        """
        Entrega un pedido, actualiza la reputación y los ingresos.
        
        Args:
            delivery (dict): El pedido a entregar.
            current_time (datetime): El tiempo actual del juego.
        """
        deadline = datetime.fromisoformat(delivery.get("deadline"))
        time_difference = (deadline - current_time).total_seconds()

        # Ajuste de reputación basado en puntualidad
        reputation_change = 0
        if time_difference >= 0:
            # Entrega a tiempo o temprana
            if time_difference > 0.20 * (deadline - datetime.fromisoformat(delivery.get("release_time"))).total_seconds():
                reputation_change = 5  # Entrega temprana (>= 20% antes) [cite: 148]
            else:
                reputation_change = 3  # Entrega a tiempo [cite: 146]
        else:
            # Entrega tardía
            time_late = abs(time_difference)
            if time_late <= 30:
                reputation_change = -2  # Tarde <= 30s [cite: 150]
            elif time_late <= 120:
                reputation_change = -5  # Tarde 31-120s [cite: 150]
            else:
                reputation_change = -10 # Tarde > 120s [cite: 150]

        # Actualizar reputación
        self.reputation += reputation_change
        if self.reputation < 20:
            print("Reputación por debajo de 20. ¡Has perdido!") [cite: 48]
        
        # Calcular y actualizar ingresos
        payout = delivery.get("payout", 0)
        if self.reputation >= 90:
            payout *= 1.05 # Bono del 5% por reputación alta 
            
        self.total_income += payout
        
        # Eliminar pedido del inventario
        if delivery in self.inventory:
            self.inventory.remove(delivery)
            print(f"Pedido {delivery.get('id')} entregado. Ganancias: {payout}. Nueva reputación: {self.reputation}.")
        
    def update_state(self):
        if (self.x, self.y) == self.last_position:
            #  recupera resistencia
            self.recover_stamina()
        else:
            # actualiza la última posición
            self.last_position = (self.x, self.y)
        pass
        
    def draw(self, screen):
        """
        Dibuja el jugador en la pantalla de Pygame.
        """
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)