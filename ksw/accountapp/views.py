from django.shortcuts import render


def account(request):
    return render(request, "accountapp/account.html")


def post_create(request, pk):
    pass


def post_read(request, pk):
    pass


def post_update(request, pk):
    pass


def post_delete(request, pk):
    pass
