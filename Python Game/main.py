import pygame
import random
import sys
import os


# Initialising Pygame
pygame.init()

# Setting the Configurations for screen 
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
pygame.display.set_caption("Card Game")

# Defining colours for cards
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

card_width, card_height = 100, 150

# Loading Nottingham-themed image for card back
nottingham_back_image = pygame.image.load('/Users/prakharprakarshgmail.com/Desktop/Python Game/IMG_1211.JPG')  
nottingham_back_image = pygame.transform.scale(nottingham_back_image, (card_width, card_height))  

# Defining suits and ranks
suits = {'Hearts': RED, 'Diamonds': RED, 'Clubs': BLACK, 'Spades': BLACK}
ranks = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
power_cards = ['7', '8', 'Jack', 'Ace']  # Define power cards

def draw_card_back(position):
    # Creating surface for card back
    card_back_surface = pygame.Surface((card_width, card_height))
    
    # Blitting the Nottingham-themed image onto the card back surface
    card_back_surface.blit(nottingham_back_image, (0, 0))
    
    screen.blit(card_back_surface, position)

def draw_card(rank, suit, position, face_up=True):
    if not face_up:
        draw_card_back(position)
        return

    # Creating surface for card
    card_surface = pygame.Surface((card_width, card_height))
    card_surface.fill(WHITE)

    # Drawing card border
    pygame.draw.rect(card_surface, BLACK, card_surface.get_rect(), 1)

    # Setting font for text
    font = pygame.font.Font(None, 36)

    # Drawing ranks and suits on card
    color = suits[suit]
    rank_text = font.render(rank, True, color)
    suit_text = font.render(suit[0], True, color)

    # If it's a power card, change the background
    if rank in power_cards:
        card_surface.fill(RED if color == BLACK else BLUE)

    # Position and blit text onto card
    card_surface.blit(rank_text, (10, 10))
    card_surface.blit(suit_text, (card_width - 30, card_height - 30))

    # Blit the card_surface onto the main screen at the given position
    screen.blit(card_surface, position)



#loading card images

def load_card_images(card_folder_path):
    card_images = {}

    try:
        # Defining paths for the images
        back_card_image_path = os.path.join(card_folder_path, "/Users/prakharprakarshgmail.com/Desktop/Python Game/nottingham1.jpg")
        special_card_image_path = os.path.join(card_folder_path, "/Users/prakharprakarshgmail.com/Desktop/Python Game/nottingham2.jpg")

        # Loading and scaling the back of card image
        card_images["back"] = pygame.image.load(back_card_image_path).convert_alpha()
        card_images["back"] = pygame.transform.scale(card_images["back"], (100, 140))

        # Loading and scaling the special card image
        card_images["special_card"] = pygame.image.load(special_card_image_path).convert_alpha()
        card_images["special_card"] = pygame.transform.scale(card_images["special_card"], (100, 140))

        # Loading unique images for each card
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = range(6, 15)  
        for suit in suits:
            for value in values:
                
                
                card_path = "/Users/prakharprakarshgmail.com/Desktop/Python Game/nottingham2.jpg"
                

                
                card_image = pygame.image.load(card_path).convert_alpha()
                card_image = pygame.transform.scale(card_image, (100, 140))

                card_images[f"{suit}_{value}"] = card_image

        return card_images

    except pygame.error as e:  
        print(f"Error loading images: {e}")
        sys.exit(1)       


class Card:
    POWER_CARDS = {'7', '8', 'Jack', 'Ace'}  
 # Constructor initialising card with a suit, value, and image.
    def __init__(self, suit, value, image):
        self.suit = suit
        self.value = value
        self.image = image or pygame.Surface((100, 140))
    
    #Method for easier debugging and logging
    def __repr__(self):
        return f"{self.value} of {self.suit}"
 
    # Returns True if the card is a power card.
    def is_power_card(self):
        return self.value in Card.POWER_CARDS  

    def draw(self, surface, x, y):
        surface.blit(self.image, (x, y))
        
class Deck:
    def __init__(self, card_images):
        # Constructor for Deck. Takes a dictionary of card_images
        self.cards = self.create_deck(card_images)
        self.playing_pile = [] 
         
    # Creates a standard deck of cards using provided images.
    def create_deck(self, card_images):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = list(range(6, 15))  

        return [Card(suit, value, card_images.get(f"{suit}_{value}")) 
                for suit in suits for value in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        return None  

    def return_card_to_bottom(self, card):
        # Places a card at the bottom of the deck.
        self.cards.insert(0, card)

    def reshuffle_from_playing_pile(self):
         # Takes the playing pile (excluding the top card) and reshuffles it into the deck.
        if not self.cards and self.playing_pile:
            self.cards = self.playing_pile[:-1]  
            self.playing_pile = [self.playing_pile[-1]]  
            self.shuffle()
        

class Player:
     # Initialises a player, marking if they are human or AI.
    def __init__(self, is_human):
        self.hand = []
        self.is_human = is_human

    def draw_cards(self, deck, num_cards):
        for _ in range(num_cards):
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                
    def play_card(self, card, game):
        if card in self.hand:
            self.hand.remove(card)
            game.playing_pile.append(card)
            print(f"{self.name} plays {card}")

            if card.is_power_card():
                self.handle_special_card_effects(card, game)

            return True
        return False
    #logic for handling special cards
    def handle_special_card_effects(self, card, game):
        if card.value == '7':
            next_player = game.next_player()
            next_player.draw_cards(game.deck, 2)
            print("Next player draws 2 cards due to a Seven being played.")
        elif card.value == '8':
            game.skip_next_player()
            print("Next player misses a turn due to an Eight being played.")
        elif card.value == 'Jack':
            chosen_suit = self.choose_suit(game)
            game.chosen_suit = chosen_suit
            print(f"Suit changed to {chosen_suit} due to a Jack being played.")
        elif card.value == 'Ace':
            self.play_additional_card(game)

    def play_additional_card(self, game):
        if self.is_human:
            self.prompt_additional_card(game)
        else:
            self.play_additional_card_ai(game)
    #setting promt for additional cards
    def prompt_additional_card(self, game):
        print("You played an Ace! Select another card to play:")
        valid_cards = self.get_valid_cards(game)
        for index, card in enumerate(valid_cards):
            print(f"{index + 1}: {card}")

        choice = input("Enter the number of the card to play, or press Enter to skip: ")
        if choice.isdigit() and 0 < int(choice) <= len(valid_cards):
            selected_card = valid_cards[int(choice) - 1]
            self.play_card(selected_card, game)

    def play_additional_card_ai(self, game):
        valid_cards = self.get_valid_cards(game)
        if valid_cards:
           
            selected_card = random.choice(valid_cards)
            self.play_card(selected_card, game)
#checking logic for valid cards
    def get_valid_cards(self, game):
        
        if not game.playing_pile:
            
            return self.hand

        top_card = game.playing_pile[-1]
        valid_cards = []

       
        if game.chosen_suit:
            valid_cards = [card for card in self.hand if card.suit == game.chosen_suit]
        else:
            
            valid_cards = [card for card in self.hand if card.suit == top_card.suit or card.value == top_card.value]

        return valid_cards
    #setting logic for suit
    def choose_suit(self, game):
        
        if self.is_human:
            return self.prompt_for_suit(game)
        else:
            return random.choice(["Hearts", "Diamonds", "Clubs", "Spades"])

   
    def choose_suit(self):
       
        if self.is_human:
            return self.choose_suit_human()
        else:
            return self.choose_suit_ai()

    def choose_suit_human(self):
       
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        print("Choose a suit: [1] Hearts, [2] Diamonds, [3] Clubs, [4] Spades")

        while True:
            try:
                choice = int(input("Enter the number of the suit: "))
                if 1 <= choice <= 4:
                    return suits[choice - 1]
                else:
                    print("Invalid number. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
       
     

         
            if choice.isdigit() and 0 < int(choice) <= 4:
             return suits[int(choice) - 1]
            else:
             print("Invalid input. Defaulting to Hearts.")
            return "Hearts"

    
    
    def play_turn(self, top_card, game):
        playable_cards = self.find_playable_cards(top_card, game)
        if playable_cards:
            chosen_card = self.choose_card(playable_cards)
            self.play_card(chosen_card, game)
            game.handle_special_card_effects(chosen_card, self)
        else:
            self.draw_and_choose_card(game)

    

       
   

    def is_valid_play(self, card, game):
        top_card = game.playing_pile[-1] if game.playing_pile else None
        return card.suit == game.chosen_suit or card.suit == top_card.suit or card.value == top_card.value
    
    
    def make_decision(self, top_card, game):
        
       
        playable_cards = self.find_playable_cards(top_card, game)
        if playable_cards:
            chosen_card = random.choice(playable_cards)
            self.play_card(chosen_card, game.playing_pile)
            game.handle_special_card(chosen_card, self)
        else:
            self.draw_and_choose_card(game)
    
   

    def find_playable_cards(self, top_card, game):
        
        if game.chosen_suit:
            return [card for card in self.hand if card.suit == game.chosen_suit]
        return [card for card in self.hand if card.suit == top_card.suit or card.value == top_card.value]
    def draw_from_pile(self, pile, count, game):
        # Draw 'count' number of cards from the given pile
        for _ in range(count):
            card = pile.draw_card()
            if card:
                self.hand.append(card)

        

    def attempt_to_play(self, game):
        # Ensuring 'top_card' is defined. It should be the last card from the playing pile.
        top_card = game.playing_pile[-1] if game.playing_pile else None

        # Check for matching cards and play one
        if top_card:
            matching_cards = [card for card in self.hand if card.suit == top_card.suit or card.value == top_card.value]
            if game.chosen_suit:
                matching_cards = [card for card in self.hand if card.suit == game.chosen_suit]
            if matching_cards:
                chosen_card = matching_cards[0]  # Take the first matching card
                self.play_card(chosen_card, game)
                if chosen_card.value in ['7', '8', 'Jack', 'Ace']:  
                    self.handle_special_card_effects(chosen_card, game)
                if chosen_card.rank != 'Jack':  
                    game.chosen_suit = None
            else:
                # If no matching cards, draw two cards from the draw pile and try to play one
                self.draw_cards(game.draw_pile, 2)
                new_drawn_cards = self.hand[-2:]  # The last two cards that were drawn
                playable_card = [card for card in new_drawn_cards if card.suit == top_card.suit or card.value == top_card.value]
                if playable_card:
                    self.play_card(playable_card[0], game.playing_pile)
                    self.hand.remove(playable_card[0])  # Remove the played card from hand
                # If no card is played, return the drawn cards to the bottom of the draw pile
                for card in new_drawn_cards:
                    if card not in self.hand:
                        game.draw_pile.insert(0, card)  # Insert at the bottom of the pile 
    
class AIPlayer(Player):
    # Inherits from Player. Represents an AI player in the game.
    def make_decision(self, top_card, game):
        
        valid_cards = [card for card in self.hand if card.suit == top_card.suit or card.value == top_card.value]

        
        if game.chosen_suit:
            valid_cards = [card for card in self.hand if card.suit == game.chosen_suit]

        
        if valid_cards:
            
            power_cards = [card for card in valid_cards if card.value in [7, 8, 11, 14]] 
            card_to_play = random.choice(power_cards) if power_cards else random.choice(valid_cards)
            self.play_card(card_to_play, game.playing_pile)

            
            if card_to_play.value in [7, 8, 11, 14]:
                self.handle_special_card_effects(card_to_play, game)

            
            if card_to_play.value != 11:  
                game.chosen_suit = None
        else:
            
            self.draw_and_choose_card(game)

    def draw_and_choose_card(self, game):
        drawn_cards = [game.deck.draw_card() for _ in range(2)]
        
        chosen_card = self.ai_choose_card(drawn_cards, game)  
        self.hand.append(chosen_card)
        game.deck.return_card_to_bottom(drawn_cards[0] if chosen_card == drawn_cards[1] else drawn_cards[1])

    def ai_choose_card(self, drawn_cards, game):
        
        drawn_cards = [card for card in drawn_cards if self.is_valid_play(card, game)]
        
        return random.choice(drawn_cards)  

    
 #setting main game class having all the essential game rules.   
class Game:
    def __init__(self):
        
        pygame.init()
        self.need_suit_selection = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        card_folder_path = ""
        self.card_images = load_card_images(card_folder_path)
        self.deck = Deck(self.card_images)
        self.show_all_cards = False
        self.deck.shuffle()
        self.show_all_button = pygame.Rect(50, SCREEN_HEIGHT - 100, 150, 40)
        self.play_for_me_button = pygame.Rect(220, SCREEN_HEIGHT - 100, 150, 40)

        self.draw_pile = list(self.deck.cards)
        self.playing_pile = [self.draw_pile.pop()] if self.draw_pile else []

        self.players = [AIPlayer(False) if i > 0 else Player(True) for i in range(4)]
        self.current_player_index = 0
        self.chosen_suit = None

        self.show_all_button, self.play_for_me_button = self.create_buttons()
        self.suit_buttons = self.create_suit_buttons()

        self.initial_card_distribution()

    def display_buttons(self):
        self.draw_button(self.show_all_button, 'Show All Cards')
        self.draw_button(self.play_for_me_button, 'Play for Me')

    def display_draw_pile(self):
        if self.draw_pile:
            draw_pile_pos = (50, 50)  
            self.screen.blit(self.card_images["back"], draw_pile_pos)

    def display_playing_pile(self):
        if self.playing_pile:
            playing_pile_pos = (200, 50) 
            top_card = self.playing_pile[-1]
            top_card.draw(self.screen, playing_pile_pos[0], playing_pile_pos[1])

    def display_opponents_hands(self):
        for i in range(1, 4):  
            opponent_hand_pos = (50, 100 + i * 30)
            self.screen.blit(self.card_images["back"], opponent_hand_pos)
    
    def toggle_show_all_cards(self):
        
        self.show_all_cards = not self.show_all_cards

    def play_for_me(self):
        
        if self.is_human_turn():
            current_player = self.players[self.current_player_index]
            current_player.make_decision(self.playing_pile[-1], self)
            self.advance_turn()

    def next_player(self):
        
        return self.players[(self.current_player_index + 1) % len(self.players)]

    def skip_next_player(self):
        
        self.current_player_index = (self.current_player_index + 2) % len(self.players)

   
    def prompt_for_suit(self):
        
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        print("Choose a suit: Hearts, Diamonds, Clubs, Spades")
        chosen_suit = input("Enter suit: ").capitalize()
        while chosen_suit not in suits:
            print("Invalid suit. Choose from Hearts, Diamonds, Clubs, Spades.")
            chosen_suit = input("Enter suit: ").capitalize()
        return chosen_suit

    def allow_additional_card(self, player):
        
        if player.hand:
            print("Choose an additional card to play or press Enter to skip:")
            for index, card in enumerate(player.hand):
                print(f"{index + 1}: {card}")

            choice = input("Enter card number or press Enter to skip: ")
            if choice.isdigit() and 0 < int(choice) <= len(player.hand):
                additional_card = player.hand[int(choice) - 1]
                if additional_card.suit == self.playing_pile[-1].suit or additional_card.value == self.playing_pile[-1].value:
                    player.play_card(additional_card, self.playing_pile)
                    return True
        return False

    def handle_mouse_click(self, event):
        
        if self.show_all_button.collidepoint(event.pos):
            self.toggle_show_all_cards()
        elif self.play_for_me_button.collidepoint(event.pos) and self.is_human_turn():
            self.play_for_me()
        else:
            self.handle_card_click(event.pos)

    def handle_card_click(self, mouse_pos):
        
        if not self.is_human_turn():
            return  

        human_player = self.players[0]  
        for card in human_player.hand:
            if self.is_card_clicked(card, mouse_pos):
                if self.can_play_card(card):
                    self.play_card(card)
                    self.advance_turn()
                    break
     
    def is_game_over(self):
        
        for player in self.players:
            if not player.hand:
                self.display_winner_message(player)
                return True
        return False

    def display_winner_message(self, winner):
        winner_text = f"Congratulations! {winner.name} has won the game!"
        font = pygame.font.SysFont(None, 36)
        text_render = font.render(winner_text, True, WHITE)
        self.screen.blit(text_render, (100, SCREEN_HEIGHT // 2))
        self.game_over = True
    

    def is_human_turn(self):
        
        return self.players[self.current_player_index].is_human

    

    
     
    def get_card_at_pos(self, pos):
        
        card_width, card_height = 100, 140  
        for i, card in enumerate(self.players[0].hand):
            card_rect = pygame.Rect(50 + i * 30, SCREEN_HEIGHT - 150, card_width, card_height)
            if card_rect.collidepoint(pos):
                return card
        return None 
            
    def initial_card_distribution(self):
        power_cards = ['7', '8', '11', '14']
        for player in self.players:
            while True:
                player.draw_cards(self.deck, 7)
                if sum(card.value in power_cards for card in player.hand) < 4:
                    break
                else:
                    self.deck.return_cards(player.hand)
     
    def can_play_card(self, player_card):
        
        top_card = self.playing_pile[-1] if self.playing_pile else None
        if not top_card:
            return False  
        
        
        if self.chosen_suit:
            return player_card.suit == self.chosen_suit
        
        
        return player_card.suit == top_card.suit or player_card.value == top_card.value
           

    def play_round(self):
        while not self.is_game_over():
            current_player = self.players[self.current_player_index]
            top_card = self.playing_pile[-1]

            current_player.play_turn(top_card, self)

            if not self.draw_pile:
                self.reshuffle_draw_pile()

            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def is_game_over(self):
        return any(not player.hand for player in self.players)

    def reshuffle_draw_pile(self):
        if not self.draw_pile and len(self.playing_pile) > 1:
            
            top_card = self.playing_pile.pop()
            
            self.draw_pile = self.playing_pile
            random.shuffle(self.draw_pile)
            self.playing_pile = [top_card]

     
    def draw_button(self, button, text):
        pygame.draw.rect(self.screen, WHITE, button)
        font = pygame.font.SysFont(None, 24)
        text_render = font.render(text, True, BLACK)
        self.screen.blit(text_render, (button.x + 5, button.y + 5))

    def handle_mouse_click(self, event):
        if self.play_for_me_button.collidepoint(event.pos):
            self.play_for_me()

    
    
    def display_all_players_cards(self):
      card_width, card_height = 100, 140 
      for player_index, player in enumerate(self.players):
        for card_index, card in enumerate(player.hand):
            
            card_x = 50 + (card_index % 10) * (card_width + 10)
            card_y = 50 + (player_index * card_height) + (card_index // 10 * 20)
            
            card.draw(self.screen, card_x, card_y)



    def calculate_card_position(self, player_index, card_index):
        
        
        return (50 + card_index * 30, 50 + player_index * 50)
    
    def run(self):
        running = True
        while running:
         for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False


        self.update_game_state()
            
            # Drawing
        self.render_game()

            # Update the display
        pygame.display.flip()

        # Clean up and close the game
        pygame.quit()
        sys.exit()



    # Clear screen
    screen.fill(GRAY)

    # Draw cards (example usage of draw_card)
    draw_card('Ace', 'Hearts', (50, 50))
    draw_card('King', 'Spades', (200, 50), face_up=False)

    # Update the display
    pygame.display.flip()

    pygame.quit()
      
    def render_game(self):
        self.screen.fill(BLACK)  

       
        self.display_draw_pile()  
        self.display_playing_pile()  
        self.display_opponents_hands()  
        self.display_player_cards()  

        
        if self.show_all_cards:
            self.display_all_players_cards()

       
        self.display_buttons()
     
     
    def handle_mouse_events(self, event):
      if self.players[self.current_player_index].is_human:
        self.handle_mouse_click(event)
      if self.need_suit_selection:
        self.handle_suit_selection(event)
    
    
     
     
 
    def display_player_cards(self):
      human_player = self.players[0]  
      for index, card in enumerate(human_player.hand):
        card_x, card_y = 50 + index * 30, SCREEN_HEIGHT - 150
        card.draw(self.screen, card_x, card_y)

    def display_draw_pile(self):
      if self.draw_pile:
        self.screen.blit(self.card_images["back"], (50, 50))  
        
    def create_buttons(self):
        
        show_all_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 150, 40)
        play_for_me_button_rect = pygame.Rect(220, SCREEN_HEIGHT - 100, 150, 40)
        
        
        return show_all_button_rect, play_for_me_button_rect
    
    def create_suit_buttons(self):
       
        button_size = (60, 30)
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        suit_buttons = {}

        for i, suit in enumerate(suits):
            button_position = (50 + i * 70, SCREEN_HEIGHT - 100)  
            suit_buttons[suit] = pygame.Rect(button_position, button_size)

        return suit_buttons
    
    def update_game_state(self):
       
        if not self.players[self.current_player_index].hand:
            self.display_winner_message(self.players[self.current_player_index])
            return True  

        
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return False  

    def play_ai_turn(self, player):
     top_card = self.playing_pile[-1] if self.playing_pile else None
     if isinstance(player, AIPlayer) and top_card:
        player.make_decision(top_card, self)

    def check_for_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player
        return None


    def prepare_next_turn(self):
     if not self.deck.cards:
        self.reshuffle_draw_pile()
     self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def end_game(self):
     pygame.time.wait(6000)
     pygame.quit()
     sys.exit()

    def initial_card_distribution(self):
     power_cards = ['7', '8', 'Jack', 'Ace']
     for player in self.players:
        while True:
            player.draw_cards(self.deck, 7)
            power_card_count = sum(card.value in power_cards for card in player.hand)
            if power_card_count < 4:
                break  
            else:
                
                self.deck.return_cards(player.hand)
                player.hand.clear()
                self.deck.shuffle()


    def deal_initial_hand(self, player, hand_size):
     while True:
        player.hand = [self.deck.draw_card() for _ in range(hand_size)]
        if self.count_power_cards(player.hand) < 4:
            break
        self.deck.return_cards(player.hand)
        self.deck.shuffle()


    def count_power_cards(self, hand):
     power_cards = [7, 8, 11, 14]
     return sum(card.value in power_cards for card in hand)
    
    
    def get_card_at_pos(self, pos):
     player_hand = self.players[self.current_player_index].hand
     return next((card for card in player_hand if card.is_clicked(pos)), None)

    def can_play_card(self, player_card):
     top_card = self.get_top_card()
     return player_card.suit == self.chosen_suit or \
           top_card.suit == player_card.suit or \
           top_card.value == player_card.value

    def get_top_card(self):
        return self.playing_pile[-1] if self.playing_pile else None

    def play_card(self, card):
     self.players[self.current_player_index].play_card(card, self.discard_pile)
     self.handle_special_card(card)

    def advance_turn(self):
     self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def handle_special_card(self, card):
     if card.value in self.special_card_effects:
        self.special_card_effects[card.value](self)

    def handle_seven(self):
     self.players[self.next_player()].draw(self.deck, 2)

    def handle_eight(self):
     self.advance_turn()  

    def handle_jack(self):
     self.chosen_suit = self.choose_suit()  

    def handle_ace(self):
        additional_card = self.players[self.current_player_index].play_additional_card()
        if additional_card:
         self.discard_pile.append(additional_card)
         self.handle_special_card(additional_card)

    def next_player(self):
     return (self.current_player_index + 1) % len(self.players)
 
    
   
        


    def display_draw_pile(self):
        if self.draw_pile:
            self.screen.blit(self.card_images["back"], (50, 50))  

    def display_playing_pile(self):
        if self.playing_pile:
            top_card = self.playing_pile[-1]
            top_card.draw(self.screen, 200, 50)  

    def display_opponents_hands(self):
        for i in range(1, 4):  
            opponent_hand_pos = (50, 100 + i * 30)
            self.screen.blit(self.card_images["back"], opponent_hand_pos)
    
    
    def display_all_players_cards(self):
        start_x = 50  
        start_y = 50  
        card_width = 71  
        card_height = 96  
        margin = 10  

        for player_index, player in enumerate(self.players):
            for card_index, card in enumerate(player.hand):
                card_x = start_x + (card_width + margin) * card_index
                card_y = start_y + (player_index * (card_height + margin))
                card.draw(self.screen, card_x, card_y)

            player_text = f"Player {player_index + 1}" if player.is_human else f"AI Player {player_index}"
            font = pygame.font.SysFont(None, 24)
            text_render = font.render(player_text, True, WHITE)
            self.screen.blit(text_render, (start_x, card_y - margin))
    
        for player_index, player in enumerate(self.players):
         for card_index, card in enumerate(player.hand):
            
            card_x = start_x + (card_width + margin) * card_index
            card_y = start_y + (player_index * (card_height + margin))
            
            
            card.draw(self.screen, card_x, card_y)
        
        
        player_text = f"Player {player_index + 1}" if player.is_human else f"AI Player {player_index}"
        font = pygame.font.SysFont(None, 24)
        text_render = font.render(player_text, True, WHITE)
        self.screen.blit(text_render, (start_x, card_y - margin))

    def display_draw_and_playing_pile(self):
    
     self.screen.blit(self.card_images["back"], (50, 50))

    
     if self.playing_pile:
        top_card = self.playing_pile[-1]
        top_card.draw(self.screen, 200, 50)  


    def draw_button(self, button, text):
     pygame.draw.rect(self.screen, WHITE, button)
     button_text = pygame.font.SysFont('Arial', 20).render(text, True, BLACK)
     self.screen.blit(button_text, (button.x + 10, button.y + 5))

    def display_suit_buttons(self):
     for suit, rect in self.suit_buttons.items():
        pygame.draw.rect(self.screen, WHITE, rect)
        suit_text = pygame.font.SysFont('Arial', 20).render(suit, True, BLACK)
        self.screen.blit(suit_text, (rect.x + 10, rect.y + 5))





if __name__ == "__main__":
    game = Game()
    game.run()
    input("Press any key to continue")

