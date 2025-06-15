import { add } from '/Users/jim/test/test-creater/test/myMath.js'; 

describe('add function', () => {
    test('1. Basic case - positive integers', () => {
        expect(add(5, 10)).toBe(15);
    });

    test('2. Basic case - negative integers', () => {
        expect(add(-3, -7)).toBe(-10);
    });

    test('3. Basic case - positive and negative integer', () => {
        expect(add(8, -3)).toBe(5);
    });

    test('4. Edge case - adding zero', () => {
        expect(add(0, 10)).toBe(10);
    });

    test('5. Edge case - adding two zeros', () => {
        expect(add(0, 0)).toBe(0);
    });

    test('6. Corner case - large integers', () => {
        expect(add(1000000000, 2000000000)).toBe(3000000000);
    });

    test('7. Corner case - large negative integers', () => {
        expect(add(-1000000000, -2000000000)).toBe(-3000000000);
    });

    test('8. Type check case - string input', () => {
        expect(() => add('5', 10)).toThrow(Error);
    });
});

