const AmaranthUtil = require('../src/AmaranthUtil');

// Test AmaranthUtil.removeSpecialCharacters
test('removes space from "hello there!"', () => {
  expect(AmaranthUtil.removeSpecialCharacters('hello there!', ' '))
      .toBe('hellothere!');
});

test('removes spaces from "  hello     there ! "', () => {
  expect(AmaranthUtil.removeSpecialCharacters('  hello     there ! ', ' '))
      .toBe('hellothere!');
});

test('removes special characters from "!@#t$#  e#@!*&^()s$#()*t"', () => {
  expect(AmaranthUtil.removeSpecialCharacters('!@#t$#[(<e#@!*&^()s$#(}]>)*t'))
      .toBe('test');
});

// Test AmaranthUtil.padArray
test('pads [1,2,3] to [1,2,3,0,0,0,0,0,0,0]', () => {
  expect(AmaranthUtil.padArray([1, 2, 3], 10, 0))
      .toStrictEqual([1, 2, 3, 0, 0, 0, 0, 0, 0, 0]);
});

test('pads ["1","2","3"] to ["1","2","3","",""]', () => {
  expect(AmaranthUtil.padArray(['1', '2', '3'], 5, ''))
      .toStrictEqual(['1', '2', '3', '', '']);
});

test('pads [] to [{}, {}, {}]', () => {
  expect(AmaranthUtil.padArray([], 3, {})).toStrictEqual([{}, {}, {}]);
});

test('does not pad [1,2,3,4,5] which is longer than desired length', () => {
  expect(AmaranthUtil.padArray([1, 2, 3, 4, 5], 3, 0))
      .toStrictEqual([1, 2, 3, 4, 5]);
});
