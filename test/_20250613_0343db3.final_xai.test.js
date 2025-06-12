describe('Arithmetic Operations', () => {
    const add = (a, b) => a + b;
    const multiply = (a, b) => a * b;
    const subtract = (a, b) => a - b;
    const divide = (a, b) => a / b;

    // Multiplication Tests
    test('Basic case - positive numbers (multiply)', () => {
        expect(multiply(3, 4)).toBe(12);
    });
    test('Edge case - zero multiplication', () => {
        expect(multiply(5, 0)).toBe(0);
    });
    test('Edge case - negative numbers (multiply)', () => {
        expect(multiply(-2, 3)).toBe(-6);
    });
    test('Edge case - large numbers (multiply)', () => {
        expect(multiply(999999, 999999)).toBe(999998000001);
    });
    test('Invalid input - string input (multiply)', () => {
        expect(multiply('2', 3)).toBe(6);
    });
    test('Invalid input - undefined input (multiply)', () => {
        expect(multiply(undefined, 5)).toBeNaN();
    });

    // Addition Tests
    test('Basic case - positive numbers (add)', () => {
        expect(add(3, 5)).toBe(8);
    });
    test('Basic case - negative numbers (add)', () => {
        expect(add(-2, -3)).toBe(-5);
    });
    test('Basic case - zero (add)', () => {
        expect(add(0, 10)).toBe(10);
    });
    test('Edge case - large numbers (add)', () => {
        expect(add(9000000000000000, 9000000000000000)).toBe(18000000000000000);
    });
    test('Edge case - decimal numbers (add)', () => {
        expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });
    test('Input type check - string and number (add)', () => {
        expect(add('2', 3)).toBe('23');
    });
    test('Input type check - null value (add)', () => {
        expect(add(null, 5)).toBe(5);
    });
    test('Input type check - undefined value (add)', () => {
        expect(add(undefined, 5)).toBeNaN();
    });

    // Subtraction Tests
    test('Basic case - positive numbers (subtract)', () => {
        expect(subtract(10, 5)).toBe(5);
    });
    test('Basic case - negative result (subtract)', () => {
        expect(subtract(3, 7)).toBe(-4);
    });
    test('Edge case - subtraction with zero', () => {
        expect(subtract(5, 0)).toBe(5);
    });
    test('Edge case - large numbers (subtract)', () => {
        expect(subtract(999999999999, 1)).toBe(999999999998);
    });
    test('Edge case - negative numbers (subtract)', () => {
        expect(subtract(-10, -5)).toBe(-5);
    });
    test('Invalid input - string input (subtract)', () => {
        expect(subtract('10', 5)).toBe(5);
    });
    test('Invalid input - null input (subtract)', () => {
        expect(subtract(null, 5)).toBe(-5);
    });
    test('Invalid input - undefined input (subtract)', () => {
        expect(subtract(undefined, 5)).toBeNaN();
    });

    // Division Tests
    test('Basic case - positive numbers (divide)', () => {
        expect(divide(10, 2)).toBe(5);
    });
    test('Basic case - negative numbers (divide)', () => {
        expect(divide(-10, 2)).toBe(-5);
    });
    test('Basic case - decimal numbers (divide)', () => {
        expect(divide(1.5, 0.5)).toBe(3);
    });
    test('Edge case - division by zero', () => {
        expect(divide(10, 0)).toBe(Infinity);
    });
    test('Input type check - string input (divide)', () => {
        expect(divide('10', 2)).toBe(5);
    });
    test('Input type check - null input (divide)', () => {
        expect(divide(10, null)).toBe(Infinity);
    });
    test('Input type check - undefined input (divide)', () => {
        expect(divide(undefined, 2)).toBeNaN();
    });
});

describe('subtract', () => {
    // Define the subtraction function with input validation
    const subtract = (a, b) => {
        if (typeof a !== 'number' || typeof b !== 'number' || isNaN(a) || isNaN(b)) {
            throw new Error('Invalid input type');
        }
        return a - b;
    };

    test('Basic case - positive numbers', () => {
        expect(subtract(10, 5)).toBe(5);
    });

    test('Basic case - negative result', () => {
        expect(subtract(3, 7)).toBe(-4);
    });

    test('Edge case - subtraction with zero', () => {
        expect(subtract(5, 0)).toBe(5);
    });

    test('Edge case - large numbers', () => {
        expect(subtract(999999999999, 1)).toBe(999999999998);
    });

    test('Edge case - negative numbers', () => {
        expect(subtract(-10, -5)).toBe(-5);
    });

    test('Invalid input - string input', () => {
        expect(() => subtract('10', 5)).toThrow('Invalid input type');
    });

    test('Invalid input - null input', () => {
        expect(() => subtract(null, 5)).toThrow('Invalid input type');
    });

    test('Invalid input - undefined input', () => {
        expect(() => subtract(undefined, 5)).toThrow('Invalid input type');
    });
});

describe('Addition Function', () => {
    const add = (a, b) => a + b;

    test('Basic case - positive numbers', () => {
        expect(add(3, 5)).toBe(8);
    });

    test('Basic case - negative numbers', () => {
        expect(add(-2, -3)).toBe(-5);
    });

    test('Basic case - zero', () => {
        expect(add(0, 10)).toBe(10);
    });

    test('Edge case - large numbers', () => {
        expect(add(9000000000000000, 9000000000000000)).toBe(18000000000000000);
    });

    test('Edge case - decimal numbers', () => {
        expect(add(0.1, 0.2)).toBeCloseTo(0.3, 5); // Using toBeCloseTo for floating-point precision issues
    });

    test('Input type check - string and number', () => {
        expect(add('2', 3)).toBe('23'); // JavaScript concatenates string with number
    });

    test('Input type check - null value', () => {
        expect(add(null, 5)).toBe(5); // null is treated as 0 in addition
    });

    test('Input type check - undefined value', () => {
        expect(add(undefined, 5)).toBeNaN(); // undefined in addition results in NaN
    });
});

describe('add function', () => {
    const add = (a, b) => a + b;
    test('Basic case - positive numbers', () => {
        expect(add(3, 5)).toBe(8);
    });
    test('Basic case - negative numbers', () => {
        expect(add(-2, -3)).toBe(-5);
    });
    test('Basic case - zero', () => {
        expect(add(0, 10)).toBe(10);
    });
    test('Edge case - large numbers', () => {
        expect(add(9000000000000000, 9000000000000000)).toBe(18000000000000000);
    });
    test('Edge case - decimal numbers', () => {
        expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });
    test('Input type check - string and number', () => {
        expect(add('2', 3)).toBe('23');
    });
    test('Input type check - null value', () => {
        expect(add(null, 5)).toBe(5);
    });
    test('Input type check - undefined value', () => {
        expect(add(undefined, 5)).toBe(NaN);
    });
});

describe('multiple function', () => {
    const multiple = (a, b) => a * b;
    test('Basic case - positive numbers', () => {
        expect(multiple(3, 4)).toBe(12);
    });
    test('Edge case - zero multiplication', () => {
        expect(multiple(5, 0)).toBe(0);
    });
    test('Edge case - negative numbers', () => {
        expect(multiple(-2, 3)).toBe(-6);
    });
    test('Edge case - large numbers', () => {
        expect(multiple(999999, 999999)).toBe(999998000001);
    });
    test('Invalid input - string input', () => {
        expect(multiple('2', 3)).toBe(6);
    });
    test('Invalid input - undefined input', () => {
        expect(multiple(undefined, 5)).toBe(NaN);
    });
});

describe('subtract function', () => {
    const subtract = (a, b) => a - b;
    test('Basic case - positive numbers', () => {
        expect(subtract(10, 5)).toBe(5);
    });
    test('Basic case - negative result', () => {
        expect(subtract(3, 7)).toBe(-4);
    });
    test('Edge case - subtraction with zero', () => {
        expect(subtract(5, 0)).toBe(5);
    });
    test('Edge case - large numbers', () => {
        expect(subtract(999999999999, 1)).toBe(999999999998);
    });
    test('Edge case - negative numbers', () => {
        expect(subtract(-10, -5)).toBe(-5);
    });
    test('Invalid input - string input', () => {
        expect(subtract('10', 5)).toBe(5);
    });
    test('Invalid input - null input', () => {
        expect(subtract(null, 5)).toBe(-5);
    });
    test('Invalid input - undefined input', () => {
        expect(subtract(undefined, 5)).toBe(NaN);
    });
});

describe('divide function', () => {
    const divide = (a, b) => a / b;
    test('Basic case - positive numbers', () => {
        expect(divide(10, 2)).toBe(5);
    });
    test('Basic case - negative numbers', () => {
        expect(divide(-10, 2)).toBe(-5);
    });
    test('Basic case - decimal numbers', () => {
        expect(divide(1.5, 0.5)).toBe(3);
    });
    test('Edge case - division by zero', () => {
        expect(divide(10, 0)).toBe(Infinity);
    });
    test('Edge case - very large numbers', () => {
        expect(divide(1e308, 2)).toBe(5e307);
    });
    test('Edge case - very small numbers', () => {
        expect(divide(1e-308, 2)).toBe(5e-309);
    });
    test('Input type check - string input', () => {
        expect(divide('10', 2)).toBe(5);
    });
    test('Input type check - null input', () => {
        expect(divide(10, null)).toBe(Infinity);
    });
    test('Input type check - undefined input', () => {
        expect(divide(undefined, 2)).toBe(NaN);
    });
});

