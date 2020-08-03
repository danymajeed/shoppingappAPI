from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.db.models import Q
from .models import Product


def combineOrQuery(mainQuery, orQuery):
    mainQuery = mainQuery & orQuery
    return mainQuery


def makeQuery(t, f, v, mainQuery, operator):
    if (t == 'contains'):
        t = 'icontains'
    elif (t == 'equals'):
        t = 'iexact'
    elif (t == 'beginsWith'):
        t = 'startswith'
    elif (t == 'endsWith'):
        t = 'endswith'
    elif (t == 'greaterThanEqual'):
        t = 'gte'
    elif (t == 'lessThanEqual'):
        t = 'lte'
    elif (t == 'greaterThan'):
        t = 'gt'
    elif (t == 'lessThan'):
        t = 'lt'
    if v != "":
        kwargs = {str('%s__%s' % (f, t)): str('%s' % v)}
        if operator == "and":
            mainQuery = mainQuery & Q(**kwargs)
        elif operator == "or":
            mainQuery = mainQuery | Q(**kwargs)

    return mainQuery


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def search(self, request, *args, **kwargs):
        mainQuery = Q()
        for obj in request.data["data"]:
            for key in obj:
                # or condition check
                if (key == 'or'):
                    orQuery = Q()
                    for newObj in obj[key]:
                        for newKey in newObj:
                            orQuery = makeQuery(
                                newKey, newObj[newKey][0], newObj[newKey][1], orQuery, "or")
                    mainQuery = combineOrQuery(mainQuery, orQuery)
                # or condition check end
                else:
                    mainQuery = makeQuery(
                        key, obj[key][0], obj[key][1], mainQuery, 'and')
        queryset = Product.objects.filter(mainQuery)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
