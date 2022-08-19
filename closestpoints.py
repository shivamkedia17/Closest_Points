import random
import math
import matplotlib.pyplot as plt

def gen_points(r,n):
    Px, Py = [],[]
    #generate x,y co-ordinates randomly
    for i in range(0,n):
        x = random.random()*r
        y = random.random()*r
        Px.append(x)
        Py.append(y)
    return (Px, Py)

def show_points(Px, Py, Dx, Dy, d):
    #Using Dark Mode
    plt.style.use('dark_background')
    
    #show all points
    plt.scatter(x = Px, y = Py, s = 10)
    
    #show closest points
    plt.scatter(x = Dx, y = Dy, c = 'r', s = 14)
    
    #line joining closest points
    plt.plot(Dx,Dy, c = "red")
    
    plt.xlabel('X-axis') # X-Label
    plt.ylabel('Y-axis') # Y-Label
    plt.show()

def bruteforce(Px, Py):
    d = None
    Dx = []
    Dy = []

    #assert: Px contains x-coordinates, Py contains y-coordinates of all points in the graph

    #d initialised to the size of the graph (no two points can be further)
    #for each point in the graph, the loop takes every other point and checks the distance between the two
    
    #INV: for i in 0..Length(Px)-1, consider a point p with coordinates (x=Px[i], y=Py[i]), 0 <= i < Length(Px)
    for i in range(len(Px)):
        
        #INV: for j in i+1..Length(Px)-1, consider a point q with coordinates (x=Px[j], y=Py[j]), i+1 <= j < Length(Px)
        for j in range(i+1, len(Py)):
            if (i != j):
                #store p and q
                Tx = [Px[i], Px[j]]
                Ty = [Py[i], Py[j]]

                #assert: this_dist is the distance between p and q
                this_dist = distance(Tx, Ty)
                if d == None or d>this_dist:
                    d = this_dist
                    Dx = Tx
                    Dy = Ty
        #assert: Dx contains the x-coordinates, Dy contains the y-coordinates of 
        # the closest points in (Px[0..i], Py[0..i]) and every other point in the graph

    #assert: Dx contains the x-coordinates, Dy contains the y-coordinates of the closest points
    return (d, Dx, Dy)

def distance(x, y):
    #returns distance between two points, (x0,y0) & (x1,y1)
    return math.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2)

def merge_sort2(A, B):
    def merge(x, b1, y, b2):
        #assert: two arrays x[] and y[] are given. Each array is individually sorted up. 
        p = len(x)
        q = len(y)
        
        if p == 0 and q == 0:
            return [],[]
        elif p == 0:
            return y, b2 
        elif q == 0:
            return x, b1
        else:
            l = p+q
            #Intialising an array of size l
            z = [None] * (p+q)
            bz = [None] * (p+q)
            i = 0
            xi = 0
            yi = 0

            #INV: for j in 0..i, z[] is sorted up, 0 <= i < l,
            #       l is the sum of lengths of x and y
            #       z[] contains all the elements in x[0..xi] and y[0..yi], 0 <=xi < p, 0 <= yi < q
            while(i < l):
                if xi < p and yi < q:   
                    if x[xi] < y[yi]:
                        z[i] = x[xi]
                        bz[i] = b1[xi]
                        xi += 1
                    else:
                        z[i] = y[yi]
                        bz[i] = b2[yi]
                        yi += 1
                elif xi >= p and yi < q:
                    z[i] = y[yi]
                    bz[i] = b2[yi]
                    yi += 1
                else:
                    z[i] = x[xi]
                    bz[i] = b1[xi]
                    xi += 1 
                i += 1        

            #assert: for i in 0..n-1, z[] is sorted up, where n is the sum of the length of x and y         
        return z, bz
        #assert: x[] and y[] are merged into one array, z[] where z[] is sorted up

    def divide(a,b,n):
        #assert: a[l...r] is established, where n = r-l+1 is the size of a[]
            
        if n == 0:
            return []
        elif n == 1:
            return a,b
        else:
            #partition at midpoint, recursively sort
            mid = n//2
            if n % 2 == 0:
                x, b1 = divide(a[:mid],b[:mid],n//2)
                y, b2 = divide(a[mid:n],b[mid:n],n//2)
                return merge(x, b1, y, b2)
            else:
                x, b1 = divide(a[:mid],b[:mid],n//2)
                y, b2 = divide(a[mid:n],b[mid:n],(mid)+1)
                return merge(x, b1, y, b2)

        #assert: a[l...r] is sorted up

    return divide(A,B,len(A))

def divconquer(Px, Py):
    l = len(Px)
    #Basis:
    if l < 4:
        return bruteforce(Px, Py)
        #Time Complexity: O(3) = constant
    else:
        #find closest pair in left side
        dL, Lx, Ly = divconquer(Px[0:l//2], Py[0:l//2])
        #find closest pair in right side
        dR, Rx, Ry = divconquer(Px[l//2:l], Py[l//2:l])
        #comparing left and right closest distances
        if dR > dL:
            d = dL
            x, y = Lx, Ly
        else:
            d = dR
            x, y = Rx, Ry
        #find closest pair in central band of width 2d
        dC, Cx, Cy = split(d, Px, Py, x, y)
        #compare all three min distances
        dmin = min(dL, dR, dC)  
        #find closest pair
        if dmin == dL:
            return dL, Lx, Ly
        elif dmin == dR:
            return dR, Rx, Ry
        else:
            return dC, Cx, Cy    

def split(d, Px, Py, x, y):
    Cx, Cy = [], []
    med = Px[len(Px)//2]

    #collect points within median band of 2d
    for i in range(len(Px)):
        if med-d <= Px[i] <= med+d:
            Cx.append(Px[i])
            Cy.append(Py[i])

    dmin = d
    Dx, Dy = x, y
    
    #Comparing each points w max 7 of its neighbours
    
    #INV: for 0..i in Cy, j in Cy, 0<=i<=len(Cx), i < j < i+8, i+8<=len(Cy)
    for i in range(len(Cy)):
        k = min(len(Cy)-i, 8)
        #INV: for a given i in Cy, j in Cy[], l in i..j, i < j < i+8
        for j in range(1, k):
            dist = distance([Cx[i],Cx[i+j]],[Cy[i],Cy[i+j]])
            if dist < dmin:
                dmin = dist
                Dx, Dy = [Cx[i],Cx[i+j]],[Cy[i],Cy[i+j]]
        #assert: for a given i in Cy, j in Cy, i < j < i+8
    #assert: for all i in Cy, j in Cy, 0<=i<len(Cx), i < j < i+8, i+8<=len(Cy)
    # dmin contains least distance of all points at i and j in Cx,Cy
    # Dx, Dy contain the closest points in Cx, Cy
    
    return dmin, Dx, Dy

def main():
    #width of graph
    width = 500
    N = 600
    #set of points (x-axis, y-axis)
    Px, Py = gen_points(width, N)
    #sorting points by x-coordinate
    Px, Py = merge_sort2(Px, Py)
    #Initialising closest points
    d, Dx, Dy = divconquer(Px, Py)
    
    #display points on graph
    print(d, Dx, Dy)
    show_points(Px, Py, Dx, Dy, d)

main()