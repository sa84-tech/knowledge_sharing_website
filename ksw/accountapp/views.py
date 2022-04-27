from django.shortcuts import render


def account(request):
    return render(request, "accountapp/account.html")


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
