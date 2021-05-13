import numpy as np
import time

class Point():

    def __init__(self, newx, newy, newz):
        self.x = newx
        self.y = newy
        self.z = newz

    def Update(self, otherx, othery, otherz):
        self.x = otherx
        self.y = othery
        self.z = otherz

    def __pow__(v, u):
        ##Crossproduct
    	return Point(
            v.y * u.z - v.z * u.y,
            v.z * u.x - v.x * u.z,
            v.x * u.y - v.y * u.x)
    def mod(self):
    	return pow((self.x ** 2) + (self.y ** 2) + (self.z ** 2), 0.5)
    def dot(self, v):
        return (self.x * v.x) + (self.y * v.y) + (self.z * v.z)
    def __add__(v, u):
        return Point(v.x + u.x, v.y + u.y, v.z + u.z)
    def __sub__(v, u):
        return Point(v.x - u.x, v.y - u.y, v.z - u.z)
    def __mul__(self, a):
        return Point(self.x*a,self.y*a,self.z*a)
    def __rmul__(self, a:float):
        return Point(self.x*a,self.y*a,self.z*a)
    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x==other.x and self.y==other.y and self.z==other.z)
        else:
            return False
    def __str__(self):
        return "{x},{y},{z}".format(x = self.x, y = self.y, z = self.z)

class Perimeter():

    def __init__(self, *args):
        self.area = Point(0,0,0)
        if args:
            if not isinstance(args[0][0], Point):
                ## np array of classes seems to point (memory level) at
                ##the first element only!!!
                ## This is a serious problem, keep an eye on it!!
                self.points = [Point(0,0,0) for i in range(args[0].shape[0])]
                for i in range(args[0].shape[0]):
                    self.points[i].Update(
                        args[0][i][0],
                        args[0][i][1],
                        args[0][i][2]
                        )
                ## Now back to numpy arrays...
                self.points = np.array(self.points)
            else:
                self.points = args[0]
        else:
            self.points = np.empty(0)

    def append(self, np_array):
    	self.points = np.append(self.points, np.array([np_array]), axis=0)
    def perimeter_fusion(self, attachment): ##not implemented
        '''
            Given a new perimeter (attachment), if we wish to connect them together
        we could gather the to closest points of each and simply draw a line linking
        them up.
            However, to avoid surfaces intersection in the final 3D mesh, we could
        acctually connect the (i-1,i+1) pair of points in the first perimeter to the
        (j-1,j+1) pair on the seccond one, given that (i,j) is the line connecting
        the nearest points from each perimeter.
        '''
        if not isinstance(attachment, Perimeter):
            raise NameError("fusion_perimeter encountered a non Perimeter data type\nCould not fusion perimeters together.\nCheck for possible empty perimeter/contours.")
        M = self.points.shape[0]
        N = attachment.pointsshape[0]
        dist = np.inf
        for i in range(self.points.shape[0]):
            for j in range(attachment.points.shape[0]):
                pi = self.points[i]
                pj = attachment.points[j]
                if (pi-pj).mod() < dist:
                    dist = (pi-pj).mod()
                    nearest = [i,j]

        final

        return
    def fix_distance(self):
        ## Creates new points between points that are too
        ##far apart from each other
        counter = 0
        distance = np.array([0.]*(self.points.shape[0]-1), dtype=float)

        for i in range(self.points.shape[0]-1):
            distance[i] = (self.points[i]-self.points[i+1]).mod()**2

        d0 = np.sum(distance)/(self.points.shape[0])
        aux = 0
        for i in range(self.points.shape[0]-1):
            if distance[i] >= (3*d0):
                factor = int(distance[i]/d0)
                points_list = np.array([Point(0,0,0)]*(factor-1))
                for j in range(1, factor):
                    np_index = j/factor
                    new_point = (self.points[i+counter]-self.points[i+1+counter])*(np_index)
                    new_point += self.points[i+counter+1]
                    points_list[j-1] = new_point
                    aux += 1
                points_list = np.flip(points_list, axis=0)
                self.points = np.insert(self.points, i+counter+1, points_list)
                counter += aux
                aux = 0
    def remove_overlap(self): ##fix conditions
        def neighbourhood(p1,p2) -> bool:
            delta = 1e-10
            if (self.points[i] - self.points[j]).mod() <= delta:
                return True
            return False
        aux = self.points
        counter = 0
        eta = 1e-5
        for i in range(self.points.shape[0]-1):
            for j in range(i+1,self.points.shape[0]-1):
                if neighbourhood(self.points[i],self.points[j]):
                    if j == i+1:
                        #aux = np.delete(aux,j)
                        print("consecutive")
                    if j == i+2:
                        print("angle")
                    if j > i+2:
                        print("move it")
                    aux = np.delete(aux,j)
                    #self.points[j] += eta*(self.points[j]-self.points[j-1])
        self.points = aux
    def c_clockwise(self):
        ## Reorients surface to counter-clockwise
        ##and creates a area vector
        self.area = Point(0,0,0)

        for n in range(self.points.shape[0]-2):
            self.area += (self.points[n]-self.points[n+1])**(self.points[n+1]-self.points[n+2])
        self.area = (1/self.area.mod())*self.area
        '''
            TOO LONG TO BE IN THE CODE??
            We are choosing 4 octants to be considered cclockwise and
        4 others to be clockwise. Also, the there must be a one to one
        correspondence between a cclockwise octant and a clockwise
        octant.
            One simple (arbitrary) way of doing this is choosing y>0
        sub-region to be the cclockwise/clockwise space, and y<0 the
        clockwise/cclockwise.
            One thing that we note is that the plane y=0 is undifined
        with that coice, so lets add a new restriction. If y is not
        sufficient to  determine the orientation (i.e., y=0), then we
        go back to the more usual 2D orientation. If we simply apply
        x>0 (or z>0) criteria to define cclockwise/clockwise orientation,
        we've exhausted all possibilities of orientation.
        '''
        if self.area.x > -1e-13 and self.area.x < 1e-13:
            self.area.x = 0
        if self.area.y > -1e-13 and self.area.y < 1e-13:
            self.area.y = 0
        if self.area.z > -1e-13 and self.area.z < 1e-13:
            self.area.z = 0

        if self.area.y < 0:
            self.points = np.flip(self.points,0)
            self.area = -1*self.area
            return
        if self.area.y == 0:
            if self.area.x < 0:
                self.points = np.flip(self.points,0)
                self.area = -1*self.area
    def geometric_center(self) -> Point:
        x = 0
        y = 0
        z = 0
        N = self.points.shape[0]
        for i in range(N):
            x += self.points[i].x
            y += self.points[i].y
            z += self.points[i].z
        return Point(x/N,y/N,z/N)
    def find_intersection(self, p1, p2, p3, p4, border = True) -> bool:
        ## Lets find a new algorithm to find intersections
        ##between lines
        '''
        https://stackoverflow.com/questions/2316490/the-algorithm-to-find-the-point-of-intersection-of-two-3d-line-segment
        Read all the comments!!

        s = Dot(Cross(dc, db), Cross(da, db)) / Norm2(Cross(da, db))

        t = Dot(Cross(dc, da), Cross(da, db)) / Norm2(Cross(da, db))

        da = p2 - p1
        db = p4 - p3
        dc = p3 - p1
        '''
        da = p2 - p1
        db = p4 - p3
        dc = p3 - p1

        norm2 = ((da**db).mod())**2
        if norm2 == 0:
            d1 = p1 - p3
            d2 = p2 - p3
            d3 = p1 - p4
            d4 = p2 - p4
            cond1 = d1.dot(d2) < 0
            cond2 = d3.dot(d4) < 0
            if cond1 or cond2:
                return True
            else:
                return False
        s = (dc**db).dot(da**db) / norm2
        t = (dc**da).dot(da**db) / norm2
        if border:
            if ((s>=0 and s<=1) and (t>=0 and t<=1)):
                return True
            return False
        else:
            if ((s>0 and s<1) and (t>0 and t<1)):
                return True
            return False
    def fix_intersection(self):
        '''
        --Fixing intersections
        .Let i and j be two independent indexations to a list of Points (x,y)
        .With i < j, if the Points between i and i+1 creates a line that
        .intersects the line created by j and j+1, than fix the intersection by:
        revesing the order of the Points in the list from i+1 and j+1
        .This fixes the list in the sense that it will be no longer a
        self-intersecting curve
        '''

        p_points = self.points.shape[0]
        Check = True
        Loops = 0   ## flexibility condition to avoid infinity
                    ##loops that may occur inside the while

        while Check:
            found = False
            for i in range(p_points-3):
                for j in range(i+2, p_points-1):
                    if i==0 and j==p_points-2:
                        break
                    '''
                        If we find a point that rests exactly on top of a line
                    segment, then we will perturbe it by a small amount to avoid
                    having a self intersecting surface on the final mesh.
                        Trying to figure out w
                    '''
                    if self.find_intersection(
                            self.points[i],
                            self.points[i+1],
                            self.points[j],
                            self.points[j+1]):
                        found = True
                        aux = np.array([Point(0,0,0)])
                        for fix in self.points[(i+1):(j+1)]:
                            aux = np.append(aux,fix)
                        aux = np.delete(aux,0)
                        aux = np.flip(aux, axis=0)
                        if aux.size != 0:
                            for replace in range(i+1, j+1):
                                self.points[replace] = aux[replace-i-1]
                        break
            ##Loop break if many intersections are encoutered
            Loops += 1
            if not found:
                Check = False
            if Loops > 10:
                Check = False

    def __str__(self):
        return "{L}\nwith shape = {S}".format(
                    L = [self.points[i].__str__()\
                        for i in range(self.points.shape[0])],
                    S = (self.points.shape)+(2,)
                    )
    def __add__(v,u):
        ## Caculates best point to connect two contours contained in the
        ## same slice

        M = v.points.shape[0]
        N = u.points.shape[0]
        cost_matrix = np.zeros((M-1,N-1))
        for m in range(M-1):
        	for n in range(N-1):
        		cost_matrix[m,n] = (v.points[m]-u.points[n]).mod()
        allMin = np.where(cost_matrix==np.amin(cost_matrix))
        final_min_cord = list(zip(allMin[0], allMin[1]))[0]
        vari = M+N
        final = [Point(0,0,0)]*(vari)
        m = 0
        n = final_min_cord[1]
        mc = 0
        nc = 0
        while mc<M:

            final[mc+nc] = Point(
                v.points[m].x,
                v.points[m].y,
                v.points[m].z)

            if m == final_min_cord[0]:

                while nc<N-1:

                    final[mc+nc] = Point(
                        u.points[n].x,
                        u.points[n].y,
                        u.points[n].z)
                    n += 1
                    nc += 1

                    if n == N:
                        n = 0

                final[mc+nc] = Point(
                    u.points[final_min_cord[1]].x,
                    u.points[final_min_cord[1]].y,
                    u.points[final_min_cord[1]].z)
                final[mc+nc + 1] = Point(
                    v.points[final_min_cord[0]-1],
                    v.points[final_min_cord[0]-1],
                    v.points[final_min_cord[0]-1])
                m += 0
                mc += 1

            m += 1
            mc += 1

            if m == M:

                m = 0

        final[vari-1] = Point(
            v.points[v.points.shape[0]-2].x,
            v.points[v.points.shape[0]-2].y,
            v.points[v.points.shape[0]-2].z)

        return final

class Surface():

    def __init__(self):
        self.slices = np.empty(0)
        self._surface = False
        self._intersection_range = 15
        self.border_intersection = False

    def create_island(self, npArray):
        #I = [Perimeter().append(npArray[i]) for i in range(npArray.shape[0])]
    	self.slices = np.append(self.slices, np.array([I]), axis=0)
    def add_island(self, *arg):
        if arg:
            self.slices = np.append(
                self.slices,
                np.array([arg[0]]),
                axis=0
                )
        else:
            self.slices = np.append(
                self.slices,
                np.array([Perimeter()]),
                axis=0
                )
    def mesh_out(self):
        if self.out_surface:
            out = 0
        else:
            error = 0
    def build_surface(self):
        self.surfaceV = "" ##3d reconstructed surface
        self.surfaceE = ""
        total_shift = 0
        for n in range(self.slices.shape[0]-1):
            print(n)
            dist_matrix =  self.__CostMatrix(self.slices[n],self.slices[n+1])
            '''

                After reordering the both sequences of points, we need
            to a way to conect all in between points that represent a
            surface that:
                1) is not self intersecting
                2) has the smallest possible area
                3) is closed
            -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
                If we find a point that all of its connections create
            intersections, than we must never use this point in our final
            mesh. So we list all this points per stitched surface and exclude
            them from our path find algorithm by setting its value to
            infinity.
            '''
            bad_connect = []

            while not self.border_intersection: ##After finding a path with o intersections
                ## finding all min values contained inthe matrix
                ##there's usually only one, but the value might
                ##be repeated somewhere
                closest_point_dist = np.amin(dist_matrix)
                allMin = np.where(dist_matrix == closest_point_dist)
                list_cordinates = list(zip(allMin[0], allMin[1]))
                final_min_cord = list_cordinates[0]
                f0 = final_min_cord[0]
                f1 = final_min_cord[1]

                ## Re-order the points: put the first connection at (0,0)
                reordered_upper =  self.__Reordering(
                    self.slices[n],
                    final_min_cord[0])
                reordered_lower =  self.__Reordering(
                    self.slices[n+1],
                    final_min_cord[1])

                cost_matrix =  self.__CostMatrix(reordered_upper,reordered_lower)

                for bad in bad_connect:
                    bad1= 0
                    bad2= 0
                    if bad[0]>=f0:
                        bad1 = bad[0]-f0
                    else:
                        bad1 = bad[0]+(self.slices[n].points.shape[0]-f0)
                    if bad[1]>=f1:
                        bad2 = bad[1]-f1
                    else:
                        bad2 = bad[1]++(self.slices[n+1].points.shape[0]-f1)
                    cost_matrix[bad1,bad2] = np.inf

                mincost,the_path,wrong = self.__FindPath(
                    cost_matrix,
                    self.slices[n].points.shape[0],
                    self.slices[n+1].points.shape[0],
                    reordered_upper,
                    reordered_lower)

                ##fixing relative order to absolute/initial order
                if not isinstance(wrong, int):
                    if wrong[0]+f0 < self.slices[n].points.shape[0]:
                        wrong[0] += f0
                    else:
                        wrong[0] = f0+wrong[0]-self.slices[n].points.shape[0]
                    if wrong[1]+f1 < self.slices[n+1].points.shape[0]:
                        wrong[1] += f1
                    else:
                        wrong[1] = f1+wrong[1]-self.slices[n+1].points.shape[0]
                    if [wrong[0],wrong[1]] in bad_connect:
                        dist_matrix[f0,f1] = np.inf
                    else:
                        bad_connect.append([wrong[0],wrong[1]])
                else:
                    dist_matrix[f0,f1] = np.inf

            ## The path is calculated based on the reordered points,
            ##so we should invert the transformation so that we have
            ##the path for the original set of points
            the_path =  self.__FixPathOrder(
                the_path,
                final_min_cord,
                self.slices[n].points.shape[0],
                self.slices[n+1].points.shape[0])

            self.surfaceV +=  self.__Vertices(self.slices[n].points)
            self.surfaceE +=  self.__Edges(
                the_path,
                self.slices[n].points.shape[0]-1,
                self.slices[n+1].points.shape[0]-1,
                total_shift)

            total_shift += self.slices[n].points.shape[0] - 1
            self.border_intersection = False

        self.surfaceV +=  self.__Vertices(self.slices[n+1].points)
        self.surfaceE += self.__CloseSurface(self.slices.shape[0]-1, total_shift)
        self.surfaceE += self.__CloseSurface(0) ##intial slice closure
        self.out_surface = True
    def super_resolution(self):
        self.super_surface

    ## Not meant for end-user
    def __CloseSurface(self, closing_index, shift=0):
        '''
            Slicing an ear using prune-and-search

            Given a good sub-polygon GSP of a polygon P and
            a vertex p_i of GSP this algorithm reports a proper ear.
                1. if p_i, is an ear report it and exit.
                2. Find a vertex pj such that (p_i, p_j) is a diagonal of
                GSP. Let GSP' be the good sub-polygon of GSP
                formed by (p_i, p_j). Re-label the vertices of GSP' so
                that p_i=p_0 and p_j=p_k-1 (or p_j=p_0 and p_1=p_k-1,
                as appropriate) where k is the number of vertices
                of GSP'.
                3. FindAnEar(GSP',floor(k/2)).
        '''
        def find_ear(Polygon, GSP, shift, area):
            def diagonal_clip(Polygon, GSP, area):
                def check_inside(Polygon, GSP, p_i, p_j, area) -> bool:
                    '''
                        We first check if the direction change in the diagonal
                        is smaller then the one made by going from the current
                        point to the next one. For example, consider the case:
                            1) from p_k going to p_k+1 we make a turn of 60o
                            2) from p_k to p_j (creating a diagonal) we make a
                            turn of 45 deegrees, then we are inside the polygon
                        If we are inside the polygon, then we need to check if
                        the diagonal intersects any order line segment in the
                        perimeter. If that is not the case, then we may say that
                        the diagonal is trully inside the polygon.
                    '''
                    displacement1 = GSP[p_i][0] - GSP[p_i-1][0]
                    if p_i+1 == GSP.shape[0]:
                        displacement2 = (GSP[0][0] - GSP[p_i][0])
                    else:
                        displacement2 = (GSP[p_i+1][0] - GSP[p_i][0])
                    diagonal_segment = (GSP[p_j][0] - GSP[p_i][0])

                    ## checking if they turn inside or not
                    sign_angle_i = displacement1**displacement2
                    if sign_angle_i.mod()>0:
                        sign_angle_i = sign_angle_i*(1/sign_angle_i.mod())
                    sign_angle_j = displacement1**diagonal_segment
                    if sign_angle_j.mod()>0:
                        sign_angle_j = sign_angle_j*(1/sign_angle_j.mod())
                    if sign_angle_i.mod()==0 and sign_angle_j.mod()==0:
                        return False
                    if (sign_angle_i+area).mod()>area.mod():
                        if sign_angle_j.mod()==0:
                            return False
                        inside1 = True
                    else:
                        inside1 = False
                    if (sign_angle_j+area).mod()>area.mod():
                        inside2 = True
                    else:
                        if sign_angle_i.mod()==0:
                            return False
                        inside2 = False


                    if inside1 and not inside2:
                        return False

                    '''
                     Remember that all the angles calculated range from
                    0 to pi. So we need the inside1 and inside2 to teel
                    whether or not its trully ranging from 0 to pi or if it
                    should be from pi to 2pi
                    '''
                    angle_i = displacement2.dot(displacement1)
                    angle_i = angle_i/(displacement2.mod()*displacement1.mod())
                    if angle_i>1:
                        print(angle_i)
                        angle_i = 1
                    if angle_i<-1:
                        print(angle_i)
                        angle_i = -1
                    angle_i = np.pi - np.arccos(angle_i)

                    angle_j = diagonal_segment.dot(displacement1)
                    angle_j = angle_j/(diagonal_segment.mod()*displacement1.mod())
                    if angle_j>1:
                        print(angle_j)
                        angle_j = 1
                    if angle_j<-1:
                        print(angle_j)
                        angle_j = -1
                    angle_j = np.pi - np.arccos(angle_j)
                    if inside2 and inside1:
                        if angle_j>=angle_i:
                            return False
                    if not inside2 and not inside1:
                        if angle_i>=angle_j:
                            return False

                    for index in range(Polygon.shape[0]-1):
                        if Perimeter().find_intersection(
                            Polygon[index][0],
                            Polygon[index+1][0],
                            GSP[p_i][0],
                            GSP[p_j][0],
                            False):
                            return False
                    return True
                half = int((GSP.shape[0]-1)/2)
                for j in range(2,half):
                    for i in range(GSP.shape[0]-j):
                        p_i = i
                        p_diag = p_i+j
                        if p_diag == GSP.shape[0]:
                            p_diag = 0
                        if check_inside(Polygon, GSP, p_i, p_diag, area):
                            if p_diag>p_i:
                                gsp1 = GSP[p_i:p_diag+1]
                                sub_deletion = [[k] for k in range(p_i+1,p_diag)]
                                gsp2 = np.delete(GSP, sub_deletion, axis=0)
                            else:
                                gsp1 = GSP[p_diag:p_i+1]
                                sub_deletion = [[k] for k in range(p_diag+1,p_i+1)]
                                gsp2 = np.delete(GSP, sub_deletion, axis=0)
                            return gsp1, gsp2
                raise Exception("Failed to find diagonal in subpolygon\nCheck CloseSurface method")
            def ear(GSP):
                if GSP.shape[0] <= 4:
                    return True
                return False
            if ear(GSP):
                if GSP.shape[0] == 4:
                    p0 = GSP[0][1]
                    p1 = GSP[1][1]
                    p2 = GSP[2][1]
                    s = "f " +str(p0+shift) +\
                            " " + str(p1+shift) +\
                            " " + str (p2+shift) + "\n"
                    p0 = GSP[2][1]
                    p1 = GSP[3][1]
                    p2 = GSP[0][1]
                    s += "f " +str(p0+shift) +\
                            " " + str(p1+shift) +\
                            " " + str (p2+shift) + "\n"
                if GSP.shape[0] == 3:
                    p0 = GSP[0][1]
                    p1 = GSP[1][1]
                    p2 = GSP[2][1]
                    s = "f " +str(p0+shift) +\
                            " " + str(p1+shift) +\
                            " " + str (p2+shift) + "\n"

                if GSP.shape[0] < 3:
                    raise Exception("GSP subdivision failed")
                return s
            else:
                edges = ''
                gsp1, gsp2 = diagonal_clip(Polygon, GSP, area)
                e1 = find_ear(Polygon, gsp1, shift, area)
                e2 = find_ear(Polygon, gsp2, shift, area)
                edges += e1 + e2
            return edges
        number_points = self.slices[closing_index].points.shape[0]-1
        area_vec = self.slices[closing_index].area
        points = np.array([[Point(0,0,0),0]]*number_points)

        for i in range(number_points):
            points[i][0] = self.slices[closing_index].points[i]
            points[i][1] = i+1 ##+1 to correct the .obj file format counting
        edges = find_ear(points, points, shift, area_vec)

        return edges
    def __CostMatrix(self, reordered_upper, reordered_lower) -> np.ndarray:
        ## Upper stands for the surface on top and Lower for the one in the bottom
        M = reordered_upper.points.shape[0]
        N = reordered_lower.points.shape[0]
        cost_matrix = np.zeros((M-1,N-1))

        for m in range(M-1):
            for n in range(N-1):
                cost_matrix[m,n] = (reordered_upper.points[m] - reordered_lower.points[n]).mod()

        return cost_matrix
    def __FindPath(self, final_matrix, M, N, reordered_upper, reordered_lower):
        def surface_intersection(the_path, path_limit, next, upper, reordered_upper, reordered_lower) -> bool:
            def line_triangle_intersection(q1, q2, p1, p2, p3):
                ## stackoverflow.com/questions/42740765/intersection-between-line-and-triangle-in-3d
                def volume(a, b, c, d):
                    vol = (b-a) ** (c-a)
                    vec = d - a
                    ## inner product
                    vol = vol.x*vec.x + vol.y*vec.y + vol.z*vec.z
                    return vol/6

                condition = volume(q1,p1,p2,p3)*volume(q2,p1,p2,p3)
                if condition < 0:
                    if volume(q1,q2,p1,p2)*volume(q1,q2,p2,p3) > 0 and\
                        volume(q1,q2,p1,p2)*volume(q1,q2,p3,p1) > 0  and\
                        volume(q1,q2,p2,p3)*volume(q1,q2,p3,p1) > 0 :
                        supp_arr = [i,j,i,j+1]
                        return True
                return False
            if path_limit < 3:
                return [-1,-1], False

            ## if speed is needed in the future
            ##we may try limiting the search range
            if path_limit > self._intersection_range-1:
                search_limit = 0 #path_limit - self._intersection_range
            else:
                search_limit = 0
            if path_limit < the_path.shape[0]:
                p_index = the_path[path_limit]
            else:
                return [-1,-1], False

            if upper:
                p1 = reordered_upper.points[next[0]]
                p2 = reordered_lower.points[next[1]]
                p3 = reordered_lower.points[p_index[1]]
            else:
                p1 = reordered_lower.points[next[1]]
                p2 = reordered_upper.points[next[0]]
                p3 = reordered_upper.points[p_index[0]]
            for i in the_path[search_limit:path_limit+1]:
                a0 = int(i[0])
                b0 = int(i[1])
                q1 = reordered_upper.points[a0]
                q2 = reordered_lower.points[b0]
                if line_triangle_intersection(q1, q2, p1, p2, p3):
                    return [a0,b0], True

            return [-1,-1], False

        M = M - 1
        N = N - 1

        ofinal_matrix = final_matrix
        min_cost = np.zeros((M,N))
        min_cost[0][0] = final_matrix[0][0]

        ## setting the upper border cost
        for j in range(1,N):
            min_cost[0][j] = min_cost[0][j-1] + final_matrix[0][j]

        ## setting the left border cost
        for i in range(1,M):
            min_cost[i][0] = min_cost[i-1][0] + final_matrix[i][0]

        for i in range(1,M):
            for j in range(1,N):
                best = min(min_cost[i-1][j],min_cost[i][j-1])
                min_cost[i][j] = best + final_matrix[i][j]
                if min_cost[i][j]<=0:
                        print("Negative cost on the path")

        ## Everything from now on is a way of finding what's the acctual path
        ##not only the cost of getting there.

        var1 = False
        var2 = False
        the_path = np.array([[0,0]]*(M+N-2), dtype=int)
        the_path[M+N-3] = [M-1,N-1]
        m = M-1
        n = N-1
        the_path = np.insert(the_path, 0, [[M-1,N-1]], axis=0)

        for i in range(M+N-3,-1,-1):
            index = M + N - i - 3
            if m>0 and n>0:
                if min_cost[m-1][n] < min_cost[m][n-1]:
                    check = surface_intersection(the_path,
                                index,
                                [m-1,n],
                                False,
                                reordered_upper,
                                reordered_lower)
                    if check[1]:
                        check2 = surface_intersection(the_path,
                                    index,
                                    [m,n-1],
                                    True,
                                    reordered_upper,
                                    reordered_lower)
                        if check2[1]:
                            ##[m,n] -> Bad point that always create intersection
                            return 0,0,[m,n]
                        else:

                            n = n - 1
                    else:
                        if not min_cost[m-1][n] == np.inf:
                            m = m - 1
                        else:
                            return 0,0,[m,n]
                else:
                    check = surface_intersection(the_path,
                                index,
                                [m,n-1],
                                True,
                                reordered_upper,
                                reordered_lower)
                    if check[1]:
                        check2 = surface_intersection(the_path,
                                    index,
                                    [m-1,n],
                                    False,
                                    reordered_upper,
                                    reordered_lower)
                        if check2[1]:
                            return 0,0,[m,n]
                        else:
                            m = m - 1
                            counter = 0
                    else:
                        if not min_cost[m][n-1] == np.inf:
                            n = n - 1
                            counter = 0
                        else:
                            return 0,0,[m,n]
            else:
                if m<=0:
                    check = surface_intersection(the_path,
                                index,
                                [m,n-1],
                                True,
                                reordered_upper,
                                reordered_lower)
                    if check[1]:
                        return 0,0,[m,n]
                    n = n - 1
                else:
                    check = surface_intersection(the_path,
                                index,
                                [m-1,n],
                                False,
                                reordered_upper,
                                reordered_lower)
                    if check[1]:
                        return 0,0,[m,n]
                    m = m - 1

            the_path[index+1] = [m,n] ##+1 because of the insert before the loop

            if [m,n] == [0,N-1]:
                var1 = True
            if [m,n] == [M-1,0]:
                var2 = True

        ##var1 and var2 are used to add a single point in order to make the
        ##the graph a closed cicle

        if var1:
            check = surface_intersection(the_path,
                        the_path.shape[0],
                        [M-1,0],
                        False,
                        reordered_upper,
                        reordered_lower)
            if check[1]:
                ### remove later
                print("border0.1")
                #####
                return 0,0, [m,n]

            the_path = np.append(the_path, [[M-1,0]], axis=0)
            self.border_intersection = True
            return [min_cost,the_path,0]
        if var2:
            the_path = np.append(the_path, [[0,N-1]], axis=0)
            min_cost[min_cost.shape[0]-1,min_cost.shape[1]-1] += ofinal_matrix[0][N-1]
            self.border_intersection = True
            return [min_cost,the_path,0]

        if ofinal_matrix[M-1][0]<ofinal_matrix[0][N-1]:
            check = surface_intersection(the_path,
                        the_path.shape[0],
                        [M-1,0],
                        True,
                        reordered_upper,
                        reordered_lower)
            if check[1]:
                ### remove later
                print("border0.1")
                #####
                return 0,0,[m,n]
            the_path = np.append(the_path, [[M-1,0]], axis=0)
            min_cost[min_cost.shape[0]-1,min_cost.shape[1]-1] += ofinal_matrix[M-1][0]
            self.border_intersection = True
            return [min_cost,the_path,0]
        else:
            #print(M,N, the_path.shape)
            check = surface_intersection(the_path,
                        the_path.shape[0],
                        [0,N-1],
                        False,
                        reordered_upper,
                        reordered_lower)
            check2 = surface_intersection(the_path[::-1],
                        the_path.shape[0],
                        [0,N-1],
                        True,
                        reordered_upper,
                        reordered_lower)
            if check[1] or check2[1]:
                ### remove later
                print("border0.1")
                #####
                return 0,0, [m,n]
            the_path = np.append(the_path, [[0,N-1]], axis=0)
            min_cost[min_cost.shape[0]-1,min_cost.shape[1]-1] += ofinal_matrix[0][N-1]
            self.border_intersection = True
            return [min_cost,the_path,0]
    def __Reordering(self, contour, final_min_cord : int):
        M = contour.points.shape[0]
        reordered = [Point(0,0,0)]*M

        for i in range(M):

            if (i-final_min_cord) >= 0:

                index = i - final_min_cord
                reordered[index] = Point(
                    contour.points[i].x,
                    contour.points[i].y,
                    contour.points[i].z
                    )
            else:
                index = M - final_min_cord + i - 1
                reordered[index] = Point(
                    contour.points[i].x,
                    contour.points[i].y,
                    contour.points[i].z
                    )

        reordered[M-1] = Point(
            contour.points[final_min_cord].x,
            contour.points[final_min_cord].y,
            contour.points[final_min_cord].z
            )

        return Perimeter(np.array(reordered))
    def __FixPathOrder(self, path, final_min_cord : list, M, N) -> np.ndarray:
        fix_path = np.zeros(path.shape, dtype=int)
        for i in range(path.shape[0]):
            if path[i][1]+final_min_cord[1]<=N-2:
                fix_path[i][1] = path[i][1] + final_min_cord[1]
            else:
                fix_path[i][1] = path[i][1] - (N - 1 - final_min_cord[1])
            if path[i][0]+final_min_cord[0]<=M-2:
                fix_path[i][0] = path[i][0] + final_min_cord[0]
            else:
                fix_path[i][0] = path[i][0] - (M - 1 - final_min_cord[0])
        return fix_path
    def __Vertices(self, vertices) -> str:
        string = ""
        for i in range(vertices.shape[0]-1):
            text =  "v " + str(vertices[i].x) +\
                    " " + str(vertices[i].y) +\
                    " " + str(vertices[i].z) + "\n"
            string = string + text
        return string
    def __Edges(self, the_path : np.ndarray, M, N, shift) -> str:
        string = ""

        for i in range(the_path.shape[0]-1):

            if int(the_path[i][1]) == int(the_path[i+1][1]):

                text1 = "f " +str(int(the_path[i][0])+1+shift) +\
                        " " + str(int(the_path[i][1])+1+M+shift) +\
                        " " + str (int(the_path[i+1][0])+1+shift) + "\n"

                string += text1

            else:

                text2 = "f " +str(int(the_path[i][1])+1+M+shift) + \
                        " " + str(int(the_path[i+1][0])+1+shift) + \
                        " " + str (int(the_path[i+1][1])+1+M+shift) + "\n"

                string += text2

        if  int(the_path[the_path.shape[0]-1][0])+1 == int(the_path[the_path.shape[0]-1][1])+1+M or\
            int(the_path[the_path.shape[0]-1][0])+1 == int(the_path[0][0])+1 or\
            int(the_path[0][0])+1 == int(the_path[the_path.shape[0]-1][1])+1+M:

            string =    string + "f " +\
                        str(int(the_path[the_path.shape[0]-1][1])+1+M+shift) + " " +\
                        str(int(the_path[the_path.shape[0]-1][0])+1+shift) + " " +\
                        str (int(the_path[0][1])+1+M+shift) + "\n"

        else:

            string =    string + "f " +\
                        str(int(the_path[the_path.shape[0]-1][0])+1+shift) + " " +\
                        str(int(the_path[the_path.shape[0]-1][1])+1+M+shift) + " " +\
                        str (int(the_path[0][0])+1+shift) + "\n"

        return string
    def __str__(self):
        return "Surface shape = {S}\nPerimeters shape = {L}".format(
                                            L = [self.slices[i].points.shape[0] for i in range(self.slices.shape[0])],
                                            S = (self.slices.shape[0]))
