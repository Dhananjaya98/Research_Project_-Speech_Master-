var app = angular.module('myApp', ['ngRoute']);

app.controller('MainController', ['$scope', '$rootScope', '$location', '$route', 'MainFactory',
    function ($scope, $rootScope, $location, $route, MainFactory) {

        $scope.test = "Hi!";

        $scope.audioFile = null;

        $scope.webScraping = function () {
            MainFactory.webScrapping()
                .then(function (res) {
                    console.log(res);
                });
        }

        $scope.suggestContent = function () {
            MainFactory.suggestContent()
                .then(function (res) {
                    console.log(res);
                });
        }

        $scope.loading = false;
        $scope.audioText = '';

        $scope.clearnerssWordsResponse = '';
        $scope.clearnerssSentenceResponse = '';
        $scope.quotesSentenceResponse = [];
        $scope.conclusionResponse = '';
        $scope.commentsResponse = '';
        $scope.questionsResponse = '';
        $scope.introductionFuncResponse = '';
        $scope.introductionBestUsesFuncResponse = '';
        $scope.keywordExtractionResponse = '';

        $scope.selectAudioFile = function (e) {
            $scope.loading = true;
            $scope.$apply(function () {
                $scope.audioFile = e.files[0];
                console.log(e.files);
                var fd = new FormData();
                fd.append('file', $scope.audioFile);
                MainFactory.uploadAudio(fd)
                    .then(function (response) {
                        console.log(response);
                        $scope.loading = false;
                        $scope.audioText = response.data;
                    }, function (error) {
                        console.log(error);
                        $scope.loading = false;
                    });
            });
        }

//facial expression diagram
        $scope.selectVideoFile = function (e) {
            $scope.chartLabels = [];
            $scope.chartdata = [];
            $scope.loading = true;
            $scope.$apply(function () {
                $scope.audioFile = e.files[0];
                console.log(e.files);
                var fd = new FormData();
                fd.append('file', $scope.audioFile);
                MainFactory.uploadVideo(fd)
                    .then(function (response) {
                        console.log(response);
                        $scope.loading = false;
                        $scope.emotions = response.data.videoResult.split(' ');
                        $scope.audioText = response.data.audioResult;
                        $scope.emotionScore = 0;
                        for (let i = 0; i < $scope.emotions.length; i++) {
                            $scope.chartLabels.push(i + 1);
                            if ($scope.emotions[i].toLowerCase().includes('angry')) {
                                $scope.chartdata.push(1);
                                $scope.emotionScore += 0.25;
                            } else if ($scope.emotions[i].toLowerCase().includes('sad')) {
                                $scope.chartdata.push(2);
                                $scope.emotionScore += 0.5;
                            } else if ($scope.emotions[i].toLowerCase().includes('neutral')) {
                                $scope.chartdata.push(3);
                                $scope.emotionScore += 0.75;
                            } else if ($scope.emotions[i].toLowerCase().includes('happy')) {
                                $scope.chartdata.push(4);
                                $scope.emotionScore += 1;
                            }
                            let totalScore = $scope.emotionScore;
                            $scope.emotionScore = totalScore / $scope.emotions.length;

                        }

                        console.log($scope.chartdata);
                        var ctx = document.getElementById('myChart').getContext('2d');
                        var myChart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: $scope.chartLabels,
                                datasets: [{
                                    data: $scope.chartdata,
                                    label: "Emotion: 1-Angry, 2-Sad, 3-Neutral, 4-Happy",
                                    borderColor: "#3e95cd",
                                    backgroundColor: "#7bb6dd",
                                    fill: false,
                                }
                                ]
                            },
                        });
                    }, function (error) {
                        console.log(error);
                        $scope.loading = false;
                    });
            });
        }

        $scope.processTheSpeech = function () {
            MainFactory.clearnerssWords({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.clearnerssWordsResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.clearnerssSentence({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.clearnerssSentenceResponse = response.data;
                }, function (error) {
                    console.log(error);
                });

            MainFactory.quotesSentence({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.quotesSentenceResponse = response.data;
                }, function (error) {
                    console.log(error);
                });

//emotion  graph text analyzing
            MainFactory.emotionSentence({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response.data);
                    $scope.emotionSentenceResponse = response.data.message;
                    $scope.emotions = response.data.message;

                    $scope.chartLabelsEmotions = [];
                    $scope.chartDataEmotions = [];
                    for (let i = 0; i < $scope.emotionSentenceResponse.length; i++) {
                        $scope.chartLabelsEmotions.push(i + 1);
                    }


                    $scope.chartdata = [];
                    for (let i = 0; i < $scope.emotions.length; i++) {
                        if ($scope.emotions[i] == 'Angry') {
                            $scope.chartdata.push(1);
                            $scope.emotionScore += 0.25;
                        } else if ($scope.emotions[i] == 'Sad') {
                            $scope.chartdata.push(2);
                            $scope.emotionScore += 0.5;
                        } else if ($scope.emotions[i] == 'Neutral') {
                            $scope.chartdata.push(3);
                            $scope.emotionScore += 0.75;
                        } else if ($scope.emotions[i] == 'Happy') {
                            $scope.chartdata.push(4);
                            $scope.emotionScore += 1;
                        }
                        let totalScore = $scope.emotionScore;
                        $scope.emotionScore = totalScore / $scope.emotions.length;
                        $scope.chartDataEmotions.push($scope.emotionScore);

                    }

                    console.log($scope.chartLabelsEmotions);
                    console.log($scope.chartdata);
                    var ctx = document.getElementById('myChart2').getContext('2d');
                    var myChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: $scope.chartLabelsEmotions,
                            datasets: [{
                                data: $scope.chartdata,
                                label: "Emotion: 1-Angry, 2-Sad, 3-Neutral, 4-Happy",
                                borderColor: "#3e95cd",
                                backgroundColor: "#7bb6dd",
                                fill: false,
                            }
                            ]
                        },
                    });

                }, function (error) {
                    console.log(error);
                });

            //end emotion graph

            MainFactory.conclusion({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.conclusionResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.comments({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.commentsResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.questions({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.questionsResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.introductionFunc({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.introductionFuncResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.introductionBestUsesFunc({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.introductionBestUsesFuncResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.keywordExtraction({ speech: $scope.audioText, topic: $scope.topic })
                .then(function (response) {
                    console.log(response);
                    $scope.keywordExtractionResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.synonymsFunction({ speech: $scope.audioText, topic: $scope.topic })
                .then(function (response) {
                    console.log(response);
                    $scope.synonymsFunctionResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.doubleWordsFunc({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.doubleWordsFuncResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.fillerWordsFunc({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.fillerWordsFuncResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.countPauses()
                .then(function (response) {
                    console.log(response);
                    $scope.countPausesResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.countFillerWords()
                .then(function (response) {
                    console.log(response);
                    $scope.countFillerWordsResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.grammarFunc({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.grammarFuncResponse = response.data;
                }, function (error) {
                    console.log(error);
                });
            MainFactory.gingerItParse({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.gingerItParseResponse = response.data;
                }, function (error) {
                    console.log(error);
                });

//comparison between the expression prediction results and emotional moment results

            MainFactory.textAnalyzeEmotion({ text: $scope.audioText })
                .then(function (response) {
                    console.log(response);
                    $scope.textAnalyzeEmotionResponse = response.data;
                    $scope.emotionScore = 0;
                    for (let i = 0; i < $scope.emotions.length; i++) {
                        if ($scope.emotions[i] == 'Angry') {
                            if ($scope.textAnalyzeEmotionResponse.message[' angry']) {
                                $scope.emotionScore += $scope.textAnalyzeEmotionResponse.message[' angry'];
                            }
                        } else if ($scope.emotions[i] == 'Sad') {
                            if ($scope.textAnalyzeEmotionResponse.message[' sad']) {
                                $scope.emotionScore += $scope.textAnalyzeEmotionResponse.message[' happy'];
                            }
                        } else if ($scope.emotions[i] == 'Happy') {
                            if ($scope.textAnalyzeEmotionResponse.message[' happy']) {
                                $scope.emotionScore += $scope.textAnalyzeEmotionResponse.message[' happy'];
                            }
                        }
                    }
                    let emotionsCount = $scope.emotionScore;
                    $scope.emotionScore = emotionsCount / $scope.emotions.length;
                }, function (error) {
                    console.log(error);
                });

        }

    }]);

app.factory('MainFactory', ['$http', function ($http) {
    var mainFactory = {};
    var restUrl = 'http://127.0.0.1:5000';
    var restUrlFillerWords = 'http://127.0.0.1:5001';

    mainFactory.uploadAudio = function (body) {
        return $http({
            method: 'POST',
            url: restUrl + '/audioUpload',
            headers: {
                'Content-Type': undefined
            },
            data: body,
            params: null
        });
    }

    mainFactory.uploadVideo = function (body) {
        return $http({
            method: 'POST',
            url: restUrl + '/videoUpload',
            headers: {
                'Content-Type': undefined
            },
            data: body,
            params: null
        });
    }

    mainFactory.clearnerssWords = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/clearness/word',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.clearnerssSentence = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/clearness/sentense',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.quotesSentence = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/quotes/sentense',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }


    mainFactory.emotionSentence = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/emotion/sentense',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.conclusion = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/conclusion',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.comments = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/conclusion/comments',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.questions = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/conclusion/questions',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.introductionFunc = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/introduction',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.introductionBestUsesFunc = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/introduction/questions',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.keywordExtraction = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/keywordExtraction',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }


    //double code *******************************************


    mainFactory.keywordExtraction = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/keywordExtraction',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.synonymsFunction = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/synonyms',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.doubleWordsFunc = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/doubleWords',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.fillerWordsFunc = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/fillerWords',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.countPauses = function () {
        return $http({
            method: 'GET',
            url: restUrl + '/countPauses',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: null
        });
    }

    mainFactory.countFillerWords = function () {
        return $http({
            method: 'GET',
            url: restUrlFillerWords + '/countFillerWords',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: null
        });
    }

    mainFactory.grammarFunc = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/grammar',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.gingerItParse = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/gingerItParse',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.textAnalyzeEmotion = function (params) {
        return $http({
            method: 'GET',
            url: restUrl + '/textAnalyzeEmotion',
            headers: {
                'Content-Type': undefined
            },
            data: null,
            params: params
        });
    }

    mainFactory.webScrapping = function () {
        return $http({
            method: 'GET',
            url: restUrl + '/webScrapping',
            headers: {
                'Content-Type': undefined
            },
            data: null
        });
    }

    mainFactory.suggestContent = function () {
        return $http({
            method: 'GET',
            url: restUrl + '/suggestContent',
            headers: {
                'Content-Type': undefined
            },
            data: null
        });
    }

    return mainFactory;
}]);
