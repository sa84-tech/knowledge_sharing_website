from django.shortcuts import render


def account(request):
    return render(request, "accountapp/account.html")


def article_create(request, pk):
    pass


def article_read(request, pk):
    pass


def article_update(request, pk):
    pass


def article_delete(request, pk):
    pass
