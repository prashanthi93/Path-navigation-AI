from django.shortcuts import render,redirect,reverse

# Create your views here.
def homePage(request):
    print(request.method)
    if request.method == 'POST':
        source = request.POST["source"]
        destination = request.POST["destination"]
        # return render(request,'backend/map.html',{"source":source,"destination":destination})
        return redirect('mappage',source,destination)
    return render(request,'backend/index.html',{"text":"hello buddy!"})

def mapPage(request,source,destination):
    print("The give source:",source,"destination:",destination)
    return render(request,'backend/index1.html',{"source":source,"destination":destination})
    # return render(request,'backend/map.html',{"source":source,"destination":destination})

def historyPage(request):
    return render(request,'backend/history.html')