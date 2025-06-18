const { add } = require('/Users/jimchung/Desktop/Code/python/test-creater/test/myMath_suggestion.js');

describe('add function', () => {
    test('Basic case - positive numbers', () => {
        expect(add(5, 3)).toBe(8);
    });

    test('Basic case - negative and positive number', () => {
        expect(add(-2, 4)).toBe(2);
    });

    test('Basic case - both negative numbers', () => {
        expect(add(-3, -7)).toBe(-10);
    });

    test('Edge case - adding zero', () => {
        expect(add(0, 5)).toBe(5);
    });

    test('Edge case - adding zero to a negative number', () => {
        expect(add(0, -5)).toBe(-5);
    });

    test('Edge case - both parameters are zero', () => {
        expect(add(0, 0)).toBe(0);
    });

    test('Edge case - large numbers', () => {
        expect(add(1e+18, 1e+18)).toBe(2e+18);
    });

    test('Invalid case - string input', () => {
        expect(() => add("five", "three")).toThrow('Invalid input: inputs must be numbers');
    });

    test('Invalid case - null input', () => {
        expect(() => add(null, null)).toThrow('Invalid input: inputs must be numbers');
    });
});

