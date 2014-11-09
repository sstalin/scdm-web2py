'use strict';

angular.module('myApp.view1', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', [function () {

    }])

    .service('View1Srvs', [function () {
        this.orderByOccurrence = function orderByOccurrence(list) {
            var lString,
                map = {},
                processed = [],
                indexes = [],
                result = [];

            lString = list.join();
            if (!Array.isArray(list))
                return;
            if (list.length === 0)
                return list;

            // create map where key = occurrence and value = list of words

            list.forEach(function (next) {
                var key, r, count = 0;
                if (processed.indexOf(next) < 0) {
                    r = new RegExp(next, 'ig');
                    while(r.exec(lString)) count ++;
                    key = count;
                    if (map.hasOwnProperty(key)) {
                        map[key].push(next);
                    } else {
                        Object.defineProperty(map, key, {
                            value: [next],
                            writable: true,
                            enumerable: true,
                            configurable: true
                        });
                    }

                    processed.push(next);
                }
            });
            /// at this point map is ready
            indexes = Object.keys(map).sort().reverse(); // sort in reverse order
            indexes.forEach(function (key) {
                var next = map[key];
                result = result.concat(next);

            });
            console.log(result.slice(0,5));
            return result;
        };
    }]);