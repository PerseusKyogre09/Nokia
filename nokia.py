import pygame
import sys

# Initialize Pygame
pygame.init()

# Wallpaper
width, height = 216, 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Nokia Interface')

# Load and scale the background images
background_img = pygame.image.load('assets/images/background.png')
background_img = pygame.transform.scale(background_img, (216, 261))

# Load Nokia font
try:
    nokia_font_large = pygame.font.Font('NokiaKokia.ttf', 20)
    nokia_font_medium = pygame.font.Font('NokiaKokia.ttf', 16)
    nokia_font_small = pygame.font.Font('NokiaKokia.ttf', 12)
except:
    nokia_font_large = pygame.font.Font(None, 24)
    nokia_font_medium = pygame.font.Font(None, 20)
    nokia_font_small = pygame.font.Font(None, 16)

# Screen states
SCREEN_HOME = 0
SCREEN_DIALER = 1
SCREEN_CONTACTS = 2
SCREEN_CALLING = 3

current_screen = SCREEN_HOME

# Load button images
call_button_img = pygame.image.load('assets/images/call_button.png')
call_button_img = pygame.transform.scale(call_button_img, (45, 45))

disconnect_button_img = pygame.image.load('assets/images/disconnect_button.png')
disconnect_button_img = pygame.transform.scale(disconnect_button_img, (45, 45))

select_button_img = pygame.image.load('assets/images/select_button.png')
select_button_img = pygame.transform.scale(select_button_img, (55, 55))

button_images = {
    "1": pygame.image.load('assets/images/button_1.png'),
    "2": pygame.image.load('assets/images/button_2.png'),
    "3": pygame.image.load('assets/images/button_3.png'),
    "4": pygame.image.load('assets/images/button_4.png'),
    "5": pygame.image.load('assets/images/button_5.png'),
    "6": pygame.image.load('assets/images/button_6.png'),
    "7": pygame.image.load('assets/images/button_7.png'),
    "8": pygame.image.load('assets/images/button_8.png'),
    "9": pygame.image.load('assets/images/button_9.png'),
    "0": pygame.image.load('assets/images/button_0.png'),
    "*": pygame.image.load('assets/images/button_star.png'),
    "#": pygame.image.load('assets/images/button_hash.png')
}

for key in button_images:
    button_images[key] = pygame.transform.scale(button_images[key], (45, 45))

dialpad_sounds = {
    "1": pygame.mixer.Sound('assets/audio/key/key_1.wav'),
    "2": pygame.mixer.Sound('assets/audio/key/key_2.wav'),
    "3": pygame.mixer.Sound('assets/audio/key/key_3.wav'),
    "4": pygame.mixer.Sound('assets/audio/key/key_4.wav'),
    "5": pygame.mixer.Sound('assets/audio/key/key_5.wav'),
    "6": pygame.mixer.Sound('assets/audio/key/key_6.wav'),
    "7": pygame.mixer.Sound('assets/audio/key/key_7.wav'),
    "8": pygame.mixer.Sound('assets/audio/key/key_8.wav'),
    "9": pygame.mixer.Sound('assets/audio/key/key_9.wav'),
    "0": pygame.mixer.Sound('assets/audio/key/key_0.wav'),
    "*": pygame.mixer.Sound('assets/audio/key/key_star.wav'),
    "#": pygame.mixer.Sound('assets/audio/key/key_hash.wav')
}

contacts_img = pygame.image.load('assets/images/contacts.png')
contacts_img = pygame.transform.scale(contacts_img, (70, 70))

# Sample contacts data
contacts_list = [
    {"name": "MOM", "number": "1234567890"},
    {"name": "DAD", "number": "1234567891"},
    {"name": "SISTER", "number": "1234567892"},
    {"name": "BROTHER", "number": "1234567893"},
    {"name": "FRIEND", "number": "1234567894"},
    {"name": "NEIGHBOUR", "number": "1234567895"},
    {"name": "ASH KETCHUM", "number": "1234567896"},
    {"name": "HARRY POTTER", "number": "1234567897"},
    {"name": "BEN TENNYSON", "number": "1234567898"},
    {"name": "GERALT OF RIVIA", "number": "1234567899"}
]

contacts_scroll = 0
selected_contact = 0

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BOTTOM_BACKGROUND = (35, 35, 35)
GLOW_COLOR = (0, 255, 100)
BUTTON_SHADOW = (20, 20, 20)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image = image
        self.font = pygame.font.Font(None, 24)
        self.is_pressed = False

    def draw(self, surface):
        shadow_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, BUTTON_SHADOW, shadow_rect, border_radius=5)
        
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, BLUE, self.rect, border_radius=5)
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

        if self.is_pressed:
            pygame.draw.rect(surface, GLOW_COLOR, self.rect, 3, border_radius=5)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

buttons = [
    Button(30, 340, 45, 45, "1", button_images["1"]), Button(85, 340, 45, 45, "2", button_images["2"]), Button(140, 340, 45, 45, "3", button_images["3"]),
    Button(30, 395, 45, 45, "4", button_images["4"]), Button(85, 395, 45, 45, "5", button_images["5"]), Button(140, 395, 45, 45, "6", button_images["6"]),
    Button(30, 450, 45, 45, "7", button_images["7"]), Button(85, 450, 45, 45, "8", button_images["8"]), Button(140, 450, 45, 45, "9", button_images["9"]),
    Button(30, 505, 45, 45, "*", button_images["*"]), Button(85, 505, 45, 45, "0", button_images["0"]), Button(140, 505, 45, 45, "#", button_images["#"]),
]

middle_buttons = {
    "call": Button(150, 285, 45, 45, "call", call_button_img),
    "disconnect": Button(20, 285, 45, 45, "disconnect", disconnect_button_img),
    "select": Button(80, 270, 55, 55, "select", select_button_img)
}

entered_number = ''
calling_number = ''
calling = False

# Scrolling text
scroll_offset = 0
scroll_timer = 0
scroll_speed = 0.01
scroll_delay = 120
def draw_scrolling_text(surface, text, font, color, rect, scroll_offset):
    """Draw text that scrolls horizontally if it's too long for the given rect"""
    text_surface = font.render(text, True, color)
    text_width = text_surface.get_width()
    rect_width = rect.width
    
    if text_width <= rect_width:
        surface.blit(text_surface, (rect.x, rect.y))
        return 0
    else:

        clip_rect = pygame.Rect(rect.x, rect.y, rect_width, rect.height)
        surface.set_clip(clip_rect)
        
        max_scroll = text_width + 20 
        current_scroll = scroll_offset % (max_scroll + rect_width)
        
        x_pos = rect.x + rect_width - current_scroll
        surface.blit(text_surface, (x_pos, rect.y))
        
        if x_pos + text_width < rect.x + rect_width:
            surface.blit(text_surface, (x_pos + max_scroll + rect_width, rect.y))
        
        surface.set_clip(None)
        return 1

def draw_home_screen(surface):
    import datetime
    
    # Get current time and date
    now = datetime.datetime.now()
    current_time = now.strftime("%H.%M")
    day_names = {"Mon": "MON", "Tue": "TUE", "Wed": "WED", "Thu": "THU", "Fri": "FRI", "Sat": "SAT", "Sun": "SUN"}
    month_names = {"Jan": "JAN", "Feb": "FEB", "Mar": "MAR", "Apr": "APR", "May": "MAY", "Jun": "JUN",
                   "Jul": "JUL", "Aug": "AUG", "Sep": "SEP", "Oct": "OCT", "Nov": "NOV", "Dec": "DEC"}
    
    day_name = day_names.get(now.strftime("%a"), now.strftime("%a").upper())
    month_name = month_names.get(now.strftime("%b"), now.strftime("%b").upper())
    current_date = f"{day_name} {now.strftime('%d')} {month_name}"
    
    # Time display
    time_text = nokia_font_large.render(current_time, True, WHITE)
    time_rect = time_text.get_rect(center=(108, 140))
    surface.blit(time_text, time_rect)
    
    # Date display
    date_text = nokia_font_small.render(current_date, True, WHITE)
    date_rect = date_text.get_rect(center=(108, 165))
    surface.blit(date_text, date_rect)
    
    # Nokia branding
    nokia_text = nokia_font_medium.render("NOKIA", True, WHITE)
    nokia_rect = nokia_text.get_rect(center=(108, 200))
    surface.blit(nokia_text, nokia_rect)
    
    # Signal indicator
    signal_text = nokia_font_small.render("IIII", True, WHITE)
    surface.blit(signal_text, (195, 10))

    # Battery indicator
    signal_text = nokia_font_small.render("OOOO", True, WHITE)
    surface.blit(signal_text, (5, 10))
    
    # Menu navigation hints
    menu_text = nokia_font_small.render("MENU", True, WHITE)
    surface.blit(menu_text, (5, 235))
    
    contacts_text = nokia_font_small.render("NAMES", True, WHITE)
    surface.blit(contacts_text, (145, 235))

def draw_dialer_screen(surface, number):
    # Title
    title_text = nokia_font_medium.render("ENTER NUMBER", True, WHITE)
    surface.blit(title_text, (10, 120))
    
    # Number display area
    display_rect = pygame.Rect(10, 145, 196, 25)
    pygame.draw.rect(surface, WHITE, display_rect)
    pygame.draw.rect(surface, BLACK, display_rect, 1)
    
    number_text = nokia_font_medium.render(number if number else "", True, BLACK)
    surface.blit(number_text, (15, 150))
    
    # Instructions
    if number:
        instruction_text = nokia_font_small.render("PRESS CALL TO DIAL", True, WHITE)
        surface.blit(instruction_text, (10, 180))

def draw_contacts_screen(surface):
    global scroll_offset, scroll_timer
    
    # Title
    title_text = nokia_font_medium.render("NAMES", True, WHITE)
    surface.blit(title_text, (10, 120))
    
    # Show current selection info
    selection_info = f"SELECTED: {selected_contact + 1}/{len(contacts_list)}"
    selection_text = nokia_font_small.render(selection_info, True, WHITE)
    surface.blit(selection_text, (10, 140))
    
    # Instructions
    instruction_text = nokia_font_small.render("2/8 NAVIGATE, CALL TO DIAL", True, WHITE)
    surface.blit(instruction_text, (10, 155))
    
    # Draw contacts list
    y_start = 175
    for i in range(4):
        contact_index = contacts_scroll + i
        if contact_index < len(contacts_list):
            contact = contacts_list[contact_index]
            
            if contact_index == selected_contact:
                highlight_rect = pygame.Rect(5, y_start + i * 22 - 2, 206, 22)
                pygame.draw.rect(surface, WHITE, highlight_rect)
                pygame.draw.rect(surface, BLACK, highlight_rect, 2)
                name_color = BLACK
                number_color = (50, 50, 50)
            else:
                name_color = WHITE
                number_color = (180, 180, 180)
            
            # Use scrolling text
            name_display = f"{contact_index + 1}. {contact['name']}"
            name_rect = pygame.Rect(10, y_start + i * 22, 196, 12)
            
            # Only scroll the selected contact's name
            if contact_index == selected_contact:
                draw_scrolling_text(surface, name_display, nokia_font_small, name_color, name_rect, scroll_offset)
            else:
                # For non-selected contacts, just draw normally
                name_text = nokia_font_small.render(name_display, True, name_color)
                surface.blit(name_text, (10, y_start + i * 22))
            
            # Draw phone number
            number_text = nokia_font_small.render(contact["number"], True, number_color)
            surface.blit(number_text, (10, y_start + i * 22 + 10))

# Function to display the calling screen
def draw_calling_screen(surface, number):
    global scroll_offset
    
    # Find contact name if it exists
    contact_name = number
    for contact in contacts_list:
        if contact["number"] == number:
            contact_name = contact["name"]
            break
    
    # Calling status
    calling_text = nokia_font_medium.render("CALLING...", True, WHITE)
    calling_rect = calling_text.get_rect(center=(108, 130))
    surface.blit(calling_text, calling_rect)
    
    name_rect = pygame.Rect(10, 155, 196, 20)
    draw_scrolling_text(surface, contact_name, nokia_font_large, WHITE, name_rect, scroll_offset)
    
    # Phone number
    if contact_name != number:
        number_text = nokia_font_small.render(number, True, WHITE)
        number_rect = number_text.get_rect(center=(108, 185))
        surface.blit(number_text, number_rect)
    
    # Instructions
    instruction_text = nokia_font_small.render("PRESS END TO HANG UP", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(108, 220))
    surface.blit(instruction_text, instruction_rect)



# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Handle number button presses
            for button in buttons:
                if button.is_clicked(mouse_pos) and current_screen != SCREEN_CALLING:
                    if current_screen == SCREEN_DIALER:
                        entered_number += button.text
                        dialpad_sounds[button.text].play()
                        button.is_pressed = True
                    elif current_screen == SCREEN_CONTACTS:
                        # Navigate contacts with number keys
                        if button.text.isdigit():
                            digit = int(button.text)
                            if digit == 2:  # Up
                                selected_contact = max(0, selected_contact - 1)
                                if selected_contact < contacts_scroll:
                                    contacts_scroll = selected_contact
                                dialpad_sounds[button.text].play()
                                button.is_pressed = True
                            elif digit == 8:  # Down
                                selected_contact = min(len(contacts_list) - 1, selected_contact + 1)
                                if selected_contact >= contacts_scroll + 4:
                                    contacts_scroll = selected_contact - 3
                                dialpad_sounds[button.text].play()
                                button.is_pressed = True
                            # Direct contact selection by number
                            elif digit >= 1 and digit <= 9:
                                if digit - 1 < len(contacts_list):
                                    selected_contact = digit - 1
                                    contacts_scroll = max(0, min(selected_contact, len(contacts_list) - 4))
                                    dialpad_sounds[button.text].play()
                                    button.is_pressed = True
                            elif digit == 0 and len(contacts_list) >= 10:
                                selected_contact = 9
                                contacts_scroll = max(0, min(selected_contact, len(contacts_list) - 4))
                                dialpad_sounds[button.text].play()
                                button.is_pressed = True
            
            # Handle middle button presses
            for button_key in middle_buttons:
                if middle_buttons[button_key].is_clicked(mouse_pos):
                    if button_key == "call":
                        if current_screen == SCREEN_HOME:
                            # Call button opens contacts from home
                            current_screen = SCREEN_CONTACTS
                        elif current_screen == SCREEN_CONTACTS:
                            # Call selected contact
                            calling_number = contacts_list[selected_contact]["number"]
                            current_screen = SCREEN_CALLING
                            pygame.mixer.Sound('assets/audio/ringing.mp3').play()
                        elif current_screen == SCREEN_DIALER and entered_number:
                            # Call entered number
                            calling_number = entered_number
                            current_screen = SCREEN_CALLING
                            entered_number = ''
                            pygame.mixer.Sound('assets/audio/ringing.mp3').play()
                    elif button_key == "disconnect":
                        if current_screen == SCREEN_CALLING:
                            current_screen = SCREEN_HOME
                        else:
                            current_screen = SCREEN_HOME  # Back to home
                    elif button_key == "select":
                        if current_screen == SCREEN_HOME:
                            current_screen = SCREEN_DIALER  # Select opens dialer
                        elif current_screen == SCREEN_CONTACTS:
                            current_screen = SCREEN_DIALER  # Select opens dialer from contacts
                            entered_number = contacts_list[selected_contact]["number"]
                        pygame.mixer.Sound('assets/audio/nokia_ringtone.mp3').play()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for button in buttons:
                button.is_pressed = False

    # Update scrolling animation
    scroll_timer += 1
    if scroll_timer > scroll_delay:
        scroll_offset += scroll_speed
        if scroll_offset > 2000:
            scroll_offset = 0

    # Draw the screen area with background
    screen.blit(background_img, (0, 0))
    
    # Draw black background for button area
    pygame.draw.rect(screen, BOTTOM_BACKGROUND, pygame.Rect(0, 261, width, height - 261))

    # Draw the appropriate screen content
    if current_screen == SCREEN_HOME:
        draw_home_screen(screen)
    elif current_screen == SCREEN_DIALER:
        draw_dialer_screen(screen, entered_number)
    elif current_screen == SCREEN_CONTACTS:
        draw_contacts_screen(screen)
    elif current_screen == SCREEN_CALLING:
        draw_calling_screen(screen, calling_number)

    # Draw the physical buttons
    for button in buttons:
        button.draw(screen)
    for button in middle_buttons.values():
        button.draw(screen)

    pygame.display.update()
