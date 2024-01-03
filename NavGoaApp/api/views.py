from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import status
from django.http import JsonResponse
from .serializers import pathSerializer
import json
from backend.models import Paths
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import random
def algorithm(finalPath,currentPath,finalHeuristicCost,finalTimeTaken,adjLst,timeTaken,currentCost,visited,node,source,destination):
    print(node)
    if timeTaken > finalTimeTaken[-1]:
        return
    if sum(visited) == len(visited)-1:
        return
    if node == destination:
        # currentPath.append(node)
        if timeTaken < finalTimeTaken[-1]:
           
            # finalHeuristicCost.pop()
            finalHeuristicCost.append(currentCost)
            # finalTimeTaken.pop()
            finalTimeTaken.append(timeTaken)
            currentPath.append(destination)
            # finalPath.pop()
            finalPath.append(currentPath)
            return
        elif currentCost <= finalHeuristicCost[-1]:
       
            # finalHeuristicCost.pop()
            finalHeuristicCost.append(currentCost)
            # finalTimeTaken.pop()
            finalTimeTaken.append(timeTaken)
            currentPath.append(destination)
            # finalPath.pop()
            finalPath.append(currentPath)
            return
        
    
    if not visited[node]:
        newVisitedArray = visited 
        newCurrentPath = [ x for x in currentPath]
        newVisitedArray[node] = 1
        newCurrentPath.append(node)
        for adjVertex in adjLst[node]:
            if not visited[adjVertex[0]]:
                if adjVertex[2]:
                    #there is an accident
                    algorithm(finalPath,newCurrentPath,finalHeuristicCost,finalTimeTaken,adjLst,timeTaken+adjVertex[3]+15,currentCost+adjVertex[1],newVisitedArray,adjVertex[0],source,destination)
                else:
                    #there is no accident
                    algorithm(finalPath,newCurrentPath,finalHeuristicCost,finalTimeTaken,adjLst,timeTaken+adjVertex[3],currentCost+adjVertex[1],newVisitedArray,adjVertex[0],source,destination)
                    
    return          
def addConstraints(adjLst,minutes,incidents):
    results = dict()
    for i in range(1,len(adjLst)):
        for j in range(len(adjLst[i])):
            cost = random.randint(1,12)
            incidents = random.choice([True,False])
            minutes = random.choice([10,15,20])
            if len(adjLst[i][j]) == 1:
                vertex =i
                adjLst[i][j].append(cost)
                adjLst[i][j].append(incidents)
                adjLst[i][j].append(minutes)
                for v in range(len(adjLst[adjLst[i][j][0]])):
                    if adjLst[adjLst[i][j][0]][v][0] == vertex:
                        adjLst[adjLst[i][j][0]][v].append(cost)
                        adjLst[adjLst[i][j][0]][v].append(incidents)
                        adjLst[adjLst[i][j][0]][v].append(minutes)
            
            
            
        
    
def starter(source,destination):
    cities = ['PERNEM',
        'BARDEZ',
        'BICHOLIM',
        'SATTARI',
        'TISWADI',
        'PONDA',
        'DHARBANDORA',
        'MORMUGAO',
        'SAICETTE',
        'SANGUEM',
        'QUEPEM',
        'CANACONA'
    ]
    
    
    mins = [10,15,20]
    isIncident=[True,False]
    adjLst = [
        [],
        [[2],[3]],
        [[1],[3],[5]],
        [[1],[2],[5],[6],[7],[4]],
        [[3],[7]],
        [[2],[3],[6],[8]],
        [[5],[3],[7],[10],[11],[9]],
        [[6],[3],[4],[10]],
        [[9],[5]],
        [[8],[6],[11]],
        [[7],[6],[11],[12]],
        [[9],[6],[10],[12]],
        [[11],[10]]
    ]
    # heuristic costs for n nodes....
    heuristicCosts = [0,12,34,16,28,14,32,30,10,5,11,13]

    addConstraints(adjLst,mins,isIncident)
    # for i in range(1,len(adjLst)):
    #     for j in range(len(adjLst[i])):
    #         print(adjLst[i][j],end=" ")
    #     print()
    
    # print("HEURISTIC COSTS>>>")
    # for i in range(len(heuristicCosts)):
    #     print(i,":",heuristicCosts[i])

    if source.upper().strip() in cities and destination.upper().strip() in cities:
        p = { cities[i]:i+1 for i in range(len(cities))}
        for i in range(len(cities)):
            p[i+1] = cities[i]

        # print(p)

        maximum = (10**9)+7
        finalHeuristicCost = [maximum]
        finalPath = [[]]
        finalTimeTaken = [maximum]
        currentPath = []
        visited = [0 for _ in range(13)]
        algorithm(finalPath,currentPath,finalHeuristicCost,finalTimeTaken,adjLst,0,0,visited,p[source.upper()],p[source.upper()],p[destination.upper()])
        print("HeuristicCost",finalHeuristicCost)
        print("TimeTaken",finalTimeTaken)
        
        finalHeuristicCost,finalTimeTaken = finalHeuristicCost[1:],finalTimeTaken[1:]
        finalPath = finalPath[1:]
        final = finalPath[-1]
       
        states = [p[final[ind]] for ind in range(len(final))]
        print(states)
        API_shortestPath = "->".join(states)
        if len(heuristicCosts) < p[destination.upper()]: 
            print("oshs shitttttttt")
        
        API_heuristicCost = finalHeuristicCost[-1]+heuristicCosts[p[destination.upper()]-1]
        API_travelTime = finalTimeTaken[-1]
        print(API_shortestPath)
        return [API_shortestPath,API_heuristicCost,API_travelTime]
    else:
        print("Some type of error")
        return "ERROR"

        
        

@api_view(['GET'])
def getData(request):
    # GET data
    # Just return all the data from the model
    allPaths = Paths.objects.all()
    serializer = pathSerializer(allPaths,many=True)
    return JsonResponse(serializer.data,safe=False)
@csrf_exempt
@api_view(['POST'])
def postData(request):
    # POST data
    # Just add it to the model and return the shortest path as the response     
    if request.method == 'POST':
        source = request.data['source']
        destination = request.data['destination']
        print(request.data)
        print("="*60)
        print(source,destination)
        chuckData = starter(source,destination)
        if(chuckData == "ERROR"):
            return Response({"status":"Invalid Source or Destination"})
        print("CHUCKDATA:",chuckData)
        myData = {
            "source":source,
            "destination":destination,
            "path":{
                "shortestPath":chuckData[0]
            },
            "heuristicCost":chuckData[1],
            "travelTime":chuckData[2]
        }
        jsonMyData = json.dumps(myData)
        print("JSON DATA:",jsonMyData)
        pathObject = Paths.objects.create(source=myData["source"],destination=myData["destination"],heuristicCost=myData["heuristicCost"],travelTime=myData["travelTime"],path={"shortestPath":myData["path"]["shortestPath"]})
        serializer = pathSerializer(pathObject)
        pathObject.save()
        print("serializer data:",serializer.data)
        return Response(serializer.data)
    return Response({"status":"failure"})
