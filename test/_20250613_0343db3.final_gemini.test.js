describe('subtract', () => {
    const subtract = (a, b) => a - b;

    test('subtract:1. Basic case - two positive integers', () => {
        expect(subtract(10, 4)).toBe(6);
    });

    test('subtract:2. Basic case - negative result', () => {
        expect(subtract(5, 8)).toBe(-3);
    });

    test('subtract:3. Basic case - subtracting a negative number', () => {
        expect(subtract(5, -3)).toBe(8);
    });

    test('subtract:4. Basic case - two negative numbers', () => {
        expect(subtract(-10, -3)).toBe(-7);
    });

    test('subtract:5. Basic case - floating point numbers', () => {
        expect(subtract(5.5, 2.1)).toBeCloseTo(3.4);
    });

    test('subtract:6. Edge case - subtracting zero', () => {
        expect(subtract(7, 0)).toBe(7);
    });

    test('subtract:7. Edge case - subtracting from zero', () => {
        expect(subtract(0, 9)).toBe(-9);
    });

    test('subtract:8. Edge case - subtracting a number from itself', () => {
        expect(subtract(15, 15)).toBe(0);
    });

    test('subtract:9. Edge case - large numbers', () => {
        expect(subtract(1000000000, 999999999)).toBe(1);
    });

    test('subtract:10. Invalid input - first parameter is a string', () => {
        expect(subtract('hello', 5)).toBeNaN();
    });

    test('subtract:11. Invalid input - second parameter is a string', () => {
        expect(subtract(10, 'world')).toBeNaN();
    });

    test('subtract:12. Invalid input - parameter is null', () => {
        // In JS, arithmetic with null coerces null to 0. So 10 - null is 10 - 0 = 10.
        expect(subtract(10, null)).toBe(10);
    });

    test('subtract:13. Invalid input - parameter is undefined string', () => {
        // Note: The input is the string 'undefined', not the primitive value.
        expect(subtract(10, 'undefined')).toBeNaN();
    });
});

describe('divide', () => {
  const divide = (a, b) => a / b;

  test('divide:1. Basic case - positive integers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('divide:2. Basic case - float result', () => {
    expect(divide(5, 2)).toBe(2.5);
  });

  test('divide:3. Basic case - negative dividend', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  test('divide:4. Basic case - negative divisor', () => {
    expect(divide(10, -2)).toBe(-5);
  });

  test('divide:5. Basic case - two negative numbers', () => {
    expect(divide(-10, -2)).toBe(5);
  });

  test('divide:6. Edge case - division by zero', () => {
    expect(divide(10, 0)).toBe(Infinity);
  });

  test('divide:7. Edge case - negative division by zero', () => {
    expect(divide(-10, 0)).toBe(-Infinity);
  });

  test('divide:8. Edge case - dividing zero', () => {
    expect(divide(0, 5)).toBe(0);
  });

  test('divide:9. Corner case - zero divided by zero', () => {
    expect(divide(0, 0)).toBeNaN();
  });

  test('divide:10. Edge case - division by one', () => {
    expect(divide(123, 1)).toBe(123);
  });

  test('divide:11. Invalid input - non-numeric dividend', () => {
    expect(divide('hello', 2)).toBeNaN();
  });

  test('divide:12. Invalid input - non-numeric divisor', () => {
    expect(divide(10, 'world')).toBeNaN();
  });

  test('divide:13. Invalid input - null divisor', () => {
    // In JavaScript, null is coerced to 0 for arithmetic operations.
    expect(divide(10, null)).toBe(Infinity);
  });
});

describe('multiply', () => {
  const multiply = (a, b) => a * b;

  test('multiple:1. Basic case - two positive integers', () => {
    expect(multiply(7, 6)).toBe(42);
  });

  test('multiple:2. Basic case - two negative integers', () => {
    expect(multiply(-5, -10)).toBe(50);
  });

  test('multiple:3. Basic case - one positive, one negative', () => {
    expect(multiply(8, -4)).toBe(-32);
  });

  test('multiple:4. Basic case - floating point numbers', () => {
    expect(multiply(2.5, 3.5)).toBe(8.75);
  });

  test('multiple:5. Edge case - multiplying by zero', () => {
    expect(multiply(1000, 0)).toBe(0);
  });

  test('multiple:6. Edge case - multiplying by one', () => {
    expect(multiply(99, 1)).toBe(99);
  });

  test('multiple:7. Type check - number and numeric string', () => {
    expect(multiply(5, '10')).toBe(50);
  });

  test("multiple:8. Type check - number and boolean 'true'", () => {
    expect(multiply(15, true)).toBe(15);
  });

  test("multiple:9. Type check - number and boolean 'false'", () => {
    expect(multiply(15, false)).toBe(0);
  });

  test('multiple:10. Type check - number and null', () => {
    expect(multiply(10, null)).toBe(0);
  });

  test('multiple:11. Invalid case - number and non-numeric string', () => {
    expect(multiply(5, 'hello')).toBeNaN();
  });

  test('multiple:12. Invalid case - number and undefined string', () => {
    // The string 'undefined' coerces to NaN
    expect(multiply(10, 'undefined')).toBeNaN();
  });

  test('multiple:13. Invalid case - one missing parameter', () => {
    // Calling multiply(7) is equivalent to multiply(7, undefined)
    expect(multiply(7)).toBeNaN();
  });

  test('multiple:14. Invalid case - no parameters', () => {
    // Calling multiply() is equivalent to multiply(undefined, undefined)
    expect(multiply()).toBeNaN();
  });
});

describe('add', () => {
  const add = (a, b) => a + b;

  test('add:1. Basic case - should add two positive integers', () => {
    const input = { a: 5, b: 10 };
    expect(add(input.a, input.b)).toBe(15);
  });

  test('add:2. Basic case - should add two floating-point numbers', () => {
    const input = { a: 2.5, b: 3.5 };
    expect(add(input.a, input.b)).toBe(6.0);
  });

  test('add:3. Edge case - should add a positive and a negative number', () => {
    const input = { a: 10, b: -3 };
    expect(add(input.a, input.b)).toBe(7);
  });

  test('add:4. Edge case - should add two negative numbers', () => {
    const input = { a: -5, b: -8 };
    expect(add(input.a, input.b)).toBe(-13);
  });

  test('add:5. Edge case - should return the number when adding zero', () => {
    const input = { a: 99, b: 0 };
    expect(add(input.a, input.b)).toBe(99);
  });

  test('add:6. Type check - should concatenate a number and a numeric string', () => {
    const input = { a: 5, b: '5' };
    expect(add(input.a, input.b)).toBe('55');
  });

  test('add:7. Type check - should concatenate a string and a number', () => {
    const input = { a: 'hello', b: 123 };
    expect(add(input.a, input.b)).toBe('hello123');
  });

  test('add:8. Type check - should concatenate two numeric strings', () => {
    const input = { a: '10', b: '20' };
    expect(add(input.a, input.b)).toBe('1020');
  });

  test('add:9. Invalid input type - should treat null as 0 in addition', () => {
    const input = { a: 10, b: null };
    expect(add(input.a, input.b)).toBe(10);
  });

  test('add:10. Invalid input type - should result in NaN when adding undefined', () => {
    const input = { a: 10, b: undefined };
    // Note: The prompt has 'undefined' as a string, but the expected 'nan' implies the undefined type.
    expect(add(input.a, input.b)).toBeNaN();
  });

  test('add:11. Invalid input type - should treat boolean true as 1 in addition', () => {
    const input = { a: 10, b: true };
    expect(add(input.a, input.b)).toBe(11);
  });
});

