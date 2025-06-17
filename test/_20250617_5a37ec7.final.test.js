const { add } = require('/Users/jimchung/Desktop/Code/python/test-creater/test/myMath.js');

describe('add', () => {
    test('Basic case - adding two positive numbers', () => {
        expect(add(5, 7)).toBe(12);
    });

    test('Basic case - adding a positive and a negative number', () => {
        expect(add(10, -3)).toBe(7);
    });

    test('Edge case - adding zero', () => {
        expect(add(15, 0)).toBe(15);
    });

    test('Edge case - adding two zeros', () => {
        expect(add(0, 0)).toBe(0);
    });

    test('Edge case - adding two negative numbers', () => {
        expect(add(-4, -6)).toBe(-10);
    });

    test('Corner case - adding large numbers', () => {
        expect(add(1000000, 2000000)).toBe(3000000);
    });

    test('Input type check - adding a string and a number', () => {
        expect(() => add('5', 3)).toThrow(TypeError);
    });

    test('Input type check - adding a null value', () => {
        expect(() => add(null, 5)).toThrow(TypeError);
    });

    test('Input type check - adding undefined values', () => {
        expect(() => add(undefined, 7)).toThrow(TypeError);
    });
});

