import itertools
import json
import uuid


class Base:
    gen_id = itertools.count().next

    def __init__(self, **kwargs):
        for field in self.__slots__:
            setattr(self, field, kwargs.get(field, None))
        self.id = self.gen_id()

class Tracker:
    def __init__(self):
        self.id = str(uuid.uuid1())
        self.history = []

    def update_history(self, question_set_dict):
        self.history.append({
            "question": Question(**question_set_dict['question']),
            "choice": Answer(**question_set_dict['choice']),
        })


class Question(Base):
    __slots__ = ['id', 'text', 'answers', 'entry']


class Answer(Base):
    __slots__ = ['id', 'text', 'next_question', 'end_message']


class QuestionListBuilder:
    questions = {}
    answers = {}

    def parse_answer(self, text, adict):
        nq_dict = adict.get('next_question')
        answer = Answer(
            text=text, end_message=adict.get('end_message', ''),
            next_question=self.parse_question(nq_dict) if nq_dict else None
        )
        self.answers[answer.id] = answer
        return answer

    def parse_question(self, qdict, entry=False):
        question = Question(
            text=qdict.get("text"), entry=entry,
            answers=[self.parse_answer(key, answer) for key, answer in qdict.get('possible_answers', {}).iteritems()]
        )
        self.questions[question.id] = question
        return question

    def setup(self):
        qlist = json.load(open('questions.json'))
        [self.parse_question(question, entry=True) for question in qlist]


qset = QuestionListBuilder()
qset.setup()

trackers = {}