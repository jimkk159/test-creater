describe('add function', () => {
    const add = async (a, b) => a + b;

    test('Basic case - positive numbers', async () => {
        expect(await add(5, 10)).toBe(15);
    });

    test('Basic case - negative and positive number', async () => {
        expect(await add(5, -3)).toBe(2);
    });

    test('Edge case - zero', async () => {
        expect(await add(0, 10)).toBe(10);
    });

    test('Edge case - adding two zeros', async () => {
        expect(await add(0, 0)).toBe(0);
    });
});

describe('subtract function', () => {
    const subtract = async (a, b) => a - b;

    test('Basic case - simple subtraction', async () => {
        expect(await subtract(10, 5)).toBe(5);
    });

    test('Basic case - negative result', async () => {
        expect(await subtract(3, 8)).toBe(-5);
    });

    test('Edge case - zero subtracted', async () => {
        expect(await subtract(10, 0)).toBe(10);
    });

    test('Edge case - subtracting from zero', async () => {
        expect(await subtract(0, 5)).toBe(-5);
    });
});

describe('multiple function', () => {
    const multiple = async (a, b) => a * b;

    test('Basic case - simple multiplication', async () => {
        expect(await multiple(4, 5)).toBe(20);
    });

    test('Basic case - multiplication by zero', async () => {
        expect(await multiple(7, 0)).toBe(0);
    });

    test('Edge case - multiplying by one', async () => {
        expect(await multiple(6, 1)).toBe(6);
    });

    test('Edge case - negative multiplication', async () => {
        expect(await multiple(-3, 5)).toBe(-15);
    });
});