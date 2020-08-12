/**
 * Utility class with helpful functions for the Amaranth Chrome extension.
 * All methods are static.
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
}
