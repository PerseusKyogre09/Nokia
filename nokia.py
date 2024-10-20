import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display with wallpaper width and height
width, height = 216, 480  # Adjusted screen dimensions
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Nokia Interface')

# Load and scale the top half wallpaper
top_wallpaper = pygame.image.load('data/nokia_wallpaper.png')  # Load the wallpaper
top_wallpaper = pygame.transform.scale(top_wallpaper, (216, 261))  # Scale down to fit top half

# Load button images (for middle buttons and number buttons)
call_button_img = pygame.image.load('data/call_button.png')
call_button_img = pygame.transform.scale(call_button_img, (40, 40))  # Resize call button to fit

disconnect_button_img = pygame.image.load('data/disconnect_button.png')
disconnect_button_img = pygame.transform.scale(disconnect_button_img, (40, 40))  # Resize disconnect button

select_button_img = pygame.image.load('data/select_button.png')
select_button_img = pygame.transform.scale(select_button_img, (55, 55))  # Resize select button

# Load images for number buttons (1-9, 0, *, #)
button_images = {
    "1": pygame.image.load('data/button_1.png'),
    "2": pygame.image.load('data/button_2.png'),
    "3": pygame.image.load('data/button_3.png'),
    "4": pygame.image.load('data/button_4.png'),
    "5": pygame.image.load('data/button_5.png'),
    "6": pygame.image.load('data/button_6.png'),
    "7": pygame.image.load('data/button_7.png'),
    "8": pygame.image.load('data/button_8.png'),
    "9": pygame.image.load('data/button_9.png'),
    "0": pygame.image.load('data/button_0.png'),
    "*": pygame.image.load('data/button_star.png'),
    "#": pygame.image.load('data/button_hash.png')
}

# Resize number button images to fit smaller buttons (reduce size)
for key in button_images:
    button_images[key] = pygame.transform.scale(button_images[key], (40, 40))

# Load dialpad sounds for each number (assuming these sound files are available in your data folder)
dialpad_sounds = {
    "1": pygame.mixer.Sound('audio/key/key_1.wav'),
    "2": pygame.mixer.Sound('audio/key/key_2.wav'),
    "3": pygame.mixer.Sound('audio/key/key_3.wav'),
    "4": pygame.mixer.Sound('audio/key/key_4.wav'),
    "5": pygame.mixer.Sound('audio/key/key_5.wav'),
    "6": pygame.mixer.Sound('audio/key/key_6.wav'),
    "7": pygame.mixer.Sound('audio/key/key_7.wav'),
    "8": pygame.mixer.Sound('audio/key/key_8.wav'),
    "9": pygame.mixer.Sound('audio/key/key_9.wav'),
    "0": pygame.mixer.Sound('audio/key/key_0.wav'),
    "*": pygame.mixer.Sound('audio/key/key_star.wav'),
    "#": pygame.mixer.Sound('audio/key/key_hash.wav')
}

# Load the contacts image
contacts_img = pygame.image.load('data/contacts.png')
contacts_img = pygame.transform.scale(contacts_img, (70, 70))  # Resize the contacts image to be slightly bigger

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BOTTOM_BACKGROUND = (50, 50, 50)  # Color for the bottom half background
GLOW_COLOR = (255, 255, 0)  # Color for glowing effect (yellow)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image = image
        self.font = pygame.font.Font(None, 24)  # Smaller font size to match smaller buttons
        self.is_pressed = False  # State to track if the button is pressed

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)  # Draw the image instead of text
        else:
            pygame.draw.rect(surface, BLUE, self.rect)
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

        # Add glowing effect if the button is pressed
        if self.is_pressed:
            pygame.draw.rect(surface, GLOW_COLOR, self.rect, 3)  # Draw a glowing border

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Resized buttons to fit smaller screen
buttons = [
    Button(25, 320, 40, 40, "1", button_images["1"]), Button(88, 320, 40, 40, "2", button_images["2"]), Button(151, 320, 40, 40, "3", button_images["3"]),
    Button(25, 380, 40, 40, "4", button_images["4"]), Button(88, 380, 40, 40, "5", button_images["5"]), Button(151, 380, 40, 40, "6", button_images["6"]),
    Button(25, 440, 40, 40, "7", button_images["7"]), Button(88, 440, 40, 40, "8", button_images["8"]), Button(151, 440, 40, 40, "9", button_images["9"]),
    Button(25, 500, 40, 40, "*", button_images["*"]), Button(88, 500, 40, 40, "0", button_images["0"]), Button(151, 500, 40, 40, "#", button_images["#"]),
]

# Middle buttons (call, disconnect, select)
middle_buttons = {
    "call": Button(151, 275, 40, 40, "call", call_button_img),
    "disconnect": Button(25, 275, 40, 40, "disconnect", disconnect_button_img),
    "select": Button(81, 257, 40, 40, "select", select_button_img)
}

# Placeholder for entered phone number
entered_number = ''
calling = False  # Flag to indicate whether calling is in progress

# Function to draw the phone number at the top
def draw_phone_number(surface, number):
    font = pygame.font.Font(None, 36)  # Slightly smaller font size
    number_surface = font.render(number, True, WHITE)
    surface.blit(number_surface, (20, 150))  # Adjust position for the smaller screen

# Function to display the "Calling..." message and contacts image
def draw_calling_message(surface):
    font = pygame.font.Font(None, 36)
    calling_text = font.render("Calling...", True, WHITE)
    screen.blit(calling_text, (60, 180))  # Draw "Calling..." text on the screen
    screen.blit(contacts_img, (73, 110))  # Draw contacts image above the "Calling..." text

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for button in buttons:
                if button.is_clicked(mouse_pos) and not calling:
                    entered_number += button.text
                    dialpad_sounds[button.text].play()  # Play sound for the pressed button
                    button.is_pressed = True  # Activate glow effect
            for button_key in middle_buttons:
                if middle_buttons[button_key].is_clicked(mouse_pos):
                    if button_key == "call" and entered_number:
                        calling = True  # Set flag to true to show calling screen
                        entered_number = ''  # Clear the entered number
                        pygame.mixer.Sound('audio/ringing.mp3').play()
                    elif button_key == "disconnect":
                        calling = False  # Reset the call state
                    elif button_key == "select":
                        pygame.mixer.Sound('audio/nokia_ringtone.mp3').play()  # Play ringtone sound

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for button in buttons:
                button.is_pressed = False  # Reset glow effect when mouse button is released

    # Fill the background with two halves
    screen.blit(top_wallpaper, (0, 0))  # Wallpaper at the top
    pygame.draw.rect(screen, BOTTOM_BACKGROUND, pygame.Rect(0, 261, width, height - 261))  # Bottom background

    # Draw the buttons and phone number
    for button in buttons:
        button.draw(screen)
    for button in middle_buttons.values():
        button.draw(screen)

    if calling:
        draw_calling_message(screen)  # Draw calling screen
    else:
        draw_phone_number(screen, entered_number)  # Draw the entered phone number

    pygame.display.update()
