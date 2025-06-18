module.exports = {
    add: function(a, b) {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error('Invalid input: inputs must be numbers');
        }
        return a + b;
    }
};
