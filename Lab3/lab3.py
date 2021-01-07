
# class definition
class shape():
    def __init__(self):
            pass
    def getArea(self):
            pass

# rectangle class
class rectangle(shape):
    def __init__(self, length, width):
        super().__init__()
        self.l = length        
        self.w = width
    def getArea(self):
        area = self.l * self.w
        return area

# circle class
class circle(shape):
    def __init__(self, radius):
        super().__init__()
        self.r = radius        
    def getArea(self):
        area = 3.14 * self.r * self.r
        return area

# triangle class
class triangle(shape):
    def __init__(self, base, height):
        super().__init__()
        self.b = base       
        self.h = height
    def getArea(self):
        area = 0.5 * self.b * self.h
        return area

# read txt file 
file = open(r'C:\GEOG392\Lab3\shape.txt')
lines = file.readlines()
file.close()

ind_lines = 0
for line in lines:
    components = line.split(',')
    shape = components[0]
    if shape == 'Rectangle':
        length = float(components[1])
        if ind_lines == len(lines)-1:   #Last line (line 10)
            width = float(components[2])
        else:                           #all previous lines (from Line 1 to Line 9)
            width = float(components[2][:-1])
        rec_obj = rectangle(length, width)
        area = rec_obj.getArea()
        print('The rectangle area is:', area)
        ind_lines = ind_lines + 1
    elif shape == 'Circle':
        if ind_lines == len(lines)-1:   #Last line (line 10)
            radius = float(components[1])
        else:                           #all previous lines (from Line 1 to Line 9)
            radius = float(components[1][:-1])
        cir_obj = circle(radius)
        area = cir_obj.getArea()
        print('The circle area is:', area)
        ind_lines = ind_lines + 1
    elif shape == 'Triangle':
        base = float(components[1])
        if ind_lines == len(lines)-1:   #Last line (line 10)
            height = float(components[2])
        else:                           #all previous lines (from Line 1 to Line 9)
            height = float(components[2][:-1])
        tri_obj = triangle(base, height)
        area = tri_obj.getArea()
        print('The triangle area is:', area)
        ind_lines = ind_lines + 1
    else:
        pass