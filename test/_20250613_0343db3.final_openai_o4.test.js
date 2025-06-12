describe('add function', () => {
    const add = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error('Invalid input types');
        }
        return a + b;
    };

    test('add:1. Basic case - positive numbers', () => {
        expect(add(2, 3)).toBe(5);
    });

    test('add:2. Basic case - negative and positive', () => {
        expect(add(-1, 5)).toBe(4);
    });

    test('add:3. Case with zero', () => {
        expect(add(0, 5)).toBe(5);
    });

    test('add:4. Case with large numbers', () => {
        expect(add(1000000, 2000000)).toBe(3000000);
    });

    test('add:5. Invalid input - string', () => {
        expect(() => add('a', 5)).toThrow('Invalid input types');
    });

    test('add:6. Invalid input - null', () => {
        expect(() => add(3, null)).toThrow('Invalid input types');
    });

    test('add:7. Edge case - both parameters as zero', () => {
        expect(add(0, 0)).toBe(0);
    });
});

describe('subtract function', () => {
    const subtract = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error('Invalid input types');
        }
        return a - b;
    };

    test('Basic case - positive numbers', () => {
        expect(subtract(10, 5)).toBe(5);
    });
    
    test('Basic case - negative result', () => {
        expect(subtract(5, 10)).toBe(-5);
    });

    test('Edge case - subtracting zero', () => {
        expect(subtract(10, 0)).toBe(10);
    });

    test('Edge case - zero from positive', () => {
        expect(subtract(10, 10)).toBe(0);
    });

    test('Edge case - zero from negative', () => {
        expect(subtract(0, 5)).toBe(-5);
    });

    test('Corner case - both numbers negative', () => {
        expect(subtract(-5, -10)).toBe(5);
    });

    test('Type case - string input', () => {
        expect(() => subtract('10', 5)).toThrow('Invalid input types');
    });

    test('Type case - null input', () => {
        expect(() => subtract(null, 5)).toThrow('Invalid input types');
    });

    test('Type case - undefined input', () => {
        expect(() => subtract(undefined, 5)).toThrow('Invalid input types');
    });
});

describe('divide function', () => {
    const divide = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error("Invalid input: both parameters must be numbers");
        }
        if (b === 0) {
            throw new Error("Cannot divide by zero");
        }
        return a / b;
    };

    test('Basic case - positive numbers', () => {
        expect(divide(10, 2)).toBe(5);
    });

    test('Basic case - negative and positive number', () => {
        expect(divide(-10, 2)).toBe(-5);
    });

    test('Edge case - division by one', () => {
        expect(divide(10, 1)).toBe(10);
    });

    test('Edge case - division by zero', () => {
        expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
    });

    test('Edge case - both numbers negative', () => {
        expect(divide(-10, -2)).toBe(5);
    });

    test('Corner case - zero divided by a number', () => {
        expect(divide(0, 5)).toBe(0);
    });

    test('Type check - string input for param1', () => {
        expect(() => divide('10', 2)).toThrow('Invalid input: both parameters must be numbers');
    });

    test('Type check - string input for param2', () => {
        expect(() => divide(10, '2')).toThrow('Invalid input: both parameters must be numbers');
    });

    test('Type check - undefined input for param1', () => {
        expect(() => divide(undefined, 2)).toThrow('Invalid input: both parameters must be numbers');
    });

    test('Type check - undefined input for param2', () => {
        expect(() => divide(10, undefined)).toThrow('Invalid input: both parameters must be numbers');
    });
});

describe('multiple function', () => {
    const multiple = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error("Invalid number");
        }
        return a * b;
    };

    test('Basic case - positive numbers', () => {
        expect(multiple(5, 4)).toBe(20);
    });

    test('Basic case - negative and positive', () => {
        expect(multiple(-3, 6)).toBe(-18);
    });

    test('Basic case - two negatives', () => {
        expect(multiple(-2, -3)).toBe(6);
    });

    test('Edge case - zero', () => {
        expect(multiple(0, 7)).toBe(0);
    });

    test('Edge case - zero as both parameters', () => {
        expect(multiple(0, 0)).toBe(0);
    });

    test('Edge case - large numbers', () => {
        expect(multiple(100000, 100000)).toBe(10000000000);
    });

    test('Type check - param1 not a number', () => {
        expect(() => multiple('abc', 5)).toThrow('Invalid number');
    });

    test('Type check - param1 as an array', () => {
        expect(() => multiple([1, 2, 3], 5)).toThrow('Invalid number');
    });

    test('Type check - param2 not a number', () => {
        expect(() => multiple('4', 'five')).toThrow('Invalid number');
    });

    test('Type check - both parameters non-numeric', () => {
        expect(() => multiple('hello', 'world')).toThrow('Invalid number');
    });
});

