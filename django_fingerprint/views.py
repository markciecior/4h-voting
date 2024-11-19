from django.http import JsonResponse

# from django.shortcuts import render


# Create your views here.
def fp(request):
    fpid = request.GET.get("fpid")
    # print(fpid)
    return JsonResponse({"fpid": fpid})
