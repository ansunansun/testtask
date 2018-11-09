import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from askbot.api import serializers
from askbot.datas import qset, trackers, Tracker


class NoModelROViewSet(ReadOnlyModelViewSet):
    instances = []

    def retrieve(self, request, pk):
        instance = self.instances.get(pk)
        instance = instance if instance else self.instances.get(int(pk))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, instances={}):
        instances = instances if instances else self.instances
        serializer = self.serializer_class(
            instance=instances.values() if instances else [], many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return []


class NoModelRWViewSet(NoModelROViewSet, ModelViewSet):
    def get_queryset(self):
        return []


class QuestionViewSet(NoModelROViewSet):
    serializer_class = serializers.QuestionSerializer
    instances = qset.questions

    def list(self, request):
        entry_only = json.loads(request.GET.get('entry', '{}'))
        instances = {}
        if entry_only:
            instances = {k:v for k, v in self.instances.iteritems() if v.entry}
        return super(QuestionViewSet, self).list(request, instances)



class AnswerViewSet(NoModelROViewSet):
    serializer_class = serializers.AnswerSerializer
    instances = qset.answers


class TrackerViewSet(NoModelRWViewSet):
    serializer_class = serializers.TrackerSerializer
    instances = trackers

    def create(self, request, *args, **kwargs):
        tracker = Tracker()
        latest_question_set = request.data.pop('question_sets')[-1]
        tracker.update_history(latest_question_set)
        trackers[tracker.id] = tracker
        serializer = self.get_serializer(tracker)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk):
        tracker = trackers.get(pk)
        latest_question_set = request.data.get('question_sets', [])[-1]
        tracker.update_history(latest_question_set)
        serializer = self.get_serializer(tracker)
        return Response(serializer.data)

    def destroy(self, request, pk):
        if pk in trackers:
            tracker = trackers.get(pk)
            for question_set in tracker.history:
                print "{}: {}".format(question_set['question'].text, question_set['choice'].text)
            del trackers[pk]
        return Response(status=status.HTTP_204_NO_CONTENT)


