describe('add function', () => {
    const add = async (a, b) => a + b;

    test('Basic case - positive numbers', async () => {
        expect(await add(2, 3)).toBe(5);
    });

    test('Basic case - negative and positive number', async () => {
        expect(await add(-1, 4)).toBe(3);
    });

    test('Edge case - zero', async () => {
        expect(await add(0, 5)).toBe(5);
    });

    test('Edge case - two zeros', async () => {
        expect(await add(0, 0)).toBe(0);
    });

    test('Corner case - large numbers', async () => {
        expect(await add(1e10, 1e10)).toBe(2e10);
    });
});

describe('subtract function', () => {
    const subtract = async (a, b) => a - b;

    test('Basic case - positive numbers', async () => {
        expect(await subtract(5, 3)).toBe(2);
    });

    test('Basic case - negative and positive number', async () => {
        expect(await subtract(2, 5)).toBe(-3);
    });

    test('Edge case - zero', async () => {
        expect(await subtract(6, 0)).toBe(6);
    });

    test('Edge case - subtracting zero', async () => {
        expect(await subtract(0, 4)).toBe(-4);
    });

    test('Corner case - large numbers', async () => {
        expect(await subtract(1e10, 1e9)).toBe(9e9);
    });
});