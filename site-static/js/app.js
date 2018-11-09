function S4() {
    return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
}
var app = angular.module('myApp', ['restangular']);
app.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('/api');
});
app.controller('MainCtrl', function($scope, Restangular) {
    $scope.tracker = {
        question_sets : [],
        done: false,
    };
    $scope.all_questions = [];
    $scope.curret_question_idx = 0;
    $scope.show_next_questionset = function() {
        var question = $scope.all_questions[$scope.curret_question_idx++];
        while(question && question.selected)
            question = $scope.all_questions[$scope.curret_question_idx++];
        if(question){
            $scope.tracker.question_sets.push({question: question, choice: null});
        } else {
            if ($scope.tracker.id)
                Restangular.one('trackers', $scope.tracker.id).remove();
            $scope.tracker.done = true;
        }
    };

    $scope.select_answer = function(question_idx, choice){
        $scope.tracker.question_sets[question_idx].choice = choice;
        if($scope.tracker.id){
            tracker = Restangular.one('trackers', $scope.tracker.id);
            tracker.question_sets = $scope.tracker.question_sets;
            tracker = tracker.put();
        } else {
            tracker = Restangular.all('trackers').post($scope.tracker);
        }

        tracker.then(function(data){
            $scope.tracker.id = data.id;
            if(choice.next_question_id){
                Restangular.all('questions').get(choice.next_question_id).then(function(next_question){
                    $scope.tracker.question_sets.push({question:next_question, choice:null});
                }, function (err) {});
            } else {
                $scope.show_next_questionset();
            }
        }, function (err) {});
    };
    Restangular.all('questions').getList({entry:true}).then(function (questions) {
        $scope.all_questions = questions;
    }, function (err) {});
});