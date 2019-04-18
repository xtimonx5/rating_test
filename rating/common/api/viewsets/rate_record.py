from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from common.api.serializers import LeaderBoardSerializer
from common.models import LeaderBoard


class LeaderBoardFilterBackend(rest_framework.DjangoFilterBackend):
    allowed_lookups = [
        'rate_place',
        'rate_place__gt',
        'rate_place__gte',
        'rate_place__lt',
        'rate_place__lte',
        'user_id',
    ]

    def filter_queryset(self, request, queryset, view):
        filter_args = request.query_params
        allowed_filter_args = {allowed_key: filter_args[allowed_key] for allowed_key in self.allowed_lookups if
                               allowed_key in filter_args.keys()}
        return queryset.filter(**allowed_filter_args)


class LeaderBoardViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoard.objects.order_by('-rating', 'datetime')
    filter_backends = (LeaderBoardFilterBackend,)

    @method_decorator(cache_page(60))  # 1 min
    def retrieve(self, request, *args, **kwargs):
        rate_place = kwargs.get('pk')
        if not rate_place:
            raise NotFound
        try:
            rate_place = int(rate_place)
        except:
            raise NotFound
        qs_params = {
            'rate_place__gte': rate_place - 1,
            'rate_place__lte': rate_place + 1
        }
        self.queryset = self.queryset.filter(**qs_params)
        return self.list(request, *args, **kwargs)

    @method_decorator(cache_page(60))  # 1 min
    def list(self, request, *args, **kwargs):
        return super(LeaderBoardViewSet, self).list(request, *args, **kwargs)
