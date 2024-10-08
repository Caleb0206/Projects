# Virtual World Wandavision
In my project 4, I was inspired by the Marvel show Wandavision. My VirtualWorld will run by just clicking anywhere in the world and will spawn in Wanda. When you first click into VirtualWorld, she will spawn in with her magical runes (background) surrounding her in adjacent tiles. If any Dudes are adjacent to her when clicked, Dudes will turn black-and-white for the remainder of the program. Wanda has two frames of moving around while hunting for fairies. A trail of her Wandavision hex will trail behind Wanda (shows as a staticy background tile). Once she consumes a fairy, she will become mad with power and have three animation frames where she blasts her chaos magic while moving to a mushroom. Then, once at a mushroom, she will change it to a black-white one-story house as well as changing the background tile to her staticy hex. Over time, her house will transform into two stories and spawn in Vision through Wanda’s hex, (which is why his animation frames go from color to black-white with a static effect). Vision will go to stumps and spawn in more fairies. The program will end when Wanda has no path to an available Mushroom.

## Course Information
- **Course Name:** CSC 203
- **Instructor:** Vanessa Rivera
- **Term:** 2023-24 Winter Quarter

## Overview

In this project, you will add entirely new functionality to the virtual world in the form of a "world-changing event" that creates brand-new entities to interact and change the world.

## Learning Objectives

In completing this assessment, you will be able to:

- Create and integrate new classes as extensions to an existing class hierarchy.
- Utilize code that interacts with external non-text, image data files.
- Write a function that performs real-time functionality through a user's mouse press.

### Task 1: New Entities

- **Description:** Design and implement *at least* two new concrete subtypes that extend your `Entity` class hierarchy.
  Some examples include a green "dude" that travels the world, randomly planting stumps, a "zombie" that seeks out and "zombifies" dudes and fairies through transformations, or a "dragon" that travels the land transforming Houses into "fire" entities and is attacked by Fairies.
- **Requirements:**
  - You must have already divided the Entity class into subclasses. You may not use the base Project 2 Entity class for this project.
  - Both entities must use entirely new graphics. You may not use any given image files.
    - Note: You must commit and push any new image files for your program to be properly graded.
  - Both entities must schedule and perform behaviors.
  - At least one entity must perform movement and this movement must be unique.
    For example, you should not make a new entity that simply moves toward trees and saplings like a dude or toward a stump like a fairy.
  - Both entities must schedule and perform animations, having at least 2 image frames of animation.

### Task 2: World-Changing Event

- **Description:** You will add your entities to the world via a "world-changing event".
  This world-changing event will lead to your task 1 entities being created, background tiles changing, and at least one entity transformation.
  Clicking in the virtual world window will cause this event to occur, localized at the position of the mouse click.
  You will implement your world-changing event by modifying logic within the `VirtualWorld.mousePressed()` method.
- **Requirements:**
  - A world-changing event must occur with respect to the cursor position when you click inside the virtual world window.
  - Your world-changing event must (eventually) create one of your new entities from task 1 within the world.
  - When the world-changing event occurs, at least 9 background tiles must be changed to at least one entirely new graphic.
    This change can be done around the mouse click area when the event occurs or can happen over time, through the newly created entity for example.
    You may not use any image files given in this, or other versions of, the project.
    - Note: You must commit and push any new image files for your program to be properly graded.
  - An entity must be "transformed" into another as a result of the world-changing event.
    You may change some entities when the mouse is clicked or your new entity may transform other entities as part of its behavior.
    Existing entities may be transformed, e.g. a dude can be transformed into either a fairy or one of your new entities.
  - Your second entity must be created either when the world-changing event occurs or as a result of it. 
    Your first entity may create or transform other entities into your second entity, for example.
  - Both entities must have their actions scheduled.

### Task 3: Event Description and Instructions

- **Description:** In your Canvas submission, write a short description of what your world-changing event does and any instructions on how to perform it (e.g., click near a Dude, etc.).
  If I cannot determine how to properly execute your world-changing event, you may not receive full credit for your submission.

### (Optional) Task 4: Extra Credit

- **Description:** You may receive up to four points of extra credit on this assignment by exceeding the above requirements in complexity and content.
  Examples include:
  - Adding more than the entities required.
  - Complex and unique entity pathing or logic.
  - Creating graphics by hand.
  - Modifying the existing virtual world by altering the world save file or existing graphics and logic.
  - Adding entirely new functionality (for example, like music and sound effects)
- **Requirements:**
  - As part of your Canvas submission, you must indicate what work you've done that constitutes extra credit.
  - You must also provide a reasonable estimate for how much extra credit you believe you deserve, citing your submitted work as evidience.
    Use the following criteria for reference:
    - No Extra Credit: Meets the above requirements but does not exceed them.
    - Full Extra Credit: A significant amount (4 - 6) of new entities were added with substantially complex logic, each with hand-crafted graphics, and entirely new features such as audio or interactivity have been added to the program.
