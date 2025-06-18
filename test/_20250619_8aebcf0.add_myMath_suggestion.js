function add(a, b) {
    if (typeof a !== 'number' || typeof b !== 'number' || isNaN(a) || isNaN(b)) {
        return NaN;
    }
    return a + b;
}

module.exports = { add };
