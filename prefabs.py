# This is where all of the shapes are.
# I moved them to a seperate file simply because there's a lot of things.

# This code is ugly.


def getVector(vector):
    # This just sets the direction of items to be placed.
    vectorxz = ''
    vectory = ''
    if (vector[2] >= -0.50 and vector[0] >= 0.50):
        # Forward
        vectorxz = 'Forward'
    elif (vector[2] > 0.50 and vector[0] < 0.50):
        # Right
        vectorxz = 'Right'
    elif (vector[2] < -0.50 and vector[0] < 0.50):
        # Left
        vectorxz = 'Left'
    elif (vector[2] <= 0.50 and vector[0] <= -0.50):
        # Backward
        vectorxz = 'Backward'
    if vector[1] >= 0.25:
        vectory = 'Up'
    elif vector[1] <= -0.25:
        vectory = 'Down'
    elif (vector[1] >= -0.25 and vector[1] <= 0.25):
        vectory = 'Mid'
    return(vectorxz, vectory)


def cube(position, gltype, batch, vector):
    # This makes a single cube.
    x, y, z = position[0], position[1], position[2]

    if type(vector) is tuple:
        vectorxz, vectory = getVector(vector)
        if vectorxz == 'Forward':
            x = x + 2
            z = z - 0.5
        elif vectorxz == 'Right':
            x = x - 0.5
            z = z + 2
        elif vectorxz == 'Left':
            x = x - 0.5
            z = z - 3
        elif vectorxz == 'Backward':
            x = x - 3
            z = z - 0.5
        if vectory == 'Up':
            y = y + 1
        elif vectory == 'Down':
            y = y - 3
        elif vectory == 'Mid':
            y = y - 1

    # Adds the cubes to a batch, makes them a pretty rainbow colour.
    X, Y, Z = x+1, y+1, z+1

    batch.add(
        4, gltype, None,
        ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z)),
        ('c4B', (255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
        ('c4B', (255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
        ('c4B', (255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z)),
        ('c4B', (255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)),
        ('c4B', (255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)),
        ('c4B', (255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255)))


def rectanglex(position, gltype, batch, vector, rotation):
    # This adds a rectangle that extends on the x axis.
    x, y, z = position[0], position[1], position[2]

    if type(vector) is tuple:
        vectorxz, vectory = getVector(vector)
        if vectorxz == 'Forward':
            x = x + 2
            z = z - 0.5
        elif vectorxz == 'Right':
            x = x - 2.5
            z = z + 2
        elif vectorxz == 'Left':
            x = x - 2.5
            z = z - 3
        elif vectorxz == 'Backward':
            x = x - 7
            z = z - 0.5
        if vectory == 'Up':
            y = y + 1
        elif vectory == 'Down':
            y = y - 3
        elif vectory == 'Mid':
            y = y - 1
    if rotation == 0:
        X, Y, Z = x+1, y+5, z+1
    elif rotation == 1:
        X, Y, Z = x+5, y+1, z+1
    elif rotation == 2:
        X, Y, Z = x+5, y+5, z+1

    batch.add(
        4, gltype, None,
        ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z)),
        ('c4B', (255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
        ('c4B', (255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
        ('c4B', (255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z)),
        ('c4B', (255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)),
        ('c4B', (255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)),
        ('c4B', (255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255)))


def rectanglez(position, gltype, batch, vector, rotation):
    # This adds a rectangle on the z axis.
    x, y, z = position[0], position[1], position[2]

    if type(vector) is tuple:
        vectorxz, vectory = getVector(vector)
        if vectorxz == 'Forward':
            x = x + 2
            z = z - 2.5
        elif vectorxz == 'Right':
            x = x - 0.5
            z = z + 2
        elif vectorxz == 'Left':
            x = x - 0.5
            z = z - 7
        elif vectorxz == 'Backward':
            x = x - 3
            z = z - 2.5
        if vectory == 'Up':
            y = y + 1
        elif vectory == 'Down':
            y = y - 3
        elif vectory == 'Mid':
            y = y - 1
    if rotation == 0:
        X, Y, Z = x+1, y+5, z+1
    elif rotation == 1:
        X, Y, Z = x+1, y+1, z+5
    elif rotation == 2:
        X, Y, Z = x+1, y+5, z+5

    batch.add(
        4, gltype, None,
        ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z)),
        ('c4B', (255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
        ('c4B', (255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
        ('c4B', (255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z)),
        ('c4B', (255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)),
        ('c4B', (255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255)))
    batch.add(
        4, gltype, None,
        ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)),
        ('c4B', (255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255)))


def hallway(position, gltype, batch, vector):
    # This is what makes the "hallway"
    # It will change direction based on where you're facing. Fancy.
    x, y, z = position[0], position[1], position[2]-0.5
    vectorxz, vectory = getVector(vector)
    vector = ''
    recDirection = ''
    if vectorxz == 'Forward':
        x = x + 2
        recDirection = rectanglex
    elif vectorxz == 'Right':
        x = x - 0.5
        z = z + 3
        recDirection = rectanglez
    elif vectorxz == 'Left':
        x = x - 0.5
        z = z - 7
        recDirection = rectanglez
    elif vectorxz == 'Backward':
        x = x - 7
        recDirection = rectanglex
    if vectory == 'Up':
        y = y + 1
    elif vectory == 'Down':
        y = y - 3
    elif vectory == 'Mid':
        y = y - 1
    if recDirection == rectanglex:
        recDirection((x, y, z+2), gltype, batch, vector, rotation=2)
        recDirection((x, y, z+1), gltype, batch, vector, rotation=1)
        recDirection((x, y, z), gltype, batch, vector, rotation=1)
        recDirection((x, y, z-1), gltype, batch, vector, rotation=1)
        recDirection((x, y, z-2), gltype, batch, vector, rotation=2)
    elif recDirection == rectanglez:
        recDirection((x+2, y, z), gltype, batch, vector, rotation=2)
        recDirection((x+1, y, z), gltype, batch, vector, rotation=1)
        recDirection((x, y, z), gltype, batch, vector, rotation=1)
        recDirection((x-1, y, z), gltype, batch, vector, rotation=1)
        recDirection((x-2, y, z), gltype, batch, vector, rotation=2)


def nudes(position, gltype, batch):
    # This is ugly and horrible. It makes the very important words.
    x, y, z = position[0], position[1]-3, position[2]-21
    vector = ''
    # S
    cube((x, y+4, z+2), gltype, batch, vector)
    cube((x, y+4, z+1), gltype, batch, vector)
    cube((x, y+4, z), gltype, batch, vector)
    cube((x, y+3, z), gltype, batch, vector)
    cube((x, y+2, z), gltype, batch, vector)
    cube((x, y+2, z+1), gltype, batch, vector)
    cube((x, y+2, z+2), gltype, batch, vector)
    cube((x, y+1, z+2), gltype, batch, vector)
    cube((x, y, z+2), gltype, batch, vector)
    cube((x, y, z+1), gltype, batch, vector)
    cube((x, y, z), gltype, batch, vector)
    # E
    rectanglex((x, y, z+5), gltype, batch, vector, rotation=0)
    cube((x, y+4, z+7), gltype, batch, vector)
    cube((x, y+4, z+6), gltype, batch, vector)
    cube((x, y+2, z+7), gltype, batch, vector)
    cube((x, y+2, z+6), gltype, batch, vector)
    cube((x, y, z+6), gltype, batch, vector)
    cube((x, y, z+7), gltype, batch, vector)
    # N
    rectanglex((x, y, z+10), gltype, batch, vector, rotation=0)
    cube((x, y+3, z+11), gltype, batch, vector)
    cube((x, y+2, z+12), gltype, batch, vector)
    rectanglex((x, y, z+13), gltype, batch, vector, rotation=0)
    # D
    rectanglex((x, y, z+16), gltype, batch, vector, rotation=0)
    cube((x, y+4, z+17), gltype, batch, vector)
    cube((x, y+4, z+18), gltype, batch, vector)
    cube((x, y+3, z+19), gltype, batch, vector)
    cube((x, y+2, z+19), gltype, batch, vector)
    cube((x, y+1, z+19), gltype, batch, vector)
    cube((x, y+1, z+19), gltype, batch, vector)
    cube((x, y, z+18), gltype, batch, vector)
    cube((x, y, z+17), gltype, batch, vector)
    cube((x, y, z+16), gltype, batch, vector)
    # SPACE
    # N
    rectanglex((x, y, z+24), gltype, batch, vector, rotation=0)
    cube((x, y+3, z+25), gltype, batch, vector)
    cube((x, y+2, z+26), gltype, batch, vector)
    rectanglex((x, y, z+27), gltype, batch, vector, rotation=0)
    # U
    rectanglex((x, y, z+30), gltype, batch, vector, rotation=0)
    cube((x, y, z+31), gltype, batch, vector)
    cube((x, y, z+32), gltype, batch, vector)
    rectanglex((x, y, z+33), gltype, batch, vector, rotation=0)
    # D
    rectanglex((x, y, z+36), gltype, batch, vector, rotation=0)
    cube((x, y+4, z+37), gltype, batch, vector)
    cube((x, y+4, z+38), gltype, batch, vector)
    cube((x, y+3, z+39), gltype, batch, vector)
    cube((x, y+2, z+39), gltype, batch, vector)
    cube((x, y+1, z+39), gltype, batch, vector)
    cube((x, y+1, z+39), gltype, batch, vector)
    cube((x, y, z+38), gltype, batch, vector)
    cube((x, y, z+37), gltype, batch, vector)
    cube((x, y, z+36), gltype, batch, vector)
    # E
    rectanglex((x, y, z+42), gltype, batch, vector, rotation=0)
    cube((x, y+4, z+44), gltype, batch, vector)
    cube((x, y+4, z+43), gltype, batch, vector)
    cube((x, y+2, z+44), gltype, batch, vector)
    cube((x, y+2, z+43), gltype, batch, vector)
    cube((x, y, z+44), gltype, batch, vector)
    cube((x, y, z+43), gltype, batch, vector)
    # S
    cube((x, y+4, z+49), gltype, batch, vector)
    cube((x, y+4, z+48), gltype, batch, vector)
    cube((x, y+4, z+47), gltype, batch, vector)
    cube((x, y+3, z+47), gltype, batch, vector)
    cube((x, y+2, z+47), gltype, batch, vector)
    cube((x, y+2, z+48), gltype, batch, vector)
    cube((x, y+2, z+49), gltype, batch, vector)
    cube((x, y+1, z+49), gltype, batch, vector)
    cube((x, y, z+49), gltype, batch, vector)
    cube((x, y, z+48), gltype, batch, vector)
    cube((x, y, z+47), gltype, batch, vector)
