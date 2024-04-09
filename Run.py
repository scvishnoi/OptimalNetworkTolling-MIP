from network import *

net = Network("SiouxFalls_net.tntp", "SiouxFalls_trips.tntp")
#net = Network("braess_net.tntp", "braess_trips.tntp")
#net = Network("ninenode_net.tntp", "ninenode_trips.tntp")

net.userEquilibrium("FW", 20, 1e-6, net.averageExcessCost)
print("done equilibrium solving!")


#############################################################################

allOD_Paths=dict()
numpaths=dict()
numpaths[0]=0
c=1
MASTER=[]
for i in net.ODpair:
   #print(i)
   O=net.ODpair[i].origin
   D=net.ODpair[i].destination
   net.printAllPaths(O,D)
   allOD_Paths[i]=net.MASTER
   numpaths[c]=len(net.MASTER)
   c+=1

print("done finding paths! Cheer Up")
'''
for i in net.ODpair:
   for path in allOD_Paths[i]:
      MASTER.append(path)
'''
#############################################################################
'''   
Path_links=[]
for path in MASTER:
    currentpath=[]
    for node in range(0,len(path)-1):
       currentpath.append('('+str(path[node])+','+str(path[node+1])+')')
    Path_links.append(currentpath)
'''
Path_linksOD=dict()
for i in net.ODpair:
   Path_linksOD[i]=[]
   for path in allOD_Paths[i]:
      currentpath=[]
      for node in range(0,len(path)-1):
         currentpath.append('('+str(path[node])+','+str(path[node+1])+')')
      Path_linksOD[i].append(currentpath)

print("Converted Paths from nodes to links! Just hold on for just a little bit more")
#############################################################################

sorted_links=[]
for i in net.link:
   sorted_links.append(i)

sorted_links.sort()

#############################################################################
'''
Z=[]
for path in Path_links:
    currentz=[]
    for link in sorted_links:
        flag=0
        for link1 in path:
            if link==link1:
                currentz.append(1)
                flag=1
                break
        if(flag==0):    
            currentz.append(0)
    Z.append(currentz)
'''
Z_OD=dict()
for i in net.ODpair:
   Z_OD[i]=dict()
   c=1
   for path in Path_linksOD[i]:
      currentz=[]
      for link in sorted_links:
         flag=0
         for link1 in path:
            if link==link1:
               currentz.append(1)
               flag=1
               break
         if(flag==0):    
            currentz.append(0)
      Z_OD[i][c]=currentz
      c+=1
print("done with z dict! Almost There")
#############################################################################

PathCostsOD=dict()
for i in net.ODpair:
   PathCostsOD[i]=dict()
   for path in Z_OD[i]:
      cost=0
      c=0
      for link in Z_OD[i][path]:
         cost+=net.link[sorted_links[c]].cost*link
         c+=1
      PathCostsOD[i][path]=cost
'''
for i in net.ODpair:
   print(i)
   for j in PathCostsOD[i]:
      print(Z_OD[i][j])
      print(PathCostsOD[i][j])
   break
'''
#############################################################################
      
print("Congratulations!!!!! Work Complete")

'''
file1 = open("Z_ninenode.txt","r+")
for num in range(0,(len(sorted_links))):
   line=''
   flag=1
   for z in Z:
       if(flag==1):
           line=str(z[num])
           flag=0
       else:
           line=line+','+str(z[num])
   file1.write(line+"\n")

flag=1
for i in range(1,len(numpaths)):
   flag=1
   line=''
   for j in range(0,numpaths[i-1]):
      if(flag==1):
         line='0'
         flag=0
      else:
         line=line+',0'
   for j in range(numpaths[i-1],numpaths[i]):
      if(flag==1):
         line='1'
         flag=0
      else:
         line=line+',1'
   for j in range(numpaths[i],len(Z)):
      line=line+',0'
   file1.write(line+'\n')

file1.close()
'''      
      
         
