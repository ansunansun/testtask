from rest_framework import serializers


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=256)
    next_question_id = serializers.SerializerMethodField()
    end_message = serializers.CharField(max_length=256)

    def get_next_question_id(self, obj):
        return obj.next_question.id if obj.next_question else None


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=256)
    answers = AnswerSerializer(many=True)


class TrackerSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)