from django.shortcuts import render

def record_list(request):
    return render(request, "records/list.html")
