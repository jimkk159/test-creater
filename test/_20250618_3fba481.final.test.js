const { add } = require('/Users/jimchung/Desktop/Code/python/test-creater/myMath.js');  # Ensure the path is correct

describe('add function', () => {
    test('Basic case - positive integers', () => {
        expect(add(5, 10)).toBe(15);
    });

    test('Basic case - negative integers', () => {
        expect(add(-3, -7)).toBe(-10);
    });

    test('Basic case - mix of positive and negative integers', () => {
        expect(add(4, -2)).toBe(2);
    });

    test('Basic case - floating point numbers', () => {
        expect(add(2.5, 3.75)).toBe(6.25);
    });

    test('Edge case - zero', () => {
        expect(add(0, 10)).toBe(10);
    });

    test('Edge case - large numbers', () => {
        expect(add(9999999999, 8888888888)).toBe(18888888887);
    });

    test('Edge case - small numbers', () => {
        expect(add(1e-07, 2e-07)).toBe(3e-07);
    });

    test('Input type check - string', () => {
        expect(add('string', 5)).toBeNaN();
    });

    test('Input type check - array', () => {
        expect(add([1, 2, 3], 2)).toBeNaN();
    });
});

