from networkso import *


net = Network("SiouxFalls_net.tntp", "SiouxFalls_tripsnew.tntp")
#net = Network("braess_net.tntp", "braess_trips.tntp")
#net = Network("ninenode_net.tntp", "ninenode_trips.tntp")
    
net.userEquilibrium("FW", 100000, 1e-6, net.averageExcessCost)
print("Finished solving for Equilibrium!")

sorted_links1=dict() 
for i in net.link:
        sorted_links1[i]=(net.link[i].tail,net.link[i].head)

sorted_links=sorted(sorted_links1, key=sorted_links1.__getitem__)

file2=open("Flowsperi_SF.txt","r+")
file3=open("Costsperi_SF.txt","r+")

#file2=open("FlowsK_ninenode.txt.","r+")
#file3=open("CostsK_ninenode.txt","r+")
for i in sorted_links:
    file2.write(str(net.link[i].flow)+"\n")
    file3.write(str(net.link[i].cost)+"\n")
    
file2.close()
file3.close()

ODpair1=dict()
for i in net.ODpair:
    ODpair1[i]=(net.ODpair[i].origin,net.ODpair[i].destination)

ODp=sorted(ODpair1, key=ODpair1.__getitem__)

file4=open("ODdemandperi_SF.txt","r+")  
#file4=open("ODdemandK_ninenode.txt","r+")
for j in ODp:
   file4.write(str(net.ODpair[j].demand)+"\n")
file4.close()


linkcost=dict()
for i in sorted_links:
    linkcost[i]=net.link[i].cost


    
MasterZ=[]
numpaths=dict()
numpaths[0]=0
ODcount=1
K=100
for OD in ODp:
#############################################################################

    all_Paths=[]
    

    #print(i)
    O=net.ODpair[OD].origin
    D=net.ODpair[OD].destination
    net.printAllPaths(O,D)
    all_Paths=net.MASTER

    #print("done finding paths! Cheer Up")
    
#############################################################################

    Path_links=[]
    for path in all_Paths:
        currentpath=[]
        for node in range(0,len(path)-1):
            currentpath.append('('+str(path[node])+','+str(path[node+1])+')')
        Path_links.append(currentpath)

    #print("Converted Paths from nodes to links! Just hold on for just a little bit more")
#############################################################################

    

#############################################################################

    Z=dict()

    c=1
    for path in Path_links:
        currentz=[]
        
        for link in sorted_links:
                if link in path:
                        currentz.append(1)
                else:
                        currentz.append(0)
        '''
            flag=0
            for link1 in path:
                
                if link==link1:
                    currentz.append(1)
                    flag=1
                    break
            if(flag==0):    
                currentz.append(0)
        '''
        
        Z[c]=currentz
        c+=1


    #print("done with z dict! Almost There")
#############################################################################

    PathCosts=dict()
    for path in Z:
        cost=0
        c=0
        for link in Z[path]:
            cost+=linkcost[sorted_links[c]]*link
            c+=1
        PathCosts[path]=cost
    #print("PathCosts calculated")
#############################################################################
    SortedIndex=sorted(PathCosts, key=PathCosts.__getitem__)

    temp=[]
    for i in range(0,min(K,len(SortedIndex))):
        temp.append(Z[SortedIndex[i]])
    #print("stored K paths in temp")
    MasterZ.append(temp)
    numpaths[ODcount]=numpaths[ODcount-1]+min(K,len(SortedIndex))
    ODcount+=1
    
    print(OD)

MasterZ1=[]
for temp1 in MasterZ:
    for paths in temp1:
        MasterZ1.append(paths)
        

file1 = open("Zperi_SF.txt","r+")
for num in range(0,(len(sorted_links))):
    line=''
    flag=1
    for z in MasterZ1:
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
          line='-1'
          flag=0
       else:
          line=line+',-1'
    for j in range(numpaths[i],len(MasterZ1)):
       line=line+',0'
    file1.write(line+'\n')
file1.close()


         
