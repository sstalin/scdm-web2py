'use strict';

angular.module('myApp.menu', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
//        $routeProvider.when('/view1', {
//            templateUrl: 'view1/view1.html',
//            controller: 'View1Ctrl'
//        });
    }])

    .controller('MenuCtrl',
    [
        '$scope', 'MenuSrvs',
        function ($scope, MenuSrvs) {
            //TODO
            var MAP_SCOPE = angular.element('#map-canvas').scope();

            var overlay = angular.element(".overlay"),
                menuBtn = angular.element("#menu-btn"),
                menuTray = angular.element('.menu-tray'),
                isMenuOn = false;

            function toggleMenu() {
                isMenuOn = !isMenuOn;

                if (isMenuOn) {
                    overlay.addClass('on');
                    menuTray.addClass('on');
                } else {
                    overlay.removeClass('on');
                    menuTray.removeClass('on');
                    loadLayers();// loading geoJson data
                }
            }

            menuBtn.click(toggleMenu);
            overlay.click(toggleMenu);

            function loadLayers() {
                var geoJsonObj;
                map.data.setStyle(
                    {
                        icon: "/scdm/static/images/icon-control-unselected-1-hori.png"
                    });

                geoJsonObj = MenuSrvs.processQueue();
                map.data.forEach(function (next) {
                        map.data.remove(next);
                    }
                );
                map.data.addGeoJson(geoJsonObj);
            }


            $scope.layToggle = function (layer) {
                if (layer.isSelected) {
                    layer.isSelected = false;
                } else {
                    layer.isSelected = true;
                }
            };


        }])

    .service('MenuSrvs',
    ['$http',
        function ($http) {
            var self = this;

            self.queue = [];

            function addGeoJSON(data, status, headers, config) {
                if (status == 200) {
                    self.queue[self.index] = data;
                }
            }

            function removeGeoJSON(index) {
                self.queue[index] = null;
            }

            this.processQueue = function () {
                var geoJsonObj = { "type": "FeatureCollection",
                    "features": []};
                self.queue.forEach(function (next) {
                    if (next) {
                        geoJsonObj.features = geoJsonObj.features.concat(next.features);
                    }
                });
                return geoJsonObj;
            };

            this.loadGeoJSON = function (layer, index) {
                var lay_URL = '/scdm/map/download/' + layer.filename;

                self.index = index;
                // Load a GeoJSON
                $http.get(lay_URL).
                    success(addGeoJSON).
                    error(function (data, status, headers, config) {
                        // called asynchronously if an error occurs
                        // or server returns response with an error status.
                    });
            };

            this.unloadGeoJSON = function (index) {
                removeGeoJSON(index);
            };


        }])

    .directive('layMenuItem', function (MenuSrvs) {

        return function (scope, element, attrs) {
            scope.$watch('layer.isSelected', function (value) {
                if (value == true) {
                    MenuSrvs.loadGeoJSON(scope.layer, scope.$index);
                } else if (value == false) {
                    MenuSrvs.unloadGeoJSON(scope.$index);
                }
            });
        }
    });

