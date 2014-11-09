'use strict';

describe('myApp.view1 module', function() {

  beforeEach(module('myApp.view1'));

  describe('view1 controller', function(){

    it('should ....', inject(function($controller) {
      //spec body
      var view1Ctrl = $controller('View1Ctrl');
      expect(view1Ctrl).toBeDefined();
    }));

  });

    describe('view1 Service', function(){

        it('should test for View1Srvs being defined ', inject(function(View1Srvs) {
            //spec body
            expect(View1Srvs).toBeDefined();
        }));

        it('should test for View1Srvs functionality  ', inject(function(View1Srvs) {
            expect(View1Srvs.orderByOccurrence).toBeDefined();

        }));

        it('should test for View1Srvs functionality  ', inject(function(View1Srvs) {
            var list = ['five',"five","five", "five", "five",
                "four", "four", "four",
                'three', 'three','three',
                'two','two', 'one',
                "six","six","six","six","six", "six",
                "seven","seven","seven","seven","seven","seven", "seven"];
            expect(View1Srvs.orderByOccurrence(list)).toEqual(['seven', "six", 'five', 'four', 'three', 'two', 'one']);

        }));

    });

});