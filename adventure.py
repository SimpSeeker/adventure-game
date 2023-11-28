# Starter code for an adventure game.
# Inspired by David Johnson for CS 1400 University of Utah.
# Written by Jim de St. Germain

# Add your Header Doc String Here
#
#

import sys, pygame, math
from pygame import Vector2

def pixel_collision( game_objects, item1, item2 ):
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
    pos1_temp = pos1 - Vector2(mask1.get_size())/2
    pos2_temp = pos2 - Vector2(mask2.get_size())/2
    offset = pos2_temp - pos1_temp

    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap( mask2, offset ) #, offset )
    return overlap != None

def draw_marker( screen, position ):
    """
    Simple helper to draw a location on the screen so you can
    see if your thoughts of what a position match Python's "thoughts".
    :param screen:  surface you are drawing on
    :param position: Vector2 : location to draw a circle
    :return: -NA-
    """
    pygame.draw.circle( screen, "black", position, 5 )


def draw_image_centered( screen, image, pos ):
    """
    On the screen, draw the given image **centered** on the given position.

    :param screen:  what we are drawing on
    :param image:   what we are drawing
    :param pos: Vector2 :  where to center the image
    :return: -NA-
    """
    containing_rectangle = image.get_rect()
    screen.blit( image, (pos.x - containing_rectangle.width/2, pos.y - containing_rectangle.height/2 ) )


def  add_game_object( game_objects, name, width, height, x, y ):
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
    game_objects[name] = information   # put the new object in the dictionary

    # Read the image file name. Note: I have put all of my images in a subfolder named "images"
    image = pygame.image.load("images/"+name+".png") # .convert_alpha()

    information[ "name" ]   = name
    information[ "pos" ]    = Vector2( x, y )
    information[ "image" ]  = pygame.transform.smoothscale( image, (width, height) )
    information[ "mask" ]   = pygame.mask.from_surface( information[ "image" ] )
    information[ "visible"] = True

    # Note: this code does not support animations.  If you want animations (and you should)
    #       you will need to update it based on the lab code!


def main():

    # Initialize pygame
    pygame.init()

    # Set up the Level by placing the objects of interest
    game_objects = {}

    #
    # Create the Game Objects and add them to the game_objects dictionary
    #
    # IMPORTANT: You must replace these images with your own.
    # IMPORTANT: the image file name is the name used for the item
    add_game_object( game_objects, "arena_map1_edit",     width=800, height=600, x=400, y=300)
    add_game_object( game_objects, "alien1",  30, 30, 100, 200)
    add_game_object( game_objects, "key",     40, 40, 300, 450 )
    # add_game_object( game_objects, "door",    200, 200, 550, 150 )
    add_game_object( game_objects, "mini_pekka",  100,70 , 100, 200 )

    # create the window based on the map size
    screen = pygame.display.set_mode( game_objects["arena_map1_edit"]["image"].get_size() )

    # The frame count records how many times the program has
    # gone through the main loop.  Normally you don't need this information
    # but if you want to do an animation, you can use this variable to
    # indicate which sprite frame to draw
    frame_count = 0

    # Get a font to use to write on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # "start" the game when the mouse moves over the player
    is_started = False

    # has the player found (moved on top of) the key to the door?
    key_found = False

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

        # Position the player to the mouse location
        if is_alive:
            if is_started:
                player = game_objects["alien1"]
                player["pos"] = Vector2( pygame.mouse.get_pos() )
            else:
                # if the mouse comes near the player, start the game
                if Vector2( pygame.mouse.get_pos() ).distance_to( game_objects["alien1"]["pos"] ) < 5:
                    is_started = True
                    # Hide the arrow cursor and replace it with a sprite.
                    pygame.mouse.set_visible( False )

        # Clear the map by putting a background gray across the screen
        screen.fill((150,150,150)) # This helps check if the image path is transparent

        # Check for game logic situation
        if not key_found and pixel_collision( game_objects, "alien1", "key" ):
            game_objects["key"]["visible"] = False
            game_objects["door"]["visible"] = False
            key_found = True

        # Draw the game objects
        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered( screen, object["image"], object["pos"] )

        # See if we touch the maze walls
        # if pixel_collision( game_objects, "alien1", "map" ):
        #     label = myfont.render( "Alien Ship Collided with Map!", True, (255, 255, 0) )
        #     screen.blit( label, (20, 40) )
        #     is_alive = False
        #     pygame.mouse.set_visible( True )

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_objects["mini_pekka"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT]:
            game_objects["mini_pekka"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN]:
            game_objects["mini_pekka"]["pos"] += Vector2(0, 5)


        # If you need to debug where something is on the screen, you can draw it
        # using this helper method
        # draw_marker( screen, Vector2(200,200) )

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = myfont.render("By Jim! - Put your Mouse on the Ship!", True, (255,255,0))
        screen.blit(label, (20,20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.flip()

        # This slows down the code so it doesn't run more than 30 frames per second
        pygame.time.Clock().tick( 30 )

    pygame.quit()
    sys.exit()


# Start the program
main()