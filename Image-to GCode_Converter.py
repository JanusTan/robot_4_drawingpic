1.	from __future__ import absolute_import, division, print_function, unicode_literals  
2.	import os  
3.	import sys  
4.	import cv2  
5.	import termcolor  
6.	import ast  
7.	import copy  
8.	import argparse  
9.	  
10.	  
11.	class ImageToGcode():  
12.	    def __init__(self,  
13.	                 img,  
14.	                 verbose=False):  
15.	        self.img = cv2.imread(img,0)  
16.	        self.output = ""  
17.	        self.outFile = os.path.splitext(os.path.abspath(img))[0]+".gco"  
18.	        self.spread = 3.175  
19.	        self.nozzles = 12  
20.	        self.increment = self.spread/self.nozzles  
21.	        self.printArea = [200, 200]  
22.	        self.feedrate = 1000  
23.	        self.black = 255  
24.	        self.offsets = [0, 0]  
25.	        self.debug_to_terminal()  
26.	        self.make_gcode()  
27.	  
28.	    def make_gcode(self):  
29.	        self.output = "M106" #Start Fan  
30.	        nozzleFirings = [0 for x in range(0, self.img.shape[1])]  
31.	        nozzleFirings = [copy.copy(nozzleFirings) for x in range(0, 4)]  
32.	        scan = range(0, self.img.shape[0])  
33.	        scan.reverse()  
34.	        for y in scan:  
35.	            for x in range(0, self.img.shape[1]):  
36.	                color = self.img[y,x]  
37.	                if color == self.black:  
38.	                    nozzleFirings[3][x] += 1 << y % self.nozzles  
39.	                else:  
40.	                    pass  
41.	            if y % 12 == 0 and y > 0:  
42.	                for headNumber, headVals in enumerate(nozzleFirings):  
43.	                    for column, firingVal in enumerate(headVals):  
44.	                        if firingVal:  
45.	                            #print(headNumber)  
46.	                            currentOffset = self.offsets  
47.	                            self.output += "G1 X"+str(self.increment*column-currentOffset[0])+" Y"+str(y/12*self.spread-currentOffset[1])+" F"+str(self.feedrate)+"\n"  
48.	                            self.output += "M400\n"  
49.	                            self.output += "M700 P"+str(headNumber)+" S"+str(firingVal)+"\n"  
50.	                            #print (self.output)  
51.	                nozzleFirings = [0 for x in range(0, self.img.shape[1])]  
52.	                nozzleFirings = [copy.copy(nozzleFirings) for x in range(0, 4)]  
53.	        f = open(self.outFile, 'w')  
54.	        f.write(self.output)  
55.	        f.close()  
56.	  
57.	    def debug_to_terminal(self):  
58.	        print("Rows: "+str(self.img.shape[0]))  
59.	        print("Cols: "+str(self.img.shape[1]))  
60.	        print("Spread: "+str(self.spread)+"mm")  
61.	        print("Nozzles: "+str(self.nozzles))  
62.	        print("Print Area: "+str(self.printArea)+"mm")  
63.	        rowStr = ""  
64.	        for y in range(0, self.img.shape[0]):  
65.	            rowStr = ""  
66.	            for x in range(0, self.img.shape[1]):  
67.	                color = self.img[y, x]  
68.	                if color == self.black:  
69.	                    rowStr += " "  
70.	                else:  
71.	                    rowStr += termcolor.colored(" ", 'white', 'on_white')  
72.	            print (rowStr)  
73.	  
74.	  
75.	if __name__ == "__main__":  
76.	    #Setup Command line arguments  
77.	    parser = argparse.ArgumentParser(prog="image-to-gcode.py",  
78.	                                     usage="%(prog)s [options] input...",  
79.	                                     description="Convert bitmaps to gcode."  
80.	                                     )  
81.	      
82.	    parser.add_argument("input",  
83.	                        help="input file, defaults to stdin"  
84.	                        )  
85.	    parser.add_argument('--version',  
86.	                        action='version',  
87.	                        version="%(prog)s 0.0.1-dev"  
88.	                        )  
89.	  
90.	  
91.	    #Always output help by default  
92.	    if len(sys.argv) == 1:  
93.	        parser.print_help()  
94.	        sys.exit(0)  # Exit after help display  
95.	                                           
96.	    args = parser.parse_args()  
97.	                 
98.	    imageProcessor = ImageToGcode(img=args.input,  
