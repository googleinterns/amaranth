const AmaranthUtil = require('../src/AmaranthUtil');

test('removeSpecialCharacters: removes special characters from "hello$#@there"',
    () => {
      expect(AmaranthUtil.removeSpecialCharacters('hello$#@there'))
          .toBe('hellothere');
    });

test('removeSpecialCharacters: removes special characters from ' +
    '"!@#t$#[(<e#@!*&^()s$#(}]>)*t"',
() => {
  expect(AmaranthUtil.removeSpecialCharacters('!@#t$#[(<e#@!*&^()s$#(}]>)*t'))
      .toBe('test');
});

test('padArray: pads [1,2,3] to [1,2,3,0,0,0,0,0,0,0]', () => {
  expect(AmaranthUtil.padArray([1, 2, 3], 10, 0))
      .toStrictEqual([1, 2, 3, 0, 0, 0, 0, 0, 0, 0]);
});

test('padArray: pads ["1","2","3"] to ["1","2","3","",""]', () => {
  expect(AmaranthUtil.padArray(['1', '2', '3'], 5, ''))
      .toStrictEqual(['1', '2', '3', '', '']);
});

test('padArray: pads [] to [{}, {}, {}]', () => {
  expect(AmaranthUtil.padArray([], 3, {})).toStrictEqual([{}, {}, {}]);
});

test('padArray: does not pad [1,2,3,4,5] which is longer than desired length',
    () => {
      expect(AmaranthUtil.padArray([1, 2, 3, 4, 5], 3, 0))
          .toStrictEqual([1, 2, 3, 4, 5]);
    });
