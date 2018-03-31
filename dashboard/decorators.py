from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import KYCdata
from django.shortcuts import render, redirect


def isKYCverified(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.kycdata.is_KYCverified:
            return function(request, *args, **kwargs)
        else:
            return redirect('kyc/uploads/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def isAdminUser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('/login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# use @isKYCverified before function to check