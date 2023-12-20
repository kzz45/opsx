import time
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from dmonitor.models.silence import Silence


class GetSilence(APIView):
    permission_classes = []

    def get(self, request):
        data = []
        Silence.objects.filter(state=1).filter(end__lt=int(time.time())).update(state=0)
        for silence in Silence.objects.filter(state=1).filter(end__gt=int(time.time())).all():
            matchers_tmp = json.loads(silence.match)
            matchers = []
            has_product = False
            for match in matchers_tmp:
                matchers.append({
                    'name': match['name'],
                    'value': str(match['value']),
                    'isRegex': False,
                })
                if match['name'] == '_product_id':
                    has_product = True
            if silence.product.id != -1 and not has_product:
                matchers.append({'isRegex': False, 'name': '_product_id', 'value': str(silence.product.id)})
            silence_dict = {
                'createdBy': str(silence.id),
                # 'createdBy': silence.user.username,
                'startsAt': silence.start,
                'endsAt': silence.end,
                'comment': silence.describe,
                'matchers': matchers
            }
            data.append(silence_dict)
        return Response({'is_change': True, 'data': data})
