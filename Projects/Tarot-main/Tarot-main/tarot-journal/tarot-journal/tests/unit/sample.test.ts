import { describe, it, expect } from 'vitest';

describe('Sample Test', () => {
  it('true should be true', () => {
    expect(true).toBe(true);
  });
  
  it('should handle basic math', () => {
    expect(1 + 1).toBe(2);
  });
});
