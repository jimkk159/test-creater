describe('add function', () => {
    const { add } = require('./path_to_your_function_file'); // adjust the path accordingly

    test('add:1. Basic case - positive numbers', () => {
        expect(add(3, 5)).toBe(8);
    });

    test('add:2. Basic case - negative and positive number', () => {
        expect(add(-4, 10)).toBe(6);
    });

    test('add:3. Basic case - negatives', () => {
        expect(add(-3, -7)).toBe(-10);
    });

    test('add:4. Edge case - adding zeros', () => {
        expect(add(0, 5)).toBe(5);
    });

    test('add:5. Edge case - adding zeros', () => {
        expect(add(0, -5)).toBe(-5);
    });

    test('add:6. Edge case - adding two zeros', () => {
        expect(add(0, 0)).toBe(0);
    });

    test('add:7. Edge case - large numbers', () => {
        expect(add(1e+10, 3e+10)).toBe(4e+10);
    });

    test('add:8. Edge case - small numbers', () => {
        expect(add(1e-10, 2e-10)).toBe(3e-10);
    });

    test('add:9. Input type check - string input', () => {
        expect(() => add('3', 5)).toThrow();
    });

    test('add:10. Input type check - boolean input', () => {
        expect(add(true, 5)).toBe(6);
    });

    test('add:11. Input type check - boolean false', () => {
        expect(add(false, 5)).toBe(5);
    });
});

