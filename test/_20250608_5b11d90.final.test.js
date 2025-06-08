describe('add function', () => {
    const add = async (a, b) => { if (typeof a !== 'number') { throw new Error('invalid input type'); } if (typeof b !== 'number') { throw new Error('invalid input type'); } return a + b; };

    // Basic test cases
    test('Basic case - positive numbers', async () => {
        expect(await add(5, 3)).toBe(8);
    });

    test('Basic case - mix of positive and negative', async () => {
        expect(await add(5, -2)).toBe(3);
    });

    test('Edge case - adding zero', async () => {
        expect(await add(7, 0)).toBe(7);
    });

    test('Edge case - adding two zeros', async () => {
        expect(await add(0, 0)).toBe(0);
    });

    test('Edge case - adding negative numbers', async () => {
        expect(await add(-4, -6)).toBe(-10);
    });

    // Edge case with large numbers
    test('Edge case - adding a large number', async () => {
        expect(await add(1e10, 1e10)).toBe(2e10);
    });

    // Input type check tests
    test('Input type check - string input', async () => {
        await expect(add('5', 3)).rejects.toThrow('invalid input type');
    });

    test('Input type check - non-numeric input', async () => {
        await expect(add('hello', {})).rejects.toThrow('invalid input type');
    });
});