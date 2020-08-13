/**
 * Utilities for the Amaranth Chrome extension.
 * This class is a wrapper for pure helper functions, therefore all
 * functions should be static and should contain no internal state.
 */
class AmaranthUtil {
  /**
   * Removes special characters from a string.
   * @param {string} str String to remove special characters from
   * @param {string} filters Characters to remove from str
   * @return {string} `str` with all characters in `filters` removed
   */
  static removeSpecialCharacters(
      str, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n') {
    let newStr = '';
    for (const char of str) {
      if (!filters.includes(char)) {
        newStr += char;
      }
    }

    return newStr;
  }

  /**
   * Pads some array `arr` with `padValue` until it's length is equal to
   * `desiredLength`. This function will modify the original array `arr` and
   * return it. If the length of `arr` is already greater than `desiredLength`,
   * the original `arr` is returned unchanged.
   * @template T
   * @param {T[]} arr The array to pad
   * @param {number} desiredLength The length that `arr` should be after padding
   * @param {T} padValue The value to add to `arr` to reach length
   * `desiredLength`
   * @return {T[]} The same array `arr` with as many `padValue`s added as
   * necessary.
   */
  static padArray(arr, desiredLength, padValue) {
    while (arr.length < desiredLength) {
      arr.push(padValue);
    }

    return arr;
  }
}

module.exports = AmaranthUtil;
