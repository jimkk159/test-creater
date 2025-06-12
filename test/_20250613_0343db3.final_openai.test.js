describe('divide function', () => {
    const divide = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error('Error: Invalid input');
        }
        if (b === 0) {
            throw new Error('Error: Division by zero');
        }
        return a / b;
    };

    test('Basic case - positive numbers', () => {
        expect(divide(10, 2)).toBe(5);
    });

    test('Basic case - negative numbers', () => {
        expect(divide(-10, -2)).toBe(5);
    });

    test('Basic case - positive and negative number', () => {
        expect(divide(10, -2)).toBe(-5);
    });

    test('Edge case - division by zero', () => {
        expect(() => divide(10, 0)).toThrow(Error); // Expecting an error
    });

    test('Edge case - zero dividend', () => {
        expect(divide(0, 5)).toBe(0);
    });

    test('Input type case - non-numeric', () => {
        expect(() => divide('string', 5)).toThrow(Error); // Expecting an error
    });

    test('Input type case - non-numeric divisor', () => {
        expect(() => divide(10, 'string')).toThrow(Error); // Expecting an error
    });

    test('Input type case - both non-numeric', () => {
        expect(() => divide('string', 'string')).toThrow(Error); // Expecting an error
    });
});

describe('multiple function', () => {
    const multiple = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error("Invalid input type");
        }
        return a * b;
    };
    test('Basic case - positive integers', () => {
        expect(multiple(3, 4)).toBe(12);
    });
    test('Basic case - negative and positive integer', () => {
        expect(multiple(-2, 5)).toBe(-10);
    });
    test('Edge case - multiplication by zero', () => {
        expect(multiple(0, 10)).toBe(0);
    });
    test('Edge case - zero multiplied by zero', () => {
        expect(multiple(0, 0)).toBe(0);
    });
    test('Corner case - large numbers', () => {
        expect(multiple(100000, 200000)).toBe(20000000000);
    });
    test('Type check case - string input for first parameter', () => {
        expect(() => multiple('3', 5)).toThrow("Invalid input type");
    });
    test('Type check case - string input for second parameter', () => {
        expect(() => multiple(3, '4')).toThrow("Invalid input type");
    });
    test('Type check case - both parameters as strings', () => {
        expect(() => multiple('3', '4')).toThrow("Invalid input type");
    });
});

describe('add function', () => {
    const add = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error('Invalid input type');
        }
        return a + b;
    };

    test('add:1. Basic case', () => {
        expect(add(5, 3)).toBe(8);
    });

    test('add:2. Basic case - negative number', () => {
        expect(add(-2, 4)).toBe(2);
    });

    test('add:3. Edge case - addition with zero', () => {
        expect(add(0, 7)).toBe(7);
    });

    test('add:4. Edge case - addition with zero', () => {
        expect(add(-5, 0)).toBe(-5);
    });

    test('add:5. Edge case - two negative numbers', () => {
        expect(add(-3, -2)).toBe(-5);
    });

    test('add:6. Corner case - large numbers', () => {
        expect(add(1000000, 5000000)).toBe(6000000);
    });

    test('add:7. Type check - string input', () => {
        expect(() => add('5', 3)).toThrow('Invalid input type');
    });

    test('add:8. Type check - array input', () => {
        expect(() => add([1, 2], 3)).toThrow('Invalid input type');
    });

    test('add:9. Type check - object input', () => {
        expect(() => add({ num: 5 }, 3)).toThrow('Invalid input type');
    });
});

describe('subtract function', () => {
    const subtract = (a, b) => a - b;

    test('subtract: Basic case - positive integers', () => {
        expect(subtract(10, 5)).toBe(5);
    });

    test('subtract: Basic case - negative integer', () => {
        expect(subtract(-5, 10)).toBe(-15);
    });

    test('subtract: Basic case - zero', () => {
        expect(subtract(5, 0)).toBe(5);
    });

    test('subtract: Edge case - maximum integer value', () => {
        expect(subtract(9007199254740991, 1)).toBe(9007199254740990);
    });

    test('subtract: Edge case - minimum integer value', () => {
        expect(subtract(-9007199254740991, -1)).toBe(-9007199254740990);
    });

    test('subtract: Corner case - subtracting the same number', () => {
        expect(subtract(7, 7)).toBe(0);
    });

    test('subtract: Invalid input - string input', () => {
        expect(subtract('string', 5)).toBeNaN();
    });

    test('subtract: Invalid input - non-numeric input', () => {
        expect(subtract(null, 'undefined')).toBeNaN();
    });
});

