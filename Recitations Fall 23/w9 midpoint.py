# 6.101 recitation: lab 9 midpoint


############################################ n-body simulation


# what classes might we want?
# what information should each class store? (properties)
# what operations do we need? (methods)















class Vector:
    def __init__(self, x, y):
        pass

    def abs(self):
        pass
    
    def add(self, other):
        pass








class Body:
    G = 6.67e-11

    def __init__(self, mass, position, velocity=Vector(0,0)):
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def force_from(self, other):
        pass

    def move(self, force, dt):
        acceleration = force / self.mass
        self.velocity = self.velocity + acceleration * dt
        self.position = self.position + self.velocity * dt







class System:
    def __init__(self, bodies):
        self.bodies = bodies

    def step(self, dt):
        # add up all the forces per body
        forces_by_body = [
            # list of pairs (body, total force on body)
            (body, sum((body.force_from(other) for other in self.bodies if body != other), 
                       start=Vector(0,0)) )
                for body in self.bodies
        ]

        # apply the forces
        for body,force in forces_by_body:
            body.move(force, dt)


def run(selection, dark=False):
    examples = {
        'two_stable': [
            Body(1e25, Vector(0,0.91e9), Vector(200, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-200, 0)),
        ],

        'two_erratic': [
            Body(1e25, Vector(0,0.91e9), Vector(200, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-200, 0)),
        ],

        'three': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(0,0), Vector(25, 0)),
        ],

        'four': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(50,0), Vector(25, 0)),
            Body(5e8, Vector(-50,0), Vector(-25, 0)),
        ],

        'seven_stable': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(1e5,0), Vector(25, 25)),
            Body(5e8, Vector(-1e5,0), Vector(-25, -25)),
            Body(1e20, Vector(1e8,1e8), Vector(0, 100)),
            Body(1e20, Vector(-1e8,-1e8), Vector(0, -100)),
            Body(1e10, Vector(0,0), Vector(0, 0)),
        ],

        'seven_erratic': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(1e5,0), Vector(25, 25)),
            Body(5e8, Vector(-1e5,0), Vector(-25, -25)),
            Body(1e20, Vector(1e8,1e8), Vector(0, 150)),
            Body(1e20, Vector(-1e8,-1e8), Vector(0, -100)),
            Body(1e10, Vector(0,0), Vector(0, 0)),
        ],

        'two_from_rest': [
            Body(1e25, Vector(1e8,1e8), Vector(0, 0)),
            Body(1e25, Vector(-1e8,-1e8), Vector(0, 0)),
        ],
    }

    import pygame
    import sys
    import time

    class GraphicalSimulation(System):
        """
        Like the simulation, but also displays things to the screen
        """
        size = 1024
        colors = [
            (255, 0, 0),
            (0, 0, 255),
            (66, 52, 0),
            (152, 152, 152),
            (0, 255, 255),
            (255, 150, 0),
            (255, 0, 255),
        ]
        background = 'white'

        def __init__(self, bodies, screen_limit):
            System.__init__(self, bodies)
            self.screen_limit = screen_limit
            self.screen = pygame.display.set_mode((self.size, self.size))


        def draw(self):
            self.screen.fill(self.background)
            for b, c in zip(self.bodies, self.colors):
                x = self.size//2 + (b.position.coordinate(0)/self.screen_limit)*self.size//2
                y = self.size//2 + (b.position.coordinate(1)/self.screen_limit)*self.size//2
                pygame.draw.circle(self.screen, c, (x, y), 10)
            pygame.display.flip()

        def step(self, dt):
            System.step(self, dt)
            self.draw()


    if dark:
        GraphicalSimulation.background = 'black'
        GraphicalSimulation.colors = [(255-r, 255-g, 255-b)
            for r,g,b in GraphicalSimulation.colors]
        #sys.argv = [arg for arg in sys.argv if '-d' != arg != '--dark']

    # if len(sys.argv) < 2:
    #     print('Pass an example name as a command-line argument.')
    #     sys.exit(1)

    # selection = sys.argv[1]
    if selection not in examples:
        print('Example not found.')
        return

    dt = 2000
    sim = GraphicalSimulation(examples[selection], 2e9)

    # Unexplained magic using the pygame library
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        sim.step(dt)
        time.sleep(.001)
