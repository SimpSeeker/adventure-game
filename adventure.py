# Starter code for an adventure game.
# Inspired by David Johnson for CS 1400 University of Utah.
# Written by Jim de St. Germain

# Add your Header Doc String Here
#
#

import sys, pygame, math
from pygame import Vector2


def pixel_collision(game_objects, item1, item2):
    """
        Given two game objects (by name), check if the non-transparent pixels of
        one mask contacts the non-transparent pixels of the other.
    :param game_objects: the dictionary of all items in the game
    :param item1 (string): the name of the first game object that is being compared to the second
    :param item2 (string): the name of the second game object
    :return: (boolean) True if they overlap
    """
    pos1 = game_objects[item1]["pos"]
    pos2 = game_objects[item2]["pos"]
    mask1 = game_objects[item1]["mask"]
    mask2 = game_objects[item2]["mask"]

    # shift images back to 0,0 for collision detection
    pos1_temp = pos1 - Vector2(mask1.get_size()) / 2
    pos2_temp = pos2 - Vector2(mask2.get_size()) / 2
    offset = pos2_temp - pos1_temp

    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, offset)  # , offset )
    return overlap is not None


def draw_marker(screen, position):
    """
    Simple helper to draw a location on the screen so you can
    see if your thoughts of what a position match Python's "thoughts".
    :param screen:  surface you are drawing on
    :param position: Vector2 : location to draw a circle
    :return: -NA-
    """
    pygame.draw.circle(screen, "black", position, 5)


def draw_image_centered(screen, image, pos):
    """
    On the screen, draw the given image **centered** on the given position.
    :param screen:  what we are drawing on
    :param image:   what we are drawing
    :param pos: Vector2 :  where to center the image
    :return: -NA-
    """
    containing_rectangle = image.get_rect()
    screen.blit(image, (pos.x - containing_rectangle.width / 2, pos.y - containing_rectangle.height / 2))


def add_game_object(game_objects, name, width, height, x, y):
    """
    Create and add a new game object (based on the provided params) to the game_objects dictionary.
    :param game_objects: dictionary of all objects in the game
    :param name:    the name of the object AND the image file
    :param width:   how wide to make the object/image in the game
    :param height:  how tall to make the object/image in the game
    :param x:       where in the game the object is
    :param y:       where in the game the object is
    :return: -NA-  The game_objects dictionary will have the new object inserted based on the name
    """
    information = {}
    game_objects[name] = information  # put the new object in the dictionary

    # Read the image file name. Note: I have put all of my images in a subfolder named "images"
    image = pygame.image.load("images/" + name + ".png")  # .convert_alpha()

    information["name"] = name
    information["pos"] = Vector2(x, y)
    information["image"] = pygame.transform.smoothscale(image, (width, height))
    information["mask"] = pygame.mask.from_surface(information["image"])
    information["visible"] = True
    information["initial_pos"] = Vector2(x, y)

    # Note: this code does not support animations.  If you want animations (and you should)
    #       you will need to update it based on the lab code!

def game_over(game_objects, screen):
    """
    Display the game over screen and wait for user input.
    :param game_objects, screen:
    :return: -NA-
    """

    # Fill the screen with red
    screen.fill((255, 0, 100))

    # Show the cursor when collided
    pygame.mouse.set_visible(True)

    # Display game over message
    font = pygame.font.SysFont('helvetica', 36)
    game_over_text = font.render("You got this!", True, (255, 255, 255))
    screen.blit(game_over_text, (300, 200))
    game_over_text_option = font.render("Use mouse to select choice", True, (0, 75, 75))
    screen.blit(game_over_text_option, (175, 275))

    # Display options
    retry_text = font.render("Try Again", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(retry_text, (250, 350))
    screen.blit(quit_text, (450, 350))
    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 <= x <= 400 and 350 <= y <= 380:  # Try Again clicked
                    return True
                elif 450 <= x <= 510 and 350 <= y <= 380:  # Quit clicked
                    return False


def level1():
    # Set up the Level by placing the objects of interest
    game_objects = {}

    def restart_game_level1(game_objects):
        for object in game_objects.values():
            init_pos = Vector2(object["initial_pos"].x, object["initial_pos"].y)
            object["pos"] = init_pos
            game_objects["clash_crown"]["visible"] = True
            game_objects["king_tower"]["visible"] = True
            game_objects["blue_flag"]["visible"] = False
            game_objects["guard_1_right"]["visible"] = False
            game_objects["guard_2_right"]["visible"] = False
            game_objects["guard_1_left"]["visible"] = False
            game_objects["guard_2_left"]["visible"] = False
            game_objects["guard_3_right"]["visible"] = False

    #
    # Create the Game Objects and add them to the game_objects dictionary
    #
    # IMPORTANT: You must replace these images with your own.
    # IMPORTANT: the image file name is the name used for the item
    add_game_object(game_objects, "arena1", 800, 600, 400, 300)
    add_game_object(game_objects, "clash_crown", 40, 40, 470, 210)
    add_game_object(game_objects, "king_tower", 70, 80, 400, 120)
    add_game_object(game_objects, "bridge_arena1_left", 60, 50, 336, 320)
    add_game_object(game_objects, "bridge_arena1_right", 60, 50, 460, 320)
    add_game_object(game_objects, "mini_pekka", 35, 25, 400, 450)
    add_game_object(game_objects, "blue_flag", 30, 30, 400, 150)
    add_game_object(game_objects, "guard_1_right", 20, 30, 450, 250)
    add_game_object(game_objects, "guard_2_right", 20, 30, 500, 250)
    add_game_object(game_objects, "guard_1_left", 20, 30, 330, 200)
    add_game_object(game_objects, "guard_2_left", 20, 30, 360, 250)
    add_game_object(game_objects, "guard_3_right", 20, 30, 460, 200)
    add_game_object(game_objects, "brick_wall1", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall2", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall3", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall4", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall5", 250, 200, 420, 235)

    # create the window based on the map size
    screen = pygame.display.set_mode(game_objects["arena1"]["image"].get_size())

    # The frame count records how many times the program has
    # gone through the main loop.  Normally you don't need this information
    # but if you want to do an animation, you can use this variable to
    # indicate which sprite frame to draw
    frame_count = 0

    # Get a font to use to write on the screen.
    myfont = pygame.font.SysFont('helvetica', 25, 4)

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # "start" the game when the mouse moves over the player
    is_started = False

    # has the player found (moved on top of) the key to the door?
    crown_found = False

    # are the guards from level 1 visible
    game_objects["guard_1_right"]["visible"] = False
    game_objects["guard_2_right"]["visible"] = False
    game_objects["guard_1_left"]["visible"] = False
    game_objects["guard_2_left"]["visible"] = False
    game_objects["guard_3_right"]["visible"] = False
    game_objects["brick_wall1"]["visible"] = True
    game_objects["brick_wall2"]["visible"] = False
    game_objects["brick_wall3"]["visible"] = False
    game_objects["brick_wall4"]["visible"] = False
    game_objects["brick_wall5"]["visible"] = False

    visible_right = False
    visible_left = False

    def move_guard_horizontal(guard_obj, max_range, movement):
        """
        Function to handle movement logic for guards.
        :param guard_obj: Dictionary containing guard object information
        :param max_range: Maximum movement range for the guard
        :param movement: Movement vector for the guard
        """
        guard_obj["pos"] += movement

        # Check if guard reached the maximum range, reverse their movement direction
        if (guard_obj["pos"] - guard_obj["initial_pos"]).length() > max_range:
            movement *= -1  # Reverse direction
        return movement

    # Define movement variables for guards
    guard_1_right_movement = Vector2(1, 0)  # Movement direction for guard 1 (right)
    guard_2_right_movement = Vector2(-1, 0)  # Movement direction for guard 2 (left)
    guard_1_right_max_range = 5  # Maximum movement range for guard 1
    guard_2_right_max_range = 5  # Maximum movement range for guard 2

    # Update guard positions using the move_guard function
    guard_1_right_movement = move_guard_horizontal(game_objects["guard_1_right"], guard_1_right_max_range,
                                                   guard_1_right_movement)
    guard_2_right_movement = move_guard_horizontal(game_objects["guard_2_right"], guard_2_right_max_range,
                                                   guard_2_right_movement)

    def move_guard_vertically(guard_obj, max_range, movement):
        """
        Function to handle vertical movement logic for guards.
        :param guard_obj: Dictionary containing guard object information
        :param max_range: Maximum movement range for the guard
        :param movement: Movement vector for the guard
        """
        guard_obj["pos"] += movement

        # Check if guard reached the maximum range, reverse their movement direction
        if abs((guard_obj["pos"].y - guard_obj["initial_pos"].y)) > max_range:
            movement *= -1  # Reverse direction
        return movement

    guard_1_left_movement = Vector2(0, 1)  # Movement direction for guard 1 left (down)
    guard_2_left_movement = Vector2(0, -1)  # Movement direction for guard 2 left (up)
    guard_1_left_max_range = 5  # Maximum movement range for guard 1 left
    guard_2_left_max_range = 5  # Maximum movement range for guard 2 left

    # Update guard positions using the move_guard_vertically function
    guard_1_left_movement = move_guard_vertically(game_objects["guard_1_left"], guard_1_left_max_range,
                                                  guard_1_left_movement)
    guard_2_left_movement = move_guard_vertically(game_objects["guard_2_left"], guard_2_left_max_range,
                                                  guard_2_left_movement)

    # This is the main game loop. In it, we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while True:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pixel_collision(game_objects, "mini_pekka", "arena1"):
            is_alive = False
            pygame.mouse.set_visible(True)
            if not game_over(game_objects, screen):
                pygame.quit()
                sys.exit()
            else:
                restart_game_level1(game_objects)
                is_alive = True
                is_started = False
                crown_found = False
                game_objects["clash_crown"]["visible"] = True
                game_objects["king_tower"]["visible"] = True
                game_objects["blue_flag"]["visible"] = False

        game_objects["brick_wall1"]["visible"] = True

        if pixel_collision(game_objects, "mini_pekka", "brick_wall1"):
            is_alive = False
            pygame.mouse.set_visible(True)
            if not game_over(game_objects, screen):
                pygame.quit()
                sys.exit()
            else:
                restart_game_level1(game_objects)
                is_alive = True
                is_started = False
                crown_found = False
                game_objects["clash_crown"]["visible"] = True
                game_objects["king_tower"]["visible"] = True
                game_objects["blue_flag"]["visible"] = False

        # Makes new text appear when player collides with bridges
        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_right"):
            label_1 = myfont.render("Hmm, what's on the other side of those bridges?", True, (255, 255, 255))
            screen.blit(label_1, (20, 20))

            label_2 = myfont.render("Ohhhhh, that's whats on the other side of the bridges", True, (255, 255, 255))
            screen.blit(label_2, (20, 20))

        # Check for game logic situation
        if is_alive:
            if not is_started:
                if not is_started and Vector2(pygame.mouse.get_pos()).distance_to(
                        game_objects["mini_pekka"]["pos"]) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible(False)

        # Position the player to the mouse location
        if is_alive:
            if is_started:
                player = game_objects["mini_pekka"]
                player["pos"] = Vector2(pygame.mouse.get_pos())
            else:
                # if the mouse comes near the player, start the game
                if Vector2(pygame.mouse.get_pos()).distance_to(game_objects["mini_pekka"]["pos"]) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible(False)

        # Clear the map by putting a background gray across the screen
        screen.fill((150, 150, 150))  # This helps check if the image path is transparent

        # Keep the flag hidden until the crown is found.
        if crown_found == False:
            game_objects["blue_flag"]["visible"] = False

        # Check for game logic situation
        if not crown_found and pixel_collision(game_objects, "mini_pekka", "clash_crown"):
            game_objects["clash_crown"]["visible"] = False
            game_objects["king_tower"]["visible"] = False
            game_objects["blue_flag"]["visible"] = True
            crown_found = True

        # Draw the game objects
        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered(screen, object["image"], object["pos"])

        # Added logic to add arrow keys and WASD keys to move the player.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game_objects["mini_pekka"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game_objects["mini_pekka"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, 5)

        if pixel_collision(game_objects, "mini_pekka", "guard_1_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level1(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_2_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level1(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_1_left") and visible_left:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level1(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_2_left") and visible_left:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level1(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_right"):
            visible_right = True
            game_objects["guard_1_right"]["visible"] = True
            game_objects["guard_2_right"]["visible"] = True

        # If both guards are visible, move them
        if game_objects["guard_1_right"]["visible"] == True and game_objects["guard_2_right"]["visible"] == True:
            guard_1_right_movement = move_guard_horizontal(game_objects["guard_1_right"], guard_1_right_max_range,
                                                           guard_1_right_movement)
            guard_2_right_movement = move_guard_horizontal(game_objects["guard_2_right"], guard_2_right_max_range,
                                                           guard_2_right_movement)

        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_left"):
            visible_left = True
            game_objects["guard_1_left"]["visible"] = True
            game_objects["guard_2_left"]["visible"] = True

        if game_objects["guard_1_left"]["visible"] == True and game_objects["guard_2_left"]["visible"] == True:
            guard_1_left_movement = move_guard_horizontal(game_objects["guard_1_left"], guard_1_left_max_range,
                                                          guard_1_left_movement)
            guard_2_left_movement = move_guard_vertically(game_objects["guard_2_left"], guard_2_left_max_range,
                                                          guard_2_left_movement)

        # Load next level
        if crown_found and pixel_collision(game_objects, "mini_pekka", "blue_flag"):
            game_objects["clash_crown"]["visible"] = False
            game_objects["king_tower"]["visible"] = False
            game_objects["blue_flag"]["visible"] = True
            game_objects["brick_wall1"]["visible"] = False
            crown_found = True
            return

        # If you need to debug where something is on the screen, you can draw it
        # using this helper method
        # draw_marker( screen, Vector2(460,320) )

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label_1 = myfont.render("Hmm, what's on the other side of those bridges?", True, (255, 255, 51))
        screen.blit(label_1, (20, 20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.flip()

        # This slows down the code so it doesn't run more than 30 frames per second
        pygame.time.Clock().tick(30)


def level2():
    # Set up the Level by placing the objects of interest
    game_objects = {}

    def restart_game_level2(game_objects):
        for object in game_objects.values():
            init_pos = Vector2(object["initial_pos"].x, object["initial_pos"].y)
            object["pos"] = init_pos
            game_objects["clash_crown"]["visible"] = True
            game_objects["king_tower"]["visible"] = True
            game_objects["blue_flag"]["visible"] = False
            game_objects["guard_1_right"]["visible"] = False
            game_objects["guard_2_right"]["visible"] = False
            game_objects["guard_1_left"]["visible"] = False
            game_objects["guard_2_left"]["visible"] = False
            game_objects["guard_3_right"]["visible"] = False
    #
    # Create the Game Objects and add them to the game_objects dictionary
    #
    # IMPORTANT: You must replace these images with your own.
    # IMPORTANT: the image file name is the name used for the item
    add_game_object(game_objects, "arena2", 800, 600, 400, 300)
    add_game_object(game_objects, "clash_crown", 40, 40, 360, 220)
    add_game_object(game_objects, "king_tower", 70, 80, 400, 120)
    add_game_object(game_objects, "bridge_arena1_left", 60, 50, 336, 320)
    add_game_object(game_objects, "bridge_arena1_right", 60, 50, 460, 320)
    add_game_object(game_objects, "mini_pekka", 35, 25, 400, 450)
    add_game_object(game_objects, "blue_flag", 30, 30, 400, 150)
    add_game_object(game_objects, "guard_1_right", 20, 30, 430, 250)
    add_game_object(game_objects, "guard_2_right", 20, 30, 490, 250)
    add_game_object(game_objects, "guard_3_right", 20, 30, 460, 200)
    add_game_object(game_objects, "guard_1_left", 20, 30, 330, 230)
    add_game_object(game_objects, "guard_2_left", 20, 30, 375, 250)
    add_game_object(game_objects, "guard_3_right", 20, 30, 460, 200)
    add_game_object(game_objects, "brick_wall1", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall2", 250, 200, 395, 235)
    add_game_object(game_objects, "brick_wall3", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall4", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall5", 250, 200, 420, 235)


    # create the window based on the map size
    screen = pygame.display.set_mode(game_objects["arena2"]["image"].get_size())

    # The frame count records how many times the program has
    # gone through the main loop.  Normally you don't need this information
    # but if you want to do an animation, you can use this variable to
    # indicate which sprite frame to draw
    frame_count = 0

    # Get a font to use to write on the screen.
    myfont = pygame.font.SysFont('helvetica', 25, 4)

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # "start" the game when the mouse moves over the player
    is_started = False

    # has the player found (moved on top of) the key to the door?
    crown_found = False

    # are the guards from level 2 visible
    game_objects["guard_1_right"]["visible"] = False
    game_objects["guard_2_right"]["visible"] = False
    game_objects["guard_1_left"]["visible"] = False
    game_objects["guard_2_left"]["visible"] = False
    game_objects["guard_3_right"]["visible"] = False
    game_objects["brick_wall1"]["visible"] = False
    game_objects["brick_wall2"]["visible"] = True
    game_objects["brick_wall3"]["visible"] = False
    game_objects["brick_wall4"]["visible"] = False
    game_objects["brick_wall5"]["visible"] = False

    visible_right = False
    visible_left = False

    def move_guard_horizontal(guard_obj, max_range, movement):
        """
        Function to handle movement logic for guards.
        :param guard_obj: Dictionary containing guard object information
        :param max_range: Maximum movement range for the guard
        :param movement: Movement vector for the guard
        """
        guard_obj["pos"] += movement

        # Check if guard reached the maximum range, reverse their movement direction
        if (guard_obj["pos"] - guard_obj["initial_pos"]).length() > max_range:
            movement *= -1  # Reverse direction
        return movement

    # Define movement variables for guards
    guard_1_right_movement = Vector2(1, 0)  # Movement direction for guard 1 (right)
    guard_2_right_movement = Vector2(-1, 0)  # Movement direction for guard 2 (left)
    guard_3_right_movement = Vector2(1, 0)  # Movement direction for guard 3 (right)
    guard_1_right_max_range = 5  # Maximum movement range for guard 1
    guard_2_right_max_range = 5  # Maximum movement range for guard 2
    guard_3_right_max_range = 5  # Maximum movement range for guard 3

    # Update guard positions using the move_guard function
    guard_1_right_movement = move_guard_horizontal(game_objects["guard_1_right"], guard_1_right_max_range,
                                                   guard_1_right_movement)
    guard_2_right_movement = move_guard_horizontal(game_objects["guard_2_right"], guard_2_right_max_range,
                                                   guard_2_right_movement)
    guard_3_right_movement = move_guard_horizontal(game_objects["guard_3_right"], guard_3_right_max_range,
                                                   guard_3_right_movement)

    def move_guard_vertically(guard_obj, max_range, movement):
        """
        Function to handle vertical movement logic for guards.
        :param guard_obj: Dictionary containing guard object information
        :param max_range: Maximum movement range for the guard
        :param movement: Movement vector for the guard
        """
        guard_obj["pos"] += movement

        # Check if guard reached the maximum range, reverse their movement direction
        if abs((guard_obj["pos"].y - guard_obj["initial_pos"].y)) > max_range:
            movement *= -1  # Reverse direction
        return movement

    guard_1_left_movement = Vector2(0, 1)  # Movement direction for guard 1 left (down)
    guard_2_left_movement = Vector2(0, -1)  # Movement direction for guard 2 left (up)
    guard_1_left_max_range = 20  # Maximum movement range for guard 1 left
    guard_2_left_max_range = 20  # Maximum movement range for guard 2 left

    # Update guard positions using the move_guard_vertically function
    guard_1_left_movement = move_guard_vertically(game_objects["guard_1_left"], guard_1_left_max_range,
                                                  guard_1_left_movement)
    guard_2_left_movement = move_guard_vertically(game_objects["guard_2_left"], guard_2_left_max_range,
                                                  guard_2_left_movement)

    # This is the main game loop. In it, we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while True:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pixel_collision(game_objects, "mini_pekka", "arena2"):
            is_alive = False
            pygame.mouse.set_visible(True)
            if not game_over(game_objects, screen):
                pygame.quit()
                sys.exit()
            else:
                restart_game_level2(game_objects)
                is_alive = True
                is_started = False
                crown_found = False
                game_objects["clash_crown"]["visible"] = True
                game_objects["king_tower"]["visible"] = True
                game_objects["blue_flag"]["visible"] = False


        if pixel_collision(game_objects, "mini_pekka", "brick_wall2"):
            is_alive = False
            pygame.mouse.set_visible(True)
            if not game_over(game_objects, screen):
                pygame.quit()
                sys.exit()
            else:
                restart_game_level2(game_objects)
                is_alive = True
                is_started = False
                crown_found = False
                game_objects["clash_crown"]["visible"] = True
                game_objects["king_tower"]["visible"] = True
                game_objects["blue_flag"]["visible"] = False

        # Makes new text appear when player collides with bridges
        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_right"):
            label_1 = myfont.render("Ooooh we are on level 2 now", True, (255, 255, 255))
            screen.blit(label_1, (20, 20))

            label_2 = myfont.render("Ohhhhh, that's whats on the other side of the bridges", True, (255, 255, 255))
            screen.blit(label_2, (20, 20))

        # Check for game logic situation
        if is_alive:
            if not is_started:
                if not is_started and Vector2(pygame.mouse.get_pos()).distance_to(
                        game_objects["mini_pekka"]["pos"]) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible(False)

        # Position the player to the mouse location
        if is_alive:
            if is_started:
                player = game_objects["mini_pekka"]
                player["pos"] = Vector2(pygame.mouse.get_pos())
            else:
                # if the mouse comes near the player, start the game
                if Vector2(pygame.mouse.get_pos()).distance_to(game_objects["mini_pekka"]["pos"]) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible(False)

        # Clear the map by putting a background gray across the screen
        screen.fill((150, 150, 150))  # This helps check if the image path is transparent

        # Keep the flag hidden until the crown is found.
        if crown_found == False:
            game_objects["blue_flag"]["visible"] = False

        # Check for game logic situation
        if not crown_found and pixel_collision(game_objects, "mini_pekka", "clash_crown"):
            game_objects["clash_crown"]["visible"] = False
            game_objects["king_tower"]["visible"] = False
            game_objects["blue_flag"]["visible"] = True
            crown_found = True

        # Draw the game objects
        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered(screen, object["image"], object["pos"])

        # Added logic to add arrow keys and WASD keys to move the player.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game_objects["mini_pekka"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game_objects["mini_pekka"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, 5)

        if pixel_collision(game_objects, "mini_pekka", "guard_1_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level2(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_2_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level2(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_3_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level2(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_1_left") and visible_left:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level2(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_2_left") and visible_left:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level2(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_right"):
            visible_right = True
            game_objects["guard_1_right"]["visible"] = True
            game_objects["guard_2_right"]["visible"] = True
            game_objects["guard_3_right"]["visible"] = True

        # If both guards are visible, move them
        if game_objects["guard_1_right"]["visible"] == True and game_objects["guard_2_right"]["visible"] == True and game_objects["guard_3_right"]["visible"] == True:
            guard_1_right_movement = move_guard_horizontal(game_objects["guard_1_right"], guard_1_right_max_range,
                                                           guard_1_right_movement)
            guard_2_right_movement = move_guard_horizontal(game_objects["guard_2_right"], guard_2_right_max_range,
                                                           guard_2_right_movement)
            guard_3_right_movement = move_guard_horizontal(game_objects["guard_3_right"], guard_3_right_max_range,
                                                              guard_3_right_movement)

        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_left"):
            visible_left = True
            game_objects["guard_1_left"]["visible"] = True
            game_objects["guard_2_left"]["visible"] = True

        if game_objects["guard_1_left"]["visible"] == True and game_objects["guard_2_left"]["visible"] == True:
            guard_1_left_movement = move_guard_horizontal(game_objects["guard_1_left"], guard_1_left_max_range,
                                                          guard_1_left_movement)
            guard_2_left_movement = move_guard_vertically(game_objects["guard_2_left"], guard_2_left_max_range,
                                                          guard_2_left_movement)

        # Load next level
        if crown_found and pixel_collision(game_objects, "mini_pekka", "blue_flag"):
            game_objects["clash_crown"]["visible"] = False
            game_objects["king_tower"]["visible"] = False
            game_objects["blue_flag"]["visible"] = True
            crown_found = True
            return

        # If you need to debug where something is on the screen, you can draw it
        # using this helper method
        # draw_marker( screen, Vector2(460,320) )

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label_1 = myfont.render("Hmm, what's on the other side of those bridges?", True, (255, 255, 51))
        screen.blit(label_1, (20, 20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.flip()

        # This slows down the code so it doesn't run more than 30 frames per second
        pygame.time.Clock().tick(30)


def level3():
    # Set up the Level by placing the objects of interest
    game_objects = {}

    def restart_game_level3(game_objects):
        for object in game_objects.values():
            init_pos = Vector2(object["initial_pos"].x, object["initial_pos"].y)
            object["pos"] = init_pos
            game_objects["clash_crown"]["visible"] = True
            game_objects["king_tower"]["visible"] = True
            game_objects["blue_flag"]["visible"] = False
            game_objects["guard_1_right"]["visible"] = False
            game_objects["guard_2_right"]["visible"] = False
            game_objects["guard_1_left"]["visible"] = False
            game_objects["guard_2_left"]["visible"] = False
            game_objects["guard_3_right"]["visible"] = False
            game_objects["brick_wall1"]["visible"] = True
            game_objects["brick_wall2"]["visible"] = True
            game_objects["brick_wall3"]["visible"] = False
            game_objects["brick_wall4"]["visible"] = False
            game_objects["brick_wall5"]["visible"] = False

    #
    # Create the Game Objects and add them to the game_objects dictionary
    #
    # IMPORTANT: You must replace these images with your own.
    # IMPORTANT: the image file name is the name used for the item
    add_game_object(game_objects, "arena3", 800, 600, 400, 300)
    add_game_object(game_objects, "clash_crown", 40, 40, 460, 215)
    add_game_object(game_objects, "king_tower", 70, 80, 400, 120)
    add_game_object(game_objects, "bridge_arena1_left", 60, 50, 336, 320)
    add_game_object(game_objects, "bridge_arena1_right", 60, 50, 460, 320)
    add_game_object(game_objects, "mini_pekka", 35, 25, 400, 450)
    add_game_object(game_objects, "blue_flag", 30, 30, 400, 150)
    add_game_object(game_objects, "guard_1_right", 20, 30, 440, 265)
    add_game_object(game_objects, "guard_2_right", 20, 30, 490, 250)
    add_game_object(game_objects, "guard_1_left", 25, 35, 330, 200)
    add_game_object(game_objects, "guard_2_left", 25, 35, 350, 240)
    add_game_object(game_objects, "guard_3_left", 20, 30, 333, 290)
    add_game_object(game_objects, "guard_3_right", 20, 30, 460, 200)
    add_game_object(game_objects, "brick_wall1", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall2", 250, 200, 395, 235)
    add_game_object(game_objects, "brick_wall3", 250, 200, 420, 235)
    add_game_object(game_objects, "brick_wall4", 250, 200, 395, 235)
    add_game_object(game_objects, "brick_wall5", 250, 200, 420, 235)
    add_game_object(game_objects, "red_clash_crown", 25, 25, 315, 270)

    # create the window based on the map size
    screen = pygame.display.set_mode(game_objects["arena3"]["image"].get_size())

    # The frame count records how many times the program has
    # gone through the main loop.  Normally you don't need this information
    # but if you want to do an animation, you can use this variable to
    # indicate which sprite frame to draw
    frame_count = 0

    # Get a font to use to write on the screen.
    myfont = pygame.font.SysFont('helvetica', 25, 4)

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # "start" the game when the mouse moves over the player
    is_started = False

    # has the player found (moved on top of) the key to the door?
    crown_found = False

    # is the player on the bridge
    game_objects["guard_1_right"]["visible"] = False
    game_objects["guard_2_right"]["visible"] = False
    game_objects["guard_1_left"]["visible"] = False
    game_objects["guard_2_left"]["visible"] = False
    game_objects["guard_3_right"]["visible"] = False
    game_objects["brick_wall1"]["visible"] = True
    game_objects["brick_wall2"]["visible"] = True
    game_objects["brick_wall3"]["visible"] = False
    game_objects["brick_wall4"]["visible"] = False
    game_objects["brick_wall5"]["visible"] = False
    game_objects["red_clash_crown"]["visible"] = False

    visible_right = False
    visible_left = False
    wall1_visible = True
    wall2_visible = True
    wall3_visible = False

    def move_guard_horizontal(guard_obj, max_range, movement):
        """
        Function to handle movement logic for guards.
        :param guard_obj: Dictionary containing guard object information
        :param max_range: Maximum movement range for the guard
        :param movement: Movement vector for the guard
        """
        guard_obj["pos"] += movement

        # Check if guard reached the maximum range, reverse their movement direction
        if (guard_obj["pos"] - guard_obj["initial_pos"]).length() > max_range:
            movement *= -1  # Reverse direction
        return movement

    # Define movement variables for guards
    guard_1_right_movement = Vector2(1, 0.)  # Movement direction for guard 1 (right)
    guard_2_right_movement = Vector2(-1, 0)  # Movement direction for guard 2 (left)
    guard_1_right_max_range = 5  # Maximum movement range for guard 1
    guard_2_right_max_range = 5  # Maximum movement range for guard 2


    # Update guard positions using the move_guard function
    guard_1_right_movement = move_guard_horizontal(game_objects["guard_1_right"], guard_1_right_max_range,
                                                   guard_1_right_movement)
    guard_2_right_movement = move_guard_horizontal(game_objects["guard_2_right"], guard_2_right_max_range,
                                                   guard_2_right_movement)

    def move_guard_vertically(guard_obj, max_range, movement):
        """
        Function to handle vertical movement logic for guards.
        :param guard_obj: Dictionary containing guard object information
        :param max_range: Maximum movement range for the guard
        :param movement: Movement vector for the guard
        """
        guard_obj["pos"] += movement

        # Check if guard reached the maximum range, reverse their movement direction
        if abs((guard_obj["pos"].y - guard_obj["initial_pos"].y)) > max_range:
            movement *= -1  # Reverse direction
        return movement

    guard_1_left_movement = Vector2(2, 2)  # Movement direction for guard 1 left (down)
    guard_2_left_movement = Vector2(-2, -2)  # Movement direction for guard 2 left (up)
    guard_1_left_max_range = 8  # Maximum movement range for guard 1 left
    guard_2_left_max_range = 30  # Maximum movement range for guard 2 left

    # Update guard positions using the move_guard_vertically function
    guard_1_left_movement = move_guard_vertically(game_objects["guard_1_left"], guard_1_left_max_range,
                                                  guard_1_left_movement)
    guard_2_left_movement = move_guard_vertically(game_objects["guard_2_left"], guard_2_left_max_range,
                                                  guard_2_left_movement)

    # This is the main game loop. In it, we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while True:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pixel_collision(game_objects, "mini_pekka", "arena3"):
            is_alive = False
            pygame.mouse.set_visible(True)
            if not game_over(game_objects, screen):
                pygame.quit()
                sys.exit()
            else:
                restart_game_level3(game_objects)
                is_alive = True
                is_started = False
                crown_found = False
                game_objects["clash_crown"]["visible"] = True
                game_objects["king_tower"]["visible"] = True
                game_objects["blue_flag"]["visible"] = False

        if ((pixel_collision(game_objects, "mini_pekka", "brick_wall3") and wall3_visible or pixel_collision(game_objects, "mini_pekka", "brick_wall1")) and wall1_visible or
                pixel_collision(game_objects, "mini_pekka", "brick_wall2") and wall2_visible):
            is_alive = False
            pygame.mouse.set_visible(True)
            if not game_over(game_objects, screen):
                pygame.quit()
                sys.exit()
            else:
                restart_game_level3(game_objects)
                is_alive = True
                is_started = False
                crown_found = False
                game_objects["clash_crown"]["visible"] = True
                game_objects["king_tower"]["visible"] = True
                game_objects["blue_flag"]["visible"] = False

        # Makes new text appear when player collides with bridges
        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_right"):
            label_1 = myfont.render("Hmm, what's on the other side of those bridges?", True, (255, 255, 255))
            screen.blit(label_1, (20, 20))

            label_2 = myfont.render("Ohhhhh, that's whats on the other side of the bridges", True, (255, 255, 255))
            screen.blit(label_2, (20, 20))

        # Check for game logic situation
        if is_alive:
            if not is_started:
                if not is_started and Vector2(pygame.mouse.get_pos()).distance_to(
                        game_objects["mini_pekka"]["pos"]) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible(False)

        # Position the player to the mouse location
        if is_alive:
            if is_started:
                player = game_objects["mini_pekka"]
                player["pos"] = Vector2(pygame.mouse.get_pos())
            else:
                # if the mouse comes near the player, start the game
                if Vector2(pygame.mouse.get_pos()).distance_to(game_objects["mini_pekka"]["pos"]) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible(False)

        # Clear the map by putting a background gray across the screen
        screen.fill((150, 150, 150))  # This helps check if the image path is transparent

        # Keep the flag hidden until the crown is found.
        if crown_found == False:
            game_objects["blue_flag"]["visible"] = False

        # Check for game logic situation
        if not crown_found and pixel_collision(game_objects, "mini_pekka", "clash_crown"):
            wall1_visible = False
            wall2_visible = False
            game_objects["clash_crown"]["visible"] = False
            game_objects["king_tower"]["visible"] = False
            game_objects["blue_flag"]["visible"] = True
            game_objects["brick_wall3"]["visible"] = True
            game_objects["brick_wall1"]["visible"] = False
            game_objects["brick_wall2"]["visible"] = False
            game_objects["brick_wall4"]["visible"] = True
            game_objects["red_clash_crown"]["visible"] = True
            crown_found = True

        # Draw the game objects
        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered(screen, object["image"], object["pos"])

        # Added logic to add arrow keys and WASD keys to move the player.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game_objects["mini_pekka"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game_objects["mini_pekka"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, 5)

        if pixel_collision(game_objects, "mini_pekka", "guard_1_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level3(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_2_right") and visible_right:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level3(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_3_left") and visible_left:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level3(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "guard_2_left") and visible_left:
            label = myfont.render("You got caught!", True, (255, 255, 0))
            screen.blit(label, (20, 40))
            game_over(game_objects, screen)
            restart_game_level3(game_objects)

        if pixel_collision(game_objects, "mini_pekka", "red_clash_crown"):
            brick_wall3_visible = False
            game_objects["red_clash_crown"]["visible"] = False
            game_objects["brick_wall3"]["visible"] = False
            game_objects["brick_wall5"]["visible"] = True

        if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_right"):
            visible_right = True
            game_objects["guard_1_right"]["visible"] = True
            game_objects["guard_2_right"]["visible"] = True

        # If both guards are visible, move them
        if game_objects["guard_1_right"]["visible"] == True and game_objects["guard_2_right"]["visible"] == True:
            guard_1_right_movement = move_guard_horizontal(game_objects["guard_1_right"], guard_1_right_max_range,
                                                           guard_1_right_movement)
            guard_2_right_movement = move_guard_horizontal(game_objects["guard_2_right"], guard_2_right_max_range,
                                                           guard_2_right_movement)

        # if pixel_collision(game_objects, "mini_pekka", "bridge_arena1_left"):
        #     visible_left = True
        #     # game_objects["guard_1_left"]["visible"] = True
        #     game_objects["guard_2_left"]["visible"] = True

        if game_objects["brick_wall4"]["visible"] == True and game_objects["brick_wall3"]["visible"] == True:
            # game_objects["guard_1_left"]["visible"] = True
            game_objects["guard_2_left"]["visible"] = True

        if game_objects["guard_1_left"]["visible"] == True or game_objects["guard_2_left"]["visible"] == True:
            guard_1_left_movement = move_guard_horizontal(game_objects["guard_1_left"], guard_1_left_max_range,
                                                          guard_1_left_movement)
            guard_2_left_movement = move_guard_vertically(game_objects["guard_2_left"], guard_2_left_max_range,
                                                          guard_2_left_movement)

        # Load next level
        if crown_found and pixel_collision(game_objects, "mini_pekka", "blue_flag"):
            game_objects["clash_crown"]["visible"] = False
            game_objects["king_tower"]["visible"] = False
            game_objects["blue_flag"]["visible"] = True
            crown_found = True
            return

        # If you need to debug where something is on the screen, you can draw it
        # using this helper method
        # draw_marker( screen, Vector2(460,320) )

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label_1 = myfont.render("Hmm, what's on the other side of those bridges?", True, (255, 255, 51))
        screen.blit(label_1, (20, 20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.flip()

        # This slows down the code so it doesn't run more than 30 frames per second
        pygame.time.Clock().tick(30)


# def congratulations(screen):
#     # Fill the screen with red
#     screen.fill((255, 50, 100))
#
#     # Show the cursor when collided
#     pygame.mouse.set_visible(True)
#
#     # Display game over message
#     font = pygame.font.SysFont('helvetica', 36)
#     game_over_text = font.render("Thanks for playing!!", True, (255, 255, 255))
#     screen.blit(game_over_text, (300, 200))
#     game_over_text_option = font.render("Hope you enjoyed the game!", True, (0, 75, 75))
#     screen.blit(game_over_text_option, (175, 275))


def main():
    # Initialize pygame
    pygame.init()

    # level1()

    # level2()

    level3()

    pygame.quit()
    sys.exit()


# Start the program
main()