#Author: Brendan Wong
#The purpose of the program is to create an art tool that allows the user to
#draw on the surface with a paint tool, erase, fill, and colourpicker/dropper. 
#In addition, when the program is closed, the art is automatically saved as a file
#in the program.

#importation of packages
import pygame
import pygame_widgets
from pygame_widgets import Slider
from pygame_widgets import TextBox
from PIL import Image
import sys


#turns on the "game"
pygame.init()


#sets the mouse as a variable, sets up the basic dimensions of the program, and also
#defines white for convenience
mouse = pygame.mouse
width = 700
height = 550
white = [255, 255, 255]


#Takes the dimensions defined before to create the surface(s) of the program.
#The window is for "temporary changes" (although it's basically only used for 
#the mouse cursor display), and the canvas is for the permanent changes 
#i.e the actual drawing.
window = pygame.display.set_mode((width, height))
canvas = window.copy()
pygame.display.set_caption('Art Tool')
canvas.fill(pygame.Color(white))


#Scales down the icons for the tools and the colour wheel (images taken 
#from the internet) to a feasible size - the icons are 25 pixels by 25,
#and the colour wheel are 150 by 200.
brushImage = pygame.transform.scale(pygame.image.load("paintbrush.png"),
                                    (25, 25))
fillImage = pygame.transform.scale(pygame.image.load("fill.png"), (25, 25))
eraserImage = pygame.transform.scale(pygame.image.load("eraser.png"), (25, 25))
dropperImage = pygame.transform.scale(pygame.image.load("colour_dropper.png"),
                                      (25, 25))
colourSelection = pygame.transform.scale(pygame.image.load("colour_wheel.png"),
                                         (150, 200))


#sets up the sliders for paintbrush/eraser size.
pen_slider = Slider(canvas,
                    570,
                    60,
                    110,
                    10,
                    min=1,
                    max=10,
                    step=1,
                    colour=(128, 128, 128),
                    handleRadius=10,
                    curved=False)
eraser_slider = Slider(canvas,
                       570,
                       145,
                       110,
                       10,
                       min=1,
                       max=10,
                       step=1,
                       colour=(128, 128, 128),
                       handleRadius=10,
                       curved=False)



#Defines fonts, and creates Text for the labels on the tool selection menu.
font = pygame.font.SysFont("dejavuserif", 15)
text = font.render("Paintbrush Settings", False, (0, 0, 0))
text1 = font.render("Eraser Settings", False, (0, 0, 0))
text2 = font.render("Tool Selection", False, (0, 0, 0))
pen_size_display = TextBox(canvas, 535, 53, 25, 25)
eraser_size_display = TextBox(canvas, 535, 138, 25, 25)
user_file = open("user_file.png", "w")


#Function for blitting images onto the display
def blit(x, y):
    window.blit(y, (x[0], x[1]))

#Locations for each of the tools (paintbrush, fill tool, eraser, colour dropper,
#colour wheel.)
brush_coord = [565, 225]
fill_coord = [565, 265]
eraser_coord = [615, 225]
dropper_coord = [615, 264]
wheel_coord = [530, 330]


#Sets default paintbrush colour as black, the state of the tool as 0 (which is later
#redirected to the paintbrush tool which is 2). Sets the "last position" of the mouse,
#the default paintbrush, eraser, and point/cursor size. Also sets the coordinates for
#cropping out the tools menu when the file is saved.
colour = [0, 0, 0]
active = 0
last_pos = None
pen_size = 6
eraser_size = 6
(left, right, upper, lower) = (0, 0, 500, 550)
point_size = 6


#driver code
while True:
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
    hover_position = list(pygame.mouse.get_pos())
    
    #Dictates the cursor; if the mouse is hovering over the tools menu, then 
    #there will be no cursor (it will just be the computer's cursor). 
    #Otherwise, there will be a program added cursor.
    if hover_position[0] >= 500 and hover_position[0] <= 700 and hover_position[
            1] >= 0 and hover_position[1] <= 550 or active == 3:
        ""
    else:
      #Sets up the cursor; if the tool being used is the eraser, then the 
      #cursor will be a hollow white circle, otherwise it'll be a 
      #filled in circle of the selected colour.
        if active == 4:
            pygame.draw.circle(window, (0, 0, 0), (pygame.mouse.get_pos()),
                               eraser_size,
                               width=1)
        else:
            pygame.draw.circle(window, pygame.Color(colour),
                               (pygame.mouse.get_pos()), point_size)
    
    events = pygame.event.get()

    for event in events:
      
        #"QUIT" didn't work so I just used the actual number which is 256;
        #when the program is closed, the program automatically saves the 
        #drawing as a png.
        if event.type == 256:
            img = Image.open(r"user_file.png")
            img1 = img.crop((left, right, upper, lower))
            img1.save(r"user_file.png")
            pygame.quit()
            sys.exit()
        
        #The follow if statement addresses when the mouse is left clicked.
        if left_pressed:
            
            #Stores the position of the mouse as of when the left click occurred.
            #Also stores the colour of the pixel the mouse is on when the left click
            #occurred.
            position = list(pygame.mouse.get_pos())
            pixel_colour = window.get_at((position[0], position[1]))
            
            #If statements regarding the position of the mouse.
            #For when the left click is on the paintbrush icon in the toolbox
            if position[0] >= 565 and position[0] <= 590 and position[
                    1] >= 225 and position[1] <= 250:
                active = 2
                break
            
            #For when the left click is on the eraser icon in the toolbox    
            elif position[0] >= 615 and position[0] <= 640 and position[
                    1] >= 225 and position[1] <= 250:
                active = 4
            
            #For when the left click is on the fill/bucket icon in the toolbox
            elif position[0] >= 565 and position[0] <= 590 and position[
                    1] >= 265 and position[1] <= 290:
                active = 1

            #For when the left click is on the colour dropper icon in the toolbox    
            elif position[0] >= 615 and position[0] <= 640 and position[
                    1] >= 264 and position[1] <= 290:
                active = 3

            #For when the left click is on the colour palette   
            elif position[0] >= 530 and position[0] <= 680 and position[
                    1] >= 330 and position[1] <= 530:
                colour = pixel_colour
            
            #For when the left click is not on the tool menu i.e on the actual canvas.
            else:
                
                #for when the fill tool is active: it fills the canvas with a specified
                #colour.
                if active == 1:
                    canvas.fill(pygame.Color(colour))
                
                #For when the paintbrush tool is active (this also incldues when
                #the program has just been opened, since the default is the paintbrush
                #tool).
                elif active == 2 or active == 0:
                    
                    #Drawing code: essentially, if the mouse is held down and dragged,
                    #it draws a line from the previous position of the mouse, to the
                    #current position, then the "last position" is updated for the
                    #next stroke. 
                    if hover_position[0] < 500:
                        if event.type == pygame.MOUSEMOTION:
                            if last_pos is not None:
                                pygame.draw.line(canvas, colour, last_pos,
                                                 position, pen_size)
                            last_pos = position
                        
                        #If a dot is drawn (i.e one click), then the last position
                        #is reset to nothing as well.
                        else:
                            last_pos = None
                            pygame.draw.circle(canvas, pygame.Color(colour),
                                               (pygame.mouse.get_pos()),
                                               point_size)
                    else:
                        ""
                
                #For when the colour dropper tool is active. On the next click, it will
                #take the colour that the mouse is over, and automatically change to
                #the paintbrush tool, but with the new colour active.
                elif active == 3:
                    colour = pixel_colour
                    active = 2
                
                #For when the eraser tool is active. The tool basically draws 
                #small white circles, ebbing away the coloured strokes.
                elif active == 4:
                    if hover_position[0] < 500:
                        pygame.draw.circle(canvas, pygame.Color(white),
                                           (pygame.mouse.get_pos()),
                                           eraser_size)
                    else:
                        ""
              
                else:
                    active = 2
    
    pygame.display.update()
    
    #fills the window white as default, and blits the canvas over.
    window.fill(white)
    window.blit(canvas, (0, 0))

    #Draws the tools menu area, then the tool box, as well as the rectangles for the
    #sliders (purely for aesthetic look)
    pygame.draw.rect(canvas, (128, 128, 128), (500, 0, 700, 550))
    pygame.draw.rect(canvas, (192, 192, 192), (550, 210, 110, 90))
    pygame.draw.rect(canvas, (192, 192, 192), (525, 40, 160, 50))
    pygame.draw.rect(canvas, (192, 192, 192), (525, 125, 160, 50))
    
    #Blits the tool icons and the colour palette
    blit(brush_coord, brushImage)
    blit(fill_coord, fillImage)
    blit(eraser_coord, eraserImage)
    blit(dropper_coord, dropperImage)
    blit(wheel_coord, colourSelection)

    #Driving code for the sliders.
    #Also takes the value that the sliders are at and applies said value to the
    #paintbrush and eraser sizes
    pen_slider.listen(events)
    pen_slider.draw()
    eraser_slider.listen(events)
    eraser_slider.draw()
    point_size = pen_slider.getValue()
    pen_size = point_size * 2
    eraser_size = eraser_slider.getValue()
    pen_size_display.setText(pen_slider.getValue())
    pen_size_display.draw()
    eraser_size_display.setText(eraser_size)
    eraser_size_display.draw()

    #Labels for tools menu
    canvas.blit(text, (525, 15))
    canvas.blit(text1, (525, 100))
    canvas.blit(text2, (525, 185))

    #saves file
    pygame.image.save(canvas, "user_file.png")