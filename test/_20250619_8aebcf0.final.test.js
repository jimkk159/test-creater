const { add } = require('/Users/jim/test/test-creater/test/_20250619_8aebcf0.add_myMath_suggestion.js'); // use exports-loader

describe('add function', () => {
    test('Basic case - positive numbers', () => {
        expect(add(5, 10)).toBe(15);
    });

    test('Basic case - negative and positive number', () => {
        expect(add(-5, 10)).toBe(5);
    });

    test('Basic case - two negative numbers', () => {
        expect(add(-5, -10)).toBe(-15);
    });

    test('Basic case - with zero', () => {
        expect(add(0, 10)).toBe(10);
    });

    test('Edge case - both inputs are zero', () => {
        expect(add(0, 0)).toBe(0);
    });

    test('Edge case - adding extreme large numbers', () => {
        expect(add(1e15, 1e15)).toBe(2e15);
    });

    test('Edge case - input type check (string)', () => {
        expect(add("5", "10")).toBeNaN();
    });

    test('Edge case - one input as a string', () => {
        expect(add(5, "10")).toBeNaN();
    });

    test('Corner case - adding small decimals', () => {
        expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });

    test('Corner case - adding large decimals', () => {
        expect(add(1.5e10, 2.5e10)).toBe(4e10);
    });
});

const { sub } = require('/Users/jim/test/test-creater/test/myMath.js');

describe('sub function', () => {
    test('Basic case', () => {
        expect(sub(5, 3)).toBe(2);
    });

    test('Basic case - negative result', () => {
        expect(sub(3, 5)).toBe(-2);
    });

    test('Basic case - zero', () => {
        expect(sub(0, 5)).toBe(-5);
    });

    test('Basic case - both zeros', () => {
        expect(sub(0, 0)).toBe(0);
    });

    test('Edge case - large numbers', () => {
        expect(sub(1000000000, 999999999)).toBe(1);
    });

    test('Edge case - large negative result', () => {
        expect(sub(1, 1000000000)).toBe(-999999999);
    });

    test('Corner case - negative numbers', () => {
        expect(sub(-5, -3)).toBe(-2);
    });

    test('Input type check - non-number (first parameter)', () => {
        expect(sub('five', 3)).toBeNaN();
    });

    test('Input type check - non-number (second parameter)', () => {
        expect(sub(5, 'three')).toBeNaN();
    });

    test('Edge case - fractional numbers', () => {
        expect(sub(5.5, 2.2)).toBeCloseTo(3.3);
    });
});

