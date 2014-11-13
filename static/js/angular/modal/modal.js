'use strict';

angular.module('myApp.modal', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
//        $routeProvider.when('/view1', {
//            templateUrl: 'view1/view1.html',
//            controller: 'View1Ctrl'
//        });
    }])

    .controller('ModalCtrl',
    ['$rootScope', '$scope',
        function ($rootScope, $scope) {
            var overlay = angular.element(".modal-overlay"),
                modal = angular.element('.modal-container');

            $rootScope.isModalOn = false;


            $rootScope.popModal = function (event) {
                $rootScope.toggleModal();

                if ($scope.$$phase) {
                    $scope.$eval(function () {
                        $scope.geometry = event.feature.getGeometry().getType();
                        $scope.keys = Object.keys(event.feature.k);
                        $scope.properties = event.feature.k;
                    });
                } else {
                    $scope.$apply(function () {
                        $scope.geometry = event.feature.getGeometry().getType();
                        $scope.keys = Object.keys(event.feature.k);
                        $scope.properties = event.feature.k;
                    });
                }
            };


            $rootScope.toggleModal = function () {
                $rootScope.isModalOn = !$rootScope.isModalOn;
                if ($rootScope.isModalOn) {
                    modal.addClass('on');
                    overlay.addClass('on');
                } else {
                    modal.removeClass('on');
                    overlay.removeClass('on');
                }

            };

            overlay.click(function () {
                $rootScope.toggleModal();
            });

        }])

    .service('ModalSrvs', [function () {

    }]);
