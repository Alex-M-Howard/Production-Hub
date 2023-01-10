/**
 *
 * @param {string} property
 * @returns sorted array
 */
function dynamicSort(property) {
  var sortOrder = 1;
  if (property[0] === "-") {
    sortOrder = -1;
    property = property.substr(1);
  }
  return function (a, b) {
    /* next line works with strings and numbers,
     * and you may want to customize it to your needs
     */
    var result =
      a[property] < b[property] ? -1 : a[property] > b[property] ? 1 : 0;
    return result * sortOrder;
  };
}

/**
 *
 * @param {string} property
 * @returns sorted array
 */
function dynamicSortReverse(property) {
  var sortOrder = 1;
  if (property[0] === "-") {
    sortOrder = -1;
    property = property.substr(1);
  }
  return function (a, b) {
    /* next line works with strings and numbers,
     * and you may want to customize it to your needs
     */
    var result =
      a[property] > b[property] ? -1 : a[property] < b[property] ? 1 : 0;
    return result * sortOrder;
  };
}

/**
 *
 * @param {string} property
 * @returns sorted array
 */
function numberSort(property) {
  var sortOrder = 1;
  if (property[0] === "-") {
    sortOrder = -1;
    property = property.substr(1);
  }
  return function (a, b) {
    var result =
      parseInt(a[property]) < parseInt(b[property])
        ? -1
        : parseInt(a[property]) > parseInt(b[property])
        ? 1
        : 0;
    return result * sortOrder;
  };
}

/**
 *
 * @param {string} property
 * @returns sorted array
 */
function numberSortReverse(property) {
  var sortOrder = 1;
  if (property[0] === "-") {
    sortOrder = -1;
    property = property.substr(1);
  }
  return function (a, b) {
    var result =
      parseInt(a[property]) > parseInt(b[property])
        ? -1
        : parseInt(a[property]) < parseInt(b[property])
        ? 1
        : 0;
    return result * sortOrder;
  };
}

/**
 *
 * @param {string} property
 * @returns sorted array
 */
function scrapSort(property) {
  var sortOrder = 1;
  if (property[0] === "-") {
    sortOrder = -1;
    property = property.substr(1);
  }
  return function (a, b) {
    var result =
      parseInt(a[property].split("%")[0]) < parseInt(b[property].split("%")[0])
        ? -1
        : parseInt(a[property].split("%")[0]) >
          parseInt(b[property].split("%")[0])
        ? 1
        : 0;
    return result * sortOrder;
  };
}

/**
 *
 * @param {string} property
 * @returns sorted array
 */
function scrapReverseSort(property) {
  var sortOrder = 1;
  if (property[0] === "-") {
    sortOrder = -1;
    property = property.substr(1);
  }
  return function (a, b) {
    var result =
      parseInt(a[property].split("%")[0]) > parseInt(b[property].split("%")[0])
        ? -1
        : parseInt(a[property].split("%")[0]) <
          parseInt(b[property].split("%")[0])
        ? 1
        : 0;
    return result * sortOrder;
  };
}
