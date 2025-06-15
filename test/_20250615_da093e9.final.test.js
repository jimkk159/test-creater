describe('add function', () => {
    const { add } = require('./path-to-your-file'); // Adjust the path as needed

    test('Basic case - positive integers', () => {
        expect(add(5, 3)).toBe(8);
    });

    test('Basic case - negative integers', () => {
        expect(add(-3, -2)).toBe(-5);
    });

    test('Basic case - negative and positive integer', () => {
        expect(add(-4, 10)).toBe(6);
    });

    test('Edge case - adding zero', () => {
        expect(add(0, 5)).toBe(5);
    });

    test('Edge case - adding zero with a negative integer', () => {
        expect(add(0, -5)).toBe(-5);
    });

    test('Edge case - adding large numbers', () => {
        expect(add(1000000, 5000000)).toBe(6000000);
    });

    test('Corner case - adding maximum safe integer values', () => {
        expect(add(Number.MAX_SAFE_INTEGER, 1)).toBe(9007199254740992);
    });

    test('Type check - string inputs', () => {
        expect(() => add('5', '3')).toThrow('Invalid input type');
    });

    test('Type check - boolean inputs', () => {
        expect(() => add(true, false)).toThrow('Invalid input type');
    });
});

