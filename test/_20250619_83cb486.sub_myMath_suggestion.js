function sub(a, b) {
    if (typeof a !== 'number' || typeof b !== 'number') {
        throw new Error("Invalid input: both parameters must be numbers.");
    }
    return a - b;
}

module.exports = { sub };
